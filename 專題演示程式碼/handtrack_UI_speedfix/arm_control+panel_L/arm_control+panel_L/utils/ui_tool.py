# utils/ui_tool.py
import cv2
import numpy as np

class ControllerButton:
    def __init__(self, center, shape, value, size=60):
        self.center = center
        self.shape = shape
        self.value = value
        self.size = size
        
    def draw(self, img, is_active=False):
        # A 按鈕在鎖定模式下顯示紅色，否則預設為淡灰色
        color = (0, 0, 255) if is_active and self.value == 'A' else (225, 225, 225)
        
        if self.shape == 'circle':
            cv2.circle(img, self.center, self.size, color, cv2.FILLED)
            cv2.circle(img, self.center, self.size, (50, 50, 50), 3)
        elif self.shape == 'triangle':
            cx, cy = self.center
            s = self.size
            if self.value == 'F': pts = np.array([[cx, cy-s], [cx-s, cy+s], [cx+s, cy+s]])
            elif self.value == 'B': pts = np.array([[cx, cy+s], [cx-s, cy-s], [cx+s, cy-s]])
            elif self.value == 'L': pts = np.array([[cx-s, cy], [cx+s, cy-s], [cx+s, cy+s]])
            elif self.value == 'R': pts = np.array([[cx+s, cy], [cx-s, cy-s], [cx-s, cy+s]])
            cv2.drawContours(img, [pts], 0, color, cv2.FILLED)
            cv2.drawContours(img, [pts], 0, (50, 50, 50), 3)
        cv2.putText(img, self.value, (self.center[0]-15, self.center[1]+15),
                    cv2.FONT_HERSHEY_PLAIN, 3, (50, 50, 50), 3)

    def is_clicked(self, x, y):
        dist = np.sqrt((x - self.center[0])**2 + (y - self.center[1])**2)
        return dist < self.size


class RectangleButton:
    def __init__(self, rect, value):
        """
        rect: (x_min, y_min, x_max, y_max)
        value: 顯示文字與標識用途
        """
        self.x_min, self.y_min, self.x_max, self.y_max = rect
        self.value = value
        
    def draw(self, img, is_active=False, is_disabled=False):
        # 繪製半透明矩形或外框
        overlay = img.copy()
        
        if is_disabled:
            color = (150, 150, 150) # 失效時較暗
            border_color = (100, 100, 100)
            text_color = (150, 150, 150)
            alpha = 0.2
        else:
            color = (0, 255, 0) if is_active else (200, 200, 200) # 若 active 為亮綠色，否則預設淡色
            border_color = (100, 100, 100)
            text_color = (50, 50, 50)
            alpha = 0.3
            
        cv2.rectangle(overlay, (self.x_min, self.y_min), (self.x_max, self.y_max), color, -1)
        # 用 addWeighted 產出半透明效果
        cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)
        
        # 畫實線外框
        cv2.rectangle(img, (self.x_min, self.y_min), (self.x_max, self.y_max), border_color, 2)
        
        # 處理文字居中
        text = self.value
        font = cv2.FONT_HERSHEY_DUPLEX
        font_scale = 1.5
        thickness = 2
        (text_w, text_h), _ = cv2.getTextSize(text, font, font_scale, thickness)
        cx = (self.x_min + self.x_max) // 2
        cy = (self.y_min + self.y_max) // 2
        text_x = cx - text_w // 2
        text_y = cy + text_h // 2
        
        cv2.putText(img, text, (text_x, text_y), font, font_scale, text_color, thickness)

    def is_clicked(self, x, y):
        # 判斷點擊座標是否在矩形範圍內
        return self.x_min <= x <= self.x_max and self.y_min <= y <= self.y_max

