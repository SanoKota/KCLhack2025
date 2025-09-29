from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
import tempfile


def latex_to_pixmap(latex_str):
    fig = plt.figure(figsize=(2, 0.7))
    fig.text(0.5, 0.5, latex_str, fontsize=32, ha='center', va='center')
    fig.patch.set_alpha(0)
    plt.axis('off')
    fig.canvas.draw()
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmpfile:
        fig.savefig(tmpfile.name, bbox_inches='tight', pad_inches=0.2, transparent=True)
        plt.close(fig)
        pixmap = QPixmap(tmpfile.name)
    return pixmap


class AnswerWindow(QWidget):
    def __init__(self, answer, explanation, current, total, parent_game):
        super().__init__()
        self.setWindowTitle("回答")
        self.parent_game = parent_game
        self.next_index = current + 1

        layout = QVBoxLayout()
        # 答えをlatex画像で表示
        answer_row = QHBoxLayout()
        answer_text_label = QLabel("答え:", self)
        answer_text_label.setFont(QFont("Arial", 24, QFont.Bold))
        answer_text_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        answer_label = QLabel(self)
        answer_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        answer_label.setPixmap(latex_to_pixmap(answer))
        answer_row.addWidget(answer_text_label)
        answer_row.addWidget(answer_label)
        layout.addStretch(1)
        layout.addLayout(answer_row)
        # 解説はテキストで表示
        explanation_label = QLabel(explanation, self)
        explanation_label.setFont(QFont("Arial", 18))
        explanation_label.setAlignment(Qt.AlignCenter)
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