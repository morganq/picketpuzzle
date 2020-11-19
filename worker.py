import pygame
import character
import pygame
import game

class Worker(character.Character):
    def __init__(self, gx, gy):
        character.Character.__init__(self, "assets/worker.png", gx, gy, 12)
        self.type = "worker"
        self._old_sheet = self._sheet
        self.inv_img = pygame.surface.Surface(self._sheet.get_rect().size, pygame.SRCALPHA)
        self.inv_img.fill((0,0,0,0))
        self.inv_img.blit(self._sheet, (0,0), None)
        for x in range(self.inv_img.get_rect()[2]):
            for y in range(self.inv_img.get_rect()[3]):
                color = self.inv_img.get_at((x, y))
                if color == (238, 32, 17, 255):
                    self.inv_img.set_at((x,y), game.FGCOLOR)
        self.blinking = False
        self.blink_time = 0
        

    def update(self, dt):
        character.Character.update(self, dt)
        if self.blinking:
            self.blink_time += dt * 12
            self._sheet = [self.inv_img, self._old_sheet][int(self.blink_time) % 2]
            self._update_image()

