import pygame

class SimpleSprite(pygame.sprite.Sprite):
    def __init__(self, img, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img).convert_alpha()
        self.rect = (pos[0], pos[1], self.image.get_rect()[2], self.image.get_rect()[3])

    def set_pos(self, x, y):
        self.rect = (x, y, self.image.get_rect()[2], self.image.get_rect()[3])