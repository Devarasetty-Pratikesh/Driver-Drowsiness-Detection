# 🚗 Driver Drowsiness Detection System with Live Location & WhatsApp Alert

## 📌 Overview

This project is a **real-time Driver Drowsiness Detection System** that monitors a driver’s face using a webcam and detects signs of fatigue such as eye closure and yawning.

If drowsiness persists, the system:

* Triggers an **alarm**
* Captures a **screenshot**
* Sends a **WhatsApp alert with live location**
* Stores data in a **database for analysis**

---

## 🎯 Features

* 👁️ Eye Aspect Ratio (EAR) based eye closure detection
* 😮 Mouth Aspect Ratio (MAR) based yawn detection
* 📊 Fatigue score calculation
* 🔔 Alarm system using pygame
* 📸 Automatic screenshot capture during drowsiness
* 📱 WhatsApp alert using Twilio API
* 📍 Live location tracking using browser geolocation
* 🗃️ SQLite database logging
* 🚗 Face missing detection (“Look Forward” alert)

---

## 🛠️ Technologies Used

* Python
* OpenCV
* MediaPipe
* Pygame
* Flask (for location server)
* JavaScript (Geolocation API)
* Twilio API (WhatsApp messaging)
* SQLite (database)

---

## 📂 Project Structure

```
Driver-Drowsiness-Detection/
│── main.py
│── location_server.py
│── location.html
│── location.txt
│── driver_data.db
│── alarm.wav
│── face_landmarker.task
```

---

## ⚙️ Installation

### 1️⃣ Install Dependencies

```bash
pip install opencv-python mediapipe pygame twilio flask flask-cors sqlite3
```

---

### 2️⃣ Setup Twilio

1. Create account at Twilio
2. Enable WhatsApp Sandbox
3. Join sandbox from your phone
4. Add your:

   * Account SID
   * Auth Token

---

### 3️⃣ Run Location Server

```bash
python location_server.py
```

---

### 4️⃣ Open Location File

Open in browser:

```
http://127.0.0.1:5500/location.html
```

Allow location access.

---

### 5️⃣ Run Main Program

```bash
python main.py
```

---

## 🚀 Working

1. Webcam captures driver face
2. EAR & MAR are calculated
3. Fatigue score increases on drowsiness
4. If threshold exceeded:

   * Alarm triggers
   * Screenshot captured
   * Timer starts
5. If drowsiness continues:

   * WhatsApp alert sent
   * Live location included
   * Data stored in database

---

## 🧠 Detection Logic

* EAR < Threshold → Eyes closed
* MAR > Threshold → Yawning
* Continuous detection → Fatigue score increases
* Score limit reached → Drowsiness detected

---

## 📱 WhatsApp Alert

Message example:

```
⚠️ Driver drowsiness detected!
Location: https://maps.google.com/?q=...
```

---

## 📊 Database

All events stored in SQLite database:

| Timestamp | Score | Blinks | Yawns | Location |
| --------- | ----- | ------ | ----- | -------- |

---

## ⚠️ Limitations

* Depends on lighting conditions
* Requires camera availability
* Browser location permission needed
* Twilio sandbox limitations

---

## 🔮 Future Improvements

* Real-time GPS integration
* Mobile app version
* Cloud database (Firebase)
* Head pose detection
* Driver identity recognition

---

## 👨‍💻 Author

Bhanu Prakash
SRM Institute of Science & Technology

---

## ⭐ Conclusion

This system enhances **road safety** by detecting driver fatigue and providing real-time alerts with location, making it suitable for intelligent transportation systems.
