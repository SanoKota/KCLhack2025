import sys
import csv
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QGridLayout, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class DifferentialGame(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("微分問題")
        self.setFont(QFont("Arial", 14))
        self.data = self.load_csv("GameFrame/GameData/differentioal.csv")
        self.current = 0
        self.init_ui()

    def load_csv(self, path):
        with open(path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return list(reader)

    def init_ui(self):
        # 問題欄（左半分の中心）
        left_layout = QVBoxLayout()
        left_layout.addStretch(1)
        self.question_label = QLabel(self.data[self.current]["Question"], self)
        self.question_label.setFont(QFont("Arial", 18, QFont.Bold))
        self.question_label.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(self.question_label)
        left_layout.addStretch(1)

        # ヒント欄（右上）
        self.hint1_label = QLabel("ヒント1: " + self.data[self.current]["Hint1"], self)
        self.hint2_label = QLabel("ヒント2: " + self.data[self.current]["Hint2"], self)
        self.hint1_label.setFont(QFont("Arial", 12))
        self.hint2_label.setFont(QFont("Arial", 12))

        # 回答欄（右下）
        self.answer_edit = QLineEdit(self)
        self.answer_edit.setPlaceholderText("回答を入力")
        self.submit_btn = QPushButton("回答", self)
        self.submit_btn.clicked.connect(self.check_answer)

        # 右側レイアウト
        right_layout = QVBoxLayout()
        right_layout.addWidget(self.hint1_label, alignment=Qt.AlignTop)
        right_layout.addWidget(self.hint2_label, alignment=Qt.AlignTop)
        right_layout.addStretch(1)
        right_layout.addWidget(self.answer_edit, alignment=Qt.AlignBottom)
        right_layout.addWidget(self.submit_btn, alignment=Qt.AlignBottom)

        # 全体レイアウト
        main_layout = QHBoxLayout()
        main_layout.addLayout(left_layout, stretch=2)
        main_layout.addLayout(right_layout, stretch=3)
        self.setLayout(main_layout)
        self.showMaximized()

    def check_answer(self):
        user_answer = self.answer_edit.text().strip()
        correct_answer = self.data[self.current]["Answer"].strip()
        explanation = self.data[self.current]["Explanation"]
        if user_answer == correct_answer:
            QMessageBox.information(self, "正解", "正解です！\n" + explanation)
        else:
            QMessageBox.warning(self, "不正解", "不正解です。\n" + explanation)

