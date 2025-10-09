import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QVBoxLayout, QGridLayout, QSizePolicy
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from .game_page import GamePage  # パッケージとして実行する場合
from .making_problem import MakingProblemWindow  # 追加
from .question import DifferentialGame  # 追加

class RangeSelectFrame(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("数学範囲選択")
        self.setFont(QFont("Arial", 14))
        self.init_ui()

    def init_ui(self):
        label = QLabel("数学の範囲を選択してください", self)
        label.setFont(QFont("Arial", 20, QFont.Bold))
        label.setAlignment(Qt.AlignCenter)
        self.buttons = []
        ranges = [
            "微分",
            "積分",
        ]
        main_layout = QVBoxLayout()
        main_layout.addWidget(label)
        main_layout.addSpacing(30)
        grid = QGridLayout()
        grid.setSpacing(30)
        col_count = 2  # 2つのボタンなので2列に設定
        for i, r in enumerate(ranges):
            btn = QPushButton(r, self)
            btn.setMinimumSize(120, 120)
            btn.setMaximumSize(200, 200)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            btn.setStyleSheet("font-size:18px; background-color:#ffe082; border-radius:18px;")
            btn.clicked.connect(self.on_select)
            grid.addWidget(btn, i // col_count, i % col_count)
            self.buttons.append(btn)
        main_layout.addLayout(grid)
        main_layout.addStretch(1)
        self.setLayout(main_layout)
        self.showMaximized()

    def on_select(self):
        sender = self.sender()
        selected_range = sender.text()
        print(f"選択された範囲: {selected_range}")

        def go_to_question_page(df):
            self.question_window = DifferentialGame(df, mode=selected_range)
            self.question_window.show()
            self.close()

        self.making_window = MakingProblemWindow(selected_range, go_to_question_page)
        self.making_window.show()
        self.hide()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RangeSelectFrame()
    window.show()
    sys.exit(app.exec_())