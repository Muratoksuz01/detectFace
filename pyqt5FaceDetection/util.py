from ultralytics import YOLO
def getAndTrain(mainFolder,trainFolder,epo=1):
    """_summary_

    Args:
        mainFolder (str): general folder
        trainFolder (_type_): generel/murat
    """
    model=YOLO(f"{mainFolder}/yolov8n.pt")
    print(trainFolder)
    model.train(data=trainFolder+"/data.yaml",epochs=epo,project=trainFolder,name="runs")

def getModel(mainFolder,selected_models):
    """mainfolderle modelleri alacak bunları bir dizi seklinde diger foksiyona verecek yada geri donecek

    Args:
        mainFolder (_type_): _description_
        selected_models (_type_): _description_
    """
    print("modeller yukleniyor !!!!!!")    
    models=[]
    try:
        
        for i in selected_models:
            text=f"{mainFolder}/{i}/runs/weights/best.pt"
            a=YOLO(text)
            models.append(a)
    except:
        print(text ," yuklenemedi ")
    return models









