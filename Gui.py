import pygame, sys
from pygame.locals import *
import cv2
#initialise
pygame.init()
monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
mainClock = pygame.time.Clock()
DEFAULT_FONT = r"C:\Users\akiso\Desktop\Gui\fonts\Zen_Old_Mincho\ZenOldMincho-Medium.ttf"

#ウィンドウの作成

def create_window(width, height,background_colour,caption):
    global screen, window_colour,WIDTH,HEIGHT,display
    WIDTH = width
    HEIGHT = height
    window_colour = background_colour
    display = pygame.display.set_mode((WIDTH, HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF |pygame.FULLSCREEN)
    screen = pygame.Surface((width, height))
    pygame.display.set_caption(str(caption))
    #screen.fill(background_colour)
    pygame.display.flip()

#テキストの描画
def create_text(font,fontsize,color,x,y,text):
    font = pygame.font.Font(font, fontsize)
    text = font.render(text, True, color)
    screen.blit(text, (x,y))

def create_center_text(font,fontsize,color,x,y,text):
    font = pygame.font.Font(font, fontsize)
    text = font.render(text, True, color)
    text_rect = text.get_rect(center=(x, y))
    screen.blit(text, text_rect)

#OPENCVのIMGをPYGAMEのIMGに転換

def BGR_TO_RGB(img):
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    height, width, _ = rgb_img.shape
    # Create a Pygame surface from the pixel buffer
    pygame_image = pygame.image.frombuffer(rgb_img.flatten(), (width, height), 'RGB')

    return pygame_image

#写真の大きさを変える関数

def resize_image(image, width, height):
    resized_image = pygame.transform.scale(image, (width, height))
    return resized_image

def create_drop_shadow(rect, size):
    shadow_surface = pygame.Surface((rect.width + size, rect.height + size ))
    shadow_surface.set_alpha(2)
    for i in range(-5, 4):
        for j in range(-5, 4):
            screen.blit(shadow_surface, (rect.x + i * size/3 , rect.y + j * size/3))
        

#他はオブジェクトのコード
class GuiObject:
    def __init__(self,w,h,x,y,color,texture=None,visible=True,stroke=False,stroke_width=5,stroke_color=(255,255,255),rounded=False,roundness=3,hollow=False,background=False,Shadow=False,shadow_size=None,):
        self.w = w
        self.h = h
        self.x = x
        self.y = y
        self.color = color
        self.original_color = color
        self.visible = visible
        self.stroke = stroke
        self.stroke_width = stroke_width
        self.stroke_color = stroke_color
        self.rounded = rounded
        self.roundness = roundness
        self.hollow = hollow
        if texture is not None:
            self.texture = pygame.image.load(texture)
            self.texture = resize_image(self.texture,self.w,self.h)
            print("working")
        else:
            self.texture = None
        self.clicked_color = (self.color[0]* 1.2,self.color[1]* 1.2,self.color[2]* 1.2)
        self.hoverd_color = (self.color[0]* 0.8,self.color[1]* 0.8,self.color[2]* 0.8)
        self.background = background
        self.shadow = Shadow
        self.rect = pygame.Rect((self.x,self.y),(self.w, self.h))
        self.shadow_size = shadow_size
        
    def draw(self):
        if self.visible == True:
            if self.shadow:
                create_drop_shadow(self.rect, self.shadow_size)  
            if self.rounded:   
                if self.stroke:

                    pygame.draw.rect(screen, self.stroke_color,((self.x - self.stroke_width,self.y - self.stroke_width),(self.w + self.stroke_width *2, self.h + self.stroke_width *2)),0,self.roundness)
                    
                if self.texture is not None:
                    if self.background:                   
                        pygame.draw.rect(screen, self.color,((self.x,self.y),(self.w, self.h)),0,self.roundness)
                    screen.blit(self.texture,(self.x,self.y))    
                elif self.texture is None:
                    pygame.draw.rect(screen, self.color,((self.x,self.y),(self.w, self.h)),0,self.roundness)    
                
            else:

                if self.stroke:
                    pygame.draw.rect(screen, self.stroke_color,((self.x - self.stroke_width,self.y - self.stroke_width),(self.w + self.stroke_width *2, self.h + self.stroke_width *2)),int(self.hollow))
                if self.texture is not None:
                    if self.background:
                        pygame.draw.rect(screen, self.color,((self.x,self.y),(self.w, self.h)),int(self.hollow))
                    screen.blit(self.texture,(self.x,self.y))
                elif self.texture is None:
                    pygame.draw.rect(screen, self.color,((self.x,self.y),(self.w, self.h)),int(self.hollow))

class Button(GuiObject):
    def __init__(self,w,h,x,y,color,texture=None,visible=True,stroke=True,stroke_width=5,stroke_color=(255,255,255),rounded=False,roundness=3,hollow=False,background=False,text=None,fontsize=None,text_offset_x=None,text_offset_y=None,Shadow=False,shadow_size=None):
        super().__init__(w, h, x, y, color, texture, visible, stroke, stroke_width, stroke_color, rounded, roundness, hollow, background,Shadow,shadow_size)
        self.hovered = False
        self.clicked = False
        self.rect = pygame.Rect((self.x,self.y),(self.w, self.h))
        self.text = text
        self.fontsize = fontsize
        self.text_offset_x = text_offset_x
        self.text_offset_y = text_offset_y
        self.changed = False
    def draw(self):
        super().draw()
        if self.text is not None:
            create_text(DEFAULT_FONT,self.fontsize,(0,0,0),self.x + self.text_offset_x,self.y + self.text_offset_y,self.text)

    def check_clicks(self,value=None,how_much=None,bool=False,string=False,list=False):
        pos = pygame.mouse.get_pos()

        self.color = self.original_color
        if self.rect.collidepoint(pygame.mouse.get_pos()): 

            self.color = self.hoverd_color
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND) 
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True                
                if value is not None:
                    if not bool:
                        if string:
                            value = how_much
                        else:
                            if list:
                                value.append(how_much)
                            else:                            
                                value =  value + how_much
                    else:
                        if value == True and self.changed == False:
                            value = False
                            self.changed = True
                        if value == False and self.changed == False:
                            value = True
            
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
            self.changed = False
        return value

            
                            
