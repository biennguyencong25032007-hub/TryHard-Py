import cv2
import mediapipe as mp
import pyautogui
import numpy as np

screen_w, screen_h = pyautogui.size()

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

prev_x, prev_y = 0, 0
smooth = 5
dragging = False

def fingers_up(hand):
    fingers = []

    # thumb
    if hand.landmark[4].x < hand.landmark[3].x:
        fingers.append(1)
    else:
        fingers.append(0)

    tips = [8, 12, 16, 20]
    for tip in tips:
        if hand.landmark[tip].y < hand.landmark[tip-2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers

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

            x1 = int(handLms.landmark[8].x * w)   # index
            y1 = int(handLms.landmark[8].y * h)

            x2 = int(handLms.landmark[12].x * w)  # middle
            y2 = int(handLms.landmark[12].y * h)

            fingers = fingers_up(handLms)

            #MOVE
            if fingers[1] == 1 and fingers[2] == 0:
                screen_x = np.interp(x1, [0, w], [0, screen_w])
                screen_y = np.interp(y1, [0, h], [0, screen_h])

                curr_x = prev_x + (screen_x - prev_x) / smooth
                curr_y = prev_y + (screen_y - prev_y) / smooth

                pyautogui.moveTo(curr_x, curr_y)
                prev_x, prev_y = curr_x, curr_y

                cv2.circle(frame, (x1, y1), 10, (0,255,0), -1)

            # LEFT CLICK
            distance = np.hypot(x2 - x1, y2 - y1)
            if distance < 30:
                pyautogui.click()
                cv2.circle(frame, (x1, y1), 15, (0,0,255), -1)
                cv2.waitKey(200)

            # RIGHT CLICK
            if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0:
                pyautogui.rightClick()
                cv2.putText(frame, "Right Click", (10,50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
                cv2.waitKey(200)

            # SCROLL 
            if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1:
                pyautogui.scroll(20)
                cv2.putText(frame, "Scroll", (10,50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)

            # DRAG
            if fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 0:
                if not dragging:
                    pyautogui.mouseDown()
                    dragging = True
                cv2.putText(frame, "Dragging", (10,80),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)
            else:
                if dragging:
                    pyautogui.mouseUp()
                    dragging = False

            # PAUSE
            if sum(fingers) == 5:
                cv2.putText(frame, "PAUSE", (200,200),
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 3)
                continue

    cv2.imshow("Virtual Mouse PRO MAX 😎", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()