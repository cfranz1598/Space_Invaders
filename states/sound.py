import pygame
from .base import BaseState


class Sound(BaseState):
    def __init__(self, game_assets):
        super(Sound, self).__init__(game_assets)
        self.active_index = 0
        self.next_state = ["MENU"]
        self.slider = 0
        self.volumes = [10, self.persist["vpewpew"], self.persist["vboom"], 50]

    def display_volumes(self, win, rect, volumes, labels, select):
        # print the three Sound level items
        for vol, vols in enumerate(volumes):
            # Sliders
            rrect = (rect[0], rect[1] + (vol * 50), rect[2], rect[3])
            grect = (rect[0], rect[1] + (vol * 50), rect[2] -
                     (rect[2] - (vols * (rect[2] // 100))), rect[3])
            win.fill("red", rrect)
            win.fill("green", grect)
            # Labels
            label_pos = (rect[0] - 136, rect[1] + (vol * 50) + 3)
            win.blit(self.game_assets.render(
                "comicsans25", f"{labels[vol]}: ({vols}%)", "white"), label_pos)

        # put the select asterisk on the correct line
        y_pos = rect[1] + (select * 50)
        win.blit(self.game_assets.render("sysfont60", "*", "red"), (15, y_pos))

    def handle_action(self):
        self.done = True
        self.next_state = "MENU"

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.volumes[self.slider] -= 5
                if self.volumes[self.slider] <= 0:
                    self.volumes[self.slider] = 0
            if event.key == pygame.K_RIGHT:
                self.volumes[self.slider] += 5
                if self.volumes[self.slider] >= 100:
                    self.volumes[self.slider] = 100
            if event.key == pygame.K_UP:
                self.slider -= 1
                if self.slider <= 0:
                    self.slider = 0
            if event.key == pygame.K_DOWN:
                self.slider += 1
                if self.slider >= 3:
                    self.slider = 3
        elif event.type == pygame.KEYUP:
            if event.key in [pygame.K_RETURN, pygame.K_SPACE, pygame.K_ESCAPE]:
                self.handle_action()

    def draw(self, surface):
        # Blank screen of black
        surface.fill("black")
        # Common menu heading
        self.show_screen_heading(surface, "Parameter Settings")
        # Draw the volumn sliders
        self.display_volumes(surface, (175, 215, 400, 25), self.volumes, [
                             "Sound", "PewPew", "KaBooms", " "], self.slider)
        # legends for the Difficulty slider
        surface.blit(self.game_assets.render(
            "comicsans25", ">Easier<", "white"), (175, 395))
        surface.blit(self.game_assets.render(
            "comicsans25", ">Harder<", "white"), (496, 395))

        # Instructions
        surface.blit(self.game_assets.render("comicsans25",
                                             "Up/Down arrows to change Item", "white"), (175, 470))
        surface.blit(self.game_assets.render("comicsans25",
                                             "Left/Right arrows to change value",  "white"), (175, 490))
        surface.blit(self.game_assets.render("comicsans25",
                                             "Escape to return to Main Menu", "white"), (175, 510))

        # flip to display
        pygame.display.flip()
