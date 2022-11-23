import pygame, random, time, sys

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

label_pos = [(0,0), (0,0), (0,0), (0,0), (0,0), (0,0)]
ace_counter = [0, 0, 0, 0, 0, 0]
temp_val = [[],[],[],[],[],[]]
cal_val = [0, 0, 0, 0, 0, 0]
final_val = 0
card_object_list = []
playing = [0, True, True, True, True, True]

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
WHITE = (255,255,255)

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
        temp_pos_x = positions[temp_pos_x_1] + offset_vals[temp_pos_x_1] * (stack_size[self.pos] - 1) # Minus 1 because why not
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
            font = pygame.font.SysFont('none', 60)
            text = font.render(self.contents, 1, (0,0,0))
            win.blit(text, (self.x + (self.w/2 - text.get_width()/2), self.y + (self.h/2 - text.get_height()/2)))

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.w:
            if pos[1] > self.y and pos[1] < self.y + self.h:
                return True
            
        return False

def render_label(x, y, contents, colour, font_size, rot, win):
    font = pygame.font.SysFont('none', font_size) # Chosing the font and size
    temp_text = font.render(contents, True, colour) # Creating the font object
    rot_text = pygame.transform.rotate(temp_text, rot) # Rotating the text object
    win.blit(temp_text, (x, y)) # Blitting the rotated text

hitButton = Button(535, 535, 150, 50, "Hit", GREY)
standButton = Button(735, 535, 150, 50, "Stand", GREY)

def init_render():
    window.blit(felt_img, (0,0))
    hitButton.render_button(window, (0,0,0))
    standButton.render_button(window, (0,0,0))
    render_label(100, 100, str(cal_val[1]), WHITE, 60, 40, window)

def main_render():
    window.blit(felt_img, (0,0))
    for i in card_object_list:
        i.render_card()
    hitButton.render_button(window, (0,0,0))
    standButton.render_button(window, (0,0,0))

    render_label(positions[1] + 100, positions[2] - 103, str(cal_val[1]), WHITE, 60, 40, window)
    render_label(positions[3] + 100, positions[4] - 188, str(cal_val[2]), WHITE, 60, 40, window)
    render_label(positions[5] + 45, positions[6] - 225, str(cal_val[3]), WHITE, 60, 40, window)
    render_label(positions[7] + 45, positions[8] - 191, str(cal_val[4]), WHITE, 60, 40, window)
    render_label(positions[9] + 75, positions[10] - 103, str(cal_val[5]), WHITE, 60, 40, window)

    render_label(positions[1] + 100, positions[2] - 203, str(playing[1]), WHITE, 60, 40, window)
    render_label(positions[3] + 100, positions[4] - 288, str(playing[2]), WHITE, 60, 40, window)
    render_label(positions[5] + 45, positions[6] - 325, str(playing[3]), WHITE, 60, 40, window)
    render_label(positions[7] + 45, positions[8] - 291, str(playing[4]), WHITE, 60, 40, window)
    render_label(positions[9] + 75, positions[10] - 203, str(playing[5]), WHITE, 60, 40, window)

# window.blit(felt_img, (0,0))

init_render()

def calc_vals():
    global final_val, ace_counter, playing, dealing_pos
    
    for i, j in enumerate(temp_val): # Enumerate is used to have both the index and actual value pulled from the list
        for k in j:
            if k == "a":
                adding_val = 11
                ace_counter[i] += 1
            else:
                adding_val = int(k)
            final_val += adding_val
        
        # if final_val > 21 and ace_counter[i] > 0: # Checking that the hand has an ace in it
        #     pass
            # Reducing the hand value by 10 and reducing the number of valid aces (Aces that haven't been used) by 1

        while ace_counter[i] > 0 and final_val > 21:
            final_val -= 10 
            ace_counter[i] -= 1


        if final_val > 21 and ace_counter[i] == 0:
            print(dealing_pos - 1)
            playing[dealing_pos] = False

            if dealing_pos == 5:
                dealing_pos = 1
            else:
                dealing_pos += 1
        
        cal_val[i] = final_val
        final_val = 0

def dealer_play():
    print("Dealer play")
    pass

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

                
                print(dealing_pos)
                if playing[dealing_pos] == True:

                    print("nee")

                    random_card = random.choice(card_list) # Change to pop
                    tempcard = Card(random_card, dealing_pos)
                    card_object_list.append(tempcard)

                    
                    stack_size[dealing_pos] += 1
                    
                    temp_face_val = random_card[0]
                    if temp_face_val.lower() in ('j', 'q', 'k', 't'): # Thanks Drew, Very cool
                        temp_val[dealing_pos].append("10")
                    else:
                        temp_val[dealing_pos].append(temp_face_val)

                    tempcard = ""

                    calc_vals() # Sorry? for what? jank? probs?

                    main_render()
                
                else:
                    print("problem")  
                    if dealing_pos == 5:
                        dealing_pos = 1
                    else:
                        dealing_pos += 1

        if event.type == pygame.MOUSEBUTTONDOWN:
            if standButton.isOver(m_pos):
                playing[dealing_pos] = False
                if dealing_pos == 5:
                    dealing_pos = 1
                else:
                    dealing_pos += 1
                print("dense")

                main_render()
        
        # if event.type == pygame.MOUSEMOTION:
        #     if hitButton.isOver(m_pos):
        #         hitButton.colour = HOVER_GREY
        #     else:
        #         hitButton.colour = GREY
        #     if standButton.isOver(m_pos):
        #         standButton.colour = HOVER_GREY
        
        if playing == [0, False, False, False, False, False]:
            dealer_play()
            playing = [0, False, False, False, False, False]
        
    pygame.display.update()
    clock.tick(60)
