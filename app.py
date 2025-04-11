from flask import Flask, render_template, request, redirect, session
import psycopg2
import pandas as pd
from datetime import datetime, timedelta
import ollama
import random
import time
from threading import Thread

app = Flask(__name__)
app.secret_key = "test_secret_123"

# to avoid latency
Thread(target=lambda: ollama.chat(
    model="gemma:2b",
    messages=[{"role": "user", "content": "Hello"}],
    options={"num_predict": 100}
)).start()


# Database connection config
def get_db_connection():
    return psycopg2.connect(
        dbname="Health",
    user="postgres",
    password="Saahit21@",
    host="localhost",
    port="5432"
    )



# Open AI generation

def add_fallback_emoji(message, category):
    # Simple emoji mapping for categories
    emojis = {
        "health": ["💊", "🩺", "❤️", "🍎"],
        "safety": ["🛡️", "🚨", "👀", "⚠️"],
        "reminder": ["⏰", "📅", "🔔", "🧠"]
    }
    suffix = " " + " ".join(random.sample(emojis.get(category.lower(), ["😊", "💡", "👍"]), 2))
    return message + suffix




def generate_friendly_message(category, details):
    system_prompt = (
        "You're a polite and humorous assistant talking to elderly users. "
        "Your messages should be simple, friendly, respectful, and a little witty. "
        "Avoid technical jargon or harsh words. Be encouraging and kind."
    )

    user_prompt = (
        f"Convert the following {category} alert into a simplified, polite, and humorous message "
        f"suitable for an elderly person. Keep it under 2-3 sentences:\n\n{details}"
    )

    try:
        response = ollama.chat(
            model="gemma:2b",  # 👈 change model here
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            options={"num_predict": 100}  # Optional: limits tokens
        )
        return response["message"]["content"]
    except Exception as e:
        print("Ollama error:", e)
        return add_fallback_emoji(details, category)

    
    
    
    
    
    
    

# Daily Reminder message
def daily_reminder(device_id):
    now = datetime.now().time().replace(second=0, microsecond=0)  # current time, ignore seconds

    conn = get_db_connection()
    cur = conn.cursor()

    # Fetch unsent reminders for this specific device and current time
    cur.execute("""
        SELECT id, caretaker_id, device_id, timestamp, scheduled_time, alert_sent_acknowledged, reminder_type
        FROM daily_reminders 
        WHERE scheduled_time = %s AND alert_sent_acknowledged = 'NO' AND device_id = %s
    """, (now, device_id))
    reminders = cur.fetchall()

    sent_alerts = []

    for reminder in reminders:
        id, caretaker_id, device_id, timestamp, sched_time, alert_status, reminder_type = reminder
        
        # Simulate alert (e.g., email/SMS notification)
        print(f"🔔 ALERT: [{reminder_type.upper()}] for Device ID: {device_id}, Caretaker ID: {caretaker_id} at {sched_time}")
        
        # Mark reminder as sent
        cur.execute("""
            UPDATE daily_reminders 
            SET alert_sent_acknowledged = 'YES' 
            WHERE id = %s
        """, (id,))

        sent_alerts.append({
            "caretaker_id": caretaker_id,
            "device_id": device_id,
            "scheduled_time": str(sched_time),
            "reminder_type": reminder_type
        })

    conn.commit()
    cur.close()
    conn.close()
    if not sent_alerts:
        return "😌 No reminders now, relax and sip some chai ☕"
    else:
        messages = []
        for alert in sent_alerts:
            msg = f"📢 {alert['reminder_type'].capitalize()} Reminder: Hello there! It’s time to {alert['reminder_type']} – Don’t forget! 😊"
            messages.append(msg)
        return " ".join(messages)




    
# Safety Status
def get_safety_message(device_id):
    df = pd.read_csv("Data/safety_monitoring.csv")
    df = df[df['Device-ID/User-ID'] == device_id]
    if df.empty:
        return "No safety data found for this device."

    latest = df.sort_values("Timestamp", ascending=False).iloc[0]
    timestamp = latest.get("Timestamp")
    location = latest.get("Location", "unknown")

    alerts = []

    if latest.get("Fall Detected (Yes/No)") == "Yes":
        alerts.append("Fall detected")

    inactivity = latest.get("Post-Fall Inactivity Duration (Seconds)", 0)
    if pd.to_numeric(inactivity, errors='coerce') > 20:
        alerts.append("Post-fall inactivity exceeded 20 seconds")

    impact = latest.get("Impact Force Level", "").strip().lower()
    if impact in ["medium", "high"]:
        alerts.append(f"Impact force was {impact}")

    if alerts:
        return f"🚨 At {timestamp}, uh-oh! " + " & ".join(alerts) + f" at {location}. Don’t worry, help is just around the corner 🧸"
    else:
        return f"✅ At {timestamp}, all is calm and safe at {location}. Like a cozy nap on a Sunday afternoon 😴"






