import sys
import csv
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QGridLayout, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from Result.result import AnswerWindow
import matplotlib.pyplot as plt
import tempfile
from PyQt5.QtGui import QPixmap

def latex_to_pixmap(latex_str):
    # latex_strが$で囲まれていなければ自動で囲む
    if not (latex_str.startswith("$") and latex_str.endswith("$")):
        latex_str = f"${latex_str}$"
    fig = plt.figure(figsize=(2, 0.7))
    fig.text(0.5, 0.5, latex_str, fontsize=24, ha='center', va='center')
    fig.patch.set_alpha(0)
    plt.axis('off')
    fig.canvas.draw()
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmpfile:
        fig.savefig(tmpfile.name, bbox_inches='tight', pad_inches=0.2, transparent=True)
        plt.close(fig)
        pixmap = QPixmap(tmpfile.name)
    return pixmap

class DifferentialGame(QWidget):
    def __init__(self, mode="微分"):
        super().__init__()
        self.mode = mode  # "微分" or "積分"
        self.setWindowTitle(f"{self.mode}問題")
        self.setFont(QFont("Arial", 14))
        # modeに応じてCSVファイルを切り替え
        if self.mode == "微分":
            csv_path = "GameFrame/GameData/differentioal.csv"
        else:
            csv_path = "GameFrame/GameData/integral.csv"
        self.data = self.load_csv(csv_path)
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
        # LaTeX数式を画像化して表示
        self.question_label = QLabel(self)
        self.question_label.setAlignment(Qt.AlignCenter)
        question_text = self.data[self.current]["Question"]
        if question_text.startswith("$") and question_text.endswith("$"):
            self.question_label.setPixmap(latex_to_pixmap(question_text))
        else:
            self.question_label.setText(question_text)
            self.question_label.setFont(QFont("Arial", 18, QFont.Bold))
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
            question_text = self.data[self.current]["Question"]
            if question_text.startswith("$") and question_text.endswith("$"):
                self.question_label.setPixmap(latex_to_pixmap(question_text))
                self.question_label.setText("")  # 画像表示時はテキストをクリア
            else:
                self.question_label.setPixmap(QPixmap())  # 画像をクリア
                self.question_label.setText(question_text)
                self.question_label.setFont(QFont("Arial", 18, QFont.Bold))
            self.hint1_label.setText("")
            self.hint2_label.setText("")
            self.hint1_btn.setEnabled(True)
            self.hint2_btn.setEnabled(True)
            self.answer_edit.clear()
            self.showMaximized()
        else:
            QMessageBox.information(self, "終了", "全ての問題が終了しました")
            self.close()
