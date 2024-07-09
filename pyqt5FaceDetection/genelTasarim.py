import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
import cv2
from PyQt5.QtWidgets import QFileDialog,QMessageBox,QListWidgetItem

from kisiekleme import KisiEklemeForm
from util import lockMouseandkey
import os
from PyQt5 import QtCore, QtGui, QtWidgets


os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = os.path.join(os.path.dirname(QtCore.__file__), "plugins")




class ExampleApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(ExampleApp, self).__init__()
        uic.loadUi('/home/murat/Documents/python/detectFace/pyqt5FaceDetection/genelTasarim.ui', self)
        self.btnOpenDir.clicked.connect(self.btnOpenDir_Click)
        self.btnKisiEkle.clicked.connect(self.open_kisi_ekleme)
        self.btnKisiSil.clicked.connect(self.open_kisi_sil)
        self.btnKaydet.clicked.connect(self.show_selected)
        # Timer ve kamera bağlantısı
        self.cap = cv2.VideoCapture(0)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(20)

        # Yeni form açma butonuna bağla
        self.folder="/home/murat/General"
        self.searchModel()
        # self.open_kisi_ekleme() # ikinci ekranı caliştirmak icin 
    def searchModel(self):
        directories = [d for d in os.listdir(self.folder) if os.path.isdir(os.path.join(self.folder, d))]
        for item in directories:
            list_item = QListWidgetItem(item)
            self.listwidget.addItem(list_item)
    def show_selected(self):
        selected_items = self.listwidget.selectedItems()
        selected_texts = [item.text() for item in selected_items]
        print("Selected items:", selected_texts)
        lockMouseandkey()
        
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
        self.new_form = KisiEklemeForm(self,folder=self.folder)
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
    def btnOpenDir_Click(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.folder = QFileDialog.getExistingDirectory(self, "Select Directory", "/home/murar/Documents/python/pyqt5FaceDetection", options=options)
        if self.folder:
            self.lblPath.setText(self.folder)
            print(self.folder)
    
app = QtWidgets.QApplication(sys.argv)
window = ExampleApp()
window.show()
sys.exit(app.exec_())




