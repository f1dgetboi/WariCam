from ultralytics import YOLO
import cv2
import cvzone
import math

cap = cv2.VideoCapture(0) #tweak the value for the second or the fiest webcam
cap.set(3,1920)
cap.set(4,1080)
model = YOLO('models/yolov8l.pt')
plate_model = YOLO('models/plate-detector.pt')
classNames = ["Plate"]

