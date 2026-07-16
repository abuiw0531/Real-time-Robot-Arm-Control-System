# config.py

# --- 視窗設定 ---
CAM_WIDTH = 1280
CAM_HEIGHT = 720

# --- 控制設定 ---
INTERVAL = 2  # 輸出頻率間隔 (數值越小，頻率越快)

# --- UI 設定 ---
CENTER_X = 950
CENTER_Y = 400
OFFSET = 120

# --- 判定閾值設定 ---
A_THRESHOLD = 0.35              # 大拇指與食指距離比例 (判斷 A: 1 或 A: 0)
CLICK_DISTANCE_THRESHOLD = 50 # 食指與中指距離 (判斷是否觸發方向按鈕或 A 按鈕)

# --- 序列通訊設定 (Pico) ---

SERIAL_PORT = 'COM6'          # 請根據實際 Pico 所在的 COM port 進行修改，例如 'COM3', 'COM5'
BAUD_RATE = 115200
