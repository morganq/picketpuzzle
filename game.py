import pygame
import csv

import sound
import tilemap
import factory
import police
import soldier
import states
import cityhall
import worker
import starttile
import levelscene
import worldmapscene
import sys

SCALE = 4
RES = (240,192)
BGCOLOR = (42,17,81)
TILESIZE = 12
DIRS_FROM_OFFSETS = {
    (1,0):0, (0,1):1, (-1,0):2, (0,-1):3
}
ROADTILES = list(range(1, 16))
DECOTILES = list(range(19, 40))
OBJ = {
    'factory': 0,
    'cityhall': 1,
    'police': 2,
    'soldier': 3,
    'start': 4,
    'celltower': 5
}
class Game:
    def __init__(self, save):
        pygame.mixer.pre_init(buffer=256)
        pygame.init()
        sound.init()
        self.save = save
        self.scaled_screen = pygame.display.set_mode((RES[0] * SCALE, RES[1] * SCALE))
        self.screen = pygame.Surface(RES)
        if len(sys.argv) > 1:
            self.scene = levelscene.LevelScene(self, sys.argv[1])
        else:
            self.scene = worldmapscene.WorldMapScene(self, 0)
        self.playing_level_index = None

    def run(self):
        clock = pygame.time.Clock()
        running = True
        self.scene.start()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT: self.scene.take_input("left", event)
                    elif event.key == pygame.K_RIGHT: self.scene.take_input("right", event)
                    elif event.key == pygame.K_UP: self.scene.take_input("up", event)
                    elif event.key == pygame.K_DOWN: self.scene.take_input("down", event)
                    elif event.key == pygame.K_SPACE: self.scene.take_input("action", event)
                    elif event.key == pygame.K_ESCAPE: self.scene.take_input("back", event)
                    else:
                        self.scene.take_input("other", event)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: self.scene.take_input("click", event)
                    if event.button == 3: self.scene.take_input("rightclick", event)

            dt = clock.tick() / 1000.0

            self.scene.update(dt)
            self.render()

    def render(self):
        self.scene.render()
        pygame.transform.scale(self.screen, self.scaled_screen.get_size(), self.scaled_screen)
        pygame.display.update()


    def start_level(self, level, index):
        self.playing_level_index = index
        self.scene = levelscene.LevelScene(self, level)
        self.scene.start()

    def return_to_map(self):
        self.scene = worldmapscene.WorldMapScene(self, self.playing_level_index)
        self.scene.start()
            
    def record_victory(self, steps):
        if self.playing_level_index is not None:
            level = worldmapscene.LEVELS[self.playing_level_index]
            s3, s2, s1 = level[4:]
            print(s3,s2,s1)
            stars = 0
            if steps <= s3: stars = 3
            elif steps <= s2: stars = 2
            elif steps <= s1: stars = 1
            old_state = self.save.get_level_state(self.playing_level_index)
            if not old_state['beaten'] or stars > old_state['stars']:
                self.save.set_level_state(self.playing_level_index, True, steps, stars)
                self.save.save()