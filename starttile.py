import pygame
import character
import game

class StartTile(character.Character):
    def __init__(self, gx, gy):
        character.Character.__init__(self, "assets/workericon.png", gx, gy, 12)
        self.type = "start"