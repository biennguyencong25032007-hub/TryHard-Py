import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PyQt5.QtCore import QTimer, QTime
from PyQt5.QtGui import QFont

class DigitalClock(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Digital Clock")
        self.setStyleSheet("background-color: black;")

        layout = QVBoxLayout()

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)

        font = QFont("DS-Digital", 60)  
        self.label.setFont(font)
        self.label.setStyleSheet("color: lime;")

        layout.addWidget(self.label)
        self.setLayout(layout)

        timer = QTimer(self)
        timer.timeout.connect(self.update_time)
        timer.start(1000)

        self.update_time()

    def update_time(self):
        current_time = QTime.currentTime()
        display_text = current_time.toString("hh:mm:ss AP")
        self.label.setText(display_text)

if __name__ == "__main__":
    from PyQt5.QtCore import Qt

    app = QApplication(sys.argv)
    clock = DigitalClock()
    clock.resize(600, 200)
    clock.show()
    sys.exit(app.exec_())