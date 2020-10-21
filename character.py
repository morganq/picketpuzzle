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
        self.last_move_direction = 0#random.randint(0,min(4, self._sheet.get_size()[0] // width))
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