import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton
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
        self.label = QLabel("中央の文字", self)
        self.setWindowTitle("メインウィンドウ")
        self.resize(400, 300)
        self.second_window = None
    def frame(self):
        self.setWindowTitle("aaa")
        self.resize(400, 300)
        self.button()
    
    def resizeEvent(self, event):
        win_width = self.width()
        win_height = self.height()

        # ラベルのサイズ
        label_width = self.label.width()
        label_height = self.label.height()

        # 配置する割合（ここでは中央＝0.5, 0.5）
        x_ratio = 0.5
        y_ratio = 0.5

        # 新しい位置を計算（中心を合わせる）
        x = int(win_width * x_ratio - label_width / 2)
        y = int(win_height * y_ratio - label_height / 2)

        self.label.move(x, y)
        
    def button(self):
        self.login = QPushButton("ログイン", self)
        self.login.setStyleSheet("background-color:red")
        self.login.move(50, 220)  # ボタンの位置を指定
        self.btn = QPushButton("新規登録", self)
        self.btn.setStyleSheet("background-color:red")
        self.btn.move(150, 220)  # ボタンの位置を指定
        self.btn.clicked.connect(self.on_button_click)
        self.login.clicked.connect(self.open_login_window)

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