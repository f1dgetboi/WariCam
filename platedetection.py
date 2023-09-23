from ultralytics import YOLO
import cv2
import cvzone
import math
cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,360)
model = YOLO('models/yolov8n.pt')
plate_model = YOLO('models/plate-detector.pt')
classNames = ["Plate"]

