import pygame
from resources import resource_path

class FrameSprite(pygame.sprite.Sprite):
    type = None
    def __init__(self, sheet, width):
        pygame.sprite.Sprite.__init__(self)
        self._sheet = pygame.image.load(resource_path(sheet)).convert_alpha()
        self._frame = 0
        self._frame_width = width
        self._update_image()
        self.rect = (0,0,width,self._sheet.get_size()[1])
        self._num_frames = self._sheet.get_size()[0] // self._frame_width

    def _update_image(self):
        self.image = self._sheet.subsurface(
            self._frame * self._frame_width, 0,
            self._frame_width, self._sheet.get_size()[1])

    def set_frame(self, frame):
        self._frame = frame
        self._update_image()

    def move(self, x, y):
        self.rect = (x,y, self.rect[2], self.rect[3])

    def step_animation(self):
        self.set_frame((self._frame + 1) % self._num_frames)

    def update(self, dt):
        pass