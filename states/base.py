import pygame


class BaseState(object):

    def __init__(self, game_assets):
        self.done = False
        self.quit = False
        self.next_state = None
        self.screen = pygame.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.screen_width = self.screen_rect.right
        self.screen_height = self.screen_rect.bottom
        self.game_assets = game_assets
        self.persist = {"level": 1, "lives": 5, "score": 0, "vpewpew": 10, "vboom": 10,
                        "plspeed": 5, "pspeed": 400, "aspeed": 900, "espeed": (400, 800)}

        # common menu fonts, why define them a more then once
        self.title_font = self.game_assets.retrieve_asset("titlefont")
        self.subtitle_font = self.game_assets.retrieve_asset("subtitlefont")
        self.text_font = self.game_assets.retrieve_asset("sysfont50")
        self.sfont = self.game_assets.retrieve_asset("sysfont60")
        self.instructions_font = self.game_assets.retrieve_asset("comicsans25")

    def show_screen_heading(self, surface, message):
        # blank screen
        surface.fill(pygame.Color("black"))

        # Draw Title
        title_render = self.title_font.render(
            "Space Invaders", True, pygame.Color("red"))
        surface.blit(title_render, title_render.get_rect(center=(300, 80)))

        # Draw Blurb
        subtitle_render = self.subtitle_font.render(
            message, True, pygame.Color("blue"))
        surface.blit(subtitle_render,
                     subtitle_render.get_rect(center=(300, 150)))

    def center_text(self, text, offset=()):
        offset = offset if offset else (0, 0)
        w = (self.screen_width // 2) + offset[0]
        h = (self.screen_height // 2) + offset[1]
        return text.get_rect(center=(w, h))

    def startup(self, persistent):
        # this is run every time a state is started
        # ie it"s run on state change in "game.py"
        self.persist = persistent

    def get_event(self, event):
        pass

    def update(self, dt):
        pass

    def draw(self, surface):
        pass


def concatinate(font, textlist, colorlist):
    """ process takes an array of strings, and an array of colors,
            renders them in the color and concatinates the results
            into a single 'string' to be blitted to a surface
    """
    # build text surfaces and gather width and height
    text_surfaces = []
    w, h = 0, 0
    for idx, text in enumerate(textlist):
        text_surfaces.append(font.render(text, True, colorlist[idx]))
        w += text_surfaces[idx].get_rect().width
        h = text_surfaces[idx].get_rect().height
    # define surface for final size
    concat_surface = pygame.Surface((w, h + 3))
    concat_surface.fill("black")
    # concatinate text surfaces
    x, y = 0, 0
    for surf in text_surfaces:
        rect = surf.get_rect(topleft=(x, y))
        concat_surface.blit(surf, rect)
        x = rect.right
        y = rect.top
    return concat_surface  # return the surface
