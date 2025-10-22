import sys
# from core.run_gemini import run_gemini  # run_geminiはcreate_problem内でインポートする
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QFrame, QGraphicsDropShadowEffect
from PyQt5.QtGui import QFont, QIcon, QColor, QPainter, QPixmap
from PyQt5.QtCore import Qt
# from .game_page import GamePage  # パッケージとして実行する場合 (そのまま残す)
# from GameFrame.question import DifferentialGame # 未使用のためコメントアウトまたは削除
import pandas as pd
import time
from core import run_gemini # run_geminiをここでインポート（実際の環境に応じて調整）

class SelectGameFrame(QWidget):
    def __init__(self, selected_range=None):
        super().__init__()
        self.selected_range = selected_range
        self.setWindowTitle("問題選択")
        self.setFont(QFont("Arial", 14))
        self.setStyleSheet("background-color: #f7f9fa;")
        self.init_ui()
        self.showMaximized()  # ウィンドウ枠付き最大化表示

    def init_ui(self):
        # タイトルバー
        title_bar = QLabel("MATH APP    微分積分マスター", self)
        title_bar.setFont(QFont("Arial", 20, QFont.Bold))
        title_bar.setStyleSheet("background-color: #222; color: white; padding: 12px 24px; border-radius: 8px;")
        title_bar.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        # 2カラムレイアウト
        main_layout = QVBoxLayout()
        main_layout.addWidget(title_bar)
        main_layout.addSpacing(20)
        columns = QHBoxLayout()
        self.buttons = []  # ボタン管理用リスト
        # 微分カラム
        diff_frame = QFrame(self)
        diff_frame.setStyleSheet("background-color: #fff; border: 2px solid #e0e3e6; border-radius: 16px; padding: 24px;")
        diff_layout = QVBoxLayout()
        diff_label = QLabel("Differential", self)
        diff_label.setFont(QFont("Arial", 16, QFont.Bold))
        diff_label.setAlignment(Qt.AlignCenter)
        diff_layout.addWidget(diff_label)
        # ボタン幅をラベル幅に合わせる
        button_width = 220
        diff_btn = QPushButton("微分", self)
        diff_btn.setFont(QFont("Arial", 20, QFont.Bold))
        diff_btn.setStyleSheet("background-color: #ffb74d; color: #222; border-radius: 32px; min-height: 60px;")
        diff_btn.setFixedWidth(button_width)
        diff_btn.clicked.connect(self.start_game)
        self.buttons.append(diff_btn)
        diff_layout.addWidget(diff_btn)
        diff_create_btn = QPushButton("  ✏️ 微分の問題作成", self)
        diff_create_btn.setFont(QFont("Arial", 14))
        diff_create_btn.setStyleSheet("background-color: #fff; color: #222; border: 2px solid #26c6da; border-radius: 24px; min-height: 40px; margin-top: 12px; margin-bottom: 8px;")
        diff_create_btn.setFixedWidth(button_width)
        diff_create_btn.clicked.connect(lambda: self.create_problem("微分"))
        self.buttons.append(diff_create_btn)
        diff_layout.addWidget(diff_create_btn)
        diff_frame.setLayout(diff_layout)
        # 影エフェクト追加
        shadow_diff = QGraphicsDropShadowEffect()
        shadow_diff.setBlurRadius(16)
        shadow_diff.setColor(QColor(0, 0, 0, 80))
        shadow_diff.setOffset(0, 4)
        diff_frame.setGraphicsEffect(shadow_diff)
        columns.addWidget(diff_frame)
        # 積分カラム
        int_frame = QFrame(self)
        int_frame.setStyleSheet("background-color: #fff; border: 2px solid #e0e3e6; border-radius: 16px; padding: 24px;")
        int_layout = QVBoxLayout()
        int_label = QLabel("Integral", self)
        int_label.setFont(QFont("Arial", 16, QFont.Bold))
        int_label.setAlignment(Qt.AlignCenter)
        int_layout.addWidget(int_label)
        int_btn = QPushButton("積分", self)
        int_btn.setFont(QFont("Arial", 20, QFont.Bold))
        int_btn.setStyleSheet("background-color: #26c6da; color: #222; border-radius: 32px; min-height: 60px;")
        int_btn.setFixedWidth(button_width)
        int_btn.setEnabled(True)  # 初期状態で有効化
        int_btn.clicked.connect(self.start_game)
        self.buttons.append(int_btn)
        int_layout.addWidget(int_btn)
        int_create_btn = QPushButton("  ⚙️ 積分の問題作成", self)
        int_create_btn.setFont(QFont("Arial", 14))
        int_create_btn.setStyleSheet("background-color: #fff; color: #222; border: 2px solid #26c6da; border-radius: 24px; min-height: 40px; margin-top: 12px; margin-bottom: 8px;")
        int_create_btn.setFixedWidth(button_width)
        int_create_btn.setEnabled(True)  # 初期状態で有効化
        int_create_btn.clicked.connect(lambda: self.create_problem("積分"))
        self.buttons.append(int_create_btn)
        int_layout.addWidget(int_create_btn)
        int_frame.setLayout(int_layout)
        # 影エフェクト追加
        shadow_int = QGraphicsDropShadowEffect()
        shadow_int.setBlurRadius(16)
        shadow_int.setColor(QColor(0, 0, 0, 80))
        shadow_int.setOffset(0, 4)
        int_frame.setGraphicsEffect(shadow_int)
        columns.addWidget(int_frame)
        main_layout.addLayout(columns)
        main_layout.addSpacing(40)
        self.setLayout(main_layout)
        self.resize(900, 700)
        
        # オーバーレイウィジェットを初期化（まだ表示しない）
        self.overlay = QWidget(self)
        self.overlay.setStyleSheet("background-color: rgba(0,0,0,180);")
        self.overlay.setAttribute(Qt.WA_TransparentForMouseEvents, False)
        self.overlay.hide()
        
        # オーバーレイ内のラベル
        self.overlay_label = QLabel("問題作成中... (AI生成)", self.overlay)
        self.overlay_label.setStyleSheet("color: white; font-size: 32px; font-weight: bold;")
        self.overlay_label.setAlignment(Qt.AlignCenter)
        
        # 初回起動時にサイズを合わせる
        self.resizeEvent(None) 

    # ゲーム開始処理（元のon_selectのゲーム開始部分）
    def start_game(self):
        sender = self.sender()
        selected_range = sender.text()
        
        # 問題データの読み込み
        df = None
        if selected_range == "微分":
            try:
                df = pd.read_csv("GameFrame/GameData/differentioal.csv", encoding="utf-8")
            except FileNotFoundError:
                print("Error: differentioal.csv not found.")
                return
        elif selected_range == "積分":
            try:
                df = pd.read_csv("GameFrame/GameData/integral.csv", encoding="utf-8")
            except FileNotFoundError:
                print("Error: integral.csv not found.")
                return
        else:
            return

        # GamePage経由でDifferentialGameを開く例
        try:
            from GameFrame.game_page import GamePage
            self.game_page = GamePage(df)
            if selected_range == "微分":
                self.game_page.Differential()
            elif selected_range == "積分":
                self.game_page.Integral()
            self.hide()
        except Exception as e:
            print(f"Error launching game page: {e}")


    # 問題作成処理（オーバーレイを有効化）
    def create_problem(self, topic):
        # 1. オーバーレイを表示し、UIの更新を強制
        self.overlay_label.setText(f"{topic}の問題をAIで作成中...")
        self.overlay.show()
        QApplication.processEvents() 

        # 2. メインボタンと作成ボタンを無効化（積分ボタンは常に有効化）
        for btn in self.buttons:
            if btn.text() in ["微分", "微分の問題作成"]:
                btn.setEnabled(False)
            elif btn.text() in ["積分", "積分の問題作成"]:
                btn.setEnabled(True)

        # 3. 問題生成・保存処理（run_gemini呼び出し）
        # run_geminiはブロッキング処理と想定
        df_new = None
        try:
            # run_geminiがファイルを保存することを期待
            df_new = run_gemini.run_gemini(topic)
            
            # 完了メッセージを一時的に表示
            self.overlay_label.setText(f"{topic}の問題生成が完了しました！\nメインボタンからゲームを開始してください。")
            QApplication.processEvents()
            time.sleep(1.5) # 1.5秒間メッセージを表示
            
        except Exception as e:
            print(f"Error during problem creation for {topic}: {e}")
            self.overlay_label.setText(f"{topic}の問題生成中にエラーが発生しました:\n{str(e)}")
            QApplication.processEvents()
            time.sleep(3) # 3秒間エラーメッセージを表示

        # 4. クリーンアップ（オーバーレイ非表示・ボタン有効化）
        self.overlay.hide()
        for btn in self.buttons:
            btn.setEnabled(True)


    def resizeEvent(self, event):
        win_width = self.width()
        win_height = self.height()
        
        # ボタンサイズを動的に変更
        btn_w = int(win_width * 0.18)
        btn_h = int(win_height * 0.18)
        for btn in getattr(self, 'buttons', []):
            btn.setMinimumSize(btn_w, btn_h)
            btn.setMaximumSize(btn_w, btn_h)
            
        # オーバーレイもリサイズ
        if hasattr(self, 'overlay'):
            self.overlay.setGeometry(0, 0, win_width, win_height)
            self.overlay_label.setGeometry(0, 0, win_width, win_height)
            
        super().resizeEvent(event)

# 互換性のためのエイリアス（旧名RangeSelectFrameでimport可能に）
RangeSelectFrame = SelectGameFrame

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SelectGameFrame()
    window.show()
    sys.exit(app.exec_())
