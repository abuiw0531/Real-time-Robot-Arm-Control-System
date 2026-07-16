# 機器手臂視覺控制系統 (Robot Arm Visual Control System)

[🇹🇼 中文版本](#中文版本) | [🇬🇧 English Version](#english-version)

---

<h2 id="中文版本">🇹🇼 中文版本</h2>

### 專案簡介
本專案為一個基於電腦視覺與手勢追蹤的「機器手臂即時控制系統」。系統結合了 Python 後端伺服器與現代化的網頁儀表板，允許使用者透過攝像頭即時捕捉手部動作，並將其即時轉換為機器手臂的控制指令。此專案充分展示了**軟硬體整合**、**即時影像處理 (Computer Vision)** 以及**前端互動設計**的實作與系統架構能力。

### 核心功能
* **即時影像串流 (Real-time Video Feed)**：透過 MJPEG 串流技術，將即時影像畫面低延遲傳輸至網頁前端。
* **手勢追蹤與辨識 (Hand Tracking)**：運用影像處理演算法即時偵測手部關鍵節點與手勢動作。
* **網頁控制儀表板 (Live Dashboard)**：具備現代化 UI 設計的前端介面，提供系統負載狀態、FPS 顯示、即時指令日誌與視覺化數據。
* **低延遲通訊 (Low-latency Communication)**：透過 Socket.IO 實現前後端的雙向即時通訊，確保機器手臂能迅速反應。

### 專案結構
- `backend/`: 核心 Python Flask 應用程式，包含即時影像處理模組、Socket.IO 通訊邏輯以及手臂控制 API。
- `frontend_mockup/`: 儀表板的初始靜態 UI 設計稿（HTML/CSS/JS），呈現現代化科技感的介面設計參考。
- `requirements.txt`: 開發與運行環境的 Python 依賴套件清單。

### 快速啟動
1. 安裝系統運行所需套件：
   ```bash
   pip install -r requirements.txt
   ```
2. 啟動後端控制伺服器：
   ```bash
   cd backend
   python main.py
   ```
3. 開啟瀏覽器並前往 `http://localhost:` 即可進入系統控制台。

---

<h2 id="english-version">🇬🇧 English Version</h2>

### Project Overview
This project is a **Real-time Robot Arm Control System** based on computer vision and hand tracking. It seamlessly integrates a Python backend server with a modern web dashboard, enabling users to capture hand gestures via a camera and translate them into precise control commands for a robotic arm. This repository demonstrates solid capabilities in **hardware-software integration**, **real-time computer vision**, and **interactive frontend design**.

### Core Features
* **Real-time Video Feed**: Utilizes MJPEG streaming to deliver low-latency live camera footage to the web frontend.
* **Hand Tracking**: Employs computer vision algorithms to detect hand landmarks and recognize gestures in real time.
* **Live Web Dashboard**: A modern, data-rich frontend interface providing system status monitoring, FPS metrics, real-time command logs, and data visualization.
* **Low-latency Communication**: Implements bidirectional, real-time communication between the frontend and backend via Socket.IO for smooth robotic arm actuation.

### Project Structure
- `backend/`: The core Python Flask application handling real-time video processing, Socket.IO communication logic, and arm control modules.
- `frontend_mockup/`: Initial static UI design mockups (HTML/CSS/JS) demonstrating a modern and professional tech aesthetic.
- `requirements.txt`: Python dependencies required for the project environment.

### Quick Start
1. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the backend control server:
   ```bash
   cd backend
   python main.py
   ```
3. Open your browser and navigate to `http://localhost:` to access the control dashboard.
