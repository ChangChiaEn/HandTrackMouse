# Hand Gesture Mouse Control

This project allows you to control the mouse pointer using hand gestures detected through a webcam. It uses MediaPipe for hand tracking and PyAutoGUI for mouse control, making it possible to move the cursor and trigger clicks without a physical mouse.

## Features
- Hand tracking using MediaPipe
- Control mouse pointer with index finger
- Click events triggered after hovering for 5 seconds
- Hand gestures such as thumb and pinky circle for pressing "ESC"
- Supports smooth cursor movement with interpolation

## Mouse Control Rules
- **Move Cursor**: The cursor follows the movement of the index finger.
- **Smooth Movement**: The movement of the cursor is smoothed using linear interpolation to avoid jerky motion.
- **Clicking**: If the cursor stays in one position for more than 5 seconds, it automatically triggers a mouse click.
- **ESC Key Simulation**: If the thumb and pinky form a circle gesture, the system simulates pressing the "ESC" key.
- **Locking Cursor**: The cursor remains free to move unless locked by specific conditions (e.g., gesture detection can lock/unlock the cursor).
- **Scrolling (Optional)**: Scrolling can be implemented by detecting a thumb and middle finger circle gesture (currently commented out in the code).

## Requirements
- Python 3.x
- OpenCV
- MediaPipe
- PyAutoGUI

# 手勢控制滑鼠

此專案允許你通過攝像頭檢測到的手勢來控制滑鼠指針。使用 MediaPipe 進行手勢追蹤，並通過 PyAutoGUI 控制滑鼠，實現無需實體滑鼠即可移動光標並觸發點擊操作。

## 功能
- 使用 MediaPipe 進行手勢追蹤
- 用食指控制滑鼠指針
- 光標懸停超過 5 秒自動觸發點擊事件
- 大拇指和小指圍成一個圈可模擬按下 "ESC" 鍵
- 支持使用插值平滑移動光標

## 滑鼠控制規則
- **移動光標**：光標會跟隨食指的移動。
- **平滑移動**：光標移動過程中使用線性插值來平滑運動，避免抖動。
- **點擊**：當光標在同一位置停留超過 5 秒時，系統會自動執行滑鼠點擊操作。
- **ESC 鍵模擬**：當大拇指和小指形成一個圈時，系統會模擬按下 "ESC" 鍵。
- **鎖定光標**：除非通過特定條件（例如手勢檢測）鎖定，否則光標可以自由移動。
- **滾動操作（可選）**：可以通過檢測大拇指和中指圍成圈的手勢來實現滾動操作（目前代碼中已註釋掉）。

## 系統需求
- Python 3.x
- OpenCV
- MediaPipe
- PyAutoGUI




