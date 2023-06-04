from ultralytics import YOLO
import cv2
import cvzone
cap = cv2.VideoCapture(0)
cap.set(3,1920)
cap.set(4,1080)
model = YOLO('models/yolov8l.pt')
classNames = ["apple"]



    
