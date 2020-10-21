import pygame
import framesprite
import game
import sound

class CityHall(framesprite.FrameSprite):
    type = "cityhall"
    def __init__(self, gx, gy):
        self.gx = gx
        self.gy = gy
        framesprite.FrameSprite.__init__(self, "assets/cityhall.png", 12)
        self.rect = (gx * game.TILESIZE, gy * game.TILESIZE-2, 12, 12)
        self.activated = False
        self.step_animation()

    def step_animation(self):
        pass

    def interact(self, state, worker):
        if not self.activated:
            if state.scene.queued_workers > 0:
                state.scene.queued_workers -= 1
            else:
                state.scene.snake[-1].kill()
                state.scene.snake.pop()
            sound.play("occupy")
            self.activated = True
            self._frame = 1
            self._update_image()
        return False