from PyQt5 import QtWidgets,uic
from PyQt5.QtWidgets import QFileDialog,QMessageBox
from PyQt5.QtCore import QTimer,pyqtSignal
from PyQt5.QtGui import QImage,QPixmap
from uuid import uuid1
import cv2,os,random,shutil
from util import getAndTrain

"""
 sonraki yapılacaklar :

"""


class KisiEklemeForm(QtWidgets.QMainWindow):
    form_closed = pyqtSignal()  # Yeni bir sinyal tanımlayın
    def __init__(self,parent=None,folder=None):
        super(KisiEklemeForm, self).__init__()
        uic.loadUi('/pyqt5FaceDetection/kisiekleme.ui', self)  # UI dosyasını yükleyin
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
        self.frame,self.X1,self.X2,self.Y1,self.Y2=None,None,None,None,None
        self.isfirstImage=True
        self.folder=folder
        self.label=self.lblSeriCekim_2.text() if self.lblSeriCekim_2.text() else "bb" #                                           
        self.main=f"{self.folder}/{self.label}"
        
        # # Timer oluştur ve update_frame fonksiyonunu çağır
        self.cap = cv2.VideoCapture(0)
        self.timer = QTimer()                                       # 20 milisaniyede signal uretir buda update_frame cagirir 
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(20)
    def btnCek_Click(self):
        # label = self.label
        print("folder :",self.folder)
        print("label :",self.label)
        
        if self.label and self.folder:
            if self.isfirstImage: self.isFolderExists() 
            name = uuid1()
            print(name)
            # Resmi kaydet
            cv2.imwrite(f"{self.folder}/{self.label}/images/{name}.png", self.frame)
            
            # Normalize değerleri hesapla
            img_height, img_width, _ = self.frame.shape
            x_center = (self.X1 + self.X2) / 2 / img_width
            y_center = (self.Y1 + self.Y2) / 2 / img_height
            width = (self.X2 - self.X1) / img_width
            height = (self.Y2 - self.Y1) / img_height
            self.main=f"{self.folder}/{self.label}"
            # Etiket dosyasına yaz
            with open(f"{self.folder}/{self.label}/labels/{name}.txt", "w") as f:
                f.write(f"0 {x_center} {y_center} {width} {height}")
            self.isfirstImage=False
        else:
            QMessageBox.critical(self, 'critical', f'you have to give a label and folder for your photos {self.label}   {self.folder}')
    

        
    def btnTrain_Click(self):
        self.ShuffleAndMove()
        getAndTrain(self.folder,self.main,epo=20)
        QMessageBox.about(self,"about","model egitildi")
        
        
        
        
        
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


    def on_sliderGenislik_value_changed(self, value):
        self.frame_witht=(self.genislik*2)*(value/10)
    def on_sliderYukseklik_value_changed(self, value):        
        self.frame_height= (self.yukseklik*2)*(value/10)
       
    
    def isFolderExists(self):
        mainpath=os.path.join(self.folder,self.label)
        imagespath=os.path.join(mainpath,"images")
        labelspath=os.path.join(mainpath,"labels")
        if os.path.exists(mainpath):
            
            QMessageBox.warning(self,"uyarı","bu label zaten var lutfen bir defa daha deneyin")
            # if os.path.exists(imagespath):pass
            # else:os.mkdir(imagespath)
            
            # if os.path.exists(labelspath):pass
            # else:os.mkdir(labelspath)
            
            
        else:
            os.mkdir(mainpath)
            os.mkdir(imagespath)
            os.mkdir(labelspath)
    
    
    
    def ShuffleAndMove(self):
        print(self.main)
        os.makedirs(self.main+"/train/images", exist_ok=True)
        os.makedirs(self.main+"/train/labels", exist_ok=True)
        os.makedirs(self.main+"/valid/images", exist_ok=True)
        os.makedirs(self.main+"/valid/labels", exist_ok=True)
        
        preImages = os.listdir(self.main+"/images/")
        if len(preImages)==0:return
        preImages=[i.split(".")[0] for  i in preImages]
        trainlen = int(len(preImages) * 0.7)
        random.shuffle(preImages)
        train = preImages[:trainlen]
        valid = preImages[trainlen:]
        
        try:
            for i in train:
                shutil.move(os.path.join(self.main, "labels", f"{i}.txt"), os.path.join(self.main, "train", "labels", f"{i}.txt"))
                shutil.move(os.path.join(self.main, "images", f"{i}.png"), os.path.join(self.main, "train", "images", f"{i}.png"))
        except FileNotFoundError as e:
            print(f"Hata: {e}")
            return
        try:
            for i in valid:
                shutil.move(os.path.join(self.main, "labels", f"{i}.txt"), os.path.join(self.main, "valid", "labels", f"{i}.txt"))
                shutil.move(os.path.join(self.main, "images", f"{i}.png"), os.path.join(self.main, "valid", "images", f"{i}.png"))
        except FileNotFoundError as e:
            print(f"Hata: {e}")
            return
        
        
        os.removedirs(self.main+"/images")
        os.removedirs(self.main+"/labels")
        
        with open(f"{self.main}/data.yaml","w") as f:
            f.write(f"train: {self.main}/train/images\nval: {self.main}/valid/images\nnc: 1\nnames: ['{self.label}']")  
            
       
