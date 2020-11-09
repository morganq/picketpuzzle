from states import State
import framesprite
import worker
import game
import text
import csv
import math
import pygame
import sound
from resources import resource_path

def autotile_around(scene, cx, cy):
    w = len(scene.tilemap._grid[0])
    h = len(scene.tilemap._grid)
    for x in range(max(cx - 1,0), min(cx + 2, w)):
        for y in range(max(cy - 1,0), min(cy + 2,h)):
            if scene.tilemap._grid[y][x] in game.ROADTILES:
                autotile(scene, x, y)

def autotile(scene, gx, gy):
    w = len(scene.tilemap._grid[0])
    h = len(scene.tilemap._grid)        
    def is_road(x,y):
        if x < 0 or y < 0 or x >= w or y >= h:
            return False
        else:
            return scene.tilemap._grid[y][x] in game.ROADTILES + [16]
    around = (
        is_road(gx - 1, gy), is_road(gx, gy - 1), is_road(gx + 1, gy), is_road(gx, gy + 1)
    )
    if around in AUTODEF:
        scene.tilemap.set_tile(gx, gy, AUTODEF[around])


DIRS_FROM_OFFSETS = {
    (1,0):0, (0,1):1, (-1,0):2, (0,-1):3
}
OFFSETS_FROM_DIRS = {y:x for x,y in DIRS_FROM_OFFSETS.items()}

class Tutorial(State):
    def __init__(self, scene, tutorial):
        State.__init__(self, scene)
        self.tutorial = tutorial

    def enter(self):
        self.tutorial.initialize(self.scene)

    def take_input(self, input, event):
        if input == "action":
            self.scene.sm.transition(self.scene.get_starting_state())

    def exit(self):
        self.tutorial.cleanup()

class PickFactory(State):
    def __init__(self, scene):
        State.__init__(self, scene)
        self.factory_index = 0
        self.selection = None

    def enter(self):
        self.selection = framesprite.FrameSprite("assets/cursor.png", 16)
        self.scene.ui_group.add(self.selection)
        self.scene.animatedsprites.append(self.selection)
        self.update_selection()

    def exit(self):
        f = self.scene.factories[self.factory_index]
        f.set_frame(3)
        f.activated = True

        w = worker.Worker(f.gx, f.gy)
        self.scene.snake = [w]

        self.selection.kill()
        self.scene.animatedsprites.remove(self.selection)

    def take_input(self, input, event):
        if input == "left":
            self.factory_index = (self.factory_index - 1) % len(self.scene.factories)
            self.update_selection()
            sound.play("blip")
        elif input == "right":
            self.factory_index = (self.factory_index + 1) % len(self.scene.factories)
            self.update_selection()
            sound.play("blip")
        elif input == "action": self.scene.sm.transition(March(self.scene))
        elif input == "click": self.scene.sm.transition(Edit(self.scene))
        elif input == "back":
            self.exit()
            self.scene.game.return_to_map()        

    def update_selection(self):
        f = self.scene.factories[self.factory_index]
        self.selection.move(f.rect[0] - 2, f.rect[1] - 2)


