import datetime
import cv2
from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtCore import QTimer
from pyzbar import pyzbar
from database import update_competition, finalize_registration
from qr_code import process_qr_code

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('main_window.ui', self)

        self.startButton.clicked.connect(self.start_camera)
        self.finalizeButton.clicked.connect(self.finalize_registration)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.cap = None
        self.start_time = datetime.datetime.now().strftime("%H:%M:%S")

        self.load_start_time()

    def load_start_time(self):
        try:
            with open('start_time.txt', 'r') as f:
                time_str = f.read().strip()
                self.start_time = datetime.datetime.strptime(time_str, "%H:%M:%S").time()
        except (FileNotFoundError, ValueError):
            self.start_time = datetime.datetime.now().time()
            self.save_start_time()

    def save_start_time(self):
        with open('start_time.txt', 'w') as f:
            f.write(self.start_time.strftime("%H:%M:%S"))

    def start_camera(self):
        self.cap = cv2.VideoCapture(0)
        self.timer.start(20)

    def getTimeDiff(self, time1, time2):
        if isinstance(time1, datetime.time):
            time1 = datetime.datetime.combine(datetime.date.today(), time1)
        if isinstance(time2, datetime.time):
            time2 = datetime.datetime.combine(datetime.date.today(), time2)
        diff = time2 - time1
        return str(diff)

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            qr_codes = pyzbar.decode(frame)
            for qr_code in qr_codes:
                qr_data = qr_code.data.decode('utf-8')
                self.textArea.setPlainText(qr_data)
                process_qr_code(qr_data, self.start_time)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = QtGui.QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QtGui.QImage.Format_RGB888)
            self.cameraFeed.setPixmap(QtGui.QPixmap.fromImage(image))

    def finalize_registration(self):
        finalize_registration()

    def closeEvent(self, event):
        if self.cap is not None:
            self.cap.release()
