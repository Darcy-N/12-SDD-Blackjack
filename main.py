# Imports

import os, sys, pygame
from pygame.locals import *
from random import randint

# Constants

WINDOW_SIZE = WIDTH, HEIGHT = 1440, 900
DIRPATH = os.path.dirname(os.path.realpath(__file__))
ASSET_FOLDER = os.path.join(DIRPATH, 'assets')
CARD_FOLDER = os.path.join(ASSET_FOLDER, 'cards')
felt_img = pygame.image.load(os.path.join(ASSET_FOLDER, 'felt.png'))

class Card:
    ''' Card class, handles everything card related '''

    def __init__(self, image, value):
        self.image = image
        self.value = value
        self.soft_total = None

    def is_ace(self, total):
        if total.total < 11:
            self.soft_total = True
            total.update(11)
        elif total.total >= 11:
            total.update(1)
        elif total.total > 21 and self.soft_total:
            self.soft_total = False
            total.update(-9)


class Deck:
    ''' Handles the deck '''

    def __init__(self):
        # 0: clubs 1: diamonds  2: hearts 3: spades
        self.cards = {0: {}, 1: {}, 2: {}, 3: {}}
        # values are assigned to their position in the created deck
        # ace is at position 0, deal with it in play.calculate_hands
        self.values = [False, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]

    def create(self):
        suits = ["Clubs ", "Diamond ", "Hearts ", "Spades "]
        # populate self cards with the appropriate images
        for suit in range(4):
            for card in range(1, 14):
                self.cards[suit][card] = Card(
                    pygame.image.load(
                        'assets/' + str(suits[suit]) + str(card) + '.png'),
                    self.values[card - 1]
                )

class Total:
    ''' Hand values class '''

    def __init__(self):
        self.total = 0

    def update(self, value):
        self.total += value

