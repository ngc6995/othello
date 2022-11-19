import pygame
from pygame import mixer
from constants import *
from othello import *

def rowcol_to_xy(row, col):
    return 12 + 68 * col, 578 - 68 * row

def xy_to_rowcol(x, y):
    row_y = (643, 575, 507, 439, 371, 303, 235, 167)
    col_x = (12, 80, 148, 216, 284, 352, 420, 488)

    if x > 12 and y > 102 and x < 553 and y < 643:
        for row in range(8):
            if y < row_y[row] and y > row_y[row] - SQUARE_HEIGHT:
                break
        for col in range(8):
            if x > col_x[col] and x < col_x[col] + SQUARE_WIDTH:
                break
        return row, col     
    else:
        return -1, -1

def draw_board():
    screen.blit(img_board, (0, 0))

def draw_move_marker():
    x, y = rowcol_to_xy(move_row, move_col)
    screen.blit(img_marker2, (x, y))

def draw_play_color():
    if play[Othello.BLACK] == "human":
        human_plays_color = img_black_disc
        ai_plays_color = img_white_disc
    else:
        human_plays_color = img_white_disc
        ai_plays_color = img_black_disc

    screen.blit(human_plays_color, (HUMAN_PLAYS_X, HUMAN_PLAYS_Y))
    screen.blit(ai_plays_color, (AI_PLAYS_X, AI_PLAYS_Y))
    
def draw_disc_counter():
    if play[Othello.BLACK] == "human":
        human_discs_on_board = str(game.black_discs)
        ai_discs_on_board = str(game.white_discs)
    else:
        human_discs_on_board = str(game.white_discs)
        ai_discs_on_board = str(game.black_discs)

    text = text_font.render(human_discs_on_board, True, WHITE)
    text_rect = text.get_rect()
    text_rect.left = RECT_LEFT
    text_rect.top = RECT_TOP
    screen.blit(text, text_rect)

    text = text_font.render(ai_discs_on_board, True, WHITE)
    text_rect = text.get_rect()
    text_rect.right = RECT_RIGHT
    text_rect.top = RECT_TOP
    screen.blit(text, text_rect)

def draw_discs_on_board():
    for row in range(8):
        for col in range(8):
            if [row, col] not in game.flip_discs:
                if game.board[row][col] == Othello.BLACK:
                    x, y = rowcol_to_xy(row, col)
                    screen.blit(img_black_disc, (x+1, y+2))
                elif game.board[row][col] == Othello.WHITE:
                    x, y = rowcol_to_xy(row, col)
                    screen.blit(img_white_disc, (x+1, y+2))

def draw_legal_moves_marker():
    if play[game.player_turn] == "human":
        for move in game.legal_moves:
            x, y = rowcol_to_xy(move[0], move[1])
            screen.blit(img_marker1, (x+18, y+19))

def draw_screen():
    if len(game.flip_discs) > 0:
        first_disc = game.flip_discs[0]

        if game.board[first_disc[0]][first_disc[1]] == Othello.BLACK:
            start, stop, step = 0, 9, 1
        else:
            start, stop, step = 8, -1, -1

        for index in range(start, stop, step):
            draw_board()
            draw_move_marker()
            draw_play_color()
            draw_disc_counter()
            draw_discs_on_board()

            for disc in game.flip_discs:
                x, y = rowcol_to_xy(disc[0], disc[1])
                # screen.blit(img_marker3, (x, y))
                screen.blit(img_marker3, (x, y))
                screen.blit(img_disc.subsurface((index * DISC_WIDTH, 0, DISC_WIDTH, DISC_HEIGHT)), (x+1, y+2))

            pygame.time.delay(FLIP_DISC_SPEED)
            draw_legal_moves_marker()
            pygame.display.update()
    else:
        draw_board()
        draw_play_color()
        draw_disc_counter()
        draw_discs_on_board()
        draw_legal_moves_marker()
        pygame.display.update()