# Health Status
def get_health_message(device_id):
    df = pd.read_csv("Data/health_monitoring.csv")
    df = df[df['Device-ID/User-ID'] == device_id]
    if df.empty:
        return "No health data found for this device."

    latest = df.sort_values("Timestamp", ascending=False).iloc[0]
    
    msg = []
    for param in ["Heart Rate", "Blood Pressure", "Glucose Levels", "Oxygen Saturation"]:
        timestamp=latest.get("Timestamp")
        if param=="Oxygen Saturation":
            status = latest.get(f"{param} Below Threshold (Yes/No)", "No")
            if status == "Yes":
                value = latest.get(param, "unknown")
                msg.append(f"{param} is abnormal (Value: {value})")
        else:
            status = latest.get(f"{param} Below/Above Threshold (Yes/No)", "No")
            if status == "Yes":
                value = latest.get(param, "unknown")
                msg.append(f"{param} is abnormal (Value: {value})")

    if msg:
        return f"🩺 At {timestamp}, we noticed something: " + " 😯 ".join(msg) + " — take it easy and maybe call your caretaker, okay?"
    else:
        return f"🎉 At {timestamp}, all vitals are dancing happily. Keep smiling and stay awesome! 😄"






# Main Page(User_Id)
@app.route('/')
def home():
    return render_template('login.html')



# Caretaker_Login
@app.route('/caretaker_login', methods=["GET", "POST"])
def caretaker_login():
    if request.method == "POST":
        caretaker_id = request.form["caretaker_id"]
        password = request.form["password"]

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM caretakers WHERE caretaker_id=%s AND password=%s", (caretaker_id, password))
        result = cur.fetchone()
        cur.close()
        conn.close()

        if result:
            session["caretaker_id"] = caretaker_id
            return redirect("/reminder_form")
        else:
            return render_template("caretaker_login.html", error="Invalid credentials")

    return render_template("caretaker_login.html")





# Add this route to render the reminder form (only for caretakers)
@app.route('/reminder_form')
def reminder_form():
    return render_template('add_reminder.html')




@app.route('/add_reminder', methods=["POST"])
def add_reminder():
    caretaker_id = session.get("caretaker_id")  # Should be set at caretaker login
    device_id = request.form["device_id"]
    scheduled_time = request.form["scheduled_time"]
    reminder_type = request.form["reminder_type"]

    if not caretaker_id:
        return "Caretaker not logged in."

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO daily_reminders (caretaker_id, device_id, scheduled_time, reminder_type)
        VALUES (%s, %s, %s, %s)
    """, (caretaker_id, device_id, scheduled_time, reminder_type))
    conn.commit()
    cur.close()
    conn.close()

    return "Reminder added successfully!"




# Check with Login
@app.route('/login', methods=["POST"])
def login():
    device_id = request.form["device_id"]
    password = request.form["password"]

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM devices WHERE device_id=%s AND password=%s", (device_id, password))
    result = cur.fetchone()
    cur.close()
    conn.close()

    if result:
        session['device_id'] = device_id
        # health_message = get_health_message(device_id)
        # safety_message=get_safety_message(device_id)
        # daily_reminder_message=daily_reminder(device_id)
        # message=health_message+safety_message
        raw_health = get_health_message(device_id)
        raw_safety = get_safety_message(device_id)
        raw_reminder = daily_reminder(device_id)
        print(raw_reminder)
        start = time.time()
        results = {}

        def run_ollama_thread(key, category, text):
            results[key] = generate_friendly_message(category, text)

        threads = [
            Thread(target=run_ollama_thread, args=("health", "health", raw_health)),
            Thread(target=run_ollama_thread, args=("safety", "safety", raw_safety)),
            Thread(target=run_ollama_thread, args=("reminder", "reminder", raw_reminder))
        ]

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        health_message = results.get("health")
        safety_message = results.get("safety")
        daily_reminder_message = results.get("reminder")
        print("Block X Time:", time.time() - start)
        return render_template("dashboard.html", device_id=device_id, health_message=health_message,safety_message=safety_message,daily_reminder_message=daily_reminder_message)
    else:
        return "Invalid credentials"

if __name__ == "__main__":
    app.run(debug=True)





