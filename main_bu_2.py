import sys, random
import pygame




#   CONSTANTS
#colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


#sizes
SCREEN_WIDTH = 750
SCREEN_HEIGHT = 750
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

CARD_HEIGHT = 50
CARD_WIDTH = int((CARD_HEIGHT/3) * 2)
CARD_SIZE = (CARD_WIDTH, CARD_HEIGHT)

PLAYER_FIELD_WIDTH = 200
PLAYER_FIELD_HEIGHT = 200
PLAYER_FIELD_SIZE = (PLAYER_FIELD_WIDTH, PLAYER_FIELD_HEIGHT)

DEFAULT_FONT_SIZE = 20
DEFAULT_FONT = 'arial.ttf'


#other
FPS = 30




#   PYGAME CONFIGURATION
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(SCREEN_SIZE)
screen_rect = screen.get_rect()




#   RESOURCE LOADING
#font
font_small = pygame.font.Font(DEFAULT_FONT, DEFAULT_FONT_SIZE - 10)
font_default = pygame.font.Font(DEFAULT_FONT, DEFAULT_FONT_SIZE)
font_big = pygame.font.Font(DEFAULT_FONT, DEFAULT_FONT_SIZE + 10)


#cards
deck = []
colors = ['red', 'green', 'blue', 'yellow']
colored_specials = ['+2', 'reverse', 'skip']
black_specials = ['+4', 'wildcard']
for color in colors:
    for i in range(10):
        card = pygame.image.load("images/" + color + "_" + str(i) + ".png").convert_alpha()
        card = pygame.transform.scale(card, CARD_SIZE)
        deck.append([color, str(i), card, card.get_rect()])

    for i in range(1, 10):
        card = pygame.image.load("images/" + color + "_" + str(i) + ".png").convert_alpha()
        card = pygame.transform.scale(card, CARD_SIZE)
        deck.append([color, str(i), card, card.get_rect()])

    for special in colored_specials:
        card = pygame.image.load("images/" + color + "_" + special + ".png").convert_alpha()
        card = pygame.transform.scale(card, CARD_SIZE)
        deck.append([color, special, card, card.get_rect()])

for special in black_specials:
    for i in range(4):
        card = pygame.image.load("images/black_" + special + ".png").convert_alpha()
        card = pygame.transform.scale(card, CARD_SIZE)
        deck.append(['black', special, card, card.get_rect()])

red_card = pygame.image.load("images/" + 'red' + ".png").convert_alpha()
red_card = pygame.transform.scale(red_card, CARD_SIZE)
green_card = pygame.image.load("images/" + 'green' + ".png").convert_alpha()
green_card = pygame.transform.scale(green_card, CARD_SIZE)
blue_card = pygame.image.load("images/" + 'blue' + ".png").convert_alpha()
blue_card = pygame.transform.scale(blue_card, CARD_SIZE)
yellow_card = pygame.image.load("images/" + 'yellow' + ".png").convert_alpha()
yellow_card = pygame.transform.scale(yellow_card, CARD_SIZE)


