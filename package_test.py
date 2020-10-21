import pygame
import sys
import os

def resource_path(relative_path): # needed for bundling                                                                                                                            
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

pygame.init()
screen = pygame.display.set_mode((800, 600))

os.system("touch ~/Desktop/hello.txt")
os.system('echo "%s" > ~/Desktop/hello.txt' % str(resource_path("something.txt")))
os.system('echo "%s" >> ~/Desktop/hello.txt' % str(os.listdir()))

im = pygame.image.load(resource_path("assets/workericon.png"))
f = pygame.font.Font(resource_path("assets/Minecraftia-Regular.ttf"), 8)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    
    

    screen.fill((255,255,0))
    screen.blit(im, (0,0))
    pygame.display.flip()