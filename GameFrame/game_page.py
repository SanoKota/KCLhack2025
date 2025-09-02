from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QVBoxLayout, QGridLayout, QSizePolicy
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from GameFrame.question import DifferentialGame
import sys

class GamePage(QWidget):
    def __init__(self):
        super().__init__()
        self.diff_window = None
        self.mode = None  # "微分" or "積分"

    def Differential(self):
        self.mode = "微分"
        self.diff_window = DifferentialGame(mode=self.mode)
        self.diff_window.show()

    def Integral(self):
        self.mode = "積分"
        self.diff_window = DifferentialGame(mode=self.mode)
        self.diff_window.show()
