import pygame
import framesprite
import game
import sound

class Factory(framesprite.FrameSprite):
    type = "factory"
    def __init__(self, gx, gy):
        self.gx = gx
        self.gy = gy
        framesprite.FrameSprite.__init__(self, "assets/factory.png", 12)
        self.rect = (gx * game.TILESIZE, gy * game.TILESIZE, 12, 12)
        self.activated = False
        self.step_animation()

    def step_animation(self):
        if not self.activated:
            self.set_frame((self._frame + 1) % 3)

    def interact(self, state, worker):
        if not self.activated:
            state.scene.add_queued_worker()
            self.activated = True
            self._frame = 3
            self._update_image()
            sound.play("factory")
        return False