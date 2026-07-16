import cv2
import config
import serial
import time
from utils import HandControlDetector, ControllerButton, RectangleButton

def generate_frames():
    # --- 狀態變數初始化 ---
    a_status = 0
    repeatCounter = 0
    prev_time = time.time()
    
    # --- 1. 初始化相機與偵測器 ---
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        cap = cv2.VideoCapture(0) # Fallback
        
    cap.set(3, config.CAM_WIDTH)
    cap.set(4, config.CAM_HEIGHT)
    cap.set(cv2.CAP_PROP_EXPOSURE, -5)

    detector = HandControlDetector(detection_con=0.8, max_hands=1)

    # --- 1.5 初始化 Serial 連線 ---
    try:
        # 增加 write_timeout 並停用 flow control (dsrdtr, rtscts, xonxoff)
        ser = serial.Serial(
            config.SERIAL_PORT, 
            config.BAUD_RATE, 
            timeout=1, 
            write_timeout=2.0,
            dsrdtr=False,
            rtscts=False,
            xonxoff=False
        )
        print(f"Serial port {config.SERIAL_PORT} opened successfully at {config.BAUD_RATE} baud.")
        time.sleep(2) # 等待連線穩定
    except Exception as e:
        print(f"Failed to open serial port {config.SERIAL_PORT}: {e}")
        ser = None

    def send_command(action, speed, a_status):
        # 負責將字串送到終端機與 Pico
        t = time.time()
        cmd_str = f"{action},{speed},{a_status}"
        print(f"Outputting: {cmd_str}")
        if ser and ser.is_open:
            try:
                ser.write((cmd_str + '\n').encode('utf-8'))
            except serial.SerialTimeoutException:
                print(f"Serial write timeout (2.0s exceeded)! Skipping command: {cmd_str}")
            except Exception as e:
                print(f"Serial write error: {e}")
        print("指令延遲時間 = ", time.time() - t)

    # --- 2. 配置按鈕 (加入 A 與 四周的按鈕) ---
    W = config.CAM_WIDTH
    H = config.CAM_HEIGHT
    
    # L: 左側 20%, R: 右側 20%, F: 剩下中間的頂部 25%, B: 剩下中間的底部 25%
    rect_R = (0, 0, int(W * 0.45), H)
    rect_L = (int(W * 0.55), 0, W, H)
    #rect_B = (int(W * 0.4), 0, int(W * 0.6), int(H * 0.45))
    rect_B = (0, 0, W , int(H * 0.45))
    #rect_F = (int(W * 0.4), int(H * 0.55), int(W * 0.6), H)
    rect_F = (0, int(H * 0.55), W , H)

    buttons = [
        
        RectangleButton(rect_F, 'F'),
        RectangleButton(rect_B, 'B'),
        RectangleButton(rect_L, 'L'),
        RectangleButton(rect_R, 'R'),
    ]

    while True:
        success, img = cap.read()
        if not success:
            break
            
        img = cv2.flip(img, 1)
        
        # 尋找手部
        hands, img = detector.find_hands(img, draw=True, flip_type=False)

        # 預設此幀變數
        aperture = 0 # 預設距離

        if hands:
            hand1 = hands[0]
            lmList = hand1['lmList']
            cursor_x, cursor_y = hand1['center'] # 使用手掌中心當作點擊位置
            bbox = hand1['bbox'] # [x, y, w, h]
            hand_size = max(bbox[2], bbox[3]) # 手部邊框最大邊長
            
            p_thumb = lmList[4][:2]
            p_index = lmList[8][:2]
            
            # --- Aperture 比例 (4與8號點距離 / 手部大小) ---
            abs_aperture, info_ap, img = detector.get_distance(p_thumb, p_index, img)
            aperture = abs_aperture / hand_size if hand_size > 0 else 0
            
            # --- 手動座標比例計算 (用於方向控制) ---
            x_prop = cursor_x / W - 0.5 
            y_prop = cursor_y / H - 0.5 
            print(f"Hand Center Rel(x, y) = ({x_prop:.2f}, {y_prop:.2f})")
            
            # --- 指令發送邏輯 ---
            # 1. Aperture 狀態更新
            new_a_status = 1 if aperture < config.A_THRESHOLD else 0
            
            # 判斷方向性指令與狀態
            center_radius = 0.08 # 增大死區以提高穩定性
            is_center = True
            commands = []
            
            # 如果 aperture 狀態改變，加入 A 指令
            if new_a_status != a_status:
                a_status = new_a_status
                commands.append(('A', 0, a_status))
            
            if x_prop > center_radius:
                commands.append(('L', x_prop - center_radius, a_status))
                is_center = False
            elif x_prop < -center_radius:
                commands.append(('R', center_radius - x_prop, a_status))
                is_center = False
                
            if y_prop > center_radius:
                commands.append(('F', y_prop - center_radius, a_status))
                is_center = False
            elif y_prop < -center_radius:
                commands.append(('B', center_radius - y_prop, a_status))
                is_center = False
            
            # 2. 指令發送 (使用 repeatCounter 進行速率限制)
            if commands:
                if repeatCounter == 0:
                    for command in commands:
                        # 統一計算速度 (如果是 A 指令則速度為 0)
                        speed = int(10 * command[1] * 2.2) + 1 if command[0] != 'A' else 0
                        
                        # 終端機 (動作, 速度, A狀態)
                        print(f"({command[0]}, {speed}, {command[2]})")
                        # Serial 統一輸出 (動作, 速度, A狀態)
                        send_command(command[0], speed, command[2])
                    repeatCounter = 1 # 開始計數
            
        # --- 持續輸出的計時器管理 (每幀執行) ---
        if repeatCounter != 0:
            repeatCounter += 1
            if repeatCounter >= config.INTERVAL:
                repeatCounter = 0

        # --- 繪製按鈕與反饋 ---
        for btn in buttons:
            if btn.value == 'A':
                btn.draw(img, is_active=a_status==1)
            else:
                # 判斷該按鈕對應的指令是否在目前的 commands 中
                is_active = any(cmd[0] == btn.value for cmd in commands) if hands else False
                btn.draw(img, is_active=is_active)

        # --- 顯示模式與狀態資訊 ---
        cv2.putText(img, "find_hands Framework Mode", (50, 50), 
                    cv2.FONT_HERSHEY_DUPLEX, 1.2, (0, 255, 0), 2)
        
        if hands:
            # 顯示手部中心座標與 Aperture 資訊
            cv2.putText(img, f"Center: ({int(cursor_x)}, {int(cursor_y)})", (50, 100), 
                        cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 1)
            cv2.putText(img, f"Aperture: {aperture:.2f}", (50, 140), 
                        cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 100, 0), 2)
            
            # 顯示目前發送的方向指令
            active_cmds = ", ".join([cmd[0] for cmd in commands]) if commands else "Center"
            cv2.putText(img, f"Control: {active_cmds}", (50, 180), 
                        cv2.FONT_HERSHEY_DUPLEX, 1.0, (0, 200, 0), 2)

        # 準備串流資料
        curr_time = time.time()
        fps = 1 / (curr_time - prev_time) if curr_time - prev_time > 0 else 30
        prev_time = curr_time

        ret, buffer = cv2.imencode('.jpg', img)
        frame = buffer.tobytes()

        # 整理要送到 Web 的數據
        cmd_list = []
        if hands and commands:
            cmd_list = [[c[0], float(c[1]), c[2]] for c in commands]

        data = {
            'has_hands': bool(hands),
            'aperture': float(aperture) if hands else 0.0,
            'a_status': a_status,
            'raw_commands': cmd_list,
            'fps': int(fps),
            'latency': 0.0 # 此處可整合 send_command 的延遲
        }
        
        yield (frame, data)

    # 程式結束後釋放資源
    cap.release()
    cv2.destroyAllWindows()
    if ser and ser.is_open:
        ser.close()
