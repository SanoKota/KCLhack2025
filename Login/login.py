import sys
import csv
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import GameFrame.select_game_frame as select_game_frame
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QVBoxLayout, QLineEdit, QMessageBox

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ログイン画面")
        self.resize(400, 250)
        layout = QVBoxLayout()
        # ユーザー名
        self.user_label = QLabel("ユーザー名")
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("ユーザー名を入力")
        layout.addWidget(self.user_label)
        layout.addWidget(self.user_input)
        # パスワード
        self.pass_label = QLabel("パスワード")
        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("パスワードを入力")
        self.pass_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.pass_label)
        layout.addWidget(self.pass_input)
        # ログインボタン
        self.login_btn = QPushButton("ログイン")
        self.login_btn.setStyleSheet("background-color:#1a73e8; color:white; font-weight:bold;")
        self.login_btn.clicked.connect(self.handle_login)
        layout.addWidget(self.login_btn)
        self.setLayout(layout)
        self.second_window = None

    def handle_login(self):
        username = self.user_input.text().strip()
        password = self.pass_input.text().strip()
        if not username or not password:
            QMessageBox.warning(self, "エラー", "ユーザー名とパスワードを入力してください。")
            return
        # CSVファイルからユーザー情報を参照
        csv_path = "./UserData/users.csv"  # ユーザー情報CSVファイル名
        if not os.path.exists(csv_path):
            QMessageBox.critical(self, "エラー", f"ユーザー情報ファイルが見つかりません: {csv_path}")
            return
        found = False
        with open(csv_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get('ユーザー名') == username and row.get('パスワード') == password:
                    found = True
                    break
        if found:
            QMessageBox.information(self, "ログイン成功", f"ようこそ、{username}さん！")
            # select_game_frame画面へ遷移
            self.game_window = select_game_frame.RangeSelectFrame()
            self.game_window.show()
            self.close()
        else:
            QMessageBox.warning(self, "エラー", "ユーザー名またはパスワードが正しくありません。")

class LoginWindowMain(QWidget):
    def main(self):
        app = QApplication(sys.argv)
        window = LoginWindow()
        window.show()
        sys.exit(app.exec_())