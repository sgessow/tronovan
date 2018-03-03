import sys
import random
import pygame
from pygame.locals import *
import pymunk #1
import pymunk.pygame_util
from objects import *
from constants import *


def main():
    pygame.init()
    screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    pygame.display.set_caption("Leg 2")
    clock=pygame.time.Clock()

    space=pymunk.Space()
    space.gravity=(0.0,-900.0)

    #add the floor
    floor=add_floor(space)

    #make the robot named tron
    tron=robot(space)
    tron.add_to_space()



    draw_options = pymunk.pygame_util.DrawOptions(screen)

    while True:
        for event in pygame.event.get():
            if event.type==QUIT:
                sys.exit(0)
            elif event.type==KEYDOWN and event.key==K_ESCAPE:
                sys.exit(0)

        screen.fill((255,255,255))

        space.debug_draw(draw_options)

        space.step(1/50.0) #3

        pygame.display.flip()
        clock.tick(50)



if __name__ == '__main__':
    sys.exit(main())
