# utils/detector_tool.py
from cvzone.HandTrackingModule import HandDetector

class HandControlDetector:
    def __init__(self, detection_con=0.8, max_hands=1):
        """
        初始化手部偵測器
        """
        self.detector = HandDetector(detectionCon=detection_con, maxHands=max_hands)

    def find_hands(self, img, draw=True, flip_type=False):
        """
        尋找手部並回傳 hands 資訊與繪製後的影像
        """
        hands, img = self.detector.findHands(img, draw=draw, flipType=flip_type)
        return hands, img

    def get_distance(self, p1, p2, img=None):
        """
        計算兩點距離，並可選擇是否畫在影像上
        p1, p2 通常為 lmList 中的座標 (如 lmList[4][:2] 與 lmList[8][:2])
        """
        if img is not None:
            length, info, img = self.detector.findDistance(p1, p2, img)
            return length, info, img
        else:
            length, info, _ = self.detector.findDistance(p1, p2)
            return length, info, None
