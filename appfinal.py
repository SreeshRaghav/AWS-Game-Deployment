import pygame, sys, random
import pandas as pd
import matplotlib.pyplot as plt

def ball_animation():
    global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time

    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1

    if ball.left <= 0:
        score_time = pygame.time.get_ticks()
        player_score += 1

    if ball.right >= screen_width:
        score_time = pygame.time.get_ticks()
        opponent_score += 1

    if ball.colliderect(player) and ball_speed_x > 0:
        if abs(ball.right - player.left) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - player.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - player.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1

    if ball.colliderect(opponent) and ball_speed_x < 0:
        if abs(ball.left - opponent.right) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - opponent.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - opponent.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1

def player_animation():
    player.y += player_speed

    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height

def opponent_animation():
    global opponent_speed

    if ball_speed_x > 0:
        desired_y = ball.centery
        opponent_center_y = opponent.centery
        error = desired_y - opponent_center_y

        opponent_speed = error * 0.1

    else:
        opponent_speed = 0

    opponent.y += opponent_speed

    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height

def ball_start():
    global ball_speed_x, ball_speed_y, ball_moving, score_time

    ball.center = (screen_width / 2, screen_height / 2)
    current_time = pygame.time.get_ticks()

    if current_time - score_time < 700:
        number_three = basic_font.render("3", False, pale_violetred)
        screen.blit(number_three, (screen_width / 2 - 10, screen_height / 2 + 20))
    if 700 < current_time - score_time < 1400:
        number_two = basic_font.render("2", False, pale_violetred)
        screen.blit(number_two, (screen_width / 2 - 10, screen_height / 2 + 20))
    if 1400 < current_time - score_time < 2100:
        number_one = basic_font.render("1", False, pale_violetred)
        screen.blit(number_one, (screen_width / 2 - 10, screen_height / 2 + 20))

    if current_time - score_time < 2100:
        ball_speed_y, ball_speed_x = 0, 0
    else:
        ball_speed_x = 7 * random.choice((1, -1))
        ball_speed_y = 7 * random.choice((1, -1))
        score_time = None

def victory_message():
    global ball_speed_x, ball_speed_y, ball_moving, score_time, basic_font, basic_font2

    if player_score == 5:
        victory_surf = basic_font.render('Player 1 wins!', False, pale_violetred)
        victory_rect = victory_surf.get_rect(center=(screen_width / 2, screen_height / 4))
        screen.blit(victory_surf, victory_rect)
        ball_speed_x = 0
        ball_speed_y = 0

def victory_message2():
    global ball_speed_x, ball_speed_y, ball_moving, score_time, basic_font, basic_font2

    if opponent_score == 5:
        victory_surf = basic_font.render('Player 2 wins!', False, pale_violetred)
        victory_rect = victory_surf.get_rect(center=(screen_width / 2, screen_height / 4))
        screen.blit(victory_surf, victory_rect)
        ball_speed_x = 0
        ball_speed_y = 0

def final_score():
    global player_score, opponent_score, df
    dict1 = {'Players': ["Player 1", "Player 2"], 'Score': [player_score, opponent_score]}
    df = pd.DataFrame(dict1)
    df.to_csv("proj.csv")

# General setup
pygame.mixer.pre_init(44100, -16, 1, 1024)
pygame.init()
clock = pygame.time.Clock()

# Main Window
screen_width = 1280
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')

# Load and scale the background image
background = pygame.image.load("background.png")
background = pygame.transform.scale(background, (screen_width, screen_height))

# Colors
pale_violetred = (255,48,48)
bg_color = pygame.Color('gray20')

# Game Rectangles
ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30)
player = pygame.Rect(screen_width - 20, screen_height / 2 - 70, 10, 140)
opponent = pygame.Rect(10, screen_height / 2 - 70, 10, 140)

# Game Variables
ball_speed_x = 7 * random.choice((1, -1))
ball_speed_y = 7 * random.choice((1, -1))
player_speed = 0
opponent_speed = 0
ball_moving = False
score_time = True

# Score Text
player_score = 0
opponent_score = 0
basic_font = pygame.font.Font('freesansbold.ttf', 32)
basic_font2 = pygame.font.Font('freesansbold.ttf', 32)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player_speed -= 7
            if event.key == pygame.K_DOWN:
                player_speed += 7
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                player_speed += 7
            if event.key == pygame.K_DOWN:
                player_speed -= 7

    # Game Logic
    ball_animation()
    player_animation()
    opponent_animation()

    # Visuals
    screen.blit(background, (0, 0))
    pygame.draw.rect(screen, pale_violetred, player)
    pygame.draw.rect(screen, pale_violetred, opponent)
    pygame.draw.ellipse(screen, pale_violetred, ball)
    pygame.draw.aaline(screen, pale_violetred, (screen_width / 2, 0), (screen_width / 2, screen_height))

    if score_time:
        ball_start()

    player_text = basic_font.render(f'{player_score}', False, pale_violetred)
    screen.blit(player_text, (660, 470))

    opponent_text = basic_font.render(f'{opponent_score}', False, pale_violetred)
    screen.blit(opponent_text, (600, 470))

    victory_message()
    victory_message2()
    final_score()

    if player_score == 5:
        df.plot(x='Players', y='Score', kind='bar')
        plt.title('Chart')
        plt.xlabel('Players')
        plt.ylabel('Score')
        plt.xticks(rotation=0)
        plt.show()

    if opponent_score == 5:
        df.plot(x='Players', y='Score', kind='bar')
        plt.title('Chart')
        plt.xlabel('Players')
        plt.ylabel('Score')
        plt.xticks(rotation=0)
        plt.show()

    pygame.display.flip()
    clock.tick(60)
