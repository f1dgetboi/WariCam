from Gui import *
import Gui
from platedetection import *
import math
#import handtrackingmodule
#from handtrackingmodule import *
import threading
import numpy as np
import pygame, sys
from pygame.locals import *
import cv2
from ultralytics import YOLO
import readexcel
import time
import socket
from tkinter import filedialog
import tkinter 

global whole_table_banana,banana_diff_global


mainClock = pygame.time.Clock()
Gui.create_window(monitor_size[0],monitor_size[1],(40, 40, 43),"WariCam")

top = tkinter.Tk()
top.withdraw()  # hide window


MONITOR_MIDDLE = (monitor_size[0] / 2,monitor_size[1] / 2)
BACKGROUND_IMG = pygame.image.load("images/background.png")
banana_big = pygame.image.load("images/Foods/fullsize_banana.png")
Table = pygame.image.load("images/Table.png")
check_box = pygame.image.load("images/Logos/check_small.png")
cross_box = pygame.image.load("images/Logos/cross_small.png")
#変数の初期化
people = 0
children = 0
y_offset = -100
x_offset = 285
current_stage = -2
BUTTON_COLORS = (225, 217, 209)
buying = None
bought = []
frames=[]
input_box1 = InputBox(MONITOR_MIDDLE[0] - 80, 250, 10, 40)
input_box2 = InputBox(565, 700, 50, 40)
input_box3 = InputBox(565, 450, 50, 40)
input_box4 = InputBox(1200, 700, 50, 40)
input_box5 = InputBox(1200, 450, 50, 40)
input_boxes = [input_box1, input_box2, input_box3, input_box4, input_box5]
places = []
Banana_kazu = [0,0,0,0,0]
tabeta_kazu = [0,0,0,0,0]
changed = False
eating_people = []
current_foods = [0,0,0,0,0]
whole_table_banana = 0
banana_diff_global = 0
eating_people = []
bananas = [0,0,0,0,0]
success,img=cap.read()
whole_table_banana = 0
mode = "heavy"
foods_list: dict = {}
foods_on_menu: dict = {}
SERVER_PC = False
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
continue_button_3 = Button(400,110,750,monitor_size[1]- 160,(BUTTON_COLORS),texture=None,visible=True,stroke=False,stroke_width=5,stroke_color=(100,100,100),rounded=True,roundness=10,hollow=False,background=True,text="続行",fontsize=100,text_offset_y=-20,text_offset_x=100)
open_filexplorer_menu = Button(400,110,450,250,(BUTTON_COLORS),texture=None,visible=True,stroke=False,stroke_width=5,stroke_color=(100,100,100),rounded=True,roundness=10,hollow=False,background=True,text="メニューを開く",fontsize=50,text_offset_y=20,text_offset_x=30)
open_filexplorer_foods = Button(400,110,monitor_size[0] - 850,250 ,(BUTTON_COLORS),texture=None,visible=True,stroke=False,stroke_width=5,stroke_color=(100,100,100),rounded=True,roundness=10,hollow=False,background=True,text="食べ物リストを開く",fontsize=40,text_offset_y=25,text_offset_x=30)
#banana_frame = buy_frame(100,100,(BUTTON_COLORS),"500円","バナナの皿","images/Foods/banana.png")
banana_buy = Button(400,110,750,950,(BUTTON_COLORS),texture=None,visible=True,stroke=False,stroke_width=5,stroke_color=(100,100,100),rounded=True,roundness=10,hollow=False,background=True,text="購入",fontsize=100,text_offset_y=-20,text_offset_x=100)
server_button = Button(300,50,800,monitor_size[1]- 260,(BUTTON_COLORS),texture="images/Logos/off.png",visible=True,stroke=False,stroke_width=3,stroke_color=(100,100,100),rounded=True,roundness=3,hollow=False,background=True,text="サーバーPCである",fontsize=30,text_offset_y=0,text_offset_x=50)
Warikan_button = Button(300,50,800,675,(BUTTON_COLORS),texture="images/Logos/off.png",visible=True,stroke=False,stroke_width=3,stroke_color=(100,100,100),rounded=True,roundness=3,hollow=False,background=True,text="割り勘機能を使用",fontsize=30,text_offset_y=0,text_offset_x=50)
back_button = Button(150,60,1750,30,(BUTTON_COLORS),texture="images/back.png",visible=True,stroke=False,stroke_width=5,stroke_color=(100,100,100),rounded=True,roundness=2,hollow=False,background=True,text="戻る",fontsize=50,text_offset_y=-10,text_offset_x=50)
warikan_look = Button(300,60,1600,1000,(BUTTON_COLORS),texture=None,visible=True,stroke=False,stroke_width=5,stroke_color=(100,100,100),rounded=True,roundness=2,hollow=False,background=True,text="割り勘を見る",fontsize=40,text_offset_y=0,text_offset_x=10)
#少しオブジェクトの値を変えている

