from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QVBoxLayout, QGridLayout, QSizePolicy
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from GameFrame.differential_game import DifferentialGame
import sys

class GamePage(QWidget):
    def __init__(self):
        super().__init__()
        self.diff_window = None
        
    def Differential(self):
        self.diff_window = DifferentialGame()
        self.diff_window.show()
    
    def Integral(self):
        print("Integral method called")
