import sys
import cv2
import numpy as np
import sqlite3
from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtCore import QTimer, QTime
from pyzbar import pyzbar

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('main_window.ui', self)  # Load the UI file

        self.startButton.clicked.connect(self.start_camera)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.cap = None

        self.start_time = QTime.currentTime()

    def start_camera(self):
        self.cap = cv2.VideoCapture(0)
        self.timer.start(20)

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            qr_codes = pyzbar.decode(frame)
            for qr_code in qr_codes:
                qr_data = qr_code.data.decode('utf-8')
                self.textArea.setPlainText(qr_data)
                try:
                    # Split only on the first slash
                    cpf, competition = qr_data.split('/', 1)
                    self.update_competition(cpf, competition)
                except ValueError:
                    print("Error processing QR code: invalid format")
                    continue
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = QtGui.QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QtGui.QImage.Format_RGB888)
            self.cameraFeed.setPixmap(QtGui.QPixmap.fromImage(image))

    def update_competition(self, cpf, competition):
        conn = sqlite3.connect('participants.db')
        cursor = conn.cursor()

        current_time = QTime.currentTime()
        elapsed_time = self.start_time.secsTo(current_time)

        # Use column name directly in query string construction
        query = f"UPDATE competicao SET \"{competition}\" = ? WHERE cpf_participante = ?"
        cursor.execute(query, (str(elapsed_time), cpf))
        conn.commit()
        conn.close()
        print(f"Updated competition for CPF {cpf} with time {elapsed_time} seconds")

    def closeEvent(self, event):
        if self.cap is not None:
            self.cap.release()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
