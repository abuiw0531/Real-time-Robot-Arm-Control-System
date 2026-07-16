# Robot Arm Control System

This project contains the backend server for controlling a robotic arm via hand tracking, along with its live dashboard.

## Project Structure

- `backend/`: The main Python Flask application that provides the real-time MJPEG video feed, socket.io communication, and arm control logic.
- `frontend_mockup/`: The initial static HTML/CSS/JS mockups for the dashboard design (not strictly required for the backend to run, but kept for reference).

## Prerequisites

- Python 3.8+
- Requirements listed in `requirements.txt`

## Installation

1. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the server:
   ```bash
   cd backend
   python main.py
   ```

3. Open your browser and navigate to `http://localhost:5000` to view the live dashboard.