people_text.roundness = 10
people_text.rounded = True
children_text.roundness = 10
children_text.rounded = True
hoverd = False
Warikan = True
setup_success = [False,False]

#frames.append(banana_frame)
def prompt_file():
    file_name = tkinter.filedialog.askopenfilename(parent=top)
    print(file_name)
    return file_name

def update_screen():
    surf = pygame.transform.scale(Gui.screen,(monitor_size))
    Gui.display.blit(surf,(0,0))
    pygame.display.update()

    

def Banana_detection_Whole_table():
    global img,diff_global, whole_table_banana
    #global x1,y1,x2,y2,w,h
    #scuccess, img = cap.read()
    results = model(img,classes= 46)
    for r in results:
        boxes = list(r.boxes) 

    diff_global = len(boxes) - whole_table_banana 
    whole_table_banana = len(boxes)

class person:
    def __init__(self, name,area):
        self.name = name
        self.area = area
        self.current_frame_local_food = [0]
        self.last_frame_local_food = [0]
        self.counted_food = [0]
        self.last_frame_whole_table_food = [0]
        self.current_frame_whole_table_food = [0]

    def update_food(self,img,x,y):

        # CAPTURE BOXES IN LOCAL AREA
        self.current_frame_whole_table_food[0] = 0
        self.current_frame_local_food[0] = 0
        results = model(img,classes= 46)

        for r in results:
            boxes = r.boxes

            for box in boxes:
                x1,y1,x2,y2 = box.xyxy[0]
                x1,y1,x2,y2 = int(x1),int(y1),int(x2),int(y2)
                w,h = x2-x1,y2-y1
                MIDDLE = (x1 + (w)/2,y1 + (h)/2)

                """ for debugging purposes """
                #cvzone.cornerRect(img,(x1,y1,w,h))
                #conf = math.ceil((box.conf[0]*100))/100
                #cls = box.cls[0]  
                """ for debugging purposes """         

                if self.area[0] <= MIDDLE[0] and self.area[1] >= MIDDLE[0] and self.area[2] <= MIDDLE[1] and self.area[3] >= MIDDLE[1] :
                    self.current_frame_local_food[0] += 1

                else:
                    self.current_frame_whole_table_food[0] += 1

            

        diff_invert = self.current_frame_whole_table_food[0] - self.last_frame_whole_table_food[0] 
        self.last_frame_whole_table_food[0]  = self.current_frame_whole_table_food[0]  

        diff_local = self.current_frame_local_food[0] - self.last_frame_local_food[0]
        self.last_frame_local_food[0] = self.current_frame_local_food[0]

        print(f"local: {diff_local}, whole: {diff_invert}")

        if diff_local < 0 :
            if diff_invert > 0:
                self.counted_food[0] -= 1#diff_local 
        elif diff_local > 0 :
            if diff_invert < 0:
                self.counted_food[0] += 1#diff_local
        else:
            pass
                
        

        create_center_text(DEFAULT_FONT, 100, (0, 0, 0), x, y, f"{self.name} has {self.counted_food[0]} bananas")

        
        

def get_keys_by_value(dictionary, value):
    keys = []
    for key, val in dictionary.items():
        if val == value:
            keys.append(key)
    return keys

def get_index_of_value(dictionary, value):
    for index, val in enumerate(dictionary.values()):
        if val == value:
            return index
    return -1




def Banana_detection_each_person(x1,x2,y1,y2) :
    global current_foods
    scuccess, img = cap.read()
    banana_diff_local = 0
    cropped_image = img[y1:y2, x1:x2]
    results = model(cropped_image,classes= 46) 
    for r in results:
        boxes = list(r.boxes) 

    banana_diff_local = len(boxes) - current_foods[0]  
    if banana_diff_local< 0:        
        if banana_diff_global <= -1:             
            current_foods[0] = len(boxes)
    else:
        current_foods[0] = len(boxes)

    cv2.waitKey(1)
    return current_foods[0]

    
