from Gui import *
import Gui
#from platedetection import *
import math
mainClock = pygame.time.Clock()
Gui.create_window(monitor_size[0],monitor_size[1],(40, 40, 43),"WariCam")

MONITOR_MIDDLE = (monitor_size[0] / 2,monitor_size[1] / 2)
BACKGROUND_IMG = pygame.image.load("images/background.png")
a = pygame.image.load("images/minus_sign.png")
banana_big = pygame.image.load("images/Foods/fullsize_banana.png")
Table = pygame.image.load("images/Table.png")
#変数の初期化
people = 0
children = 0
y_offset = -100
x_offset = 285
current_stage = 0
BUTTON_COLORS = (225, 217, 209)
frames =[]
buying = None
bought = []
input_box1 = InputBox(MONITOR_MIDDLE[0] - 80, 250, 10, 40)
input_box2 = InputBox(565, 700, 50, 40)
input_box3 = InputBox(565, 450, 50, 40)
input_box4 = InputBox(1200, 700, 50, 40)
input_box5 = InputBox(1200, 450, 50, 40)
input_boxes = [input_box1, input_box2, input_box3, input_box4, input_box5]

#オブジェクトのインスタンスを初期化

background = GuiObject(1000,750,455,MONITOR_MIDDLE[1]-375,(255,255,255),texture=None,visible=True,stroke=False,stroke_width=5,stroke_color=(255,255,255),rounded=True,roundness=10)
background_2 = GuiObject(1000,900,455,MONITOR_MIDDLE[1]-375,(255,255,255),texture=None,visible=True,stroke=False,stroke_width=5,stroke_color=(255,255,255),rounded=True,roundness=10)
plus_button = Button(100,100,820 + x_offset,400+ y_offset,(BUTTON_COLORS),texture="images/plus.png",visible=True,stroke=False,stroke_width=5,stroke_color=(100,100,100),rounded=True,roundness=10,hollow=False,background=True)
minus_button = Button(100,100,380 + x_offset,400+ y_offset,(BUTTON_COLORS),texture="images/minus.png",visible=True,stroke=False,stroke_width=5,stroke_color=(100,100,100),rounded=True,roundness=10,hollow=False,background=True)
people_text = TextBox(300,100,500 + x_offset,400+ y_offset,(BUTTON_COLORS),str(people),100,130,-30)
c_plus_button = Button(100,100,820 + x_offset,650+ y_offset,(BUTTON_COLORS),texture="images/plus.png",visible=True,stroke=False,stroke_width=5,stroke_color=(100,100,100),rounded=True,roundness=10,hollow=False,background=True)
c_minus_button = Button(100,100,380 + x_offset,650+ y_offset,(BUTTON_COLORS),texture="images/minus.png",visible=True,stroke=False,stroke_width=5,stroke_color=(100,100,100),rounded=True,roundness=10,hollow=False,background=True)
children_text = TextBox(300,100,500 + x_offset,650+ y_offset,(BUTTON_COLORS),str(people),100,130,-30)
continue_button = Button(400,110,750,750,(BUTTON_COLORS),texture=None,visible=True,stroke=False,stroke_width=5,stroke_color=(100,100,100),rounded=True,roundness=10,hollow=False,background=True,text="続行",fontsize=100,text_offset_y=-20,text_offset_x=100)
continue_button_2 = Button(400,110,750,925,(BUTTON_COLORS),texture=None,visible=True,stroke=False,stroke_width=5,stroke_color=(100,100,100),rounded=True,roundness=10,hollow=False,background=True,text="続行",fontsize=100,text_offset_y=-20,text_offset_x=100)
banana_frame = buy_frame(100,100,(BUTTON_COLORS),"500円","バナナの皿","images/Foods/banana.png")
banana_buy = Button(400,110,750,950,(BUTTON_COLORS),texture=None,visible=True,stroke=False,stroke_width=5,stroke_color=(100,100,100),rounded=True,roundness=10,hollow=False,background=True,text="購入",fontsize=100,text_offset_y=-20,text_offset_x=100)
Warikan_button = Button(300,50,800,675,(BUTTON_COLORS),texture="images/Logos/off.png",visible=True,stroke=False,stroke_width=3,stroke_color=(100,100,100),rounded=True,roundness=3,hollow=False,background=True,text="割り勘機能を使用",fontsize=30,text_offset_y=0,text_offset_x=50)

