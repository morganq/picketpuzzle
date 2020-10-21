import scene
import pygame
import game
import simplesprite
import framesprite
import random
import text
import levelscene
import sound

LEVELS = [
    ('intro1', 'SEATTLE', 'The Port', (93, 139), 16, 20, 50),
    ('intro2', 'SEATTLE', 'Industrial District', (243, 145), 32, 33, 50), # Simplify
    ('intro3', 'SEATTLE', 'Intro 3', (243, 145), 50, 100, 120), # Simplify a bit
    ('backandforth', 'SEATTLE', 'Back and Forth', (243, 145), 28, 30, 50),
    ('multidrop', 'SEATTLE', 'Multidrop', (243, 145), 50, 100, 120), # make more interesting?
    # Insert a simpler turnaround level
    ('basicturnaround', 'OAKLAND', 'Basic Turnaround', (243, 145), 19, 50, 100), # simplify
    ('extrafacts', 'OAKLAND', 'Extra Factories', (243, 145), 24, 30, 40),
    ('turnaroundtiming', 'OAKLAND', 'Turnaround Timing', (243, 145), 26, 28, 40),
    ('hardturnaround', 'OAKLAND', 'Hard Turnaround', (243, 145), 43, 50, 70),
    ('simplepicker', 'OAKLAND', 'Simple Picker', (243, 145), 37, 40, 50),
    ('harderpicker', 'SANTIAGO', 'Harder Picker', (243, 145), 58, 62, 120),
    ('intropolice', 'SANTIAGO', 'Intro Police', (243, 145), 10, 12, 15),
    ('policeline', 'SANTIAGO', 'Police Line', (243, 145), 25, 30, 40),
    ('policemaneuver', 'SANTIAGO', 'Police Maneuver', (243, 145), 33, 100, 120),
    ('policeavoid', 'SANTIAGO', 'Police Avoid', (243, 145), 40, 45, 50),
    ('multipolice', 'BARCELONA', 'Multi Police', (243, 145), 34, 44, 54),
    ('policeblock', 'BARCELONA', 'Police Block', (243, 145), 22, 25, 32),
    ('policemultihall', 'BARCELONA', 'Police Multi Hall', (243, 145), 45, 50, 55),
    ('introsoldier', 'BARCELONA', 'Intro Soldier', (243, 145), 29, 33, 36),
    ('intromultisoldier', 'BARCELONA', 'Intro Multi Soldier', (243, 145), 63, 70, 85), 
    ('awkwardsoldier', 'ALGIERS', 'Awkward Soldier', (243, 145), 45, 50, 55),
    ('hardsoldierpolice', 'ALGIERS', 'Harder Soldier Police', (243, 145), 70, 80, 90),
    ('complexmultisoldier', 'BARCELONA', 'Complex Multi Soldier', (243, 145), 63, 70, 85),
    ('diagonalroute', 'ALGIERS', 'Diagonal Route', (243, 145), 49, 52, 75),
    ('coplocks', 'ALGIERS', 'Cop Locks', (243, 145), 51, 58, 65),
    ('coplock2', 'ALGIERS', 'Cop Locks 2', (243, 145), 50, 100, 120),
    ('tonsofcops', 'ALGIERS', 'Tons of Cops', (243, 145), 50, 100, 120),
    ('push2copsaround', 'MINSK', 'Push Police Around', (243, 145), 50, 100, 120),
    ('complex1', 'MINSK', 'Complex 1', (243, 145), 50, 100, 120),
    ('pods', 'MINSK', 'Pods', (243, 145), 58, 70, 85),
    ('introtower', 'MINSK', 'Intro Tower', (243, 145), 50, 100, 120),
    ('tower2', 'MINSK', 'Tower 2', (243, 145), 50, 100, 120),
    # unstick police from corners or t-junction.
    ('rearrangesoldiers', 'MINSK', 'Rearrange Soldiers', (0,0), (30, 40, 50)),
    # Undo one-way police valve.
    ('breakupcops', 'MINSK', 'Breakup Cops', (0,0), (59, 65, 90)),
    ('twotowers', 'MINSK', 'Two Towers', (0,0), (35, 42, 50)),
    ('towerring', 'MINSK', 'Tower Ring', (0,0), (60, 65, 70)),
    ('towercomplex', 'MINSK', 'Tower Complex', (0,0), (50, 60, 70)),
    ('twotowercomplex', 'MINSK', 'Two Tower Complex', (0,0), (50, 60, 70)),
    ('dividesoldiers', 'MINSK', 'Divide Soldiers', (0,0), (50, 60, 70)),
    ('complex2', 'MINSK', 'Complex 1', (243, 145), 50, 100, 120),
    # Fancy complicated blocks of police can be managable, use up more than one worker to take multiple steps…
]
# SEATTLE, OAKLAND, SANTIAGO, BARCELONA, ALGIERS, MINSK, TEHRAN, MUMBAI, HONG KONG, BEIJING

