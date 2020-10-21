import pygame
import character

class Worker(character.Character):
    def __init__(self, gx, gy):
        character.Character.__init__(self, "assets/worker.png", gx, gy, 12)
        self.type = "worker"
        