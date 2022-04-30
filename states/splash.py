import pygame
from .base import BaseState


class Splash(BaseState):
    """ Provides the opening screen introducing the game 
        It will hang around for roughly 4 seconds before
        going on the the Main Menu
    """

    def __init__(self, game_assets):
        super(Splash, self).__init__(game_assets)
        self.next_state = "MENU"
        self.time_active = 0

    def splash_screen(self, screen):

        # build the title heading for the screen
        self.show_screen_heading(
            screen, "Alas, poor Xeno, I killed thee well...")

        # Space Invaders Enemies
        railen = self.game_assets.retrieve_asset("alien/red")
        yailen = self.game_assets.retrieve_asset("alien/yellow")
        gailen = self.game_assets.retrieve_asset("alien/green")
        eailen = self.game_assets.retrieve_asset("extra")
        railen_rect = railen.get_rect(center=(150, 300))
        yailen_rect = yailen.get_rect(center=(250, 300))
        gailen_rect = gailen.get_rect(center=(350, 300))
        eailen_rect = eailen.get_rect(center=(450, 300))

        # Space Invaders Enemy kill points
        rtext = self.game_assets.render(
            "sysfont50", "100",  pygame.Color("white"))
        rtext_rect = rtext.get_rect(center=(150, 350))
        ytext = self.game_assets.render(
            "sysfont50", "200", pygame.Color("white"))
        ytext_rect = ytext.get_rect(center=(250, 350))
        gtext = self.game_assets.render(
            "sysfont50", "300", pygame.Color("white"))
        gtext_rect = gtext.get_rect(center=(350, 350))
        etext = self.game_assets.render(
            "sysfont50", "???", pygame.Color("white"))
        etext_rect = etext.get_rect(center=(450, 350))

        # a message from the programmer?
        xx = self.game_assets.render(
            "subtitlefont", "Kill all the little green buggers", pygame.Color("green"))
        xx_rect = xx.get_rect(center=(300, 400))

        # put on screen
        screen.blit(railen, railen_rect)
        screen.blit(yailen, yailen_rect)
        screen.blit(gailen, gailen_rect)
        screen.blit(eailen, eailen_rect)

        screen.blit(rtext, rtext_rect)
        screen.blit(ytext, ytext_rect)
        screen.blit(gtext, gtext_rect)
        screen.blit(etext, etext_rect)

        screen.blit(xx, xx_rect)

        pygame.display.flip()

    def update(self, dt):
        self.time_active += dt
        if self.time_active >= 2000:
            self.done = True

    def draw(self, surface):
        self.splash_screen(surface)
