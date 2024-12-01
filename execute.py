import firebase_admin
from firebase_admin import credentials, storage, db
import os
from flask import Flask, send_from_directory, render_template
from flask_socketio import SocketIO
import threading
import time

# Path to your Firebase service account key file
service_account_key = 'guardian-gesture-firebase-adminsdk-vc1w6-266d1d9c74.json'

# Initialize Firebase Admin SDK
cred = credentials.Certificate(service_account_key)
firebase_admin.initialize_app(cred, {
    'storageBucket': 'guardian-gesture.appspot.com',
    'databaseURL': 'https://guardian-gesture-default-rtdb.firebaseio.com'
})

# Define the local folder to save images
local_folder = 'downloaded_images'

# Create the folder if it does not exist
if not os.path.exists(local_folder):
    os.makedirs(local_folder)

# Flask application setup
app = Flask(__name__)
socketio = SocketIO(app)

def download_images_from_firebase():
    bucket = storage.bucket()
    blobs = bucket.list_blobs(prefix='images/')

    for blob in blobs:
        if blob.name.endswith('.jpg'):
            local_path = os.path.join(local_folder, os.path.basename(blob.name))
            if not os.path.exists(local_path):
                blob.download_to_filename(local_path)
                print(f'Downloaded {local_path}')
                socketio.emit('new_image', {'filename': os.path.basename(blob.name)})

def background_task():
    while True:
        download_images_from_firebase()
        time.sleep(5)  # Check for new images every 5 seconds

# Start the background task
threading.Thread(target=background_task, daemon=True).start()

@app.route('/')
def index():
    # List all image files in the local folder
    image_files = [f for f in os.listdir(local_folder) if f.endswith('.jpg')]
    
    # Fetch the location data from Firebase Realtime Database
    location_ref = db.reference('location')
    location_data = location_ref.get()

    return render_template('index.html', image_files=image_files, location_data=location_data)

@app.route('/image/<filename>')
def image(filename):
    # Serve an image file from the local folder
    return send_from_directory(local_folder, filename)

if __name__ == '__main__':
    socketio.run(app, debug=True)
