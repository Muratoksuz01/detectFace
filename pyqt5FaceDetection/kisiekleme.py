from PyQt5 import QtWidgets,uic
from PyQt5.QtWidgets import QFileDialog,QMessageBox
from PyQt5.QtCore import QTimer,pyqtSignal
from PyQt5.QtGui import QImage,QPixmap
from uuid import uuid1
import cv2,os

"""
 sonraki yapılacaklar :
 rresim kayıt edilirken biraz kanal degişikligi olmus bunu duzelt 
 kullacı path a class ları belirten yolo icin kullacagın sey işte o yazılcak 
 yaml dosyası yazılacak minumun train ve val olsa yeter
 ornek:
    train: /path/to/your/train/images
    val: /path/to/your/validation/images

    names: 
        0: paper
        1: glass
        2: metal
        3: plastic
"""


class KisiEklemeForm(QtWidgets.QMainWindow):
    form_closed = pyqtSignal()  # Yeni bir sinyal tanımlayın
    def __init__(self,parent=None):
        super(KisiEklemeForm, self).__init__()
        uic.loadUi('kisiekleme.ui', self)  # UI dosyasını yükleyin
        self.btnOpenDir.clicked.connect(self.btnOpenDir_Click)
        self.btnCek.clicked.connect(self.btnCek_Click)
        self.btntrain.clicked.connect(self.btnTrain_Click)
        self.sliderGenislik_2.valueChanged.connect(self.on_sliderGenislik_value_changed)
        self.sliderYukseklik.valueChanged.connect(self.on_sliderYukseklik_value_changed)
        # print("yukseklik ",self.VideoLabel.height())
        # print("genişlik ",self.VideoLabel.width())
        self.yukseklik=int(self.VideoLabel.height()/2)
        self.genislik=int(self.VideoLabel.width()/2)
        self.frame_witht=200
        self.frame_height=300
        self.frame=None
        self.X1=None
        self.X2=None
        self.Y1=None
        self.Y2=None
        self.folder=None
        
        # # Timer oluştur ve update_frame fonksiyonunu çağır
        self.cap = cv2.VideoCapture(0)
        self.timer = QTimer()                                       # 20 milisaniyede signal uretir buda update_frame cagirir 
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(20)
    def btnCek_Click(self):
        label = self.lblSeriCekim_2.text()
        if label or self.folder:
            self.isFolderExists()
            name = uuid1()
            print(name)
            # Resmi kaydet
            cv2.imwrite(f"{self.folder}/{self.lblSeriCekim_2.text()}/images/11{name}.png", cv2.cvtColor(self.frame, cv2.COLOR_RGB2BGR))
            cv2.imwrite(f"{self.folder}/{self.lblSeriCekim_2.text()}/images/{name}.png", cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB))
            
            # Normalize değerleri hesapla
            img_height, img_width, _ = self.frame.shape
            x_center = (self.X1 + self.X2) / 2 / img_width
            y_center = (self.Y1 + self.Y2) / 2 / img_height
            width = (self.X2 - self.X1) / img_width
            height = (self.Y2 - self.Y1) / img_height
            
            # Etiket dosyasına yaz
            with open(f"{self.folder}/{self.lblSeriCekim_2.text()}/labels/{name}.txt", "w") as f:
                f.write(f"0 {x_center} {y_center} {width} {height}")
        else:
            QMessageBox.critical(self, 'critical', 'you have to give a label and folder for your photos.')

    def btnTrain_Click(self):
        print("ogren basıldı")
    def update_frame(self):
        self.X1, self.Y1 = (int(self.genislik - self.frame_witht / 2), int(self.yukseklik - self.frame_height / 2))
        self.X2, self.Y2 = (int(self.genislik + self.frame_witht / 2), int(self.yukseklik + self.frame_height / 2))
        ret, self.frame = self.cap.read()
        if ret:
            img = self.frame.copy()
            # Kareyi RGB formatına dönüştür
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            cv2.rectangle(img,
                        (self.X1, self.Y1),
                        (self.X2, self.Y2),
                        (0, 255, 0), 3)  # Renk ve kalınlık
            # Kareyi QImage formatına dönüştür
            height, width, channel = img.shape
            step = channel * width
            qimg = QImage(img.data, width, height, step, QImage.Format_RGB888)
            
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
        self.folder = QFileDialog.getExistingDirectory(self, "Select Directory", "/home/murar/Documents/python/pyqt5FaceDetection", options=options)
        if self.folder:
            self.lblPath.setText(self.folder)
            print(self.folder)
    
    def on_sliderGenislik_value_changed(self, value):
        self.frame_witht=(self.genislik*2)*(value/10)
    def on_sliderYukseklik_value_changed(self, value):        
        self.frame_height= (self.yukseklik*2)*(value/10)
       
    
    def isFolderExists(self):
        mainpath=os.path.join(self.folder,self.lblSeriCekim_2.text())
        imagespath=os.path.join(mainpath,"images")
        labelspath=os.path.join(mainpath,"labels")
        if os.path.exists(mainpath):
            if os.path.exists(imagespath):pass
            else:os.mkdir(imagespath)
            
            if os.path.exists(labelspath):pass
            else:os.mkdir(labelspath)
            
            
        else:
            os.mkdir(mainpath)
            os.mkdir(imagespath)
            os.mkdir(labelspath)
            
            
       