#if there comes new bananas and there comes another one into your area check the other areas and find if that banan came to you therefore add 1 number of banana to the search value too make it more accurate


def check_if_update():
    pass
 

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

def server_script():
    update_screen() 
    clientsocket, adress = server.accept()
    print(f"connection from {adress} has been established")
    clientsocket.send(bytes("accesed the server","utf-8"))
    data = clientsocket.recv(1024)
    data = data.decode("utf-8")
    if data == "Hello, server!":
        print("msg recv")


def draw():
    global setup_success
    if current_stage == -2:
        X_OFFSET = 500
        Y_OFFSET = 500
        Gui.screen.fill((255,255,255))
        create_center_text(DEFAULT_FONT,100,(64,224,208),MONITOR_MIDDLE[0],MONITOR_MIDDLE[1],"セットアップをしましょう")   
        continue_button_3.draw()
        if SERVER_PC == False:
            server_button.texture = pygame.image.load("images/Logos/off.png")           

        if SERVER_PC == True:
            server_button.texture = pygame.image.load("images/Logos/on.png")
        server_button.draw()
        update_screen() 
    if current_stage == -1:
        Gui.screen.fill((255,255,255))
        create_center_text(DEFAULT_FONT,80,(64,224,208),MONITOR_MIDDLE[0],100,"ファイルを選択してください")
        open_filexplorer_menu.draw()

        if setup_success[0] == True:
            Gui.screen.blit(check_box,(450,400))
        if setup_success[1] == True:
            Gui.screen.blit(check_box,(monitor_size[0] -850,400)) 
        if setup_success[0] == False:
            Gui.screen.blit(cross_box,(450,400))
        if setup_success[1] == False:
            Gui.screen.blit(cross_box,(monitor_size[0] -850,400))

        open_filexplorer_foods.draw()
        continue_button_3.draw()
        update_screen() 
        
    if current_stage == 0:
        #draw background
        Gui.screen.blit(BACKGROUND_IMG,(0,0))
        draw_welcome()
        Warikan_button.draw()
    if current_stage == 1:
        Gui.screen.fill((248, 248, 255))
        for item in frames:
            item.draw()
        if Warikan == True:
            warikan_look.draw()
    if current_stage == 2:
        Gui.screen.fill((248, 248, 255))
        for item in frames:
            if buying == item.name:
                Gui.screen.blit(item.fullsize_photo,(412,100))
                create_center_text(DEFAULT_FONT,100,(0,0,0),MONITOR_MIDDLE[0],750,buying)
                create_center_text(DEFAULT_FONT,50,(0,0,0),MONITOR_MIDDLE[0],850,item.price)
                banana_buy.draw()
        back_button.draw()
    if current_stage == 3:
        Gui.screen.blit(BACKGROUND_IMG,(0,0))
        background_2.draw()
        continue_button_2.draw()
        Gui.screen.blit(Table,(455,MONITOR_MIDDLE[1]-375))
    if current_stage == 4:
        success,img=cap.read()
        Gui.screen.fill((248, 248, 255))
        x = MONITOR_MIDDLE[0]
        y = MONITOR_MIDDLE[1]
        #Banana_detection_Whole_table()

        for person in eating_people:
            person.update_food(img,x,y)
            y += 100
        
        
