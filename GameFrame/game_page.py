import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QVBoxLayout, QGridLayout, QSizePolicy
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class GamePage(QWidget):
    def __init__(self):
        super().__init__()
        
    def Differential(self):
        print("Differential method called")
    
    def Integral(self):
        print("Integral method called")