class TextBox():
    def __init__(self,w,h,x,y,color,text,fontsize,text_offset_x=0,text_offset_y=0,visible=True,stroke=False,stroke_width=5,stroke_color=(255,255,255),rounded=False,roundness=3,hollow=False):
        self.w = w
        self.h = h
        self.x = x
        self.y = y
        self.color = color
        self.original_color = color
        self.visible = visible
        self.stroke = stroke
        self.stroke_width = stroke_width
        self.stroke_color = stroke_color
        self.rounded = rounded
        self.roundness = roundness
        self.hollow = hollow
        self.text = text
        self.fontsize = fontsize
        self.text_offset_x = text_offset_x
        self.text_offset_y = text_offset_y

    def draw(self):

        if self.visible == True:

            if self.rounded:   

                if self.stroke:
                    pygame.draw.rect(screen, self.stroke_color,((self.x - self.stroke_width,self.y - self.stroke_width),(self.w + self.stroke_width *2, self.h + self.stroke_width *2)),0,self.roundness)
                pygame.draw.rect(screen, self.color,((self.x,self.y),(self.w, self.h)),0,self.roundness)    
                create_text(DEFAULT_FONT,self.fontsize,(0,0,0),self.x + self.text_offset_x,self.y + self.text_offset_y,self.text)
            else:

                if self.stroke:
                    pygame.draw.rect(screen, self.stroke_color,((self.x - self.stroke_width,self.y - self.stroke_width),(self.w + self.stroke_width *2, self.h + self.stroke_width *2)),int(self.hollow))
                pygame.draw.rect(screen, self.color,((self.x,self.y),(self.w, self.h)),int(self.hollow))
                create_text(DEFAULT_FONT,self.fontsize,(0,0,0),self.x + self.text_offset_x,self.y + self.text_offset_y,self.text)

class buy_frame():
    def __init__(self,x,y,color,price,name,photo):
        self.name= name
        self.width = 400
        self.height = 400
        self.x = x
        self.y = y
        self.color = color
        self.price = price
        self.name = name
        self.photo = self.texture = pygame.image.load(photo)
        self.background = Button(self.width,self.height,self.x,self.y,self.color)
        self.background.hoverd_color = self.color
    def draw(self):
        self.background.shadow = False
        if self.background.rect.collidepoint(pygame.mouse.get_pos()): 
            self.background.shadow = True
            self.background.shadow_size = 10
        self.background.rounded = True
        self.background.roundness = 10
        self.background.draw()
        screen.blit(self.photo,(self.x + 13 ,self.y + 10))
        create_center_text(DEFAULT_FONT,50,(0,0,0),self.x + self.width /2  ,self.y + self.height- 60 ,self.name)
        create_center_text(DEFAULT_FONT,30,(100,100,100),self.x + self.width /2 ,self.y + self.height- 17 ,self.price)

COLOR_ACTIVE = (10,10,10)
COLOR_INACTIVE = (100,100,100)

class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface =  pygame.font.Font(DEFAULT_FONT,32).render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:

            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface =  pygame.font.Font(DEFAULT_FONT,32).render(self.text, True, self.color)

    def update(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM)      
        width = max(150, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        pygame.draw.rect(screen, (255,255,255), self.rect, 0)
        pygame.draw.rect(screen, self.color, self.rect, 5)
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y-5))

