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

        # ヒント欄（右上）: ボタンで隠す
        self.hint1_btn = QPushButton("ヒント1を表示", self)
        self.hint1_label = QLabel("", self)
        self.hint1_label.setFont(QFont("Arial", 12))
        self.hint1_btn.clicked.connect(self.show_hint1)

        self.hint2_btn = QPushButton("ヒント2を表示", self)
        self.hint2_label = QLabel("", self)
        self.hint2_label.setFont(QFont("Arial", 12))
        self.hint2_btn.clicked.connect(self.show_hint2)

        # 回答欄（右下）
        self.answer_edit = QLineEdit(self)
        self.answer_edit.setPlaceholderText("回答を入力")
        self.submit_btn = QPushButton("回答", self)
        self.submit_btn.clicked.connect(self.check_answer)

        # 右側レイアウト
        right_layout = QVBoxLayout()
        right_layout.addWidget(self.hint1_btn, alignment=Qt.AlignTop)
        right_layout.addWidget(self.hint1_label, alignment=Qt.AlignTop)
        right_layout.addWidget(self.hint2_btn, alignment=Qt.AlignTop)
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

    def show_hint1(self):
        self.hint1_label.setText("ヒント1: " + self.data[self.current]["Hint1"])
        self.hint1_btn.setEnabled(False)

    def show_hint2(self):
        self.hint2_label.setText("ヒント2: " + self.data[self.current]["Hint2"])
        self.hint2_btn.setEnabled(False)

    def check_answer(self):
        user_answer = self.answer_edit.text().strip()
        correct_answer = self.data[self.current]["Answer"].strip()
        explanation = self.data[self.current]["Explanation"]
        # 回答後にAnswer画面を表示
        self.answer_window = AnswerWindow(
            correct_answer, explanation, self.current, len(self.data), self
        )
        self.answer_window.showMaximized()
        self.hide()

    def show_next(self, next_index):
        if next_index < len(self.data):
            self.current = next_index
            self.question_label.setText(self.data[self.current]["Question"])
            self.hint1_label.setText("")
            self.hint2_label.setText("")
            self.hint1_btn.setEnabled(True)
            self.hint2_btn.setEnabled(True)
            self.answer_edit.clear()
            self.showMaximized()
        else:
            QMessageBox.information(self, "終了", "全ての問題が終了しました")
            self.close()

class AnswerWindow(QWidget):
    def __init__(self, answer, explanation, current, total, parent_game):
        super().__init__()
        self.setWindowTitle("回答")
        self.parent_game = parent_game
        self.next_index = current + 1

        layout = QVBoxLayout()
        answer_label = QLabel(f"答え: {answer}", self)
        answer_label.setFont(QFont("Arial", 32, QFont.Bold))
        answer_label.setAlignment(Qt.AlignCenter)
        explanation_label = QLabel(explanation, self)
        explanation_label.setFont(QFont("Arial", 18))
        explanation_label.setAlignment(Qt.AlignCenter)
        layout.addStretch(1)
        layout.addWidget(answer_label)
        layout.addWidget(explanation_label)
        layout.addStretch(1)

        btn_layout = QHBoxLayout()
        self.next_btn = QPushButton("次の問題へ", self)
        self.next_btn.setFont(QFont("Arial", 16))
        self.next_btn.clicked.connect(self.next_question)
        self.exit_btn = QPushButton("終了する", self)
        self.exit_btn.setFont(QFont("Arial", 16))
        self.exit_btn.clicked.connect(self.close)
        btn_layout.addWidget(self.next_btn)
        btn_layout.addWidget(self.exit_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)
        self.showMaximized()

    def next_question(self):
        self.close()
        self.parent_game.show_next(self.next_index)

