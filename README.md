

# ElderEase Tech — ByteCure Team 🧓💖

> **Hack the Future: A Gen AI Sprint | Powered by Data**

---

## 🚀 Problem Statement
Many seniors living independently find it challenging to keep up with regular health monitoring and often lack immediate support during emergencies.  
This gap can compromise their well-being, highlighting the need for a **user-friendly, real-time system** that delivers **constant monitoring** and **timely alerts** to both elderly users and their caregivers.

---

## 💡 Proposed Solution Overview
- **Continuous Monitoring:**  
  Track vital signs in real-time through wearable sensors and data feeds.
- **Instant Alerts:**  
  Automatically detect falls or inactivity and notify caregivers immediately.
- **Personalized Reminders:**  
  Send gentle, elder-friendly notifications for medicines and daily routines.
- **User-Friendly Dashboard:**  
  Provide an intuitive, supportive interface for seniors and caregivers.
- **Integrated Care Approach:**  
  Combine health, safety, and daily reminder modules for proactive care.

---

## 🛠 Technologies Used
- **Backend:** Python (Flask)
- **Database:** PostgreSQL with psycopg2
- **Data Handling:** Pandas (CSV manipulation)
- **Frontend:** HTML, CSS, JavaScript
- **Natural Language Generation:** Ollama (`gemma:2b` model for elder-appropriate messaging)
- **IoT Integration (Conceptual):** Wearable sensors for health monitoring

---

## 🧠 Agents' Interaction Design

| Agent              | Responsibilities                                    |
|--------------------|-----------------------------------------------------|
| **Monitoring Agent** | Tracks vital signs continuously |
| **Notification Agent** | Sends friendly alerts and reminders using LLMs |
| **Caretaker Agent** | Views health dashboard and manages reminder schedules |
| **Elder User Agent** | Receives personalized notifications and interacts via device |

> ![Agent Interaction Diagram](https://your_uploaded_image_link)  
*(Replace this with your actual uploaded diagram link or GitHub assets folder.)*

---

## 🏗 Code Structure (Brief)
- `app.py`: Flask application managing device login, caretaker login, real-time monitoring, friendly message generation via Ollama
- `templates/`: Frontend templates (login.html, dashboard.html, caretaker forms)
- `static/`: Stylesheets (CSS)
- `Data/`: Health and safety monitoring CSV files
- `database.sql`: Table schemas (devices, caretakers, reminders)

---

## 🎥 Demo Video
Watch the full project demo here:  
[👉 View Demo Video](https://drive.google.com/file/d/1N5YK7TnQtogcvppLN48zK_yZ89GwquDJ/view?usp=sharing)

---

## 📈 Conclusion
Our system is built thoughtfully for elderly individuals who live alone.  
It ensures **real-time health tracking**, **instant support**, and **personalized reminders** — improving emergency response times and quality of life.  
This fosters **independent, safer living** while giving **peace of mind** to loved ones.

---

## 🔗 References and Other Details
- [Ollama Documentation](https://ollama.ai)
- [Sample Concept Video on Elder Monitoring](https://youtu.be/Lb5D892-2HY?si=oV9siVY9-MJ45sPb)
- Future Scope:
  - Deeper wearable device integration
  - Mobile push notifications
  - Multilingual support (Telugu, Hindi)

---

# 🙏 Thank You!
