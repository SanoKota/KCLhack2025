from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


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