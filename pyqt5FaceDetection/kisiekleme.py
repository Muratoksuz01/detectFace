import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QTimer,pyqtSignal
from PyQt5.QtGui import QImage, QPixmap
import cv2

class KisiEklemeForm(QtWidgets.QMainWindow):
    form_closed = pyqtSignal()  # Yeni bir sinyal tanımlayın

    def __init__(self,parent=None):
        super(KisiEklemeForm, self).__init__()
        uic.loadUi('kisiekleme.ui', self)  # UI dosyasını yükleyin
        self.btnOpenDir.clicked.connect(self.btnOpenDir_Click)
        # btnCek butonuna tıklandığında print_frame_values fonksiyonunu çağır
        
        # Kamera bağlantısı
        # self.cap = cv2.VideoCapture(0)
        
        # # Timer oluştur ve update_frame fonksiyonunu çağır
        # self.timer = QTimer()#                          20milisaniyede signal uretir buda update_frame cagirir 
        # self.timer.timeout.connect(self.update_frame)
        # self.timer.start(20)
       
    def btnOpenDir_Click(self):
        dir_name = QFileDialog.getExistingDirectory(self, 'Select Directory')
        if dir_name:
            print(f'Selected Directory: {dir_name}') 
            self.lblPath.setText(dir_name)
       
       
       
       
    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            # Kareyi RGB formatına dönüştür
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Kareyi QImage formatına dönüştür
            height, width, channel = frame.shape
            step = channel * width
            qimg = QImage(frame.data, width, height, step, QImage.Format_RGB888)
            
            # QImage'i QLabel üzerine ayarla
            self.VideoLabel.setPixmap(QPixmap.fromImage(qimg))
        
    def closeEvent(self, event):
        self.timer.stop()
        self.cap.release()
        self.form_closed.emit()  # Form kapandığında sinyali gönderin
        event.accept()

    


