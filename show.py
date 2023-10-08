from ultralytics.yolo.engine.model import YOLO
import cv2
import cvzone
import math
import handtrackingmodule


model = YOLO("models/plate-detector.pt")
results = model.predict(source=r'images\test_imgs\IMG_3218.JPG', save=True, save_txt=True)
detector = handtrackingmodule.handDetector()
cap = cv2.VideoCapture(0)

def show():
    global x1,y1,x2,y2,w,h
    scuccess, img = cap.read()
    results = model(img,classes= 46, stream=True)          
    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1,y1,x2,y2 = box.xyxy[0]
            x1,y1,x2,y2 = int(x1),int(y1),int(x2),int(y2)
            #cv2.rectangle(img,(x1,y1),(x2,y2),(0,0,255),3)
            #cv2.putText(img, str(conf), (x1,y1), cv2.FONT_HERSHEY_COMPLEX, 3, (0, 0, 255), 3)
            w,h = x2-x1,y2-y1
            MIDDLE = (x1 + (w)/2,y1 + (h)/2)
            cvzone.cornerRect(img,(x1,y1,w,h))
            conf = math.ceil((box.conf[0]*100))/100
            cls = box.cls[0]
            print(" x1: " + str(x1)," x2: " + str(x2)," y1: " + str(y1)," y2: " + str(y2))
            print(f"MIDDLE: {MIDDLE}") 

    height = img.shape[0]
    width = img.shape[1]
    img = detector.findHands(img)
    lmlist = detector.findPosition(img)
    #cv2.waitKey(1)

    return img
