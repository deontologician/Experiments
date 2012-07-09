#!/usr/bin/env python2

import pygame
from pygame.locals import *
from sys import exit
import time
import random

pygame.init()

screen_width = 1280
screen_height = 800
rect_h = 100
rect_w = 100
fade_time = 2
screen = pygame.display.set_mode((screen_width, screen_height), HWSURFACE | DOUBLEBUF | FULLSCREEN , 32)

color1 = (random.randint(0,255),
          random.randint(0,255),
          random.randint(0,255))
color2 = (random.randint(0,255),
          random.randint(0,255),
          random.randint(0,255))
factor = 0.

def blend_color(color1, color2, blend_factor):
    red1, green1, blue1 = color1
    red2, green2, blue2 = color2
    red = red1+(red2-red1)*blend_factor
    green = green1+(green2-green1)*blend_factor
    blue = blue1+(blue2-blue1)*blend_factor
    return int(red), int(green), int(blue)

old_time = time.time()
dot_list = []

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == KEYDOWN:
            exit()
    
    screen.fill((255, 255, 255))

    new_time = time.time()
    if new_time > old_time + fade_time:
        old_time = new_time
        color1 = color2
        color2 = (random.randint(0,255),
                  random.randint(0,255),
                  random.randint(0,255))
        dot_list = []
    
    factor = (new_time - old_time)/fade_time
    color = blend_color(color1, color2, factor)
    screen.fill(color)

    #throw in some random pixel changes.
    dot_list.append((random.randint(0,screen_width),
                     random.randint(0,screen_height)))
    for dot in dot_list:
        screen.set_at(dot, color2)

    # display rectangle
    pygame.draw.rect(screen, color2, (screen_width/2 - rect_w/2,
                                      screen_height/2 - rect_h/2,
                                      rect_w,
                                      rect_h))
    pygame.display.update()
