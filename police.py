import pygame
import character
import game

class Police(character.Character):
    def __init__(self, gx, gy):
        character.Character.__init__(self, "assets/police.png", gx, gy, 12)
        self.type = "police"

    def interact(self, state, worker):
        offset = (self.gx - worker.gx, self.gy - worker.gy)
        check = (self.gx + offset[0], self.gy + offset[1])
        # Either a list of police objects, or empty to indicate a failure to push
        to_push = [self]
        while True:
            # Check if there's another police behind me
            obj = state.scene.object_grid[check[1]][check[0]]
            if obj == None:
                # If not, check if it's empty
                if state.scene.road_grid[check[1]][check[0]] == True:
                    break
                else:
                    to_push = []
                    break
            elif obj.type == "police":
                # If so, that's great, we can add them to the push list
                to_push.append(obj)
            else: 
                # If another object, give up
                to_push = []
                break

            # Advance to the next space
            check = (check[0] + offset[0], check[1] + offset[1])

        if len(to_push) > len(state.scene.snake) + state.scene.queued_workers:
            return False

        for obj in to_push:
            state.scene.object_grid[obj.gy][obj.gx] = None

        for obj in to_push:
            obj.gx += offset[0]
            obj.gy += offset[1]
            obj.move(obj.gx * game.TILESIZE, obj.gy * game.TILESIZE - 6)
            obj.last_move_direction = game.DIRS_FROM_OFFSETS[(-offset[0], -offset[1])]
            obj.step_animation()
            state.scene.object_grid[obj.gy][obj.gx] = obj
            
        
        return len(to_push) > 0

                
        