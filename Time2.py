import sys
import cv2
import numpy as np
import sqlite3
import datetime
from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtCore import QTimer
from pyzbar import pyzbar

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
        return diff

    def format_timedelta(self, td):
        total_seconds = int(td.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            qr_codes = pyzbar.decode(frame)
            for qr_code in qr_codes:
                qr_data = qr_code.data.decode('utf-8')
                self.textArea.setPlainText(qr_data)
                try:
                    cpf, competition = qr_data.split('/')
                    self.update_competition(cpf, competition)
                except ValueError:
                    self.textArea.setPlainText("Error processing QR code: invalid format")
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = QtGui.QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QtGui.QImage.Format_RGB888)
            self.cameraFeed.setPixmap(QtGui.QPixmap.fromImage(image))

    def update_competition(self, cpf, competition):
        conn = sqlite3.connect('participants.db')
        cursor = conn.cursor()

        # Calculate elapsed time
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"Current time: {current_time}")  # Debug print
        print(f"Start time: {self.start_time}")  # Debug print
        final_time = self.getTimeDiff(self.start_time, datetime.datetime.strptime(current_time, "%H:%M:%S"))
        
        # Convert final_time to a formatted string
        formatted_time = self.format_timedelta(final_time)
        
        # Check if record exists
        query_check = """
        SELECT COUNT(*) FROM competicao
        WHERE cpf_participante = ?
        """
        cursor.execute(query_check, (cpf,))
        exists = cursor.fetchone()[0] > 0

        if exists:
            # Update existing record
            query_update = f"""
            UPDATE competicao
            SET {competition} = ?
            WHERE cpf_participante = ?
            """
            cursor.execute(query_update, (formatted_time, cpf))
            print(f"Updated {competition} for {cpf} with {formatted_time}")  # Debug print
        else:
            # Insert new record
            query_insert = f"""
            INSERT INTO competicao (cpf_participante, {competition})
            VALUES (?, ?)
            """
            cursor.execute(query_insert, (cpf, formatted_time))
            print(f"Inserted {competition} for {cpf} with {formatted_time}")  # Debug print

        conn.commit()
        conn.close()

    def finalize_registration(self):
        conn = sqlite3.connect('participants.db')
        cursor = conn.cursor()

        categories = {
            "A - Sub 15": (0, 15),
            "B - 16-19": (16, 19),
            "C - 20-24": (20, 24),
            "D - 25-29": (25, 29),
            "E - 30-34": (30, 34),
            "F - 35-39": (35, 39),
            "G - 40-44": (40, 44),
            "H - 45-49": (45, 49),
            "I - 50-54": (50, 54),
            "J - 55-59": (55, 59),
            "K - 60-64": (60, 64),
            "L - 65-69": (65, 69),
            "M - 70-74": (70, 74),
            "N - 75-80": (75, 80),
            "O - 80-84": (80, 84),
            "P - 85-89": (85, 89),
            "Q - 90-94": (90, 94),
            "R - 95-99": (95, 99),
        }

        ranking = {}

        for category, age_range in categories.items():
            min_age, max_age = age_range
            query = f"""
            SELECT participante.NOME, competicao.Clinica_17_08_24
            FROM participante
            JOIN competicao ON participante.CPF = competicao.cpf_participante
            WHERE participante.IDADE BETWEEN {min_age} AND {max_age}
            ORDER BY CAST(competicao.Clinica_17_08_24 AS TEXT)
            """
            cursor.execute(query)
            ranking[category] = cursor.fetchall()

        # Handle PCD category separately
        query = """
        SELECT participante.NOME, competicao.Clinica_17_08_24
        FROM participante
        JOIN competicao ON participante.CPF = competicao.cpf_participante
        WHERE participante.PCD = 1
        ORDER BY CAST(competicao.Clinica_17_08_24 AS TEXT)
        """
        cursor.execute(query)
        ranking["PCD"] = cursor.fetchall()

        conn.close()

        # Save ranking to file
        with open('ranking.txt', 'w') as f:
            for category, participants in ranking.items():
                f.write(f"Category: {category}\n")
                for participant in participants:
                    f.write(f"{participant[0]}: {participant[1]}\n")
                f.write("\n")

        print("Ranking list generated and saved to ranking.txt")

    def closeEvent(self, event):
        if self.cap is not None:
            self.cap.release()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