print(len(LEVELS))

for i,l in enumerate(LEVELS):
    row = list(LEVELS[i])
    row[3] = (93 + i * 30, 139)
    LEVELS[i] = row


MAP_SPOTS = []
for y in range(5):
    MAP_SPOTS.append([])
    for x in range(10):
        MAP_SPOTS[-1].append((x * 110 + 30, y * 90 + 30))
    

class WorldMapScene(scene.Scene):
    def __init__(self, game, level_index):
        scene.Scene.__init__(self, game)
        self.starting_level_index = level_index or 0


    def start(self):
        self.scroll = (0,0)
        self.back_group = pygame.sprite.Group()
        self.fore_group = pygame.sprite.Group()
        self.levelobjs = []
        self.map = simplesprite.SimpleSprite("assets/worldmap.png", (0,0))
        self.back_group.add(self.map)

        for i,level in enumerate(LEVELS):
            x,y = level[3][0], level[3][1]
            obj = framesprite.FrameSprite("assets/mapflag.png", 12)
            if self.game.save.get_level_state(i)['beaten']:
                obj.set_frame(1)
            obj.move(x - 6,y - 10)
            self.levelobjs.append((obj, level))
            self.back_group.add(obj)

        self.popup_sprites = []

        arrow = framesprite.FrameSprite("assets/selectarrow.png", 9)
        arrow.move(117, 136)
        self.fore_group.add(arrow)

        overlay = simplesprite.SimpleSprite("assets/mapoverlay.png", (0,0))
        self.fore_group.add(overlay)
        self.selected_level = self.starting_level_index
        self.update_selection()

    def render(self):
        self.game.screen.fill(game.BGCOLOR)
        scrollsurf = pygame.Surface(self.map.image.get_size())
        self.back_group.draw(scrollsurf)
        self.game.screen.blit(scrollsurf, (-self.scroll[0], -self.scroll[1]))
        self.fore_group.draw(self.game.screen)

    def update_selection(self):
        (lvl, name1, name2, pos, *extras) = LEVELS[self.selected_level]

        self.scroll = (pos[0] - 120, pos[1] - 130)

        self.back_group.remove(self.popup_sprites)
        self.popup_sprites = []
        
        y = self.scroll[1] + 10
        w,h = (text.FONTS['big'].get_rect(name1)[2] + 12, 50)
        w2 = text.FONTS['small'].get_rect(name2)[2] + 12
        w = max(w, w2, 120)
        x = self.scroll[0] + 120 - w / 2
        city = text.Text(name1, "big", (x + 5, y + 5), color=(game.BGCOLOR), border=False)
        background = pygame.sprite.Sprite()
        
        background.image = pygame.Surface((w,h))
        background.rect = (x, y, background.image.get_size()[0] + 10, background.image.get_size()[1])
        background.image.fill((247, 249, 223))
        pygame.draw.rect(background.image, game.BGCOLOR, (1,1, w-2, h-2), 1)
        desc = text.Text(name2, "small", (x+5, y+21), color=(game.BGCOLOR), border=False)

        self.popup_sprites.append(background)
        self.popup_sprites.append(city)
        self.popup_sprites.append(desc)

        savestate = self.game.save.get_level_state(self.selected_level)

        for i in range(3):
            star = framesprite.FrameSprite("assets/star.png",13)
            star.move(x + 6 + i * 15, y + 32)
            if i < savestate['stars']:
                star.set_frame(1)
            self.popup_sprites.append(star)

        if savestate['beaten']:
            steptext = "%d Steps" % savestate['steps']
            stepwidth = text.FONTS['small'].get_rect(steptext)[2]
            steps = text.Text(steptext, "small", (x + w - 6 - stepwidth, y + 35), color=(game.BGCOLOR),border=False)
            self.popup_sprites.append(steps)

        self.back_group.add(self.popup_sprites)        

    def take_input(self, inp, event):
        if inp == "right":
            self.selected_level = min(self.selected_level + 1, len(LEVELS)-1)
            self.update_selection()
            sound.play("blip")

        elif inp == "left":
            self.selected_level = max(self.selected_level - 1, 0)
            self.update_selection()
            sound.play("blip")

        elif inp == "action":
            sound.play("step2")
            self.game.start_level(LEVELS[self.selected_level][0], self.selected_level)

        elif inp == "other":
            if event.key == pygame.K_c:
                self.game.save.level_state = {}
                
            if event.key == pygame.K_b:
                self.game.save.set_level_state(self.selected_level, True, 1, 3)

            if event.key == pygame.K_s:
                self.game.save.save()
                self.game.return_to_map()
                