import cv2
import mediapipe as mp
import time
import math
import pygame
import requests
import os
from twilio.rest import Client
from dotenv import load_dotenv

# Load local environment configurations
load_dotenv()

# ---------- Twilio Setup ----------
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
to_whatsapp = os.getenv("TWILIO_TO_WHATSAPP", "whatsapp:+919014804332")
alert_threshold = float(os.getenv("DROWSY_THRESHOLD_SECONDS", "2.0"))

client = Client(account_sid, auth_token) if account_sid and auth_token else None

def send_whatsapp_alert():
    try:
        if not client:
            print("WhatsApp error: Twilio credentials are not configured in .env file.")
            return

        with open("location.txt", "r") as f:
            lat, lng = f.read().split(",")

        location_link = f"https://maps.google.com/?q={lat},{lng}"

        message = client.messages.create(
            body=f"⚠️ Driver drowsiness detected!\nLocation: {location_link}",
            from_="whatsapp:+14155238886",
            to=to_whatsapp
        )

        print("Message sent:", message.sid)

    except Exception as e:
        print("WhatsApp error:", e)

# ---------- Alarm Setup ----------
pygame.mixer.init()
pygame.mixer.music.load("alarm.wav")

# ---------- MediaPipe Setup ----------
BaseOptions = mp.tasks.BaseOptions
FaceLandmarker = mp.tasks.vision.FaceLandmarker
FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = FaceLandmarkerOptions(
    base_options=BaseOptions(model_asset_path="face_landmarker.task"),
    running_mode=VisionRunningMode.VIDEO,
    num_faces=2
)

cap = cv2.VideoCapture(0)

# ---------- Utility Functions ----------
def dist(a, b):
    return math.dist(a, b)

def eye_aspect_ratio(eye, w, h):
    pts = [(int(lm.x * w), int(lm.y * h)) for lm in eye]
    return (dist(pts[1], pts[5]) + dist(pts[2], pts[4])) / (2 * dist(pts[0], pts[3]))

def mouth_aspect_ratio(mouth, w, h):
    pts = [(int(lm.x * w), int(lm.y * h)) for lm in mouth]
    return dist(pts[2], pts[6]) / dist(pts[0], pts[4])

# ---------- Thresholds ----------
EAR_THR = 0.22
MAR_THR = 0.6
DROWSY_SCORE_LIMIT = 15

# ---------- Variables ----------
score = 0
captured = False
blink_count = 0
eye_closed = False
yawn_count = 0
mouth_open = False

drowsy_start_time = None
message_sent = False

with FaceLandmarker.create_from_options(options) as landmarker:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        h, w, _ = frame.shape
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        timestamp = int(time.time() * 1000)

        results = landmarker.detect_for_video(mp_image, timestamp)

        status = "ALERT"
        color = (0, 255, 0)

        if results.face_landmarks:
            face = results.face_landmarks[0]

            # ---------- Face Landmarks ----------
            right_eye = [face[i] for i in [33, 160, 158, 133, 153, 144]]
            mouth = [face[i] for i in [61, 81, 13, 311, 291, 308, 14]]

            # ---------- EAR / MAR ----------
            ear = eye_aspect_ratio(right_eye, w, h)
            mar = mouth_aspect_ratio(mouth, w, h)

            # ---------- Blink Counter ----------
            if ear < EAR_THR:
                if not eye_closed:
                    blink_count += 1
                    eye_closed = True
            else:
                eye_closed = False

            # ---------- Yawn Counter ----------
            if mar > MAR_THR:
                if not mouth_open:
                    yawn_count += 1
                    mouth_open = True
            else:
                mouth_open = False

            # ---------- Drowsiness Logic ----------
            if ear < EAR_THR or mar > MAR_THR:
                score += 1
            else:
                score = max(0, score - 1)
                pygame.mixer.music.stop()
                captured = False
                drowsy_start_time = None
                message_sent = False

            # ---------- Drowsy Alert ----------
            if score >= DROWSY_SCORE_LIMIT:
                status = "DROWSY – TAKE A BREAK"
                color = (0, 0, 255)

                if not pygame.mixer.music.get_busy():
                    pygame.mixer.music.play(-1)

                # ---------- Screenshot ----------
                

                # ---------- Timer ----------
                if drowsy_start_time is None:
                    drowsy_start_time = time.time()

                elapsed = time.time() - drowsy_start_time
                print("Elapsed:", elapsed)

                # ---------- WhatsApp After 5 sec (test) ----------
                if elapsed >= alert_threshold and not message_sent:
                    send_whatsapp_alert()
                    message_sent = True

            # ---------- Display EAR ----------
            cv2.putText(frame, f"EAR: {ear:.2f}", (20, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)

            # ---------- Display MAR ----------
            cv2.putText(frame, f"MAR: {mar:.2f}", (20, 110),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)

        else:
            # ---------- Face Missing ----------
            cv2.putText(frame, "LOOK FORWARD", (20, 270),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)
            score += 1

        # ---------- Status ----------
        cv2.putText(frame, f"STATUS: {status}", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

        # ---------- Fatigue Score ----------
        score_color = (0,255,0)
        if score > 5:
            score_color = (0,255,255)
        if score > 10:
            score_color = (0,0,255)

        cv2.putText(frame, f"FATIGUE SCORE: {score}", (20, 150),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, score_color, 2)

        # ---------- Blink Count ----------
        cv2.putText(frame, f"BLINKS: {blink_count}", (20, 190),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

        # ---------- Yawn Count ----------
        cv2.putText(frame, f"YAWNS: {yawn_count}", (20, 230),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

        cv2.imshow("Driver Drowsiness Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# ---------- Cleanup ----------
cap.release()
cv2.destroyAllWindows()
pygame.mixer.music.stop()