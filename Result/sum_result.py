from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from GameFrame.select_game_frame import RangeSelectFrame

class SumResultWindow(QWidget):
    def __init__(self, correct_count, total_count=10):
        super().__init__()
        self.setWindowTitle("結果まとめ")
        self.setFont(QFont("Arial", 18))
        layout = QVBoxLayout()
        result_label = QLabel(f"10問中 {correct_count} 問正解！", self)
        result_label.setFont(QFont("Arial", 32, QFont.Bold))
        result_label.setAlignment(Qt.AlignCenter)
        layout.addStretch(1)
        layout.addWidget(result_label)
        layout.addStretch(1)

        # 正解数に応じたメッセージを表示
        message = self.get_message(correct_count)
        message_label = QLabel(message, self)
        message_label.setFont(QFont("Arial", 24))
        message_label.setAlignment(Qt.AlignCenter)
        layout.addStretch(1)
        layout.addWidget(message_label)
        layout.addStretch(1)
        self.setLayout(layout)
        self.showMaximized()
        home_btn = QPushButton("次へ", self)
        home_btn.setFont(QFont("Arial", 24))
        home_btn.setStyleSheet("color: white; border: 7px solid red; border-radius: 20px; background-color: red; margin-bottom: 40px; min-width: 300px; max-width: 300px;")
        layout.addWidget(home_btn, alignment=Qt.AlignCenter)
        home_btn.clicked.connect(self.showRangeSelectFrame)

    def showRangeSelectFrame(self):
        self.hide()
        self.range_select_frame = RangeSelectFrame()
        self.range_select_frame.show()
        self.close()

    # 正解数に応じたメッセージ
    def get_message(self, correct_count):
        if correct_count >= 9:
            return "Fantastic!"
        elif correct_count >= 7:
            return "Good!"
        else:
            return "Try again!"