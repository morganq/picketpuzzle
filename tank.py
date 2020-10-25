import pygame
import character
import game

class Tank(character.Character):
    def __init__(self, gx, gy):
        character.Character.__init__(self, "assets/tank.png", gx, gy, 16)
        self.type = "tank"
        self.last_move_direction = 0

    def step(self):
        pass