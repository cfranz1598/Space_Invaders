import pygame
from .base import BaseState, concatinate


class GameIntermission(BaseState):
    def __init__(self, game_assets):
        super(GameIntermission, self).__init__(game_assets)

    def startup(self, persistent):
        self.persist = persistent

        # Since we won the game, up the level and if possible up the lives
        self.persist["level"] += 1
        self.persist["lives"] += 1 if self.persist["lives"] < 5 else 0

        # set up timer (3..2..1)
        self.timer = 3
        self.ticker = [pygame.time.get_ticks() + 4000,
                       pygame.time.get_ticks() + 3000,
                       pygame.time.get_ticks() + 2000,
                       pygame.time.get_ticks() + 1000]

    def handle_action(self):
        self.done = True

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.done = True
                self.next_state = "GAMEOVER"

    def update(self, dt):
        pass

    def draw(self, surface):
        surface.fill("black")
        # Space Invaders Logo
        self.show_screen_heading(
            surface, "Intermission")

        # Next Level blurb
        blurb_render = self.sfont.render(
            f"Level completed...", True, "blue")
        surface.blit(blurb_render,
                     blurb_render.get_rect(center=(300, 275)))

        blurb_render = self.leveltext = concatinate(
            self.sfont, ["Level ", f"{self.persist['level']}", " starting in..."], ["blue", "white", "blue"])
        surface.blit(blurb_render,
                     blurb_render.get_rect(center=(300, 325)))

        if pygame.time.get_ticks() >= self.ticker[self.timer]:
            self.timer -= 1
            if self.timer <= 0:
                self.next_state = "GAMEPLAY"
                self.handle_action()

        countdown_render = self.title_font.render(
            f"{self.timer}", True, "white")
        surface.blit(countdown_render,
                     countdown_render.get_rect(center=(300, 425)))


class GameStart(BaseState):
    def __init__(self, game_assets):
        super(GameStart, self).__init__(game_assets)

    def startup(self, persistent):
        self.persist = persistent
        self.timer = 3
        self.ticker = [pygame.time.get_ticks() + 4000,
                       pygame.time.get_ticks() + 3000,
                       pygame.time.get_ticks() + 2000,
                       pygame.time.get_ticks() + 1000]

    def handle_action(self):
        self.done = True

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.next_state = "MENU"
            self.done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.done = True
                self.next_state = "GAMEOVER"
                self.handle_action()

    def update(self, dt):
        pass

    def draw(self, surface):
        surface.fill("black")

        # Space Invaders Title
        self.show_screen_heading(surface, "Game will start momentarially")

        # Next Level blurb
        blurb_render = self.sfont.render(
            f"Starting level {self.persist['level']} in...", True, "blue")
        surface.blit(blurb_render, blurb_render.get_rect(center=(300, 325)))

        if pygame.time.get_ticks() >= self.ticker[self.timer]:
            self.timer -= 1
            if self.timer <= 0:
                self.next_state = "GAMEPLAY"
                self.handle_action()

        countdown_render = self.title_font.render(
            f"{self.timer}", True, "white")
        surface.blit(countdown_render,
                     countdown_render.get_rect(center=(300, 425)))
