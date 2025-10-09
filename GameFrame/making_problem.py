from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal

class ProblemMakerThread(QThread):
    finished = pyqtSignal(object)  # DataFrameなどを返す

    def __init__(self, subject):
        super().__init__()
        self.subject = subject

    def run(self):
        from core.run_gemini import run_gemini
        # 10問分生成（run_geminiが10問返すようにプロンプトを調整してください）
        df = run_gemini(self.subject)
        self.finished.emit(df)

class MakingProblemWindow(QWidget):
    def __init__(self, subject, next_callback):
        super().__init__()
        self.subject = subject
        self.next_callback = next_callback  # 問題生成後に呼び出す関数

        self.setWindowTitle("問題生成中")
        layout = QVBoxLayout()
        layout.addStretch(1)
        self.loading_label = QLabel("Now Loading...", self)
        self.loading_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        self.loading_label.setStyleSheet("font-size: 24px; color: #1a73e8; margin: 30px;")
        layout.addWidget(self.loading_label)
        self.setLayout(layout)
        self.showMaximized()

        # 問題生成スレッド開始
        self.thread = ProblemMakerThread(self.subject)
        self.thread.finished.connect(self.on_finished)
        self.thread.start()

    def on_finished(self, df):
        # 問題生成が終わったら次の画面へ
        self.next_callback(df)
        self.close()