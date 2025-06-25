import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QVBoxLayout, QGridLayout, QSizePolicy
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

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
            "三角関数",
            "指数・対数関数",
            "微分",
            "積分",
            "ベクトル",
            "数列",
            "確率・統計",
            "微分方程式",
            "行列(固有値・固有ベクトル)",
            "複素数",
            "その他",
        ]
        main_layout = QVBoxLayout()
        main_layout.addWidget(label)
        main_layout.addSpacing(30)
        grid = QGridLayout()
        grid.setSpacing(30)
        col_count = 4
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
        self.hide()
        self.grade_window = SelectGameFrame(selected_range)
        self.grade_window.show()

class SelectGameFrame(QWidget):
    def __init__(self, selected_range=None):
        super().__init__()
        self.selected_range = selected_range
        self.setWindowTitle("学年選択")
        self.setFont(QFont("Arial", 14))
        self.init_ui()

    def init_ui(self):
        label = QLabel(f"{self.selected_range} の学年を選択してください" if self.selected_range else "学年を選択してください", self)
        label.setFont(QFont("Arial", 20, QFont.Bold))
        label.setAlignment(Qt.AlignCenter)
        self.buttons = []
        high_school = [
            "高校1年の問題",
            "高校2年の問題",
            "高校3年の問題"
        ]
        university = [
            "大学1年の問題",
            "大学2年の問題",
            "大学3年の問題",
            "大学4年の問題"
        ]
        main_layout = QVBoxLayout()
        main_layout.addWidget(label)
        main_layout.addSpacing(100)  # ボタン群を下に下げる
        # 高校
        hs_label = QLabel("高校", self)
        hs_label.setFont(QFont("Arial", 20, QFont.Bold))
        hs_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(hs_label)
        hs_grid = QGridLayout()
        hs_grid.setSpacing(30)
        for i, grade in enumerate(high_school):
            btn = QPushButton(grade, self)
            btn.setMinimumSize(120, 120)
            btn.setMaximumSize(200, 200)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            btn.setStyleSheet("font-size:18px; background-color:#e3f2fd; border-radius:18px;")
            btn.clicked.connect(self.on_select)
            hs_grid.addWidget(btn, 0, i)
            self.buttons.append(btn)
        main_layout.addLayout(hs_grid)
        # 大学
        main_layout.addSpacing(80)
        uni_label = QLabel("大学", self)
        uni_label.setFont(QFont("Arial", 20, QFont.Bold))
        uni_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(uni_label)
        uni_grid = QGridLayout()
        uni_grid.setSpacing(30)
        for i, grade in enumerate(university):
            btn = QPushButton(grade, self)
            btn.setMinimumSize(120, 120)
            btn.setMaximumSize(200, 200)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            btn.setStyleSheet("font-size:18px; background-color:#e3f2fd; border-radius:18px;")
            btn.clicked.connect(self.on_select)
            uni_grid.addWidget(btn, 0, i)
            self.buttons.append(btn)
        main_layout.addLayout(uni_grid)
        main_layout.addStretch(1)
        # 戻るボタン
        back_btn = QPushButton("← 戻る", self)
        back_btn.setFixedWidth(100)
        back_btn.setStyleSheet("font-size:16px; background-color:#bdbdbd; border-radius:10px; margin-bottom:20px;")
        back_btn.clicked.connect(self.go_back)
        main_layout.addWidget(back_btn, alignment=Qt.AlignLeft)
        self.setLayout(main_layout)
        self.showMaximized()

    def go_back(self):
        self.hide()
        self.range_window = RangeSelectFrame()
        self.range_window.show()

    def on_select(self):
        sender = self.sender()
        selected_grade = sender.text()
        # ここで選択された範囲と学年に応じた処理を実装
        print(f"範囲: {self.selected_range}, 学年: {selected_grade}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RangeSelectFrame()
    window.show()
    sys.exit(app.exec_())