def play_again():
    if game.black_discs > game.white_discs:
        if play[Othello.BLACK] == "human":
            screen.blit(img_human_win, (HUMAN_WIN_X, HUMAN_WIN_Y))
        else:
            screen.blit(img_ai_win, (AI_WIN_X, AI_WIN_Y))
    elif game.white_discs > game.black_discs:
        if play[Othello.WHITE] == "human":
            screen.blit(img_human_win, (HUMAN_WIN_X, HUMAN_WIN_Y))
        else:
            screen.blit(img_ai_win, (AI_WIN_X, AI_WIN_Y))
    else:
        screen.blit(img_draw, (DRAW_GAME_X, DRAW_GAME_Y))

    screen.blit(img_play_again, (PLAY_AGAIN_X, PLAY_AGAIN_Y))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    return True
                elif event.key == pygame.K_n:
                    return False

def player_pass(who):
    original_screen = screen.copy()

    if play[who] == "human":
        screen.blit(img_human_pass, (HUMAN_PASS_X, HUMAN_PASS_Y))
    else:
        screen.blit(img_ai_pass, (AI_PASS_X, AI_PASS_Y))

    pygame.display.update()

    pass_move_sound = mixer.Sound(r"sounds\pass_move.wav")
    pass_move_sound.play()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONUP:
                screen.blit(original_screen, (0, 0))
                pygame.display.update()
                return

def player_move():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_xy = pygame.mouse.get_pos()
                row, col = xy_to_rowcol(*mouse_xy)
                if [row, col] in game.legal_moves:
                    return row, col

# Initialize Pygame
pygame.init()
pygame.font.init()

# Font to display disc counter for both players
text_font = pygame.font.SysFont("Arial", 53, True)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WITH, SCREEN_HEIGHT))

# Title and icon
pygame.display.set_caption("Othello")
icon = pygame.image.load(r"images\othello.png")
pygame.display.set_icon(icon)

# Load images
img_board = pygame.image.load(r"images\board.png").convert()
img_disc = pygame.image.load(r"images\disc.png").convert_alpha()
img_white_disc = img_disc.subsurface((0, 0, DISC_WIDTH, DISC_HEIGHT))
img_black_disc = img_disc.subsurface((DISC_WIDTH * 8, 0, DISC_WIDTH, DISC_HEIGHT))
img_ai_win = pygame.image.load(r"images\ai_win.png").convert_alpha()
img_ai_pass = pygame.image.load(r"images\ai_pass.png").convert_alpha()
img_human_win = pygame.image.load(r"images\you_win.png").convert_alpha()
img_human_pass = pygame.image.load(r"images\you_pass.png").convert_alpha()
img_draw = pygame.image.load(r"images\draw.png").convert_alpha()
img_play_again = pygame.image.load(r"images\play_again.png").convert_alpha()
img_marker1 = pygame.image.load(r"images\marker1.png").convert_alpha()
img_marker2 = pygame.image.load(r"images\marker2.png").convert_alpha()
# img_marker3 = pygame.image.load(r"images\marker3.png").convert_alpha()
img_marker3 = pygame.image.load(r"images\marker3.png").convert_alpha()

game = Othello()
play = {Othello.BLACK:"human", Othello.WHITE:"ai"}
last_turn = None
draw_screen()

# Game loop  
while True:
    if game.game_over:
        if play_again():
            game = Othello()
            play[Othello.BLACK], play[Othello.WHITE] = play[Othello.WHITE], play[Othello.BLACK]
            last_turn = None
            draw_screen()
        else:
            pygame.quit()
            exit()

    if last_turn == game.player_turn:
        player_pass(game.player_turn * -1)
    else:
        last_turn = game.player_turn

    if play[game.player_turn] == "human":
        move_row, move_col = player_move()
        game.move(move_row, move_col)
        human_move_sound = mixer.Sound(r"sounds\human_move.wav")
        human_move_sound.play()
        draw_screen()
        continue

    if play[game.player_turn] == "ai":
        move_row, move_col = game.ai()
        game.move(move_row, move_col)
        ai_move_sound = mixer.Sound(r"sounds\ai_move.wav")
        ai_move_sound.play()
        draw_screen()
