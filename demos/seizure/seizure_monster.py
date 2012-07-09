#!/usr/bin/env python2

background_image_filename = "pic"
bg_ext = ".jpg"
monster_filename = 'monster.png'

import pygame
from pygame.locals import *
from sys import exit
import random
import time

pygame.init()

screen_width = 1280
screen_height = 770
px_per_second = 250
jitter_size = 10
do_monster = False

title = "Loading... "
screen = pygame.display.set_mode((screen_width, screen_height), NOFRAME, 32)
pygame.display.set_caption(title)
font = pygame.font.Font("Bleeding_Cowboys.ttf",130)

background = [pygame.image.load(background_image_filename + '1' + bg_ext).convert(),
              pygame.image.load(background_image_filename + '2' + bg_ext).convert(),
              pygame.image.load(background_image_filename + '3' + bg_ext).convert()]

line_persist = 0
draw_a_line = 0

def blit_title():
    choices = [0,128,255]
    color = (random.choice(choices),
             random.choice(choices),
             random.choice(choices))
    screen.blit(font.render(title, True,tuple(color)),
                (random.randint(-2,2),
                 screen_height/2 + random.randint(-2,2)))

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == MOUSEBUTTONDOWN:
            exit()

    screen.blit(background[random.choice([0,1])],
                (random.randint(-3,3),0 ))

    hide_title = random.randint(0,7)
    if hide_title  != 0:
        blit_title()
        
    if draw_a_line == 47:
        if line_persist == 0:
            base_x = random.randint(0,screen_width)
            line_persist = random.randint(0,5)
        else:
            pygame.draw.line(screen, (255,255,255), (base_x,0), (base_x, screen_height), 2)
            base_x += random.randint(-3,3)
            line_persist -= 1
            if line_persist == 0:
                draw_a_line = random.randint(0,47)
    else:
        draw_a_line = random.randint(0,47)   

    pygame.display.flip()

