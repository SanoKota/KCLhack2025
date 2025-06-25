import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from PyQt5.QtCore import Qt

class RatioLabelWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("割合で文字を配置")
        self.resize(400, 300)

        # ラベル作成
        self.label = QLabel("中央の文字", self)
        self.label.setStyleSheet("font-size: 16px; background: lightgray;")
        self.label.adjustSize()  # サイズを自動調整

    def resizeEvent(self, event):
        # 現在のウィンドウサイズを取得
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RatioLabelWindow()
    window.show()
    sys.exit(app.exec_())
