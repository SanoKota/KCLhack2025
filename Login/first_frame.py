import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import form  # Uncomment and use this if you have a form.py file in the same directory
from login import LoginWindow  # Uncomment and use this if you have a login.py file in the same directory

class SecondWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.form_window = form.MainWindow()
        self.form_window.show()
        self.login_window = LoginWindow()
        self.login_window.show()


class VariableWindows(QWidget):
    def __init__(self):
        super().__init__()

    def frame(self):
        self.setWindowTitle("aaa")
        self.label = QLabel("中央の文字", self)
        self.label.setFont(QFont("Arial", 18, QFont.Bold))
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("color: #1a73e8; margin: 20px;")

        self.login = QPushButton("ログイン", self)
        self.login.setStyleSheet("background-color:red")
        self.btn = QPushButton("新規登録", self)
        self.btn.setStyleSheet("background-color:red")
        self.btn.clicked.connect(self.on_button_click)
        self.login.clicked.connect(self.open_login_window)

        # ボタンを横並びで中央に
        btn_layout = QHBoxLayout()
        btn_layout.addStretch(1)
        btn_layout.addWidget(self.login)
        btn_layout.addSpacing(40)
        btn_layout.addWidget(self.btn)
        btn_layout.addStretch(1)

        # 全体を縦並びで中央に
        layout = QVBoxLayout()
        layout.addStretch(2)
        layout.addWidget(self.label)
        layout.addStretch(1)
        layout.addLayout(btn_layout)
        layout.addStretch(3)
        self.setLayout(layout)
        self.showMaximized()

    def open_login_window(self):
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()

    def on_button_click(self):
        self.label.setText("ボタンが押されました")
        self.label.adjustSize()  # ラベルサイズを自動調整
        self.second_window = form.MainWindow()
        self.second_window.show()
        self.close()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VariableWindows()
    window.frame()
    window.show()
    sys.exit(app.exec_())