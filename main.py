import sys, random
import pygame




#   CONSTANTS
#colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)


#sizes
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 750
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

CARD_HEIGHT = 50
CARD_WIDTH = int((CARD_HEIGHT/3) * 2)
CARD_SIZE = (CARD_WIDTH, CARD_HEIGHT)

PLAYER_FIELD_WIDTH = 250
PLAYER_FIELD_HEIGHT = 200
PLAYER_FIELD_SIZE = (PLAYER_FIELD_WIDTH, PLAYER_FIELD_HEIGHT)

DEFAULT_FONT_SIZE = 30
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
blank_cards = {}
colors = ['red', 'green', 'blue', 'yellow']
colored_specials = ['plus2', 'reverse', 'skip']
black_specials = ['plus4', 'wildcard']
for color in colors:
    for i in range(10):
        card = pygame.image.load("images/" + color + "_" + str(i) + ".png").convert_alpha()
        deck.append([color, str(i), card, None])

    for i in range(1, 10):
        card = pygame.image.load("images/" + color + "_" + str(i) + ".png").convert_alpha()
        deck.append([color, str(i), card, None])

    for special in colored_specials:
        card = pygame.image.load("images/" + color + "_" + special + ".png").convert_alpha()
        deck.append([color, special, card, None])

    card = pygame.image.load("images/" + color + ".png").convert_alpha()
    blank_cards[color] = [color, "none", card, None]

for special in black_specials:
    for i in range(4):
        card = pygame.image.load("images/black_" + special + ".png").convert_alpha()
        deck.append(['black', special, card, None])


for card in deck:
    card[2] = pygame.transform.scale(card[2], CARD_SIZE)
    card[3] = card[2].get_rect()
for card in blank_cards.values():
    card[2] = pygame.transform.scale(card[2], CARD_SIZE)
    card[3] = card[2].get_rect()


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
        self.playing = False
        self.player_type = font_default.render('P', True, BLACK)

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

    def update_cards(self):
        self.sort_hand()

        self.card_count = font_default.render(str(len(self.hand)), True, BLACK)
        self.card_count_rect = self.card_count.get_rect()
        self.card_count_rect[0] = (self.rect.right - self.card_count_rect[2]) - 10
        self.card_count_rect[1] = (self.y + 10)

        self.update_card_positions()

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


    def update_card_positions(self):
        card_x = self.x
        card_y = self.y
        max_card_x = self.rect.right - CARD_WIDTH - self.card_count_rect[2] - 10
        for card in self.hand:
            if card_x > max_card_x:
                card_x = self.x
                card_y += CARD_HEIGHT + 3

            card[3][0] = card_x
            card[3][1] = card_y

            card_x += CARD_WIDTH + 3

    def update(self):
        pass


    def draw(self):
        if self.playing:
            pygame.draw.rect(screen, GREEN, self.rect, 2)
        else:
            pygame.draw.rect(screen, BLACK, self.rect, 1)

        for card in self.hand:
            screen.blit(card[2], card[3])

        screen.blit(self.player_type, self.player_type_rect)

        screen.blit(self.card_count, self.card_count_rect)





#human player class
class human_player(player):
    def __init__(self):
        player.__init__(self)
        self.player_type = font_default.render('H', True, BLACK)

    def update(self):
        player.update(self)

    def draw(self):
        player.draw(self)


#ai player class
class ai_player(player):
    def __init__(self):
        player.__init__(self)
        self.player_type = font_default.render('AI', True, BLACK)

    def play_turn(self):
        for card in self.hand:
            if validate_card(card):
                play_card(card, self)
                return
        take_cards_from_deck(1, self)

    def update(self):
        player.update(self)
        if self.playing:
            self.play_turn()
            turn_handler.end_turn()

    def draw(self):
        player.draw(self)




#   GAME LOGIC CLASSES
class turn_handler():
    def __init__(self):
        self.index = random.randint(0, player_count - 1)
        self.direction = True
        self.current_player = players[self.index]
        self.current_player.playing = True
        self.card_draw_count_next_player = 0

    def update_current_player(self):
        self.current_player.playing = False
        self.current_player = players[self.index]
        self.current_player.playing = True

    def switch_direction(self):
        if self.direction:
            self.direction = False
        else:
            self.direction = True

    def increase_index(self, increase=1):
        if self.direction:
            self.index += increase
        else:
            self.index -= increase

        self.fix_index_oor()

    def end_turn(self):
        self.increase_index()
        self.update_current_player()
        if self.card_draw_count_next_player != 0:
            take_cards_from_deck(self.card_draw_count_next_player, self.current_player)
            self.card_draw_count_next_player = 0

    def fix_index_oor(self):
        overshoot = self.index - player_count
        if self.direction:
            if overshoot >= 0:
                self.index = overshoot
        else:
            if overshoot < -player_count:
                self.index = player_count - (player_count + overshoot) - 2


