import scene
import sys
import game
import tilemap
import factory
import police
import soldier
import levelstates
import states
import cityhall
import worker
import starttile
import levelscene
import celltower
import pygame
import tank
import csv
import framesprite
import tutorial
import sound
from resources import resource_path
import traceback

class LevelScene(scene.Scene):
    def __init__(self, game, level=None):
        scene.Scene.__init__(self, game)
        self.animation_timer = 0
        self.level_file = level or "empty"

    def load(self):
        gx, gy = game.RES[0] // game.TILESIZE, game.RES[1] // game.TILESIZE
        self.tilemap = tilemap.Tilemap(game.TILESIZE, gx, gy, pygame.image.load(resource_path("assets/tiles.png")).convert_alpha())
        self.background_group = pygame.sprite.Group()
        self.background_group.add(self.tilemap)
        self.game_group = pygame.sprite.LayeredUpdates()
        self.ui_group = pygame.sprite.Group()
        self.tutorial_group = pygame.sprite.Group()

        self.tanks = []
        self.overlay = framesprite.FrameSprite("assets/gameoverlay.png", 240)
        self.ui_group.add(self.overlay)        
        self.worker_queue = tilemap.Tilemap(12, 20, 1, pygame.image.load(resource_path("assets/workericon.png")).convert_alpha())
        self.worker_queue.rect = (2, 1, 240, 12)
        self.ui_group.add(self.worker_queue)

        self.animatedsprites = []

        self.road_grid = []
        self.object_grid = []
        self.factories = []
        self.cityhalls = []
        for row in range(gy):
            self.object_grid.append([])
            self.road_grid.append([])
            for col in range(gx):
                self.object_grid[-1].append(None)        
                self.road_grid[-1].append(False)

        try:
            self.tilemap.load("levels/%s_tiles.csv" % self.level_file)
            self.load_objects("levels/%s_objects.csv" % self.level_file)
        except Exception as e:
            traceback.print_exc()
            self.tilemap.load("levels/empty_tiles.csv")
            self.load_objects("levels/empty_objects.csv")
            self.level_file = "empty"

        self.queued_workers = 0
        self.start_tile = None        

    def place_obj_by_index(self, index, x, y):
        o = None
        if index == game.OBJ['factory']: # Factory
            o = factory.Factory(x, y)
            self.factories.append(o)
            self.game_group.add(o)
            self.animatedsprites.append(o)

        if index == game.OBJ['cityhall']: # City Hall
            
            o = cityhall.CityHall(x, y)
            self.cityhalls.append(o)
            self.game_group.add(o)
            self.animatedsprites.append(o)

        elif index == game.OBJ['police']: # Police
            o = police.Police(x, y)
            self.game_group.add(o)
            self.animatedsprites.append(o)
            o.set_starting_dir(self.road_grid)

        elif index == game.OBJ['soldier']: # Soldier
            o = soldier.Soldier(x, y)
            self.game_group.add(o)
            self.animatedsprites.append(o)
            o.set_starting_dir(self.road_grid)

        elif index == game.OBJ['start']: #Starting tile
            o = starttile.StartTile(x, y)
            self.game_group.add(o)
            self.animatedsprites.append(o)

        elif index == game.OBJ['celltower']: 
            o = celltower.CellTower(x, y)
            self.game_group.add(o)
            self.animatedsprites.append(o)            

        elif index == game.OBJ['tank']:
            o = tank.Tank(x,y)
            self.game_group.add(o)
            self.animatedsprites.append(o)
            self.tanks.append(o)
            o.set_starting_dir(self.road_grid)

        self.object_grid[y][x] = o  

    def load_objects(self, filename):
        for y,row in enumerate(self.tilemap._grid):
            for x,cell in enumerate(row):
                if cell in game.ROADTILES:
                    self.road_grid[y][x] = True

        with open(resource_path(filename)) as f:
            reader = csv.reader(f)
            for y,row in enumerate(reader):
                for x,cell in enumerate(row):
                    cell = int(cell)
                    o = None
                    tmd = self.tilemap._grid[y][x]
                    self.place_obj_by_index(cell, x, y)   


    def add_queued_worker(self):
        self.queued_workers += 1
        self.worker_queue.set_tile(self.queued_workers - 1, 0, 1)
        
    def remove_queued_worker(self):
        self.queued_workers -= 1
        self.worker_queue.set_tile(self.queued_workers, 0, 0)

    def get_starting_state(self):
        for s in self.animatedsprites:
            if s.type == "start":
                s.kill()
                self.object_grid[s.gy][s.gx] = None
                self.animatedsprites.remove(s)
                w = worker.Worker(s.gx, s.gy)
                self.snake = [w]
                return levelstates.March(self)
                
        if self.factories:
            return levelstates.PickFactory(self)
        else:
            return levelstates.Edit(self)

    def initialize_state(self):
        if self.level_file in tutorial.tutorials:
            self.sm = states.Machine(levelstates.Tutorial(self, tutorial.tutorials[self.level_file]()))

        else:
            self.sm = states.Machine(self.get_starting_state())        

    def update_layers(self):
        for sprite in self.game_group.sprites():
            adjustment = 0
            if sprite.type == "particle":
                adjustment = -12
            self.game_group.change_layer(sprite, pygame.Rect(sprite.rect).bottom + adjustment)

    def start(self):
        self.load()
        self.initialize_state()      
        sound.play_music('game')  

    def update(self, dt):
        scene.Scene.update(self, dt)
        self.animation_timer += dt
        if self.animation_timer > 0.38:
            self.animation_timer -= 0.38
            for sprite in self.animatedsprites:
                sprite.step_animation()        

        for sprite in self.game_group.sprites():
            sprite.update(dt)

    def render(self):
        self.game.screen.fill(game.BGCOLOR)
        self.update_layers()
        self.background_group.draw(self.game.screen)
        self.game_group.draw(self.game.screen)
        self.ui_group.draw(self.game.screen)        
        self.tutorial_group.draw(self.game.screen)
        self.sm.state.render(self.game.screen)