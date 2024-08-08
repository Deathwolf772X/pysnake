import pygame
import time
import random
import os

pygame.init()

width, height = 800, 600

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

block_size = 20
border_size = 10

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Game by Callum Kenyon')

clock = pygame.time.Clock()
snake_speed = 15

font_style = pygame.font.SysFont(None, 35)
score_font = pygame.font.SysFont(None, 35)

high_score_file = 'high_score.txt'

def read_high_score():
    if not os.path.exists(high_score_file):
        with open(high_score_file, 'w') as file:
            file.write('0')
    with open(high_score_file, 'r') as file:
        return int(file.read())

def write_high_score(score):
    with open(high_score_file, 'w') as file:
        file.write(str(score))

def display_score(score):
    value = score_font.render(f"Score: {score}", True, white)
    screen.blit(value, [0, 0])

def display_high_score(high_score):
    value = score_font.render(f"High Score: {high_score}", True, white)
    screen.blit(value, [width - 200, 0])

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [width / 6, height / 3])

def draw_border():
    pygame.draw.rect(screen, white, [0, 0, width, border_size])
    pygame.draw.rect(screen, white, [0, 0, border_size, height])
    pygame.draw.rect(screen, white, [0, height - border_size, width, border_size])
    pygame.draw.rect(screen, white, [width - border_size, 0, border_size, height])

def game_loop():
    game_over = False
    game_close = False

    x1 = width / 2
    y1 = height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    length_of_snake = 1

    foodx = round(random.randrange(border_size, width - block_size - border_size) / block_size) * block_size
    foody = round(random.randrange(border_size, height - block_size - border_size) / block_size) * block_size

    score = 0
    high_score = read_high_score()

    while not game_over:

        while game_close:
            screen.fill(black)
            message("You Lost! Press Q-Quit or C-Play Again", red)
            display_score(score)
            display_high_score(high_score)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -block_size
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = block_size
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -block_size
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = block_size
                    x1_change = 0

        if x1 >= width - border_size or x1 < border_size or y1 >= height - border_size or y1 < border_size:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        screen.fill(black)
        draw_border()
        pygame.draw.rect(screen, green, [foodx, foody, block_size, block_size])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        for segment in snake_List:
            pygame.draw.rect(screen, white, [segment[0], segment[1], block_size, block_size])

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(border_size, width - block_size - border_size) / block_size) * block_size
            foody = round(random.randrange(border_size, height - block_size - border_size) / block_size) * block_size
            length_of_snake += 1
            score += 1
            if score > high_score:
                high_score = score
                write_high_score(high_score)

        display_score(score)
        display_high_score(high_score)
        clock.tick(snake_speed)

    pygame.quit()
    quit()

game_loop()
