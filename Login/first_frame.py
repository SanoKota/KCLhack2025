import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QFont, QPainter, QPixmap
from PyQt5.QtCore import Qt
from GameFrame.select_game_frame import RangeSelectFrame

class VariableWindows(QWidget):
    def __init__(self):
        super().__init__()
        self.background = QPixmap("Login/LoginPage.png")  # 画像パスを指定

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.background)

    def frame(self):
        self.setWindowTitle("微分積分マスター")
        self.label = QLabel("スタート", self)
        self.label.setFont(QFont("Arial", 24, QFont.Bold))
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("color: #1a73e8; margin: 20px; background: transparent;")

        self.start_btn = QPushButton("スタート", self)
        self.start_btn.setFont(QFont("Arial", 18, QFont.Bold))
        self.start_btn.clicked.connect(self.open_select_window)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch(1)
        btn_layout.addWidget(self.start_btn)
        btn_layout.addStretch(1)

        layout = QVBoxLayout()
        layout.addStretch(2)
        layout.addWidget(self.label)
        layout.addStretch(1)
        layout.addLayout(btn_layout)
        layout.addStretch(3)
        self.setLayout(layout)
        self.showMaximized()

    def open_select_window(self):
        self.select_window = RangeSelectFrame()
        self.select_window.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VariableWindows()
    window.frame()
    window.show()
    sys.exit(app.exec_())