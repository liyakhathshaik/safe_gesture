import cv2
import mediapipe as mp
import os
from datetime import datetime
import pyrebase
import threading

lat, long = 22.294858, 73.362279



def detect_gesture_and_upload():
    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands

    # Initialize MediaPipe Hands
    hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)

    # Initialize video capture
    cap = cv2.VideoCapture(0)

    gesture_state = 0  # 0 - open hand, 1 - closed hand, 2 - gesture completed
    k = 0  # Counter for gesture detection
    output_directory = 'captured_images'  # Directory to save images

    # Create output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Firebase configuration
    firebaseConfig = {
        "apiKey": "YOUR API KEY",
        "authDomain": "guardian-gesture.firebaseapp.com",
        "projectId": "guardian-gesture",
        "storageBucket": "guardian-gesture.appspot.com",
        "messagingSenderId": "503802348568",
        "appId": "1:503802348568:web:e75129179e7735369aaf6d",
        "databaseURL": "https://guardian-gesture-default-rtdb.firebaseio.com"
    }

    # Initialize Firebase
    firebase = pyrebase.initialize_app(firebaseConfig)
    storage = firebase.storage()
    db = firebase.database()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            continue

        # Convert the frame to RGB
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        res = hands.process(img)

        if res.multi_hand_landmarks:
            for hand_landmarks in res.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                thumb_y = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y
                index_y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
                middle_y = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y
                ring_y = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y
                pinky_y = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y

                if (thumb_y < index_y and thumb_y < middle_y and thumb_y < ring_y and thumb_y < pinky_y) and gesture_state == 0:
                    gesture_state = 1
                    k += 1
                    print("Hand closed")

                if (thumb_y > index_y and thumb_y > middle_y and thumb_y > ring_y and thumb_y > pinky_y) and gesture_state == 1:
                    if k == 2:
                        gesture_state = 2
                    else:
                        gesture_state = 0
                    print("Hand opened")

                if (thumb_y < index_y and thumb_y < middle_y and thumb_y < ring_y and thumb_y < pinky_y) and gesture_state == 2:
                    gesture_state = 0
                    k = 0
                    print("Gesture completed")
                    img_filename = f'image_{datetime.now().strftime("%Y%m%d_%H%M%S")}.jpg'
                    img_path = os.path.join(output_directory, img_filename)
                    cv2.imwrite(img_path, frame)
                    print(f'Saved {img_filename}')

                    cloudpath = f"images/{img_filename}"
                    storage.child(cloudpath).put(img_path)
                    print(f"Image {img_filename} successfully uploaded to Firebase.")

        # Send latitude and longitude to Firebase Realtime Database
                    db.child("location").set({"latitude": lat, "longitude": long})
                    print(f"Location {lat}, {long} successfully sent to Firebase.")
 
        # Display the video feed
        cv2.imshow('Gesture Detection', frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    detect_gesture_and_upload()
