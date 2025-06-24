import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton
from PyQt5.QtCore import Qt


class SecondWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.setWindowTitle("セカンドウィンドウ")
        self.resize(400, 300)
        label = QLabel("2画面目に遷移しました", self)
        label.move(100, 130)
        self.parent = parent

        self.back_btn = QPushButton("戻る", self)
        self.back_btn.move(150, 200)
        self.back_btn.clicked.connect(self.go_back)

    def go_back(self):
        if self.parent:
            self.parent.show()
        self.close()




class VariableWindows(QWidget):
    def __init__(self):
        super().__init__()
        self.label = QLabel("中央の文字", self)
        self.btn = QPushButton("画面遷移", self)
        self.btn.setStyleSheet("background-color:red")
        self.btn.move(150, 220)
        self.btn.clicked.connect(self.on_button_click)
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
        self.btn = QPushButton("ボタン", self)
        self.btn.setStyleSheet("background-color:red")
        self.btn.move(150, 220)  # ボタンの位置を指定
        self.btn.clicked.connect(self.on_button_click)

    def on_button_click(self):
        self.label.setText("ボタンが押されました")
        self.label.adjustSize()  # ラベルサイズを自動調整
        self.second_window = SecondWindow(parent = self)
        self.second_window.show()
        self.hide()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VariableWindows()
    window.frame()
    window.show()
    sys.exit(app.exec_())