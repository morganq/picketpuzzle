import pygame
import character

class Soldier(character.Character):
    def __init__(self, gx, gy):
        character.Character.__init__(self, "assets/soldier.png", gx, gy, 14)
        self.type = "soldier"
        
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
        contig = self.find_contiguous_soldiers(state.scene)
        if len(state.scene.snake) >= len(contig):
            enough_workers = True
            snake_poss = [(s.gx, s.gy) for s in state.scene.snake]
            for s in contig:
                any_worker_neighbor = False
                for nx,ny in s.get_neighbors(state.scene):
                    if (nx,ny) in snake_poss:
                        any_worker_neighbor = True
                if not any_worker_neighbor:
                    enough_workers = False

            if enough_workers:
                for s in contig:
                    s.kill()
                    state.scene.animatedsprites.remove(s)
                    state.scene.object_grid[s.gy][s.gx] = None
                    state.scene.add_queued_worker()