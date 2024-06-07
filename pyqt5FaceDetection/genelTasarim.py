import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QTimer, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap
import cv2
from kisiekleme import KisiEklemeForm
from PyQt5.QtWidgets import QMessageBox


class ExampleApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(ExampleApp, self).__init__()
        uic.loadUi('genelTasarim.ui', self)
        
        # Timer ve kamera bağlantısı
        # self.cap = cv2.VideoCapture(0)
        # self.timer = QTimer(self)
        # self.timer.timeout.connect(self.update_frame)
        # self.timer.start(20)

        # Yeni form açma butonuna bağla
        self.btnKisiEkle.clicked.connect(self.open_kisi_ekleme)
        self.btnKisiSil.clicked.connect(self.open_kisi_sil)
    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, channel = frame.shape
            step = channel * width
            qimg = QImage(frame.data, width, height, step, QImage.Format_RGB888)
            self.videoLabel.setPixmap(QPixmap.fromImage(qimg))

    def open_kisi_sil(self):
        QMessageBox.warning(self, 'Warning', 'This is a warning message.')
 

    def open_kisi_ekleme(self):
        self.timer.stop()  # Ana formdaki kamerayı durdur
        self.cap.release()  # Kamerayı serbest bırak
        self.new_form = KisiEklemeForm(self)
        self.new_form.form_closed.connect(self.resume_camera)  # Yeni form kapanınca kamera akışını yeniden başlat
        self.new_form.show()

    def resume_camera(self):
        # Kamerayı tekrar başlat
        self.cap = cv2.VideoCapture(0)
        self.timer.start(20)

    def closeEvent(self, event):
        self.timer.stop()
        self.cap.release()
        event.accept()
        super().closeEvent(event)

app = QtWidgets.QApplication(sys.argv)
window = ExampleApp()
window.show()
sys.exit(app.exec_())