#少しオブジェクトの値を変えている
people_text.roundness = 10
people_text.rounded = True
children_text.roundness = 10
children_text.rounded = True
hoverd = False
Warikan = False
frames.append(banana_frame)

#画面に描画する関数

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
    if current_stage == 0:
        #draw background
        Gui.screen.blit(BACKGROUND_IMG,(0,0))
        draw_welcome()
        Warikan_button.draw()
    if current_stage == 1:
        Gui.screen.fill((248, 248, 255))
        banana_frame.draw()
       
    if current_stage == 2:
        Gui.screen.fill((248, 248, 255))
        if buying == "バナナの皿":
            Gui.screen.blit(banana_big,(412,100))
            create_center_text(DEFAULT_FONT,100,(0,0,0),MONITOR_MIDDLE[0],750,buying)
            create_center_text(DEFAULT_FONT,50,(0,0,0),MONITOR_MIDDLE[0],850,"500円")
            banana_buy.draw()
    if current_stage == 3:
        Gui.screen.blit(BACKGROUND_IMG,(0,0))
        background_2.draw()
        continue_button_2.draw()
        Gui.screen.blit(Table,(455,MONITOR_MIDDLE[1]-375))

def handle_button():
    global people,children,current_stage,frames,buying,Warikan
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    if current_stage == 0:
        if children > 0:
            children = c_minus_button.check_clicks(children,-1)  
        if people > 0:
            people = minus_button.check_clicks(people,-1)


        children = c_plus_button.check_clicks(children,1)
        people = plus_button.check_clicks(people,1)
        Warikan = Warikan_button.check_clicks(Warikan,how_much=None,bool=True)
        people_text.text = str(people)
        children_text.text = str(children)
        if Warikan == False:
            Warikan_button.texture = pygame.image.load("images/Logos/off.png")           
            current_stage = continue_button.check_clicks(current_stage,1)
        if Warikan == True:
            Warikan_button.texture = pygame.image.load("images/Logos/on.png")
            current_stage = continue_button.check_clicks(current_stage,3)
    if current_stage == 1:
        for frame in frames:
            current_stage = frame.background.check_clicks(current_stage,1,bool=False,string=False,list=False) 
            if frame.background.clicked == True:
                buying =  str(frame.name)
                print(current_stage)
    if current_stage == 2:
        banana_buy.check_clicks(bought,how_much="Banana Plate",bool=False,string=False,list=True)
        if banana_buy.clicked == True:
            current_stage = 1
            buying = None  
        banana_buy.clicked = False 
    if current_stage == 3:
        for box in input_boxes:
            box.update()
            box.draw(Gui.screen) 
        current_stage = continue_button_2.check_clicks(current_stage,-1)
#背景動作

def pygame_background_functionts(testsubject=None,value_x=None,value_y=None):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if testsubject is not None:
                with open('test.txt', 'w') as f:
                    #f.write(f'Y is: {testsubject.y} X is: {testsubject.x} width is: {testsubject.w} height is: {testsubject.h}')
                    f.write(f'Y is: {value_y} X is: {value_x} ')
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if testsubject is not None:
                if event.key == K_DOWN:
                    value_y += 1
                    testsubject.y += 5
                if event.key == K_UP:
                    value_y -= 1
                    testsubject.y -= 5
                if event.key == K_RIGHT:
                    value_x += 1
                    testsubject.x += 5
                if event.key == K_LEFT:
                    value_x -= 1
                    testsubject.x -= 5
                if event.key == K_m:
                    testsubject.w +=5
                if event.key == K_n:
                    testsubject.w -=5
                if event.key == K_x:
                    testsubject.h +=5
                if event.key == K_c:
                    testsubject.h -=5

        for box in input_boxes:
                box.handle_event(event)

    surf = pygame.transform.scale(Gui.screen,(monitor_size))
    Gui.display.blit(surf,(0,0))
    pygame.display.update()

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
    pygame_background_functionts()
    draw()
    #display computer vision onto screen
    #Gui.screen.blit(resize_image(BGR_TO_RGB(img),800,450),(100,100))
    mainClock.tick(60)
