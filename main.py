from Gui import *
import Gui
#from platedetection import *
import math
mainClock = pygame.time.Clock()
Gui.create_window(monitor_size[0],monitor_size[1],(40, 40, 43),"WariCam")

MONITOR_MIDDLE = (monitor_size[0] / 2,monitor_size[1] / 2)
BACKGROUND_IMG = pygame.image.load("images/background.png")
a = pygame.image.load("images/minus_sign.png")

people = 0
children = 0
y_offset = -50
x_offset = 285
current_stage = 0

#define objects
background = GuiObject(1000,750,455,MONITOR_MIDDLE[1]-375,(255,255,255),texture=None,visible=True,stroke=False,stroke_width=5,stroke_color=(255,255,255),rounded=True,roundness=10)
plus_button = Button(100,100,820 + x_offset,400+ y_offset,(220,220,220),texture="images/plus.png",visible=True,stroke=False,stroke_width=5,stroke_color=(100,100,100),rounded=True,roundness=10,hollow=False,background=True)
minus_button = Button(100,100,380 + x_offset,400+ y_offset,(220,220,220),texture="images/minus.png",visible=True,stroke=False,stroke_width=5,stroke_color=(100,100,100),rounded=True,roundness=10,hollow=False,background=True)
people_text = TextBox(300,100,500 + x_offset,400+ y_offset,(220,220,220),str(people),100,130,-30)
c_plus_button = Button(100,100,820 + x_offset,650+ y_offset,(220,220,220),texture="images/plus.png",visible=True,stroke=False,stroke_width=5,stroke_color=(100,100,100),rounded=True,roundness=10,hollow=False,background=True)
c_minus_button = Button(100,100,380 + x_offset,650+ y_offset,(220,220,220),texture="images/minus.png",visible=True,stroke=False,stroke_width=5,stroke_color=(100,100,100),rounded=True,roundness=10,hollow=False,background=True)
children_text = TextBox(300,100,500 + x_offset,650+ y_offset,(220,220,220),str(people),100,130,-30)
continue_button = Button(400,110,750,750,(220,220,220),texture=None,visible=True,stroke=False,stroke_width=5,stroke_color=(100,100,100),rounded=True,roundness=10,hollow=False,background=True,text="続行",fontsize=100,text_offset_y=-20,text_offset_x=100)

people_text.roundness = 10
people_text.rounded = True
children_text.roundness = 10
children_text.rounded = True
hoverd = False

#draw functions
def draw_welcome():
    background.draw()
    plus_button.draw()
    minus_button.draw()
    people_text.draw()
    people_text.text = str(people)
    children_text.text = str(children)
    Gui.create_text(DEFAULT_FONT,100,(0,0,0),550+ x_offset,250+ y_offset,"人数")
    Gui.create_text(DEFAULT_FONT,100,(0,0,0),400+ x_offset,500+ y_offset,"子供の人数")
    c_minus_button.draw()
    c_plus_button.draw()
    children_text.draw()
    continue_button.draw()
def draw():
    print(current_stage)
    if current_stage == 0:
        #draw background
        Gui.screen.blit(BACKGROUND_IMG,(0,0))
        draw_welcome()
    if current_stage == 1:
        pass
def handle_button():
    global people,children,current_stage
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    if children > 0:
        children = c_minus_button.check_clicks(children,-1)  
    if people > 0:
        people = minus_button.check_clicks(people,-1)


    children = c_plus_button.check_clicks(children,1)
    people = plus_button.check_clicks(people,1)

    people_text.text = str(people)
    children_text.text = str(children)
    current_stage = continue_button.check_clicks(current_stage,1)


def plate_detection():
    #global x1,y1,x2,y2,w,h
    scuccess, img = cap.read()
    results = model(img, stream=True)
    for r in results:
        boxes = r.boxes
        for box in boxes:
            #bounding boxes
           x1,y1,x2,y2 = box.xyxy[0]
           x1,y1,x2,y2 = int(x1),int(y1),int(x2),int(y2)
           #cv2.rectangle(img,(x1,y1),(x2,y2),(0,0,255),3)
           # cv2.putText(img, str(conf), (x1,y1), cv2.FONT_HERSHEY_COMPLEX, 3, (0, 0, 255), 3)
           w,h = x2-x1,y2-y1
           cvzone.cornerRect(img,(x1,y1,w,h))
           conf = math.ceil((box.conf[0]*100))/100
           cls = box.cls[0]
           cvzone.putTextRect(img,f"Plate  {conf}",(max(0,x1),max(35,y1)))

    cv2.waitKey(1)

while True:
    
    #find plates
    handle_button()
    draw()
    #display computer vision onto screen
    #Gui.screen.blit(resize_image(BGR_TO_RGB(img),800,450),(100,100))
    pygame_background_functionts()
    mainClock.tick(60)