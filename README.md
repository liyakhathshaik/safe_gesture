# Gesture_Recognisition
 ❗ PROBLEM STATEMENT
Despite advances in public surveillance and emergency services, women still face critical safety challenges:

🚶‍♀️ Vulnerability in Public Spaces: Harassment and assault often go unnoticed or unreported.

📵 Delayed Response: Victims may be unable to call for help in time.

🔍 Lack of Proactive Detection: Most CCTV systems record passively; they don’t “understand” when something is wrong.

🛡️ Insufficient Integration: Alerts, first responders, and nearby safe zones aren’t always connected.

⏳ Lost Minutes Matter: Every second’s delay in detecting and notifying law enforcement or bystanders dramatically increases risk.


Developed an AI-powered surveillance system utilizing OpenCV and MediaPipe to detect SOS gestures through widespread camera networks. Integrated geolocation data transmission to Firebase Cloud, enabling real-time alerts to the nearest police stations. Designed a desktop application with Electron for law enforcement, featuring live incident imagery, geolocation details, and emergency notifications, operating seamlessly in the background.
here is desktop application link: https://github.com/liyakhathshaik/Desktop_application_women_safety
here is recognisation link: https://github.com/liyakhathshaik/Gesture_Recognision
How It Works & What We Use
Video Capture

Fixed-location cameras stream video frames to our central server.

Frame Extraction

On the server, a process continuously pulls frames from each camera feed.

Gesture Detection

We run a Python script using OpenCV and MediaPipe to detect pre-defined SOS hand signs in each frame.

Event Packaging

When a gesture is detected, we extract the relevant frame(s), attach the camera ID and timestamp, and bundle them into an “event” packet.

Cloud Upload

The event packet is uploaded to a secure Firebase Cloud Storage bucket that corresponds to the nearest police station.

Desktop Alert App

A desktop application built with Electron polls the Firebase bucket.

When a new event appears, it downloads the image, displays it, and sounds an alarm.

Police Station Response

Officers see the live image and location in the desktop app and can dispatch help immediately.

Tech Used

OpenCV & MediaPipe for gesture recognition

Python for server-side processing

Firebase Cloud Storage for secure image delivery

Electron for the desktop alert application
