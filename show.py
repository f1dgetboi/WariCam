from ultralytics.yolo.engine.model import YOLO

model = YOLO("models/plate-detector.pt")
results = model.predict(source=r'images\test_imgs\IMG_3218.JPG', save=True, save_txt=True)