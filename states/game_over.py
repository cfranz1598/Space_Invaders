import pygame
from .base import BaseState, concatinate


class GameOver(BaseState):
    def __init__(self, game_assets):
        super(GameOver, self).__init__(game_assets)
        self.startup({"score": 0, "level": 0})

    def startup(self, persistent):
        self.persist = persistent

        # Game Over
        self.title = concatinate(
            self.game_assets.retrieve_asset("sysfont50"), ["Game Over - ", "You Lost"],  ["white", "red"])
        self.title_rect = self.center_text(self.title, offset=(0, -30))

        # player score
        self.scoretext = concatinate(
            self.game_assets.retrieve_asset("sysfont50"), ["Score: ", f"{self.persist['score']}"],  ["blue", "white"])
        self.scoretext_rect = self.center_text(self.scoretext, offset=(0, 50))

        # player leveltext
        self.leveltext = concatinate(
            self.game_assets.retrieve_asset("sysfont50"), ["You lost on level ", f"{self.persist['level']}"],  ["blue", "white"])
        self.leveltext_rect = self.center_text(self.leveltext, offset=(0, 90))

        # User Instructions - line 1
        self.instructions = self.game_assets.render(
            "comicsans25", "Press SPACE to restart game,", "white")
        self.instructions_rect = self.center_text(
            self.instructions, offset=(0, 150))

        # User Instructions - line 2
        self.instructions1 = self.game_assets.render(
            "comicsans25", "or ENTER to return to the menu", "white")
        self.instructions1_rect = self.center_text(
            self.instructions1, offset=(0, 170))

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RETURN:
                self.next_state = "MENU"
                self.done = True
            elif event.key == pygame.K_SPACE:
                self.next_state = "GAMEPLAY"
                self.done = True
            elif event.key == pygame.K_ESCAPE:
                self.quit = True

    def draw(self, surface):

        surface.fill("black")

        # Space Invaders Logo
        self.show_screen_heading(
            surface, "Died alone--- in the dark--- you did.")

        # rest of the screen title and instructions
        surface.blit(self.title, self.title_rect)
        surface.blit(self.scoretext, self.scoretext_rect)
        surface.blit(self.leveltext, self.leveltext_rect)
        surface.blit(self.instructions, self.instructions_rect)
        surface.blit(self.instructions1, self.instructions1_rect)

        # Now... put it on the screen
        pygame.display.flip()
