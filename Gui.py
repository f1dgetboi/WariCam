import pygame, sys
from pygame.locals import *
import cv2
#initialise everything here
pygame.init()
monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
mainClock = pygame.time.Clock()
DEFAULT_FONT = r"C:\Users\akiso\Desktop\Gui\fonts\Zen_Old_Mincho\ZenOldMincho-Medium.ttf"

def create_window(width, height,background_colour,caption):
    global screen, window_colour,WIDTH,HEIGHT
    WIDTH = width
    HEIGHT = height
    window_colour = background_colour
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF |pygame.FULLSCREEN)
    pygame.display.set_caption(str(caption))
    screen.fill(background_colour)
    pygame.display.flip()

def create_text(font,fontsize,color,x,y,text):
    font = pygame.font.Font(font, fontsize)
    text = font.render(text, True, color)
    screen.blit(text, (x,y))

def BGR_TO_RGB(img):
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    height, width, _ = rgb_img.shape
    # Create a Pygame surface from the pixel buffer
    pygame_image = pygame.image.frombuffer(rgb_img.flatten(), (width, height), 'RGB')

    return pygame_image

def resize_image(image, width, height):
    resized_image = pygame.transform.scale(image, (width, height))
    return resized_image

class GuiObject:
    def __init__(self,w,h,x,y,color,texture=None,visible=True,stroke=False,stroke_width=5,stroke_color=(255,255,255),rounded=False,roundness=3,hollow=False,background=False):
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
    def draw(self):
        if self.visible == True:

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
    def __init__(self,w,h,x,y,color,texture=None,visible=True,stroke=True,stroke_width=5,stroke_color=(255,255,255),rounded=False,roundness=3,hollow=False,background=False,text=None,fontsize=None,text_offset_x=None,text_offset_y=None):
        super().__init__(w, h, x, y, color, texture, visible, stroke, stroke_width, stroke_color, rounded, roundness, hollow, background)
        self.hovered = False
        self.clicked = False
        self.rect = pygame.Rect((self.x,self.y),(self.w, self.h))
        self.text = text
        self.fontsize = fontsize
        self.text_offset_x = text_offset_x
        self.text_offset_y = text_offset_y

    def draw(self):
        super().draw()
        if self.text is not None:
            create_text(DEFAULT_FONT,self.fontsize,(0,0,0),self.x + self.text_offset_x,self.y + self.text_offset_y,self.text)

    def check_clicks(self,value=None,how_much=None):
        pos = pygame.mouse.get_pos()

        self.color = self.original_color
        if self.rect.collidepoint(pygame.mouse.get_pos()): 

            self.color = self.hoverd_color
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND) 
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                if value is not None:
                    value =  value + how_much
            
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
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
    pygame.display.update()
