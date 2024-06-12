from PyQt5 import QtWidgets,uic
from PyQt5.QtWidgets import QFileDialog,QMessageBox
from PyQt5.QtCore import QTimer,pyqtSignal
from PyQt5.QtGui import QImage,QPixmap
from uuid import uuid1
import cv2,os

"""
name kısmı etiket gibi dusun 
kullanıcı path belirtedek biz oraya images ve labels diye klosor olusturp icini dolduracagiz 
seri cekimde resimler belli bir aralıkla ceklirise iyi olur ve  bu sn ona gostermeliyiz
 
 
 sonraki yapılacaklar :
 rresim kayıt edilirken biraz kanal degişikligi olmus bunu duzelt 
 resimleri images klosorune ve labels klosoru ve icincekileri yazmak olacak 
 kullacı path a class ları belirten yolo icin kullacagın sey işte o yazılcak 
 windowa train butonu ekle 
"""


class KisiEklemeForm(QtWidgets.QMainWindow):
    form_closed = pyqtSignal()  # Yeni bir sinyal tanımlayın
    def __init__(self,parent=None):
        super(KisiEklemeForm, self).__init__()
        uic.loadUi('kisiekleme.ui', self)  # UI dosyasını yükleyin
        self.btnOpenDir.clicked.connect(self.btnOpenDir_Click)
        self.btnCek.clicked.connect(self.btnCek_Click)
        self.sliderGenislik_2.valueChanged.connect(self.on_sliderGenislik_value_changed)
        self.sliderYukseklik.valueChanged.connect(self.on_sliderYukseklik_value_changed)
        # print("yukseklik ",self.VideoLabel.height())
        # print("genişlik ",self.VideoLabel.width())
        self.yukseklik=int(self.VideoLabel.height()/2)
        self.genislik=int(self.VideoLabel.width()/2)
        self.frame_witht=200
        self.frame_height=300
        self.frame=None
        # # Timer oluştur ve update_frame fonksiyonunu çağır
        self.cap = cv2.VideoCapture(0)
        self.timer = QTimer()                                       # 20 milisaniyede signal uretir buda update_frame cagirir 
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(20)
    def btnCek_Click(self):
        print(self.cbSeriCekim.isChecked())
        label=self.lblSeriCekim_2.text()
        if label:
            print(name)
            name=uuid1()
           # cv2.imwrite(f"{name}.png",self.frame)
        else:
            QMessageBox.critical(self, 'critical', 'you have to give a label for your photos.')
 
   
    def update_frame(self):
        ret, self.frame = self.cap.read()
        if ret:
            
            # Kareyi RGB formatına dönüştür
            self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            cv2.rectangle(self.frame ,
                          (int(self.genislik-self.frame_witht/2),int(self.yukseklik-self.frame_height/2)),# baslangıc 
                          (int(self.genislik+self.frame_witht/2),int(self.yukseklik+self.frame_height/2)),# sonu 
                          (0,255,0),3)# renk ve kalınlık 
            # Kareyi QImage formatına dönüştür
            height, width, channel = self.frame.shape
            step = channel * width
            qimg = QImage(self.frame.data, width, height, step, QImage.Format_RGB888)
            
            # QImage'i QLabel üzerine ayarla
            self.VideoLabel.setPixmap(QPixmap.fromImage(qimg))
        
    def closeEvent(self, event):
        self.timer.stop()
        self.cap.release()
        self.form_closed.emit()  # Form kapandığında sinyali gönderin
        event.accept()

    def btnOpenDir_Click(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        folder = QFileDialog.getExistingDirectory(self, "Select Directory", "/home/murar", options=options)
        if folder:
            print(folder)
    
    def on_sliderGenislik_value_changed(self, value):
        print(value)
        self.frame_witht=(self.genislik*2)*(value/10)
    def on_sliderYukseklik_value_changed(self, value):
        print(value)
        
        self.frame_height= (self.yukseklik*2)*(value/10)
       
    
        
       
       