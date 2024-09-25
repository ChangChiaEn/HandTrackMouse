import cv2
import mediapipe as mp
import pyautogui
import math
import time

# 初始化MediaPipe手勢識別
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# 初始化攝像頭
cap = cv2.VideoCapture(0)

# 獲取螢幕大小
screen_width, screen_height = pyautogui.size()

# 上一次光標移動的時間
prev_move_time = time.time()

# 上一個食指的座標
prev_index_x, prev_index_y = 0, 0
lerp_factor = 0.6  # 插值因子，用於平滑光標移動

# 光標鎖定相關變數
cursor_locked = False
locked_x, locked_y = 0, 0

# 用來存儲是否檢測到了手掌展開的手勢
palm_open_detected = False

# 函數：計算兩點之間的距離
def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# 函數：線性插值
def lerp(start, end, factor):
    return start + (end - start) * factor

# 上一個中指的座標
prev_middle_y = 0

# 函數：檢測是否握拳
def is_fist(hand_landmarks):
    landmarks = hand_landmarks.landmark
    tips = [mp_hands.HandLandmark.THUMB_TIP, mp_hands.HandLandmark.INDEX_FINGER_TIP,
            mp_hands.HandLandmark.MIDDLE_FINGER_TIP, mp_hands.HandLandmark.RING_FINGER_TIP,
            mp_hands.HandLandmark.PINKY_TIP]
    joints = [mp_hands.HandLandmark.THUMB_IP, mp_hands.HandLandmark.INDEX_FINGER_PIP,
              mp_hands.HandLandmark.MIDDLE_FINGER_PIP, mp_hands.HandLandmark.RING_FINGER_PIP,
              mp_hands.HandLandmark.PINKY_PIP]

    for tip, joint in zip(tips, joints):
        distance = calculate_distance(landmarks[tip].x, landmarks[tip].y, landmarks[joint].x, landmarks[joint].y)
        if distance > 0.05:  # 根據需要調整閾值
            return False
    return True

# 函數：檢測大拇指和小指是否圍成一個圈
def is_thumb_and_pinky_circle(hand_landmarks):
    landmarks = hand_landmarks.landmark
    thumb_tip = landmarks[mp_hands.HandLandmark.THUMB_TIP]
    pinky_tip = landmarks[mp_hands.HandLandmark.PINKY_TIP]
    distance = calculate_distance(thumb_tip.x, thumb_tip.y, pinky_tip.x, pinky_tip.y)
    return distance < 0.05  # 根據需要調整閾值

# 函數：檢測手掌是否展開
def is_palm_open(hand_landmarks):
    landmarks = hand_landmarks.landmark
    tips = [mp_hands.HandLandmark.THUMB_TIP, mp_hands.HandLandmark.INDEX_FINGER_TIP,
            mp_hands.HandLandmark.MIDDLE_FINGER_TIP, mp_hands.HandLandmark.RING_FINGER_TIP,
            mp_hands.HandLandmark.PINKY_TIP]
    joints = [mp_hands.HandLandmark.THUMB_IP, mp_hands.HandLandmark.INDEX_FINGER_PIP,
              mp_hands.HandLandmark.MIDDLE_FINGER_PIP, mp_hands.HandLandmark.RING_FINGER_PIP,
              mp_hands.HandLandmark.PINKY_PIP]

    for tip, joint in zip(tips, joints):
        distance = calculate_distance(landmarks[tip].x, landmarks[tip].y, landmarks[joint].x, landmarks[joint].y)
        if distance < 0.05:  # 根據需要調整閾值
            return False
    return True

# # 函數：檢測大拇指和中指是否圍成一個圈
# def is_thumb_and_middle_circle(hand_landmarks):
#     landmarks = hand_landmarks.landmark
#     thumb_tip = landmarks[mp_hands.HandLandmark.THUMB_TIP]
#     middle_tip = landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
#     distance = calculate_distance(thumb_tip.x, thumb_tip.y, middle_tip.x, middle_tip.y)
#     return distance < 0.05  # 根據需要調整閾值

while True:
    success, image = cap.read()
    if not success:
        continue

    # 處理圖像並進行手勢識別
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    results = hands.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            landmarks = hand_landmarks.landmark
            index_tip = landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            middle_tip = landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP] # 獲取中指尖座標
            thumb_tip = landmarks[mp_hands.HandLandmark.THUMB_TIP]
            h, w, c = image.shape
            index_x, index_y = int(index_tip.x * w), int(index_tip.y * h)
            middle_x, middle_y = int(middle_tip.x * w), int(middle_tip.y * h)

            # 放大因子，用於增大手指移動光標的距離
            scale_factor = 1.3  # 根據需要調整
            # 禁用安全特性
            pyautogui.FAILSAFE = False
            # 如果光標未鎖定，則根據食指位置移動光標
            if not cursor_locked:
                # 使用插值平滑光標移動
                screen_x = lerp(prev_index_x, index_x / w * screen_width * scale_factor, lerp_factor)
                screen_y = lerp(prev_index_y, index_y / h * screen_height * scale_factor, lerp_factor)
                pyautogui.moveTo(screen_x, screen_y, duration=0.1)

                # 更新上一個座標
                prev_index_x, prev_index_y = screen_x, screen_y

                # 如果光標停留在一處超過5秒，則進行點擊操作
                if time.time() - prev_move_time > 5:
                    pyautogui.click(screen_x, screen_y)
                    prev_move_time = time.time()   
                # 如果檢測到大拇指和小指圍成一個圈的手勢，就模擬按下ESC鍵
                if is_thumb_and_pinky_circle(hand_landmarks):
                    pyautogui.press('esc')   
            # # 大拇指和中指圍成一個圈的滾動操作
            # if is_thumb_and_middle_circle(hand_landmarks):
            #     if prev_middle_y != 0:
            #         y_movement = middle_y - prev_middle_y
            #         scroll_threshold = 10  # 滾動閾值，根據需要進行調整
            #         if abs(y_movement) > scroll_threshold:
            #             scroll_amount = int(y_movement / scroll_threshold) * 10  # 增大滾動的量
            #             pyautogui.scroll(-scroll_amount)  # 反轉滾動方向
            
            prev_middle_y = middle_y
            # 如果檢測到手掌展開動作，就退出主循環
            if is_palm_open(hand_landmarks):
                break
    # 在每一幀圖像中，無論是否檢測到手勢，都檢查是否檢測到了手掌展開的手勢
    if palm_open_detected:
        break

    cv2.imshow("Hand Tracking", image)
    if cv2.waitKey(1) & 0xFF == 27:  # 使用ESC鍵退出
        break

cap.release()
cv2.destroyAllWindows()
