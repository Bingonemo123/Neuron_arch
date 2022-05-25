import sys, pygame
import os
from PIL import Image
import time
import pickle
import random
pygame.init()
display_info = pygame.display.Info()
size = width, height = round(0.45572917*display_info.current_w), round(0.45572917*display_info.current_w/2.35)
flags = pygame.NOFRAME 
depth = 32
origin = (0, 0)

def pilImageToSurface(pilImage):
    return pygame.image.fromstring(
        pilImage.tobytes(), pilImage.size, pilImage.mode)
        

background = Image.open("NInterface\\III.png")
background = background.resize(size, Image.LANCZOS)
background = pilImageToSurface(background)

main_title = Image.open("NInterface\\Main_TitleI.png")
main_title = main_title.resize(size, Image.LANCZOS)
main_title = pilImageToSurface(main_title)

background.blit(main_title, origin)

screen = pygame.display.set_mode(size, flags, depth=depth)

background = background.convert(depth)


screen.blit(background, origin)
pygame.display.flip()

for x in range(width)[20:-20]:
    for y in range(5):
        if y in [0,4] and x in [20, width-21]: continue
        background.set_at((x, height - y - 5), (166, 161, 159))

    screen.blit(background, origin)
    pygame.display.flip()
    time.sleep(0.001)
    

pygame.quit()