class Play:
    ''' Pretty much all other constants, also incudes functions used by the game '''

    def __init__(self):
        # hands
        self.player_hand = []
        self.dealer_hand = []
        self.cpu1_hand = []
        self.cpu2_hand = []

        # gui
        self.player_text = "Player: "
        self.dealer_text = "Dealer: "
        self.cpu1_text = "CPU 1: "
        self.cpu2_text = "CPU 2: "
        self.player_text_x = 625
        self.player_text_y = 300
        self.dealer_text_x = 390
        self.dealer_text_y = 115
        self.cpu1_x = 335
        self.cpu1_y = 300
        self.cpu2_x = 935
        self.cpu2_y = 300

        self.money = 1000
        self.bet = 0

        # Key images

        self.display_keys = [
            pygame.image.load("assets/H_key.png"),
            pygame.image.load("assets/S_key.png"),
            pygame.image.load("assets/R_key.png"),
            pygame.image.load("assets/C_key.png"),
            pygame.image.load("assets/D_key.png"),
        ]

        self.betting_keys = [
            pygame.image.load("assets/Up_key.png"),
            pygame.image.load("assets/Down_key.png")
        ]

        self.display_keys_text = {
            0: "Hit",
            1: "Stand",
            2: "New Game",
            3: "Confirm bet",
            4: "Double"
        }
        
        self.betting_keys_text = {
            0: "Increase bet (100)",
            1: "Decrease bet (100)"
        }

        self.message_log = [" ", " ", " ", " ", ]
        self.message_log_text = {
            0: "Player wins",
            1: "Dealer wins, game over",
            2: "Game is a tie",
            3: "Player stays",
            4: "Player busts, game over",
            5: "Dealer busts, Player wins",
            6: "Player hits",
            7: "Please place bets",
            8: "Player doubled",
            9: "Not enough money"
        }

        # action
        self.player = True
        self.game_over = False
        self.acc_bet = True # Accepting bets

    # calcualations and actions

    def get_card(self, hand, number=1):
        for get_card in range(number):
            suit, card = randint(0, 3), randint(1, 13) # change to pop card from a deck
            hand.append(game.deck.cards[suit][card])

        self.calculate_hands(self.player_hand, player)
        self.calculate_hands(self.dealer_hand, dealer)
        self.calculate_hands(self.cpu1_hand, cpu1)
        self.calculate_hands(self.cpu2_hand, cpu2)

    # Calc vals

    def calculate_hands(self, hand, total):
        total.total = 0
        for card in range(len(hand)):
            # cards
            if hand[card].value:
                total.update(hand[card].value)
            # aces
            else: pass
        for card in range(len(hand)):
            if not hand[card].value:
                hand[card].is_ace(total)

        # player bust

        if hand == self.player_hand and player.total > 21:
            self.player_bust()
        if self.game_over:
            # dealer bust
            if hand == self.dealer_hand and dealer.total > 21:
                play.message_log.insert(0, play.message_log_text[5])
                play.message_log.pop()
                play.money += play.bet * 1.5 # Pay 2:3
                play.bet = 0
            # tie
            if hand == self.dealer_hand and player.total == dealer.total:
                play.message_log.insert(0, play.message_log_text[2])
                play.message_log.pop()
                play.money += play.bet
                play.bet = 0
            # player win
            elif hand == self.dealer_hand and player.total > dealer.total:
                play.message_log.insert(0, play.message_log_text[0])
                play.message_log.pop()
                play.money += play.bet * 1.5 # Pay 2:3
                play.bet = 0
            # dealer win
            elif hand == self.dealer_hand and dealer.total > player.total and dealer.total <= 21:
                play.message_log.insert(0, play.message_log_text[1])
                play.message_log.pop()

    def player_bust(self):
        self.player = False
        play.message_log.insert(0, play.message_log_text[4])
        play.message_log.pop()

    def player_stay(self):
        self.player = False
        self.dealer_action()

    def dealer_action(self):
        while dealer.total < 17:
            self.get_card(self.dealer_hand)
        self.game_over = True
        self.calculate_hands(self.player_hand, player)
        self.calculate_hands(self.dealer_hand, dealer)
    
    def cpu_action(self): # ccpu = current cpu
        if self.player == False:
            while cpu1.total < 17:
                self.get_card(self.cpu1_hand)
                self.get_card(self.cpu2_hand)
        else:
            if cpu1.total < 17:
                self.get_card(self.cpu1_hand)
            if cpu2.total < 16:
                self.get_card(self.cpu2_hand)
        # self.calculate_hands(ccpu, ctotal) 

    # gui

    def display_hands(self):
        # Player
        x, y = 670, 80
        for card in range(len(self.dealer_hand)):
            game.screen.blit(self.dealer_hand[card].image, (x, y))
            x += 40
            y += 15
        # Dealer
        x, y = 670, 380
        for card in range(len(self.player_hand)):
            game.screen.blit(self.player_hand[card].image, (x, y))
            x += 40
            y += 15
        x, y = 375, 380
        # CPU1
        for card in range(len(self.cpu1_hand)):
            game.screen.blit(self.cpu1_hand[card].image, (x, y))
            x += 40
            y += 15
        # CPU2
        x, y = 975, 380
        for card in range(len(self.cpu2_hand)):
            game.screen.blit(self.cpu2_hand[card].image, (x, y))
            x += 40
            y += 15
        # totals
        game.screen.blit(game.render_font(self.player_text + str(player.total)), (self.player_text_x, self.player_text_y))
        game.screen.blit(game.render_font(self.dealer_text + str(dealer.total)), (self.dealer_text_x, self.dealer_text_y))
        game.screen.blit(game.render_font(self.cpu1_text + str(cpu1.total)), (self.cpu1_x, self.cpu1_y))
        game.screen.blit(game.render_font(self.cpu2_text + str(cpu2.total)), (self.cpu2_x, self.cpu2_y))

        # Bet amount text

        game.screen.blit(game.render_font("Bet ammount:" + str(self.bet)), (900, 710))
        game.screen.blit(game.render_font("Money left:" + str(self.money)), (900, 765))
        game.screen.blit(game.render_font("Betting open:" + str(self.acc_bet)), (900, 820))


    def display_gui(self):

        # Controls GUI

        x, y = 45, 600
        for key in range(len(self.display_keys)):
            game.screen.blit(self.display_keys[key], (x, y))
            y += 55

        x, y = 105, 600
        for text in self.display_keys_text:
            game.screen.blit(game.render_font(
                self.display_keys_text[text]), (x, y))
            y += 55

        # Betting GUI

        x, y = 1300, 600
        for key in range(len(self.betting_keys)):
            game.screen.blit(self.betting_keys[key], (x, y))
            y += 55

        x, y = 900, 600
        for text in self.betting_keys_text:
            game.screen.blit(game.render_font(
                self.betting_keys_text[text]), (x, y))
            y += 55

        # Game messages GUI

        x, y = 350, 695
        for message in range(len(self.message_log)):
            game.screen.blit(game.render_font(
                self.message_log[message]), (x, y))
            y += 55

    # initialisation and loop

    def initialise(self):
        self.get_card(self.player_hand, 2)
        self.get_card(self.dealer_hand, 1)
        self.get_card(self.cpu1_hand, 2)
        self.get_card(self.cpu2_hand, 2)

    def loop(self):
        game.get_input()
        self.display_gui()
        self.display_hands()
        pygame.display.flip()

    def reset(self):
        # reset game to 0
        self.player_hand = []
        self.dealer_hand = []
        self.cpu1_hand = []
        self.cpu2_hand = []
        player.total = 0
        dealer.total = 0
        cpu1.total = 0
        cpu2.total = 0
        self.bet = 0

        self.message_log = [" ", " ", " ", " ", ]
        self.player = True
        self.game_over = False

