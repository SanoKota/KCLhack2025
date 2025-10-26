import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QComboBox, QHeaderView
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class ProblemListWindow(QWidget):
    def __init__(self, topic=None):
        super().__init__()
        self.setWindowTitle("問題一覧")
        self.setFont(QFont("Arial", 14))
        self.resize(1200, 700)
        layout = QVBoxLayout()
        self.label = QLabel("範囲を選択してください（微分/積分）", self)
        self.label.setFont(QFont("Arial", 18, QFont.Bold))
        layout.addWidget(self.label)
        self.combo = QComboBox(self)
        self.combo.addItems(["微分", "積分"])
        self.combo.currentTextChanged.connect(self.load_table)
        layout.addWidget(self.combo)
        self.table = QTableWidget(self)
        self.table.setWordWrap(True)
        self.table.verticalHeader().setVisible(False)  # 行番号（左端の数字）を非表示
        layout.addWidget(self.table)
        self.setLayout(layout)
        # topicが指定されていれば初期選択
        if topic in ["微分", "積分"]:
            idx = self.combo.findText(topic)
            if idx >= 0:
                self.combo.setCurrentIndex(idx)
        self.load_table(self.combo.currentText())

    def load_table(self, topic):
        if topic == "微分":
            csv_path = "GameFrame/GameData/differentioal.csv"
        else:
            csv_path = "GameFrame/GameData/integral.csv"
        try:
            df = pd.read_csv(csv_path, encoding="utf-8")
        except Exception as e:
            self.label.setText(f"CSV読み込みエラー: {e}")
            self.table.clear()
            return
        self.table.setRowCount(len(df))
        self.table.setColumnCount(len(df.columns))
        self.table.setHorizontalHeaderLabels(df.columns)
        for i, row in df.iterrows():
            for j, col in enumerate(df.columns):
                item = QTableWidgetItem(str(row[col]))
                item.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                self.table.setItem(i, j, item)
        # 横幅いっぱいにカラムを広げる
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # セル内のテキストを自動改行＆行の高さも文字に合わせて調整
        self.table.resizeRowsToContents()
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.label.setText(f"{topic}の問題一覧（{len(df)}件）")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProblemListWindow()
    window.showMaximized()
    sys.exit(app.exec_())
