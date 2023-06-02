from imports import *

class handDetector():
   
    def __init__(self,mode=False,maxHands = 2, modelComplexity=1,detectionCon=0.5,trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.modelComplex = modelComplexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode,self.maxHands, self.modelComplex,self.detectionCon,self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self,img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
            
        return img
                
    def findPosition(self,img,handNo=0,draw=True):
        lmlist = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]

            for id, lm in enumerate(myHand.landmark):  
                h,w,c = img.shape
                cx,cy = int(lm.x*w), int(lm.y*h) 
                lmlist.append([id, cx, cy])
                if draw:
                     cv2.circle(img,(cx,cy),15,(255,0,255),cv2.FILLED)
    
        return lmlist

def main():
    cap = cv2.VideoCapture(1)
    pTime = 0
    cTime = 0
    detector = handDetector()
    while True:
        success, img = cap.read()
        height = img.shape[0]
        width = img.shape[1]
        img = detector.findHands(img)
        lmlist = detector.findPosition(img)
        print(lmlist)
        cTime = time.time()
        fps = 1/(cTime -pTime)
        pTime = cTime

        #cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_COMPLEX,3,(0,0,255),3)

        cv2.imshow("image", img)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()