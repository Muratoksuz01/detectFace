from ultralytics import YOLO
import cv2
import random

model = YOLO("/home/murat/General/murat/runs/weights/best.pt")

cap = cv2.VideoCapture(0)
while True:
    ret, img = cap.read()
    if not ret:
        print("Failed to capture image")
        break
    
    img = cv2.resize(img, (640, 640))
    results = model.predict(img, conf=0.3)  # Increased confidence threshold

    for r in results:
        boxes = r.boxes
        cls = boxes.cls
        print("classname:", cls)
        print("len:", len(cls))
        
        for box in boxes.xyxy:  
            x1, y1, x2, y2 = box
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            cv2.rectangle(img, (x1, y1), (x2, y2), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), 1)
    
    cv2.imshow("aaa", img)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()





"""

model=YOLO("/home/murat/General/yolov8n.pt")
model.train(data="/home/murat/General/murat/data.yaml",epochs=20,name="runs",project="/home/murat/General/murat")"""