class Game:
    ''' Game object handles all of the game related processes '''

    def __init__(self):
        # initialise pygame and set window values
        pygame.init()
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption("Blackjack")
        self.font = pygame.font.Font('assets/clacon.ttf', 50)
        # assign cards to images
        self.deck = Deck()
        self.deck.create()

        # text and settings for main menu
        self.main_menu = True
        self.menu_text = {
            0: "Blackjack",
            1: " ",
            2: "New Game",
            3: "How to play",
            4: "Exit Game",
        }
        self.menu_selector = '>'
        self.menu_selector_x = 475
        self.menu_selector_y = 490

        # how to play
        self.how_to_play = False
        self.how_to_play_text = {
            0: "How to play Blackjack - simplified",
            1: " ",
            2: "Beat the dealer's hand without going over 21.",
            3: "'23465789' are worth their face value.",
            4: "'JQK' = 10, 'A' = 1, 11 depending on best hand.",
            5: "Each player starts with two cards.",
            6: "HIT gets another card, STAY keeps the hand you have.",
            7: "If you go over 21 you BUST, and the dealer wins.",
            8: "2 card total of 21 equals BLACKJACK.",
            9: "Dealer plays until their cards total 17 or higher.",
        }

        # new game
        self.new_game = False

    # handle any player key presses
    def get_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                # back to main menu
                if event.key == pygame.K_ESCAPE:
                    if not self.main_menu:
                        self.main_menu = True
                        self.new_game = False
                        self.how_to_play = False

                # main menu
                if self.main_menu:
                    if event.key == pygame.K_DOWN:
                        if self.menu_selector_y < 580:
                            self.menu_selector_y += 45
                    if event.key == pygame.K_UP:
                        if self.menu_selector_y > 490:
                            self.menu_selector_y -= 45

                    if event.key == pygame.K_RETURN:
                        if self.menu_selector_y == 490:
                            self.main_menu = False
                            self.new_game = True
                            self.how_to_play = False
                            play.reset()
                        if self.menu_selector_y == 535:
                            self.main_menu = False
                            self.new_game = False
                            self.how_to_play = True
                        if self.menu_selector_y == 580:
                            pygame.quit()
                            sys.exit("Thanks for playing!")

                # while possible to take action (i.e ingame)

                if play.player:
                    if event.key == pygame.K_h and play.acc_bet == False:
                        play.message_log.insert(0, play.message_log_text[6])
                        play.message_log.pop()
                        play.get_card(play.player_hand)
                        play.cpu_action()
                    if event.key == pygame.K_s and play.acc_bet == False:
                        play.message_log.insert(0, play.message_log_text[3])
                        play.message_log.pop()
                        play.cpu_action()
                        play.player_stay()
                    if event.key == pygame.K_UP and play.acc_bet == True:
                        if play.money >= 100:
                            play.bet += 100
                            play.money -= 100
                        else: pass
                    if event.key == pygame.K_DOWN and play.acc_bet == True:
                        if play.bet >= 100:
                            play.bet -= 100
                            play.money += 100
                    if event.key == pygame.K_c:
                        if play.bet > 0:
                            play.initialise()
                            play.acc_bet = False
                        else: play.message_log.insert(0, play.message_log_text[7])
                    if event.key == pygame.K_d:
                        if play.money >= play.bet:
                            play.money -= play.bet
                            play.bet *= 2
                            play.get_card(play.player_hand)
                            play.player_stay()
                            play.message_log.insert(0, play.message_log_text[8])

                        else: play.message_log.insert(0, play.message_log_text[9])

                # reset
                if event.key == pygame.K_r:
                    play.acc_bet = True
                    play.reset()

    # render all game objects
    def render(self):
        # render main menu
        if self.main_menu:
            menu_text_x, menu_text_y = 500, 400
            for text in self.menu_text:
                self.screen.blit(self.render_font(
                    self.menu_text[text]), (menu_text_x, menu_text_y))
                menu_text_y += 45
            self.screen.blit(self.render_font(self.menu_selector),
                             (self.menu_selector_x, self.menu_selector_y))

        # render how to play
        if self.how_to_play:
            x, y = 45, 45
            for text in self.how_to_play_text:
                self.screen.blit(self.render_font(
                    self.how_to_play_text[text]), (x, y))
                y += 45
            # display cards
            x, y = 45, 600
            for suit in range(0, 2):
                for card in self.deck.cards[suit]:
                    self.screen.blit(self.deck.cards[suit][card].image, (x, y))
                    x += 40
            x, y = 45, 700
            for suit in range(2, 4):
                for card in self.deck.cards[suit]:
                    self.screen.blit(self.deck.cards[suit][card].image, (x, y))
                    x += 40

    # function that will render font to blit
    def render_font(self, text):
        text_to_render = self.font.render(text, True, (255, 255, 255))
        return text_to_render

    # main game loop
    def loop(self):
        while True:
            if self.main_menu == False and self.how_to_play == False:
                self.screen.blit(felt_img, (0,0))
            else:
                self.screen.fill((0,128,0))

            self.render()
            self.get_input()

            if self.new_game:
                play.loop()

            pygame.display.flip()


if __name__ == "__main__":
    game = Game()
    play = Play()
    player = Total()
    dealer = Total()
    cpu1 = Total()
    cpu2 = Total()
    game.loop()
