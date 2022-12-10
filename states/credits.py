import pygame
from .base import BaseState, concatinate


class Credits(BaseState):
    def __init__(self, game_assets):
        super(Credits, self).__init__(game_assets)

    def startup(self, persistent):
        self.persist = persistent

    def handle_action(self):
        self.done = True

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.done = True
                self.next_state = "MENU"

    def update(self, dt):
        pass

    def draw(self, surface):
        surface.fill("black")
        # Space Invaders Logo
        self.show_screen_heading(surface, "Game Credits")

        credits_array = []
        # Game Credits
        credits = self.game_assets.render(
            "comicsans25", "Credit for the original game:", "white")
        credits_rect = self.center_text(credits, offset=(0, -50))
        credits_array.append((credits, credits_rect))

        credits = self.game_assets.render(
            "comicsans25", "Clear Code", "white")
        credits_rect = self.center_text(credits, offset=(0, -25))
        credits_array.append((credits, credits_rect))

        credits = self.game_assets.render(
            "comicsans25", "Youtube: https://www.youtube.com/channel/UCznj32AM2r98hZfTxrRo9bQ", "white")
        credits_rect = self.center_text(credits, offset=(0, 0))
        credits_array.append((credits, credits_rect))

        credits = self.game_assets.render(
            "comicsans25", "GitHub: https://github.com/clear-code-projects/Space-invaders", "white")
        credits_rect = self.center_text(credits, offset=(0, 25))
        credits_array.append((credits, credits_rect))

        credits = self.game_assets.render(
            "comicsans25", "Credit for the state machine code:", "white")
        credits_rect = self.center_text(credits, offset=(0, 75))
        credits_array.append((credits, credits_rect))

        credits = self.game_assets.render(
            "comicsans25", "incompetent_ian", "white")
        credits_rect = self.center_text(credits, offset=(0, 100))
        credits_array.append((credits, credits_rect))

        credits = self.game_assets.render(
            "comicsans25", "YouTube: https://www.youtube.com/channel/UCmRJyLjnQ035ng6XP295zXg", "white")
        credits_rect = self.center_text(credits, offset=(0, 125))
        credits_array.append((credits, credits_rect))

        credits = self.game_assets.render(
            "comicsans25", "GitHub: https://github.com/ianrufus/youtube/pygame-state", "white")
        credits_rect = self.center_text(credits, offset=(0, 150))
        credits_array.append((credits, credits_rect))

        credits = self.game_assets.render(
            "comicsans25", "Credit for this mess:", "white")
        credits_rect = self.center_text(credits, offset=(0, 200))
        credits_array.append((credits, credits_rect))

        credits = self.game_assets.render(
            "comicsans25", "Carl Franz", "blue")
        credits_rect = self.center_text(credits, offset=(0, 225))
        credits_array.append((credits, credits_rect))

        # blit it to the screen
        for credit in credits_array:
            surface.blit(credit[0], credit[1])
