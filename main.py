import sys
import cv2
import datetime
from PyQt5 import QtWidgets
from ui import MainWindow
from database import setup_database
from database import clean_database_for_competition

if __name__ == '__main__':
    setup_database()
    clean_database_for_competition("Clinica_17_08_24")
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
