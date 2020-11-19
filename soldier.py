import pygame
import character
import sound
import game

class Soldier(character.Character):
    def __init__(self, gx, gy):
        character.Character.__init__(self, "assets/soldier.png", gx, gy, 14)
        self.type = "soldier"
        self.state = "stand"
        self.state_time = 0
        
    def get_neighbors(self, game):
        x,y = self.gx, self.gy
        n = []
        if x > 0: n.append((x-1,y))
        if y > 0: n.append((x,y-1))
        if x < len(game.object_grid[0]) - 1: n.append((x+1,y))
        if y < len(game.object_grid) - 1: n.append((x,y+1))
        return n

    def find_contiguous_soldiers(self, game):
        open = self.get_neighbors(game)
        closed = [(self.gx, self.gy)]
        soldiers = [self]
        for (gx,gy) in open:
            if (gx,gy) in closed:
                continue
            obj = game.object_grid[gy][gx]
            if obj and obj.type == "soldier":
                soldiers.append(obj)
                open.extend(obj.get_neighbors(game))
                closed.append((gx,gy))
        return soldiers

    def interact(self, state, worker):
        soldier_group = self.find_contiguous_soldiers(state.scene)
        
        enough_workers = True
        snake_poss = [(s.gx, s.gy) for s in state.scene.snake]
        for s in soldier_group:
            any_worker_neighbor = False
            for nx,ny in s.get_neighbors(state.scene):
                if (nx,ny) in snake_poss:
                    any_worker_neighbor = True
                    s.state = "disarm"
                    s.state_time = 0.5
                    dx = nx - s.gx
                    dy = ny - s.gy
                    s.last_move_direction = game.DIRS_FROM_OFFSETS[(dx, dy)]
            if not any_worker_neighbor:
                enough_workers = False
            
        if len(state.scene.snake) < len(soldier_group):
            enough_workers = False

        if enough_workers:
            sound.play("soldier")
            for s in soldier_group:
                state.scene.object_grid[s.gy][s.gx] = None
                state.scene.add_queued_worker()
                state.scene.animatedsprites.remove(s)
                s.state = "won"
                s.state_time = 0.2
        else:
            sound.play("cannot")

    def update(self, dt):
        character.Character.update(self,dt)
        if self.state == "disarm" or self.state == "won":
            self.set_frame(self.last_move_direction + 8)
            self.state_time -= dt
            if self.state_time < 0:
                if self.state == "disarm":
                    self.state = "standing"
                    self.step_animation()
                    self.update_direction()
                elif self.state == "won":
                    self.kill()
                    
