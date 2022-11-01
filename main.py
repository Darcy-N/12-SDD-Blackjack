import pygame
import random
import time

from func import *

clear()

WINDOW_DIM = WINDOW_WIDTH, WINDOW_HEIGHT = 1440, 900
CARD_DIM = CARD_DIM_X, CARD_DIM_Y =  110, 150

rotations = [0, -30, -15, 0, 15, 30]
positions = [0, 195, 560, 413, 645, 664, 682, 877, 648, 1070, 560] # What is THIS ?
#           [0, 1,x  1,y  2,x  2,y  3,x  3,y  4,x  4,y  5,x  5,y]
#           [0, 1    2    3    4    5    6    7    8    9    10]
offset_vals = [0, 15, 30, 20, 25, 25, 25, 30, 10, 30, 15]
#             [0, 1x  1y  2x  2y  3x  3y  4x  4y  5x  5y]
#             [0, 1,  2,  3,  4,  5,  6,  7,  8,  9,  10]
stack_size = [0,0,0,0,0,0] 
pos_val = [0, 0, 0, 0, 0, 0]

temp_val = [[],[],[],[],[],[]]

cal_val = [0, 0, 0, 0, 0, 0]

card_object_list = []

card_count = 0

pygame.init()
window = pygame.display.set_mode(WINDOW_DIM, 0, 32)
pygame.display.set_caption('Blackjack')
clock = pygame.time.Clock()

DIRPATH = os.path.dirname(os.path.realpath(__file__))
ASSET_FOLDER = os.path.join(DIRPATH, 'assets')
CARD_FOLDER = os.path.join(ASSET_FOLDER, 'cards')

felt_img = pygame.image.load(os.path.join(ASSET_FOLDER, 'felt.png'))

card_list = card_loader(CARD_FOLDER)

dealing_pos = 0

GREY = (66,66,66)
HOVER_GREY = (99,99,99)

def init_play():
    global dealing_pos
    for i in range(10):
        if dealing_pos == 5:
            dealing_pos = 1
        else:
            dealing_pos += 1
    
class Card:

    def __init__(self, face_val, pos):
        self.face_val = face_val
        self.pos = pos
    
    def render_card(self):

        # Calculating the position of the card, checking the size of the stack, and multiplying that value by an offset

        temp_pos_x_1 = self.pos * 2 - 1 # Done because of the weird way I store the values in my lists
        temp_pos_y_1 = self.pos * 2
        temp_pos_x = positions[temp_pos_x_1] + offset_vals[temp_pos_x_1] * (stack_size[self.pos] - 1) # Negative 1 because why not
        temp_pos_y = positions[temp_pos_y_1] + offset_vals[temp_pos_y_1] * (stack_size[self.pos] - 1)
        temp_pos = (temp_pos_x, temp_pos_y)

        # Loading the image, scaling it to correct size and rotating to fit the slot

        load_img = pygame.image.load(os.path.join(CARD_FOLDER, self.face_val))
        scaled_card = pygame.transform.scale(load_img, CARD_DIM)
        final_render_card = pygame.transform.rotate(scaled_card, rotations[self.pos])
        window.blit(final_render_card, temp_pos)

        

class Button:
    def __init__(self, x, y, w, h, contents, colour):
        self.x = x
        self.y = y
        self.w = w                  # Width
        self.h = h                  # Height
        self.contents = contents    # Message in the button
        self.colour = colour

    def render_button(self,win,outline=None):
        if outline:
            pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.w+4,self.h+4),0)
            
        pygame.draw.rect(win, self.colour, (self.x,self.y,self.w,self.h),0)
        
        if self.contents != '':
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(self.contents, 1, (0,0,0))
            win.blit(text, (self.x + (self.w/2 - text.get_width()/2), self.y + (self.h/2 - text.get_height()/2)))

    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.w:
            if pos[1] > self.y and pos[1] < self.y + self.h:
                return True
            
        return False

hitButton = Button(50, 800, 100, 50, "Hit", GREY)

def update_render():
    for i in card_object_list:
        i.render_card()

def main_render():
    hitButton.render_button(window, (0,0,0))

def init_render():
    window.blit(felt_img, (0,0))
    hitButton.render_button(window, (0,0,0))

init_render()

while True:
    
    for event in pygame.event.get():
        
        m_pos = pygame.mouse.get_pos()

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:

            if event.key == ord('p'):
                pass

            if event.key == ord('l'):
                init_play()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if hitButton.isOver(m_pos):

                if dealing_pos == 5:
                    dealing_pos = 1
                else:
                    dealing_pos += 1

                random_card = random.choice(card_list)
                tempcard = Card(random_card, dealing_pos)
                card_object_list.append(tempcard)
                
                
                stack_size[dealing_pos] += 1
                
                temp_face_val = random_card[0]
                print(temp_face_val)
                if temp_face_val.lower() == "j" or temp_face_val.lower() == "q" or temp_face_val.lower() == "k" or temp_face_val.lower() == "t":
                    temp_val[dealing_pos].append("10")
                else:
                    temp_val[dealing_pos].append(temp_face_val)

                print(temp_val)

                tempcard = ""

                update_render()
        
        if event.type == pygame.MOUSEMOTION:
            if hitButton.isOver(m_pos):
                hitButton.colour = HOVER_GREY
            else:
                hitButton.colour = GREY
        

    main_render()
    pygame.display.update()
    clock.tick(60)

