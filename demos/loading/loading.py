#!/usr/bin/env python2

bg_filename = "car"
ext = ".jpg"
monster_filename = 'monster.png'

import pygame
from pygame.locals import *
from sys import exit
import random
import time

pygame.init()

screen_width = 1280
screen_height = 800
hardware = FULLSCREEN | HWSURFACE | DOUBLEBUF
software = NOFRAME
jitter_size = 10
fps_decay = 46.0
max_framerate = 45.0

title = "Loading... "
screen = pygame.display.set_mode((screen_width, screen_height), hardware, 32)
pygame.display.set_caption(title)
font = pygame.font.Font("Bleeding_Cowboys.ttf",130)
little_font = pygame.font.Font("BitStreamVeraSansMono.ttf", 10)

background = [pygame.image.load(bg_filename + '1' + ext).convert(),
              pygame.image.load(bg_filename + '2' + ext).convert()]

line_persist = 0
draw_a_line = 0
old_time = 0.0
show_fps = False
fps_average = 0

def blit_title():
    choice = random.randint(0,20)
    screen.blit(font.render(title,
                            True,
                            (choice, choice, choice)),
                (random.randint(-2,2),
                 screen_height/2 + random.randint(-2,2)))


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == MOUSEBUTTONDOWN:
            exit()

    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[K_f]:
        show_fps = not show_fps
    
    new_time = time.time()
    if new_time < old_time + 1/max_framerate:
        continue
    
    fps = 1/(new_time - old_time)
    old_time = time.time()        
    

    screen.fill((0,0,0))
    screen.blit(background[random.choice([0,1,1,1,1,1,1,1,1])],
                (random.randint(-3,3),0))

    hide_title = random.randint(0,15)
    if hide_title  != 0:
        blit_title()

    
        
    if draw_a_line == 47:
        if line_persist == 0:
            base_x = random.randint(0,screen_width)
            line_persist = random.randint(3,15)
        else:
            pygame.draw.line(screen, (0,0,0), (base_x,0), (base_x, screen_height), 2)
            base_x += random.randint(-3,3)
            line_persist -= 1
            if line_persist == 0:
                draw_a_line = random.randint(0,47)
    else:
        draw_a_line = random.randint(0,47)   


    if fps != 0:
        fps_average = fps if fps_average == 0 else (fps_average*(fps_decay - 1) + fps)/fps_decay
        if show_fps:
            screen.blit(little_font.render(str(int(fps_average)) + " fps",
                                           True,
                                           (0,0,0)),
                        (0,0))


    pygame.display.flip()

