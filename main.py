import sys
from PyQt5.QtWidgets import QApplication, QLabel
from src.app.myapp import MyApp

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myapp = MyApp()
    sys.exit(app.exec_())