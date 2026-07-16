from flask import Flask, render_template, Response
from flask_socketio import SocketIO
from main import generate_frames
import eventlet
import time
import config

# Patch for eventlet (necessary for SocketIO async features)
eventlet.monkey_patch()

app = Flask(__name__)
socketio = SocketIO(app, async_mode='eventlet')

current_frame = None

def background_thread():
    """Background task to extract frames and data from main.py generator and emit to clients"""
    global current_frame
    for frame, data in generate_frames():
        current_frame = frame
        socketio.emit('update_data', data)
        socketio.sleep(0.001) # Yield to eventlet

@app.route('/')
def index():
    # Pass threshold from config to template
    return render_template('index.html', config_threshold=config.A_THRESHOLD)

def gen_video_stream():
    """Generator for the MJPEG video stream"""
    global current_frame
    while True:
        if current_frame is not None:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + current_frame + b'\r\n')
        socketio.sleep(0.016) # Roughly 60 FPS update rate

@app.route('/video_feed')
def video_feed():
    return Response(gen_video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

import os
import signal

@app.route('/shutdown', methods=['POST'])
def shutdown():
    print("Received shutdown request. Exiting...")
    # Send SIGINT to the current process to terminate gracefully
    os.kill(os.getpid(), signal.SIGINT)
    return "Server shutting down..."

if __name__ == '__main__':
    print(f"Starting Robot Arm Dashboard on http://127.0.0.1:5000")
    socketio.start_background_task(background_thread)
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)
