import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import QTimer, Qt

class Stopwatch(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Stopwatch")

        self.time = 0  

        self.label = QLabel("00:00:00.00")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("""
            background-color: lightblue;
            font-size: 40px;
            font-weight: bold;
            padding: 20px;
        """)

        self.start_btn = QPushButton("Start")
        self.stop_btn = QPushButton("Stop")
        self.reset_btn = QPushButton("Reset")

        hbox = QHBoxLayout()
        hbox.addWidget(self.start_btn)
        hbox.addWidget(self.stop_btn)
        hbox.addWidget(self.reset_btn)

        vbox = QVBoxLayout()
        vbox.addWidget(self.label)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)

        self.start_btn.clicked.connect(self.start)
        self.stop_btn.clicked.connect(self.stop)
        self.reset_btn.clicked.connect(self.reset)

    def update_time(self):
        self.time += 1

        cs = self.time % 100
        s = (self.time // 100) % 60
        m = (self.time // 6000) % 60
        h = self.time // 360000

        self.label.setText(f"{h:02}:{m:02}:{s:02}.{cs:02}")

    def start(self):
        self.timer.start(10)  

    def stop(self):
        self.timer.stop()

    def reset(self):
        self.timer.stop()
        self.time = 0
        self.label.setText("00:00:00.00")




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Stopwatch()
    window.resize(500, 200)
    window.show()
    sys.exit(app.exec_())
