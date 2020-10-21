import pygame
import framesprite
import game
import sound

class CellTower(framesprite.FrameSprite):
    type = "celltower"
    def __init__(self, gx, gy):
        self.gx = gx
        self.gy = gy
        framesprite.FrameSprite.__init__(self, "assets/celltower.png", 12)
        self.rect = (gx * game.TILESIZE, gy * game.TILESIZE - 7, 12, 12)
        self.activated = False    

    def step_animation(self):
        if not self.activated:
            self.set_frame((self._frame + 1) % 2)

    def interact(self, state, worker):
        if not self.activated:
            if state.scene.queued_workers > 0:
                state.scene.queued_workers -= 1
            else:
                state.scene.snake[-1].kill()
                state.scene.snake.pop()     
            sound.play("occupy")       
            self.activated = True
            self._frame = 2
            self._update_image()
            state.activate_tower(self)
        return False