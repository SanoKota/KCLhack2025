import sys
from PyQt5.QtWidgets import QApplication
from Login.first_frame import VariableWindows

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VariableWindows()
    window.frame()
    window.show()
    sys.exit(app.exec_())