class special_card_handler():
    def __init__(self):
        self.wildcard_in_middle = False

    def wildcard(self, color):
        wildcard_red_button = font_small.render('Red', True, BLACK)
        wildcard_red_button_rect = wildcard_red_button.get_rect()

        wildcard_green_button = font_small.render('Green', True, BLACK)
        wildcard_green_button_rect = wildcard_green_button.get_rect()

        wildcard_blue_button = font_small.render('Blue', True, BLACK)
        wildcard_blue_button_rect = wildcard_blue_button.get_rect()

        wildcard_yellow_button = font_small.render('Yellow', True, BLACK)
        wildcard_yellow_button_rect = wildcard_yellow_button.get_rect()

        self.wildcard_in_middle = True

        play_card(blank_cards[color])

    def reverse(self):
        turn_handler.switch_direction()

    def skip(self):
        turn_handler.increase_index()

    def plus4(self):
        turn_handler.card_draw_count_next_player = 4

    def plus2(self):
        turn_handler.card_draw_count_next_player = 2




#   GAME LOGIC FUNCTIONS
def play_card(card, p=None):
    if p != None:
        p.del_card_by_object(card)
    card[2] = pygame.transform.scale2x(card[2])
    card[3] = card[2].get_rect()
    card[3][0] = screen_rect.centerx - (card[3][2] / 2)
    card[3][1] = screen_rect.centery - (card[3][3] / 2)
    middle.append(card)

    if not card[1].isdigit():
        getattr(special_card_handler, card[1])()

    global draw_once
    draw_once = True


def take_cards_from_deck(card_count, p=None):
    cards = []
    for i in range(card_count):
        rand_num = random.randint(0, len(deck) - 1)
        cards.append(deck[rand_num])
        del deck[rand_num]

    global draw_once
    draw_once = True

    if p != None:
        p.add_cards(cards)
    else:
        return cards


def validate_card(card):
    middle_card = middle[-1]
    if card[0] == 'black' or middle_card[1] == 'plus4' or card[0] == middle_card[0] or card[1] == middle_card[1]:
        return True
    else:
        return False


#main update function (this is where all the other update functions are called from)
def update():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            global run
            run = False
#        elif event.type == pygame.KEYDOWN:
#            if event.key == pygame.K_a:
#                pass
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos

            p = turn_handler.current_player
            if isinstance(p, human_player):
                if p.rect.collidepoint(mouse_x, mouse_y):
                    for card in p.hand:
                        if card[3].collidepoint(mouse_x, mouse_y):
                            if validate_card(card):
                                play_card(card, p)
                                turn_handler.end_turn()
                            break

                elif draw_button_rect.collidepoint(mouse_x, mouse_y):
                    take_cards_from_deck(1, p)
                    turn_handler.end_turn()

    for p in players:
        p.update()


#main draw function (this is where all the other draw functions are called from)
def draw():
    #background
    screen.fill(WHITE)

    #middle card
    screen.blit(middle[-1][2], middle[-1][3])

    #draw button
    screen.blit(draw_button, draw_button_rect)

    for p in players:
        p.draw()

    pygame.display.update()

    global draw_once
    draw_once = False




#   MAIN
if __name__ == '__main__':
    #game variables
    delta = 1/FPS
    players = [
        human_player(),
        human_player(),
        human_player(),
        human_player(),
        human_player()
    ]
    player_count = len(players)
    middle = []
    turn_handler = turn_handler()
    special_card_handler = special_card_handler()


    #creating the players
    for i in range(player_count):
        players[i].set_position(player_field_positions[player_count - 1][i])


    #dealing cards
    for p in players:
        take_cards_from_deck(7, p)

    card = take_cards_from_deck(1)[0]
    play_card(card)

    #create draw button
    draw_button = font_default.render('Draw', True, BLACK)
    draw_button_rect = draw_button.get_rect()
    draw_button_rect[0] = screen_rect.centerx - (draw_button_rect[2]/2) + 100
    draw_button_rect[1] = screen_rect.centery - (draw_button_rect[3]/2)

    #main loop
    draw_once = True
    run = True
    while run:
        delta = clock.tick(FPS)
        update()
        if draw_once:
            draw()




#   QUIT
pygame.quit()
sys.exit()