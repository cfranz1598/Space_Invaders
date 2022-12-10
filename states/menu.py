import pygame
from .base import BaseState, concatinate


class Menu(BaseState):
    def __init__(self, game_assets):
        super(Menu, self).__init__(game_assets)
        self.active_index = 0
        self.options = ["Start Game", "Sound", "Credits", "Quit Game"]

    def render_text(self, index):
        color = pygame.Color(
            "red") if index == self.active_index else pygame.Color("white")
        return self.text_font.render(self.options[index], True, color)

    def get_text_position(self, text, index):
        center = (self.screen_rect.center[0],
                  (self.screen_rect.center[1] - 25) + (index * 50))
        return text.get_rect(center=center)

    def handle_action(self):
        if self.active_index == 0:
            self.done = True
            self.next_state = "GAMESTART"
        elif self.active_index == 1:
            self.done = True
            self.next_state = "SOUND"
        elif self.active_index == 2:
            self.done = True
            self.next_state = "CREDITS"
        elif self.active_index == 3:
            self.quit = True

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                self.active_index -= 1 if self.active_index > 0 else 0
            elif event.key == pygame.K_DOWN:
                self.active_index += 1 if self.active_index < 3 else 0
            elif event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                self.handle_action()

    def draw(self, surface):
        surface.fill("black")
        # draw screen header
        self.show_screen_heading(surface, "Main Menu")

        # Draw Menu Items
        for index, option in enumerate(self.options):
            text_render = self.render_text(index)
            surface.blit(text_render, self.get_text_position(
                text_render, index))

        # Now... put it on the screen
        pygame.display.flip()


# Unit testing stuff, not done in regular game play
if __name__ == "__main__":
    from time import sleep
    from sys import exit
    pygame.init()
    screen_width = 600
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    menu = Menu()
    menu.draw(screen)
    sleep(5)
    pygame.quit()
    exit()