def handle_button():
    global people,children,current_stage,frames,buying,Warikan,places,eating_people,setup_success,SERVER_PC,server,client_socket,foods_list

    X_OFFSET = 500
    Y_OFFSET = 500

    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    if current_stage == -2:
        current_stage = continue_button_3.check_clicks(current_stage,1)
        SERVER_PC = server_button.check_clicks(SERVER_PC,how_much=None,bool=True)


    if current_stage == -1:
        if setup_success[0] == True and setup_success[1] == True:
            current_stage = continue_button_3.check_clicks(current_stage,1)

        open_filexplorer_foods.check_clicks()
        open_filexplorer_menu.check_clicks()

        """
        ・理想のフレーム画像の大きさは375x300でそれに大きさを合わせるのはパフォーマンスを下げるからしていない
        ・理想のふるの大きさの画像の大きさは1096x559でそれに大きさを合わせるのはパフォーマンスを下げるからしていない
        """

        if SERVER_PC == False:         

            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(("SERVER IP", 45000))
            print(f"connected successfully")
        if SERVER_PC == True:

            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.bind((socket.gethostname(), 45000))
            server.listen(5)
            print(f"server started succesfully")

        if open_filexplorer_menu.clicked :
            #本当は：filedialog.askopenfilename(title="エクセルファイルを選択")　をする
            excel_file_name = prompt_file()
            menu_file = readexcel.read_menu(excel_file_name)
            for i in range(0,menu_file[1]):
                print(f"price:{menu_file[0]['値段'][i]} name:{menu_file[0]['品名'][i]} photo:{menu_file[0]['写真'][i]}")
                frames.append(buy_frame(100 + i * X_OFFSET, 100,(BUTTON_COLORS),str(menu_file[0]["値段"][i]),str(menu_file[0]["品名"][i]),str(menu_file[0]["写真"][i]),str(menu_file[0]["フルサイズ写真"][i])))
                foods_on_menu.update({str(menu_file[0]["品名"][i]): str(menu_file[0]["食べ物"][i])})
            setup_success[0] = True
            open_filexplorer_menu.clicked = False


        if open_filexplorer_foods.clicked:

            #本当は：filedialog.askopenfilename(title="エクセルファイルを選択")　をする
            excel_file_name = prompt_file()
            foods_on_list  = readexcel.read_menu(excel_file_name)
            for i in range(0,foods_on_list[1]):
                foods_list.update({str(foods_on_list[0]["食べ物"][i]): [ str(foods_on_list[0]["モデル"][i]) , str(foods_on_list[0]["クラス"][i]), str(foods_on_list[0]["値段"][i])]})
            setup_success[1] = True
            open_filexplorer_foods.clicked = False 
     
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
            frame.background.check_clicks() 
            if frame.background.clicked == True:
                buying =  str(frame.name)
                current_stage = 2
                print(current_stage)
        if Warikan == True:
            current_stage = warikan_look.check_clicks(current_stage,3)

    if current_stage == 2:
        banana_buy.check_clicks(bought,how_much="Banana Plate",bool=False,string=False,list=True)
        if banana_buy.clicked == True:
            current_stage = 1
            buying = None  
        banana_buy.clicked = False 
        back_button.check_clicks()
        if back_button.clicked:
            current_stage = 1
            back_button.clicked = False

    if current_stage == 3:
        for box in input_boxes:
            box.update()
            box.draw(Gui.screen)
        if mode == "heavy": 
            places = [input_box1.text ,[0,250,230,850], 
                    input_box2.text , [1166,1920,846,1080],
                    input_box3.text , [400,1016,846,1080], 
                    input_box4.text , [1166,1920,0,250], 
                    input_box5.text , [400,1016,0,250]]
        if mode == "light":
            places = [input_box1.text ,[0,84,77,283], 
                    input_box2.text , [382,640,276,360],
                    input_box3.text , [127,333,276,360], 
                    input_box4.text , [382,640,0,84], 
                    input_box5.text , [127,333,0,84]]    
#       eating_people = [input_box1.text, input_box2.text,input_box3.text, input_box4.text, input_box5.text]
        current_stage = continue_button_2.check_clicks(current_stage,-1)
        if continue_button_2.clicked:
            # Iterate through the places list and create person instances
            for i_key in range(0, 5):
                name = places[i_key * 2]
                area = places[i_key * 2 + 1]
                eating_people.append(person(name, area))
                print(name, area)

#背景動作



def pygame_background_functionts(testsubject=None,value_x=None,value_y=None):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if testsubject is not None:
                with open('test.txt', 'w') as f:
                    #f.write(f'Y is: {testsubject.y} X is: {testsubject.x} width is: {testsubject.w} height is: {testsubject.h}')
                    f.write(f'Y is: {value_y} X is: {value_x} ')
            top.destroy()
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



while True:
    
    #find plates
    pygame_background_functionts()
    if SERVER_PC == True:
        draw()
    if SERVER_PC == False:
        draw()    
        handle_button()
    #display computer vision onto screen
    mainClock.tick(30)