class March(State):
    def enter(self):
        sound.play("factory")
        self.num_steps = 0
        w = self.scene.snake[0]
        self.scene.game_group.add(w)
        self.scene.animatedsprites.append(w)

        self.flag = framesprite.FrameSprite("assets/flag.png", 12)
        self.scene.game_group.add(self.flag)
        self.scene.animatedsprites.append(self.flag)

        self.steps = text.Text("0", "small", (0,0))
        self.scene.ui_group.add(self.steps)

        self.position_extras()

        self.enemies_to_control = []

        self.cell_arrow = framesprite.FrameSprite("assets/cellarrow.png", 9)
        self.cell_arrow.move(-10,-10)
        self.scene.ui_group.add(self.cell_arrow)
        self.scene.animatedsprites.append(self.cell_arrow)

        self.update_steps()

    def position_extras(self):
        self.flag.rect = (self.scene.snake[0].rect[0] - 2, self.scene.snake[0].rect[1] - 7, self.flag.rect[2], self.flag.rect[3])
        self.steps.set_pos(self.scene.snake[0].rect[0] + 9, self.scene.snake[0].rect[1] - 4)

    def take_input(self, input, event):
        w = self.scene.snake[0]
        if input == "left": self.try_move(w.gx - 1, w.gy, 2)
        elif input == "right":  self.try_move(w.gx + 1, w.gy, 0)
        elif input == "up":  self.try_move(w.gx, w.gy - 1, 3)
        elif input == "down":  self.try_move(w.gx, w.gy + 1, 1)
        elif input == "action":
            if self.enemies_to_control:
                self.step_enemy(None, None)
            #else:
            #    self.scene.load()
            #    self.scene.initialize_state()
        elif input == "click": self.scene.sm.transition(Edit(self.scene))
        elif input == "back":
            self.exit()
            self.scene.game.return_to_map()
        elif input == "other" and event.key == pygame.K_r:
            self.scene.load()
            self.scene.initialize_state()            

    def step_enemy(self, enemy, dir):
        if enemy is None:
            moved = True
        else:
            dx, dy = OFFSETS_FROM_DIRS[dir]
            tx = enemy.gx + dx
            ty = enemy.gy + dy
            moved = False
            w = len(self.scene.road_grid[0])
            h = len(self.scene.road_grid)
            if tx >= 0 and tx < w and ty >= 0 and ty < h:
                worker_poss = [(w.gx, w.gy) for w in self.scene.snake]
                o = self.scene.object_grid[ty][tx]
                if o == None and (tx,ty) not in worker_poss:
                    destructable = (self.scene.tilemap._grid[ty][tx] == 16 and enemy.type == "tank")
                    if self.scene.road_grid[ty][tx] == True or destructable:
                        self.scene.object_grid[enemy.gy][enemy.gx] = None
                        enemy.gx = tx
                        enemy.gy = ty
                        enemy.move(tx * game.TILESIZE + enemy.x_offset, ty * game.TILESIZE - 6)
                        enemy.last_move_direction = dir
                        enemy.update_direction()
                        self.scene.object_grid[enemy.gy][enemy.gx] = enemy
                        moved = True
                        sound.play("step0")
                    if destructable:
                        self.scene.tilemap.set_tile(tx, ty, 15)
                        self.scene.road_grid[ty][tx] = True
                        autotile_around(self.scene, tx, ty)

            
        if moved:
            self.enemies_to_control.pop(0)
            if self.enemies_to_control:
                sound.play("cell")
                self.cell_arrow.move(self.enemies_to_control[0].rect[0] + 2, self.enemies_to_control[0].rect[1] - 10)
            else:
                self.cell_arrow.move(-10, -10)
                self.scene.overlay.set_frame(0)
        else:
            sound.play("cannot")
            

    def activate_tower(self, tower):
        enemies = []
        for row in self.scene.object_grid:
            for cell in row:
                if cell and (cell.type == "soldier" or cell.type == "police" or cell.type == "tank"):
                    enemies.append(cell)
        def dist(e):
            return math.sqrt((e.gx - tower.gx) ** 2 + (e.gy - tower.gy) ** 2)
        enemies.sort(key=dist)
        self.enemies_to_control = enemies
        if self.enemies_to_control:
            self.cell_arrow.move(self.enemies_to_control[0].rect[0] + 2, self.enemies_to_control[0].rect[1] - 10)
            sound.play("cell")
            self.scene.overlay.set_frame(1)


    def try_move(self, tx, ty, dir):
        # If we used cell tower and are controlling an enemy...
        if self.enemies_to_control:
            self.step_enemy(self.enemies_to_control[0], dir)
            return

        w = self.scene.snake[0]
        o = self.scene.object_grid[ty][tx]
        if o == None:
            self.move(tx, ty, dir)
        else:
            did_push = o.interact(self, w)
            if len(self.scene.snake) == 0:
                if all([f.activated for f in self.scene.cityhalls]):
                    self.scene.sm.transition(Victory(self.scene, self.num_steps))
                else:
                    self.scene.sm.transition(Defeat(self.scene))
                return
            if did_push:
                self.move(tx, ty, dir)

    def move_tanks(self):
        for tank in self.scene.tanks:
            tank.step(self.scene)


    def move(self, tx, ty, dir):
        w = len(self.scene.road_grid[0])
        h = len(self.scene.road_grid)
        if tx >= 0 and tx < w and ty >= 0 and ty < h:
            if self.scene.road_grid[ty][tx] == True and self.scene.object_grid[ty][tx] == None:
                # Check if we're trying to double-back and we have a tail
                if len(self.scene.snake) > 1:
                    if self.scene.snake[1].gx == tx and self.scene.snake[1].gy == ty:
                        sound.play("cannot")
                        return # Don't move

                # Figure out the positions of the new snake
                new_snake_spots = []
                new_snake_spots.append((tx, ty, dir))
                for i in range(1, len(self.scene.snake)):
                    cur = self.scene.snake[i]
                    next = self.scene.snake[i-1]
                    offset = (next.gx - cur.gx, next.gy - cur.gy)
                    new_snake_spots.append((next.gx, next.gy, DIRS_FROM_OFFSETS[offset]))

                # If the place we're trying to go is occupied in the new arrangement of the snake, we can't do it
                q = [(x,y) for (x,y,z) in new_snake_spots]
                if (tx,ty) not in q[1:]:
                    add_worker = None
                    # Add a queued worker to the end of the tail
                    if self.scene.queued_workers > 0:
                        self.scene.remove_queued_worker()
                        add_worker = worker.Worker(self.scene.snake[-1].gx, self.scene.snake[-1].gy)
                        self.scene.game_group.add(add_worker)
                        self.scene.animatedsprites.append(add_worker)                        

                    for i,cell in enumerate(self.scene.snake):
                        ss = new_snake_spots[i]
                        cell.gx = ss[0]
                        cell.gy = ss[1]
                        cell.move(ss[0] * game.TILESIZE, ss[1] * game.TILESIZE - 6)
                        cell.last_move_direction = ss[2]
                        cell.update_direction()

                    # Actually add to the snake now, so it's not processed by the above loop
                    if add_worker:
                        offset = (self.scene.snake[-1].gx - add_worker.gx, self.scene.snake[-1].gy - add_worker.gy)
                        add_worker.last_move_direction = DIRS_FROM_OFFSETS[offset]
                        add_worker.update_direction()
                        self.scene.snake.append(add_worker)

                    self.num_steps += 1
                    self.update_steps()
                    if len(self.scene.snake) > 2:
                        sound.play("step2")
                    elif len(self.scene.snake) > 1:
                        sound.play("step1")
                    else:
                        sound.play("step0")
                    self.move_tanks()
            else:
                sound.play("cannot")
                        
        self.position_extras()

    def update_steps(self):
        max_steps = self.scene.game.get_max_steps()
        if max_steps == 0:
            self.steps.set_text(str(self.num_steps))
        else:
            steps_left = max_steps - self.num_steps
            if steps_left < 10:
                self.steps.color = (255,213,17)
            if steps_left <= -1:
                self.scene.sm.transition(Defeat(self.scene))
            self.steps.set_text(str(steps_left))

    def exit(self):
        if self.flag in self.scene.animatedsprites:
            self.scene.animatedsprites.remove(self.flag)
            self.flag.kill()
            self.steps.kill()
        self.scene.overlay.kill()