#the player field positions per player count
player_field_positions = [
    [
        (screen_rect.centerx - (PLAYER_FIELD_WIDTH/2), screen_rect.bottom - PLAYER_FIELD_HEIGHT)
    ],
    [
        (screen_rect.centerx - (PLAYER_FIELD_WIDTH/2), screen_rect.bottom - PLAYER_FIELD_HEIGHT),
        (screen_rect.centerx - (PLAYER_FIELD_WIDTH/2), 0)
    ],
    [
        (screen_rect.centerx - (PLAYER_FIELD_WIDTH/2), screen_rect.bottom - PLAYER_FIELD_HEIGHT),
        (0, 0),
        (screen_rect.right - PLAYER_FIELD_WIDTH,  0)
    ],
    [
        (screen_rect.centerx - (PLAYER_FIELD_WIDTH/2), screen_rect.bottom - PLAYER_FIELD_HEIGHT),
        (0, screen_rect.centery - (PLAYER_FIELD_HEIGHT/2)),
        (screen_rect.centerx - (PLAYER_FIELD_WIDTH/2), 0),
        (screen_rect.right - PLAYER_FIELD_WIDTH, screen_rect.centery - (PLAYER_FIELD_HEIGHT/2))
    ],
    [
        (screen_rect.centerx - (PLAYER_FIELD_WIDTH/2), screen_rect.bottom - PLAYER_FIELD_HEIGHT),
        (0, ((screen_rect.bottom/10) * 6) - (PLAYER_FIELD_HEIGHT/2)),
        ((screen_rect.right/6), 0),
        (((screen_rect.right/6) * 5) - PLAYER_FIELD_WIDTH, 0),
        (screen_rect.right - PLAYER_FIELD_WIDTH, ((screen_rect.bottom/10) * 6) - (PLAYER_FIELD_HEIGHT/2))
    ],
    [
        (screen_rect.centerx - (PLAYER_FIELD_WIDTH/2), screen_rect.bottom - PLAYER_FIELD_HEIGHT),
        (0, ((screen_rect.bottom/3) * 2) - (PLAYER_FIELD_HEIGHT/2)),
        (0, ((screen_rect.bottom/3) * 1) - (PLAYER_FIELD_HEIGHT/2)),
        (screen_rect.centerx - (PLAYER_FIELD_WIDTH/2), 0),
        (screen_rect.right - PLAYER_FIELD_WIDTH, ((screen_rect.bottom/3) * 1) - (PLAYER_FIELD_HEIGHT/2)),
        (screen_rect.right - PLAYER_FIELD_WIDTH, ((screen_rect.bottom/3) * 2) - (PLAYER_FIELD_HEIGHT/2)),
    ]
]




#   GAME OBJECT CLASSES
#player base class
class player():
    def __init__(self):
        self.hand = []

        self.player_type = font_big.render('P', True, BLACK)

    def set_position(self, pos):
        self.rect = pygame.Rect(pos, (PLAYER_FIELD_WIDTH, PLAYER_FIELD_HEIGHT))
        self.x = pos[0]
        self.y = pos[1]

        self.player_type_rect = self.player_type.get_rect()
        if self.rect.bottom == screen_rect.bottom:
            self.player_type_rect[0] = self.rect.centerx - (self.player_type_rect[2]/2)
            self.player_type_rect[1] = self.rect.top - 10 - self.player_type_rect[3]
        elif self.rect.top == 0:
            self.player_type_rect[0] = self.rect.centerx - (self.player_type_rect[2]/2)
            self.player_type_rect[1] = self.rect.bottom + 10
        elif self.rect.left == 0:
            self.player_type_rect[0] = self.rect.right + 10
            self.player_type_rect[1] = self.rect.centery - (self.player_type_rect[3]/2)
        elif self.rect.right == screen_rect.right:
            self.player_type_rect[0] = self.rect.left - 10 - self.player_type_rect[2]
            self.player_type_rect[1] = self.rect.centery - (self.player_type_rect[3]/2)
        else:
            self.player_type_rect[0] = self.rect.centerx - (self.player_type_rect[2]/2)
            self.player_type_rect[1] = self.rect.centery - (self.player_type_rect[3]/2)

    def add_cards(self, cards):
        for card in cards:
            self.hand.append(card)
        self.update_cards()

    def del_card_by_index(self, index):
        del self.hand[index]
        self.update_cards()

    def del_card_by_object(self, object):
        self.hand.remove(object)
        self.update_cards()

    def sort_hand(self):
        red_cards = []
        green_cards = []
        blue_cards = []
        yellow_cards = []
        black_cards = []
        for card in self.hand:
            if card[0] == 'red':
                red_cards.append(card)
            elif card[0] == 'green':
                green_cards.append(card)
            elif card[0] == 'blue':
                blue_cards.append(card)
            elif card[0] == 'yellow':
                yellow_cards.append(card)
            else:
                black_cards.append(card)

        self.hand = blue_cards + green_cards + red_cards + yellow_cards + black_cards

    def update_cards(self):
        self.sort_hand()
        self.update_card_positions()

        self.card_count = font_big.render(str(len(self.hand)), True, BLACK)
        self.card_count_rect = self.card_count.get_rect()
        self.card_count_rect[0] = (self.rect.right - self.card_count_rect[2]) - 10
        self.card_count_rect[1] = (self.y + 10)

    def update_card_positions(self):
        card_x = self.x
        card_y = self.y
        max_card_x = self.rect.right - CARD_WIDTH - 30
        for card in self.hand:
            if card_x > max_card_x:
                card_x = self.x
                card_y += CARD_HEIGHT + 5

            card[3][0] = card_x
            card[3][1] = card_y

            card_x += CARD_WIDTH + 5

    def update(self):
        pass


    def draw(self):
        pygame.draw.rect(screen, BLACK, self.rect, 1)

        for card in self.hand:
            screen.blit(card[2], card[3])

        screen.blit(self.player_type, self.player_type_rect)

        screen.blit(self.card_count, self.card_count_rect)





