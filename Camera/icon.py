import sys
import cv2
import mediapipe as mp
import urllib.request
import os
import datetime
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QPushButton, QHBoxLayout
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap

# ================= DOWNLOAD ICON =================
def download_icon(url, filename):
    if not os.path.exists(filename):
        urllib.request.urlretrieve(url, filename)

download_icon("https://cdn-icons-png.flaticon.com/512/742/742751.png", "smile.png")
download_icon("https://cdn-icons-png.flaticon.com/512/742/742752.png", "sad.png")
download_icon("https://cdn-icons-png.flaticon.com/512/742/742774.png", "angry.png")
download_icon("https://cdn-icons-png.flaticon.com/512/742/742750.png", "surprise.png")

# ================= LOAD ICON =================
def load_icon(path):
    return cv2.imread(path, cv2.IMREAD_UNCHANGED)

icons = {
    "smile": load_icon("smile.png"),
    "sad": load_icon("sad.png"),
    "angry": load_icon("angry.png"),
    "surprise": load_icon("surprise.png"),
}

# ================= MEDIAPIPE =================
mp_face = mp.solutions.face_mesh
face_mesh = mp_face.FaceMesh()

# ================= FILTER =================
def beauty_filter(frame):
    return cv2.bilateralFilter(frame, 9, 75, 75)

# ================= OVERLAY =================
def overlay_icon(img, icon, x, y, size=120):
    if icon is None:
        return img

    icon = cv2.resize(icon, (size, size))
    h, w, _ = img.shape

    if y < 0 or x < 0 or y+size > h or x+size > w:
        return img

    if icon.shape[2] == 4:
        alpha = icon[:, :, 3] / 255.0
        for c in range(3):
            img[y:y+size, x:x+size, c] = (
                alpha * icon[:, :, c] +
                (1 - alpha) * img[y:y+size, x:x+size, c]
            )

    return img

# ================= APP =================
class App(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("TikTok Style Camera 😎")
        self.setGeometry(100, 100, 900, 700)

        self.label = QLabel()

        # Buttons
        self.btn_capture = QPushButton("📸 Chụp ảnh")
        self.btn_capture.clicked.connect(self.capture_image)

        self.btn_filter = QPushButton("✨ Bật/Tắt Filter")
        self.btn_filter.clicked.connect(self.toggle_filter)

        # Layout
        hbox = QHBoxLayout()
        hbox.addWidget(self.btn_capture)
        hbox.addWidget(self.btn_filter)

        vbox = QVBoxLayout()
        vbox.addWidget(self.label)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

        self.cap = cv2.VideoCapture(0)
        self.filter_on = True
        self.current_frame = None

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def toggle_filter(self):
        self.filter_on = not self.filter_on

    def capture_image(self):
        if self.current_frame is not None:
            filename = f"capture_{datetime.datetime.now().strftime('%H%M%S')}.jpg"
            cv2.imwrite(filename, self.current_frame)
            print("Đã lưu:", filename)

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        frame = cv2.flip(frame, 1)

        # ✨ Filter
        if self.filter_on:
            frame = beauty_filter(frame)

        h, w, _ = frame.shape

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = face_mesh.process(rgb)

        emotion = "sad"  # mặc định

        if result.multi_face_landmarks:
            for face in result.multi_face_landmarks:
                top = face.landmark[13]
                bottom = face.landmark[14]
                left = face.landmark[61]
                right = face.landmark[291]

                mouth_h = abs(int(bottom.y*h) - int(top.y*h))
                mouth_w = abs(int(right.x*w) - int(left.x*w))

                # 🧠 Nhận diện
                if mouth_h > 35:
                    emotion = "surprise"
                elif mouth_w > 90:
                    emotion = "smile"
                elif mouth_h < 8:
                    emotion = "angry"
                else:
                    emotion = "sad"

        # 🔥 ICON Ở GÓC PHẢI TRÊN
        frame = overlay_icon(frame, icons[emotion], w-140, 20)

        self.current_frame = frame.copy()

        # Show Qt
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        qt_image = QImage(rgb_image.data, w, h, ch*w, QImage.Format_RGB888)

        self.label.setPixmap(QPixmap.fromImage(qt_image))


# ================= RUN =================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())