AUTODEF = {
# (L, U, R, D): tile index
    (1,0,0,0): 12,
    (0,1,0,0): 13,
    (0,0,1,0): 14,
    (0,0,0,1): 11,
    (1,1,0,0):4,
    (0,1,1,0):5,
    (0,0,1,1):6,
    (1,0,0,1):3,
    (1,0,1,0):1,
    (0,1,0,1):2,
    (1,1,1,0):10,
    (0,1,1,1):7,
    (1,0,1,1):8,
    (1,1,0,1):9,
    (1,1,1,1):15,
}
class Edit(State):
    def take_input(self, inp, event):
        if inp == "click": 
            pos = (event.pos[0] // game.TILESIZE // game.SCALE, event.pos[1] // game.TILESIZE // game.SCALE)
            self.place(*pos)
        elif inp == "rightclick":
            pos = (event.pos[0] // game.TILESIZE // game.SCALE, event.pos[1] // game.TILESIZE // game.SCALE)
            self.place_obj(self.tileselect._frame, *pos)

        elif inp == "back":
            self.exit()
            self.scene.initialize_state()
        elif inp == "right":
            self.tileselect.set_frame((self.tileselect._frame + 1) % len(game.OBJ))
        elif inp == "left":
            self.tileselect.set_frame((self.tileselect._frame - 1) % len(game.OBJ))    
        elif inp == "up":
            self.deco = (self.deco - 1) % (len(game.DECOTILES) + 1)
            if self.deco == 0:
                self.decoselect.set_frame(15)
            else:
                self.decoselect.set_frame(self.deco - 1 + game.DECOTILES[0])
        elif inp == "down":
            self.deco = (self.deco + 1) % (len(game.DECOTILES) + 1)
            if self.deco == 0:
                self.decoselect.set_frame(15)
            else:
                self.decoselect.set_frame(self.deco - 1 + game.DECOTILES[0])
        elif inp == "action":
            print(self.scene.level_file)
            fn = input()
            self.save(fn)

        elif inp == "other":
            if event.key == pygame.K_j: self.shift(-1,0)
            if event.key == pygame.K_i: self.shift(0,-1)
            if event.key == pygame.K_l: self.shift(1,0)
            if event.key == pygame.K_k: self.shift(0,1)

    def shift(self, dx, dy):
        w = len(self.scene.tilemap._grid[0])
        h = len(self.scene.tilemap._grid)
        tg = []
        og = []
        for y in range(h):
            tg.append([])
            og.append([])
            for x in range(w):
                tv = 0
                ov = 0
                if y - dy >= 0 and y - dy < h and x - dx >= 0 and x - dx < w:
                    tv = self.scene.tilemap._grid[y - dy][x - dx]
                    ov = self.scene.object_grid[y - dy][x - dx]
                    if ov:
                        ov.rect = (ov.rect[0] + dx * 12, ov.rect[1] + dy * 12, ov.rect[2], ov.rect[3])
                tg[-1].append(tv)
                og[-1].append(ov)

        self.scene.tilemap._grid = tg
        self.scene.tilemap.invalidate()
        self.scene.tilemap.update_image()
        self.scene.object_grid = og

    def save(self, name):
        w = len(self.scene.tilemap._grid[0])
        h = len(self.scene.tilemap._grid)
        f1 = open(resource_path("levels/%s_tiles.csv" % name), "w")
        f2 = open(resource_path("levels/%s_objects.csv" % name), "w")
        tile_writer = csv.writer(f1)
        object_writer = csv.writer(f2)
        for y in range(h):
            tile_row = []
            object_row = []
            for x in range(w):
                tile_row.append(str(self.scene.tilemap._grid[y][x]))
                obj = self.scene.object_grid[y][x]
                obj_value = -1
                if obj:
                    obj_value = game.OBJ[obj.type]

                object_row.append(str(obj_value))
                
            tile_writer.writerow(tile_row)
            object_writer.writerow(object_row)

        f1.close()
        f2.close()

    def place_obj(self, obj, gx, gy):
        if self.scene.object_grid[gy][gx]:
            o = self.scene.object_grid[gy][gx]
            o.kill()
            self.scene.object_grid[gy][gx] = None
        else:
            self.scene.place_obj_by_index(obj, gx, gy)

    def place(self, gx, gy):
        if self.deco == 0:
            if self.scene.tilemap._grid[gy][gx] in game.ROADTILES:
                self.scene.tilemap.set_tile(gx, gy, 0)
            else:
                self.scene.tilemap.set_tile(gx, gy, 1)
            self.autotile_around(gx, gy)
        else:
            if self.scene.tilemap._grid[gy][gx] == self.decoselect._frame:
                self.scene.tilemap.set_tile(gx, gy, 0)
            else:
                self.scene.tilemap.set_tile(gx, gy, self.decoselect._frame)
            if self.deco == 1:
                self.autotile_around(gx,gy)

    def autotile_around(self, cx, cy):
        autotile_around(self.scene, cx, cy)

    def exit(self):
        self.save("temp")

        self.scene.ui_group.remove(self.tileselect)
        self.scene.ui_group.remove(self.decoselect)
        # Save tiles and objects
        # Reload objects
        self.scene.level_file = "temp"
        self.scene.load()

    def enter(self):
        self.scene.load()
        self.tileselect = framesprite.FrameSprite("assets/objects.png", 12)
        self.scene.ui_group.add(self.tileselect)
        self.decoselect = framesprite.FrameSprite("assets/tiles.png", 12)
        self.scene.ui_group.add(self.decoselect)
        self.decoselect.rect = (0, 12, self.decoselect.rect[2], self.decoselect.rect[3])
        self.decoselect.set_frame(15)
        self.deco = 0



class Victory(State):
    def __init__(self, scene, num_steps):
        State.__init__(self, scene)
        self.num_steps = num_steps

    def enter(self):
        self.wintext = text.Text("Victory!", "huge", (50, -20))
        self.wintext_t = 0
        self.scene.ui_group.add(self.wintext)
        self.scene.game.record_victory(self.num_steps)
        sound.play_music('victory', 0)

    def update(self, dt):
        self.wintext_t += dt
        y = ( - math.cos(min(self.wintext_t,1) * 3.14159) * 0.5 + 0.5) ** 1.5 * 102 - 20
        self.wintext.set_pos(self.wintext.rect[0], y)

        if self.wintext_t > 3:
            self.exit()
            self.scene.game.return_to_map(won=True)

    def take_input(self, input, event):
        if input == "click": 
            self.scene.sm.transition(Edit(self.scene))


class Defeat(State):
    def enter(self):
        self.deftext = text.Text("Defeat...", "huge", (55, -20))
        self.deftext_t = 0
        self.scene.ui_group.add(self.deftext)
        sound.play("defeat")

    def update(self, dt):
        self.deftext_t += dt
        y = ( - math.cos(min(self.deftext_t,1) * 3.14159) * 0.5 + 0.5) ** 1.5 * 102 - 20
        self.deftext.set_pos(self.deftext.rect[0], y)

        if self.deftext_t > 3:
            self.exit()
            self.scene.load()
            self.scene.initialize_state()

    def take_input(self, input, event):
        if input == "click": 
            self.scene.sm.transition(Edit(self.scene))    

class TankFireState(State):
    def __init__(self, scene, tank):
        self.tank = tank
        State.__init__(self, scene)

    def update(self, dt):
        self.tank.fire_update(self.scene, dt)