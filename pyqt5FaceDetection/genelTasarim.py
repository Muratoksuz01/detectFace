import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
import cv2
from PyQt5.QtWidgets import QFileDialog,QMessageBox,QListWidgetItem

from kisiekleme import KisiEklemeForm
from util import *
import os,random
from PyQt5 import QtCore, QtWidgets


os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = os.path.join(os.path.dirname(QtCore.__file__), "plugins")




class ExampleApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(ExampleApp, self).__init__()
        uic.loadUi('/home/murat/Documents/python/detectFace/pyqt5FaceDetection/genelTasarim.ui', self)
        self.btnOpenDir.clicked.connect(self.btnOpenDir_Click)
        self.btn_durdur.clicked.connect(self.btn_durdur_Click)
        self.btnKisiEkle.clicked.connect(self.open_kisi_ekleme)
        self.btnKisiSil.clicked.connect(self.open_kisi_sil)
        self.btnKaydet.clicked.connect(self.show_selected)
        # Timer ve kamera bağlantısı
        self.cap = cv2.VideoCapture(0)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(20)
        self.allmodels=None
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
        self.allmodels=getModel(self.folder,selected_texts)
    def btn_durdur_Click(self):
        self.allmodels.clear()
        print("modeller durduruldu !!!!!")
        
    def update_frame(self):
        def predictModel(img):
            img=cv2.resize(img,(640,640))
            for model in self.allmodels:
                
                results=model.predict(img,conf=0.5)
                if len(results)==0:
                    continue
                for r in results:
                    boxes=r.boxes
                    cls=boxes.cls
                    print("classname:",cls)
                    print("len:",len(cls))
                    for box,conf in zip(boxes.xyxy,boxes.conf): #                       sonradan burayı duzeltitrsin 
                        x1,y1,x2,y2=box
                        x1,y1,x2,y2=int(x1),int(y1),int(x2),int(y2)
                        cv2.rectangle(img,(x1,y1),(x2,y2),(random.randint(0,255),random.randint(0,255),random.randint(0,255)),1)

                    
            return img           
            
            
            
            
            
            
            
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, channel = frame.shape
            step = channel * width
            if self.allmodels:
                frame=predictModel(frame)
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




