import cv2
import mediapipe as mp
import numpy as np

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

cv2.namedWindow("Air Draw PRO UI 😎", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Air Draw PRO UI 😎", 1000, 700)
cv2.moveWindow("Air Draw PRO UI 😎", 200, 100)

canvas = None
prev_x, prev_y = 0, 0

colors = [(255,0,0), (0,255,0), (0,0,255), (0,255,255)]
color = colors[0]

thickness = 5

show_panel = False
toggle_cooldown = 0

def count_fingers(hand):
    fingers = []
    if hand.landmark[4].x < hand.landmark[3].x:
        fingers.append(1)
    else:
        fingers.append(0)

    tips = [8,12,16,20]
    for tip in tips:
        if hand.landmark[tip].y < hand.landmark[tip-2].y:
            fingers.append(1)
        else:
            fingers.append(0)
    return sum(fingers)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)

    if canvas is None:
        canvas = np.zeros_like(frame)

    h, w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)

            x = int(handLms.landmark[8].x * w)
            y = int(handLms.landmark[8].y * h)

            fingers = count_fingers(handLms)

            if fingers == 4 and toggle_cooldown == 0:
                show_panel = not show_panel
                toggle_cooldown = 20
                prev_x, prev_y = 0, 0

            if toggle_cooldown > 0:
                toggle_cooldown -= 1

            if show_panel:
                cv2.rectangle(frame, (0,0), (w,120), (50,50,50), -1)

                # palette màu
                for i, c in enumerate(colors):
                    cv2.rectangle(frame, (10+i*60, 10), (60+i*60, 60), c, -1)

                # thanh thickness
                cv2.rectangle(frame, (10, 70), (200, 100), (200,200,200), -1)
                cv2.rectangle(frame, (10, 70), (10+thickness*10, 100), color, -1)

                # chọn màu
                if y < 60 and x < 60*len(colors):
                    index = x // 60
                    color = colors[index]

                # chỉnh nét
                if 70 < y < 100 and 10 < x < 200:
                    thickness = max(1, (x-10)//10)

                prev_x, prev_y = 0, 0

            else:
                # vẽ
                if fingers == 1:
                    if prev_x == 0 and prev_y == 0:
                        prev_x, prev_y = x, y

                    cx = (prev_x + x)//2
                    cy = (prev_y + y)//2

                    cv2.line(canvas, (prev_x, prev_y), (cx, cy), color, thickness)
                    prev_x, prev_y = cx, cy

                # xóa
                elif fingers == 2:
                    cv2.circle(canvas, (x,y), 30, (0,0,0), -1)
                    prev_x, prev_y = 0, 0

                # clear
                elif fingers == 5:
                    canvas = np.zeros_like(frame)
                    prev_x, prev_y = 0, 0

                else:
                    prev_x, prev_y = 0, 0

    gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, inv = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY_INV)
    inv = cv2.cvtColor(inv, cv2.COLOR_GRAY2BGR)

    frame = cv2.bitwise_and(frame, inv)
    frame = cv2.bitwise_or(frame, canvas)

    cv2.imshow("Air Draw PRO UI 😎", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()