#human player class
class human_player(player):
    def __init__(self):
        player.__init__(self)
        self.player_type = font_big.render('H', True, BLACK)

    def update(self):
        player.update(self)

    def draw(self):
        player.draw(self)


#ai player class
class ai_player(player):
    def __init__(self):
        player.__init__(self)
        self.player_type = font_big.render('AI', True, BLACK)

    def play_turn(self):
        for card in self.hand:
            if validate_card(card):
                play_card(card, self)
                return
        take_cards_from_deck(1, self)

    def update(self):
        player.update(self)

    def draw(self):
        player.draw(self)




#   GAME LOGIC CLASSES
class turn_handler():
    def __init__(self):
        pass




#   GAME LOGIC FUNCTIONS
def play_card(card, p=None):
    if p != None:
        p.del_card_by_object(card)
    card[2] = pygame.transform.scale2x(card[2])
    card[3] = card[2].get_rect()
    card[3][0] = (screen_rect.right / 2) - (card[3][2] / 2)
    card[3][1] = (screen_rect.bottom / 2) - (card[3][3] / 2)
    middle.append(card)


def take_cards_from_deck(draw_count, p=None):
    cards = []
    for i in range(draw_count):
        rand_num = random.randint(0, len(deck) - 1)
        cards.append(deck[rand_num])
        del deck[rand_num]

    if p != None:
        p.add_cards(cards)
    else:
        return cards


def validate_card(card):
    middle_card = middle[-1]
    if card[0] == 'black' or middle_card[1] == '+4' or card[0] == middle_card[0] or card[1] == middle_card[1]:
        return True
    else:
        return False


#main update function (this is where all the other update functions are called from)
def update():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
#        elif event.type == pygame.KEYDOWN:
#            if event.key == pygame.K_s:
#                pass
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click_found = False
            for p in players:
                if not click_found:
                    if isinstance(p, human_player):
                        mouse_x, mouse_y = event.pos
                        if p.rect.collidepoint(mouse_x, mouse_y):
                            click_found = True
                            for card in p.hand:
                                if card[3].collidepoint(mouse_x, mouse_y):
                                    if validate_card(card):
                                        play_card(card, p)
                                    break
                else:
                    break

    for p in players:
        p.update()

    return True


#main draw function (this is where all the other draw functions are called from)
def draw():
    screen.fill(WHITE)

    screen.blit(middle[-1][2], middle[-1][3])

    for p in players:
        p.draw()

    pygame.display.update()




#   MAIN
if __name__ == '__main__':
    #game variables
    delta = 1/FPS
    players = [
        human_player(),
        ai_player(),
        human_player(),
        ai_player()
    ]
    player_count = len(players)
    middle = []


    #creating the players
    for i in range(player_count):
        players[i].set_position(player_field_positions[player_count - 1][i])


    #dealing cards
    for p in players:
        take_cards_from_deck(7, p)

    card = take_cards_from_deck(1)[0]
    play_card(card)


    #main loop
    run = True
    while run:
        delta = clock.tick(FPS)
        run = update()
        draw()




#   QUIT
pygame.quit()
sys.exit()