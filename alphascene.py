import game
import pygame
import text
import scene
import menuscene

class AlphaScene(scene.Scene):
    def start(self):
        self.group = pygame.sprite.Group()
        self.group.add(text.Text("This game is in ALPHA.", "small", (10, 20)))
        self.group.add(text.Text("There are likely bugs, puzzles which are", "small", (10, 32)))
        self.group.add(text.Text("too hard or too easy, and uses stolen music!", "small", (10, 44)))

        self.group.add(text.Text("Please let me know what you think:", "small", (10, 80)))
        self.group.add(text.Text("morganquirk@gmail.com", "small", (10, 92)))

        self.group.add(text.Text("Press Space to continue.", "small", (10, 120)))

    def take_input(self, inp, event):
        if inp == "action":
            self.game.scene = menuscene.MenuScene(self.game)
            self.game.scene.start()

    def render(self):
        self.game.screen.fill(game.BGCOLOR)
        self.group.draw(self.game.screen)