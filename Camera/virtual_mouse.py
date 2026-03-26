import cv2
import mediapipe as mp
import pyautogui
import numpy as np

# lấy kích thước màn hình
screen_w, screen_h = pyautogui.size()

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

# set camera mượt hơn
cap.set(3, 640)
cap.set(4, 480)

prev_x, prev_y = 0, 0
smoothening = 5

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)

            # lấy vị trí ngón trỏ
            x1 = int(handLms.landmark[8].x * w)
            y1 = int(handLms.landmark[8].y * h)

            # ngón giữa
            x2 = int(handLms.landmark[12].x * w)
            y2 = int(handLms.landmark[12].y * h)

            # kiểm tra ngón trỏ giơ lên
            if handLms.landmark[8].y < handLms.landmark[6].y:

                # chuyển tọa độ sang màn hình
                screen_x = np.interp(x1, [0, w], [0, screen_w])
                screen_y = np.interp(y1, [0, h], [0, screen_h])

                # làm mượt chuột
                curr_x = prev_x + (screen_x - prev_x) / smoothening
                curr_y = prev_y + (screen_y - prev_y) / smoothening

                pyautogui.moveTo(curr_x, curr_y)

                prev_x, prev_y = curr_x, curr_y

                cv2.circle(frame, (x1, y1), 10, (0,255,0), -1)

            # click (2 ngón gần nhau)
            distance = np.hypot(x2 - x1, y2 - y1)

            if distance < 40:
                cv2.circle(frame, (x1, y1), 15, (0,0,255), -1)
                pyautogui.click()
                cv2.waitKey(200)  # delay tránh spam click

    cv2.imshow("Virtual Mouse 😎", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()

