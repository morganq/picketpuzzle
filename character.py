import pygame
import framesprite
import game
import random

class Character(framesprite.FrameSprite):
    type = "character"
    def __init__(self, sheet, gx, gy, width):
        self.gx = gx
        self.gy = gy
        x = gx * game.TILESIZE
        y = gy * game.TILESIZE
        framesprite.FrameSprite.__init__(self, sheet, width)
        self.rect = (x, y - 6, width, self._sheet.get_size()[1])
        self.activated = False
        self.last_move_direction = random.randint(0,min(4, self._sheet.get_size()[0] // width // 2) - 1)
        self.step_animation()

    def step_animation(self):
        base_frame = self.last_move_direction * 2
        if not self.activated:
            self.set_frame((self._frame + 1) % 2 + base_frame)

    def update_direction(self):
        base_frame = self.last_move_direction * 2
        self.set_frame((self._frame % 2) + base_frame)
        
    def interact(self, state, worker):
        return False        

    def try_push(self, state, offset):
        pass

    def set_starting_dir(self, roads):
        if roads[self.gy][self.gx-1]:
            self.last_move_direction = 2
        elif roads[self.gy][self.gx+1]:
            self.last_move_direction = 0
        elif roads[self.gy+1][self.gx]:
            self.last_move_direction = 1
        elif roads[self.gy-1][self.gx]:
            self.last_move_direction = 3
        self.update_direction()