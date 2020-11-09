import pygame
import character
import game
import levelstates
import framesprite
import sound

DIRS_FROM_OFFSETS = {
    (1,0):0, (0,1):1, (-1,0):2, (0,-1):3
}
OFFSETS_FROM_DIRS = {y:x for x,y in DIRS_FROM_OFFSETS.items()}

class Tank(character.Character):
    def __init__(self, gx, gy):
        character.Character.__init__(self, "assets/tank.png", gx, gy, 16, x_offset=-2)
        self.type = "tank"
        self.fire_obj = None
        self.bullet_obj = None
        self.time = 0
        
    def is_aiming_at_player(self, scene):
        dx = self.gx
        dy = self.gy
        while True:
            dx += OFFSETS_FROM_DIRS[self.last_move_direction][0]
            dy += OFFSETS_FROM_DIRS[self.last_move_direction][1]
            if dx < 0 or dy < 0 or dx >= 20 or dy >= 16:
                return False
            obj = scene.object_grid[dy][dx]
            if obj is not None:
                return False
            snake_poss = [(w.gx, w.gy) for w in scene.snake]
            if (dx, dy) in snake_poss:
                return True
        return False

    def fire(self, scene):
        scene.sm.transition(levelstates.TankFireState(scene, self))
        dx,dy = OFFSETS_FROM_DIRS[self.last_move_direction]
        self.fire_obj = framesprite.FrameSprite("assets/tankfire.png", 12)
        self.fire_obj.set_frame(self.last_move_direction)
        scene.ui_group.add(self.fire_obj)
        off = (0,0)
        if self.last_move_direction == 0: off = (-2, -9)
        elif self.last_move_direction == 1: off = (0, -8)
        elif self.last_move_direction == 2: off = (2, -9)
        elif self.last_move_direction == 3: off = (0, -4)
        self.fire_obj.move((self.gx + dx) * game.TILESIZE + off[0], (self.gy + dy) * game.TILESIZE + off[1])
        self.step_animation = self.post_fire_step_animation
        self.set_frame(self._frame // 2 + 8)

        self.bullet_obj = framesprite.FrameSprite("assets/tankshell.png", 8)
        self.bullet_obj.set_frame(self.last_move_direction)
        scene.ui_group.add(self.bullet_obj)
        off = (0,0)
        if self.last_move_direction == 0: off = (-2, -6)
        elif self.last_move_direction == 1: off = (2, -8)
        elif self.last_move_direction == 2: off = (2, -6)
        elif self.last_move_direction == 3: off = (2, 0)        
        self.bullet_obj.move((self.gx + dx) * game.TILESIZE + off[0], (self.gy + dy) * game.TILESIZE + off[1])
        sound.play("tankfire")

    def post_fire_step_animation(self):
        pass

    def fire_update(self, scene, dt):
        self.time += dt
        if self.time > 0.5:
            self.fire_obj.move(-20, -20)
            self.set_frame(self.last_move_direction * 2)
        dx,dy = OFFSETS_FROM_DIRS[self.last_move_direction]

        s = min(12 + (self.time*3) ** 2 * 20, 256)
        self.bullet_obj.move(self.bullet_obj.rect[0] + dx * dt * s, self.bullet_obj.rect[1] + dy * dt * s)
        yo = 6
        bx,by = ((self.bullet_obj.rect[0] + 4) // game.TILESIZE, (self.bullet_obj.rect[1] + yo) // game.TILESIZE)
        snake_poss = [(w.gx, w.gy) for w in scene.snake]
        if (bx,by) in snake_poss:
            self.bullet_obj.move(-20, -20)
            for w in scene.snake:
                w.move(-20, -20)
            scene.sm.transition(levelstates.Defeat(scene))


    def step(self, scene):
        if self.is_aiming_at_player(scene):
            self.fire(scene)
            return
        nx = self.gx + OFFSETS_FROM_DIRS[self.last_move_direction][0]
        ny = self.gy + OFFSETS_FROM_DIRS[self.last_move_direction][1]
        blocked = False
        next_space = scene.road_grid[ny][nx]
        if next_space:
            next_obj = scene.object_grid[ny][nx]
            if next_obj is None:
                scene.object_grid[self.gy][self.gx] = None
                self.move(nx * game.TILESIZE + self.x_offset, ny * game.TILESIZE - 6)
                self.gx = nx
                self.gy = ny
                scene.object_grid[self.gy][self.gx] = self
            else:
                blocked = True
        else:
            blocked = True

        if blocked:
            self.last_move_direction = (2 + self.last_move_direction) % 4
            self.update_direction()