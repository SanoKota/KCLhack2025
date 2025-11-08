import sys
import csv
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QGridLayout, QMessageBox, QButtonGroup
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
from Result.result import AnswerWindow
from Result.sum_result import SumResultWindow
import matplotlib.pyplot as plt
import tempfile
from PyQt5.QtGui import QPixmap
import random
from GameFrame.select_game_frame import RangeSelectFrame

def latex_to_pixmap(latex_str):
    import matplotlib
    fig = plt.figure(figsize=(2, 0.7))
    try:
        fig.text(0.5, 0.5, latex_str, fontsize=24, ha='center', va='center')
        fig.patch.set_alpha(0)
        plt.axis('off')
        fig.canvas.draw()
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmpfile:
            fig.savefig(tmpfile.name, bbox_inches='tight', pad_inches=0.2, transparent=True)
            plt.close(fig)
            pixmap = QPixmap(tmpfile.name)
        return pixmap
    except Exception as e:
        plt.close(fig)
        # フォールバック: テキストとして表示
        from PyQt5.QtGui import QImage, QPainter
        image = QImage(400, 60, QImage.Format_ARGB32)
        image.fill(Qt.transparent)
        painter = QPainter(image)
        painter.setFont(QFont("Arial", 24))
        painter.setPen(Qt.black)
        painter.drawText(10, 40, latex_str)
        painter.end()
        return QPixmap.fromImage(image)

