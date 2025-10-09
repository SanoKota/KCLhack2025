from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QScrollArea
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
import tempfile
import re


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

        main_layout = QVBoxLayout()
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
        main_layout.addLayout(answer_row)

        # 解説部分をスクロール可能＆画面全体に表示
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        explanation_widget = QWidget()
        explanation_layout = QVBoxLayout(explanation_widget)
        explanation_layout.setContentsMargins(40, 40, 40, 40)  # 余白を追加

        parts = re.split(r'(\$.*?\$|\$\$.*?\$\$)', explanation)
        for part in parts:
            if re.match(r'^\$.*\$$', part) or re.match(r'^\$\$.*\$\$$', part):
                label = QLabel(explanation_widget)
                label.setAlignment(Qt.AlignCenter)
                label.setPixmap(latex_to_pixmap(part))
                explanation_layout.addWidget(label)
            elif part.strip():
                label = QLabel(part, explanation_widget)
                label.setFont(QFont("Arial", 18))
                label.setAlignment(Qt.AlignCenter)
                label.setWordWrap(True)
                explanation_layout.addWidget(label)
        scroll_area.setWidget(explanation_widget)
        main_layout.addWidget(scroll_area, stretch=1)  # 画面全体に広げる

        btn_layout = QHBoxLayout()
        self.next_btn = QPushButton("次の問題へ", self)
        self.next_btn.setFont(QFont("Arial", 16))
        self.next_btn.clicked.connect(self.next_question)
        self.exit_btn = QPushButton("終了する", self)
        self.exit_btn.setFont(QFont("Arial", 16))
        self.exit_btn.clicked.connect(self.close)
        btn_layout.addWidget(self.next_btn)
        btn_layout.addWidget(self.exit_btn)
        main_layout.addLayout(btn_layout)

        self.setLayout(main_layout)
        self.showMaximized()

    def next_question(self):
        self.close()
        self.parent_game.show_next(self.next_index)