class DifferentialGame(QWidget):
    def show_hint1(self):
        hint1 = self.data[self.current]["Hint1"]
        # $...$ で囲まれた数式があれば画像表示
        if "$" in hint1:
            import re
            parts = re.split(r'(\$.*?\$|\$\$.*?\$\$)', hint1)
            self.hint1_label.clear()
            hint_layout = QVBoxLayout()
            for part in parts:
                if re.match(r'^\$.*\$$', part) or re.match(r'^\$\$.*\$\$$', part):
                    label = QLabel(self)
                    label.setPixmap(latex_to_pixmap(part))
                    label.setAlignment(Qt.AlignLeft)
                    hint_layout.addWidget(label)
                elif part.strip():
                    label = QLabel(part, self)
                    label.setFont(QFont("Arial", 12))
                    label.setWordWrap(True)
                    label.setAlignment(Qt.AlignLeft)
                    hint_layout.addWidget(label)
            # QWidgetにレイアウトを設定
            hint_widget = QWidget()
            hint_widget.setLayout(hint_layout)
            # ヒントラベルの親レイアウトに追加
            parent_layout = self.hint1_label.parentWidget().layout()
            parent_layout.replaceWidget(self.hint1_label, hint_widget)
            self.hint1_label.hide()
        else:
            self.hint1_label.setText("ヒント1: " + hint1)
        self.hint1_btn.setEnabled(False)
    def update_progress_label(self):
        # 1始まりで表示
        self.progress_label.setText(f"{self.question_count+1}/10")
    def __init__(self, df, mode="微分"):
        super().__init__()
        self.mode = mode
        self.setWindowTitle(f"{self.mode}問題")
        self.setFont(QFont("Arial", 14))
        # カラム名の空白を除去
        df.columns = [col.strip() for col in df.columns]
        self.data = df.to_dict(orient="records")
        self.max_id = max([int(row["ID"]) for row in self.data if str(row["ID"]).isdigit()])
        # ランダムなIDで出題
        import random
        self.current = random.randint(0, self.max_id)
        # self.currentが存在しないIDの場合は最初のIDに
        if not any(int(row["ID"]) == self.current for row in self.data):
            self.current = int(self.data[0]["ID"])
        self.correct_count = 0  # 正解数カウント
        self.question_count = 0 # 問題数カウント
        self.init_ui()

    def init_ui(self):
        # 進捗ラベル（中央寄り上部）
        self.progress_label = QLabel(self)
        self.progress_label.setFont(QFont("Arial", 40, QFont.Bold))
        self.progress_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.update_progress_label()

        # 問題欄（左半分の中心）
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.progress_label, alignment=Qt.AlignHCenter | Qt.AlignTop)
        left_layout.addStretch(1)
        # Question（テキスト）を上に表示
        question_text = self.data[self.current]["Question"]
        self.question_text_label = QLabel(question_text, self)
        self.question_text_label.setFont(QFont("Arial", 24, QFont.Bold))
        self.question_text_label.setAlignment(Qt.AlignCenter)
        self.question_text_label.setWordWrap(True)
        left_layout.addWidget(self.question_text_label)
        # formula（数式）をlatex画像で表示
        formula_text = self.data[self.current]["formula"]
        self.formula_label = QLabel(self)
        self.formula_label.setAlignment(Qt.AlignCenter)
        # latex数式部分のみ抽出して画像化
        if formula_text.startswith("$") and formula_text.endswith("$"):
            self.formula_label.setPixmap(latex_to_pixmap(formula_text))
        else:
            # $で囲まれていない場合は自動で囲む
            self.formula_label.setPixmap(latex_to_pixmap(f"${formula_text}$"))
        left_layout.addWidget(self.formula_label)
        left_layout.addStretch(1)

        # ヒント欄（右上）: ボタンで隠す
        self.hint1_btn = QPushButton("ヒント1を表示", self)
        self.hint1_btn.setFont(QFont("Arial", 20))
        self.hint1_label = QLabel("", self)
        self.hint1_label.setFont(QFont("Arial", 20))
        self.hint1_label.setWordWrap(True)  # ←追加：自動改行
        self.hint1_btn.clicked.connect(self.show_hint1)
        self.hint1_btn.setCheckable(False)

        self.hint2_btn = QPushButton("ヒント2を表示", self)
        self.hint2_btn.setFont(QFont("Arial", 20))
        self.hint2_label = QLabel("", self)
        self.hint2_label.setFont(QFont("Arial", 20))
        self.hint2_label.setWordWrap(True)  # ←追加：自動改行
        self.hint2_btn.clicked.connect(self.show_hint2)
        self.hint2_btn.setCheckable(False)

        # 回答欄（右下）を3択ボタン（数式画像）に変更
        self.choices = [
            self.data[self.current]["select1"].strip(),
            self.data[self.current]["select2"].strip(),
            self.data[self.current]["Answer"].strip()
        ]
        random.shuffle(self.choices)

        self.answer_group = QButtonGroup(self)
        self.answer_buttons = []
        answer_layout = QHBoxLayout()

        for i, ans in enumerate(self.choices):
            btn = QPushButton(self)
            btn.setCheckable(True)
            pixmap = latex_to_pixmap(ans)
            btn.setIcon(QIcon(pixmap))
            btn.setIconSize(pixmap.size())
            self.answer_group.addButton(btn, i)
            self.answer_buttons.append(btn)
            answer_layout.addWidget(btn)
            btn.setCheckable(False)

        # レイアウトの設定
        right_layout = QVBoxLayout()
        right_layout.addWidget(self.hint1_btn)
        right_layout.addWidget(self.hint1_label)
        right_layout.addWidget(self.hint2_btn)
        right_layout.addWidget(self.hint2_label)
        right_layout.addStretch(1)
        right_layout.addLayout(answer_layout)

        main_layout = QHBoxLayout()
        main_layout.addLayout(left_layout, 2)
        main_layout.addLayout(right_layout, 3)
        self.setLayout(main_layout)

        # 選択肢ボタンのクリックイベント
        for idx, btn in enumerate(self.answer_buttons):
            btn.clicked.connect(lambda checked, i=idx: self.on_choice_selected(i, self.choices[i] == self.data[self.current]["Answer"].strip()))
        self.showMaximized()

    def show_hint2(self):
        hint2 = self.data[self.current]["Hint2"]
        if "$" in hint2:
            import re
            parts = re.split(r'(\$.*?\$|\$\$.*?\$\$)', hint2)
            self.hint2_label.clear()
            hint_layout = QVBoxLayout()
            for part in parts:
                if re.match(r'^\$.*\$$', part) or re.match(r'^\$\$.*\$\$$', part):
                    label = QLabel(self)
                    label.setPixmap(latex_to_pixmap(part))
                    label.setAlignment(Qt.AlignLeft)
                    hint_layout.addWidget(label)
                elif part.strip():
                    label = QLabel(part, self)
                    label.setFont(QFont("Arial", 12))
                    label.setWordWrap(True)
                    label.setAlignment(Qt.AlignLeft)
                    hint_layout.addWidget(label)
            hint_widget = QWidget()
            hint_widget.setLayout(hint_layout)
            parent_layout = self.hint2_label.parentWidget().layout()
            parent_layout.replaceWidget(self.hint2_label, hint_widget)
            self.hint2_label.hide()
        else:
            self.hint2_label.setText("ヒント2: " + hint2)
        self.hint2_btn.setEnabled(False)

    def on_choice_selected(self, idx, is_correct):
        user_answer = self.choices[idx].strip()
        correct_answer = self.data[self.current]["Answer"].strip()
        explanation = self.data[self.current]["Explanation"]
        if is_correct:
            self.correct_count += 1
        self.question_count += 1
        self.answer_window = AnswerWindow(
            correct_answer, explanation, self.current, len(self.data), self, is_correct
        )
        self.answer_window.showMaximized()
        self.hide()

    def show_next(self, next_index):
        # 10問解いたら結果まとめ画面に遷移
        if self.question_count >= 10:
            self.result_window = SumResultWindow(self.correct_count, 10)
            self.result_window.show()
            self.close()
            return
        if next_index < len(self.data):
            self.current = next_index
        else:
            self.current = 0
        self.update_progress_label()
        question_text = self.data[self.current]["Question"]
        self.question_text_label.setText(question_text)
        self.question_text_label.setFont(QFont("Arial", 18, QFont.Bold))
        formula_text = self.data[self.current]["formula"]
        if formula_text.startswith("$") and formula_text.endswith("$"):
            self.formula_label.setPixmap(latex_to_pixmap(formula_text))
        else:
            self.formula_label.setPixmap(latex_to_pixmap(f"${formula_text}$"))
        self.choices = [
            self.data[self.current]["select1"].strip(),
            self.data[self.current]["select2"].strip(),
            self.data[self.current]["Answer"].strip()
        ]
        random.shuffle(self.choices)
        for i, btn in enumerate(self.answer_buttons):
            pixmap = latex_to_pixmap(self.choices[i])
            btn.setIcon(QIcon(pixmap))
            btn.setIconSize(pixmap.size())
            btn.setChecked(False)
        self.hint1_label.setText("")
        self.hint2_label.setText("")
        self.hint1_btn.setEnabled(True)
        self.hint2_btn.setEnabled(True)
        self.showMaximized()
