'''
        Author: Carl Franz
        Name: Pygame Assets
        Date: 02/09/2022
        License: use it, don't use it, whatever

    A method to collect and load all of your pygame assets at once.  I needed
    this for a game I was re-writing and so I generalized it.  You define your
    program/pyame assets in a python dictionary and create an instance of the
    class.  You can then retrieve any asset by the name you gave it in the
    asset dictionary.

    This process will read a dictionary of assets formated as:
    {asset name : (asset type, asset file, font size]), ...}
    where:
        asset name : string - is whatever name you wish to give it
        asset type : string - 'i': image, 'f': font, 's': sound
        asset file : path to the asset including file name
        font size  : if the asset is a font, the font size must be provided

        Note: because of the nature of how pygame handles fonts, if you need a
        particular font in more then one size, you'll need more then one dictionary
        entry.  Sorry.

    At the bottom of this file there is an example after the:  if __name__ == '__main__':

    At some point I'm going to deal with animation in this... later.
'''
import pygame


class PygameAssets():
    """
    Array with associated pygame assets.

    Attributes
    ----------
    assetdict : dictionary
        your assets, what kind and where they are.
        see: modules docstring and example below

    Methods
    -------
    retrieve_asset(name)
        provide the asset name you assigned originally
        return: the asset as pygame likes it
    render(name, string, color)
        will render the string from font dictionary item 'name'
        return: retunds render string ready to blit
    push_font(name, font)
        you can add system fonts to the dictionary
        return: None
    """

    def __init__(self, assetdict):
        self.assets = {}
        for item_name, item in assetdict.items():
            if item[0] == 'i':  # load image
                self.assets[item_name] = [item[0], pygame.image.load(
                    item[1]).convert_alpha()]
            elif item[0] == 'f':  # load font
                self.assets[item_name] = [item[0], pygame.font.Font(
                    item[1], int(item[2]))]
            elif item[0] == 's':  # load audio
                self.assets[item_name] = [item[0], pygame.mixer.Sound(item[1])]
            else:
                # this should be an exception, maybe next time
                print(f'bad asset load type: {item[0]} - item: {item[1]}')

    def retrieve_asset(self, assetname):
        ''' Input: the asset name...
            returns: the asset
        '''
        return self.assets[assetname][1]

    def render(self, assetname, rstring, color):
        ''' This one is merely for convenience
            Input: the asset name
                    string to render
                    color
            returns: a rendered string ready to blit
        '''
        return self.retrieve_asset(assetname).render(rstring, True, color)

    def push_font(self, name, font):
        ''' This one is merely for convenience, all fonts in one place.
            It'll load system fonts into the asset dictionary.
            Input:  the asset name
                    font (pygame.font.SysFont or Font)
            returns: nothing
        '''
        self.assets[name] = ('f', font)


if __name__ == '__main__':
    # an example of the asset doctionary
    example_directory = {
        'an image': ('i', 'graphics/red.png'),
        'a font': ('f', 'font/StarcruiserExpandedSemiItalic-gKeY.ttf', '30'),
        'some music': ('s', 'audio/music.wav'),
        'bad asset': ('b', 'bad asset type'),
    }

    # initalize pygame screen
    pygame.init()
    screen_width = 600
    screen_height = 600
    display = pygame.display.set_mode((screen_width, screen_height))
    screen = pygame.Surface((screen_width, screen_height))
    clock = pygame.time.Clock()

    # Feed the dictionary into the PygameAssets
    assetdict = PygameAssets(example_directory)
    assetdict.push_font('comicsans30', pygame.font.SysFont('comicsans', 30))

    # Retrieve an image by name
    animage = assetdict.retrieve_asset('an image')
    animage_rect = animage.get_rect(center=(300, 200))

    # retriece font/font size by name
    afont = assetdict.render(
        'a font', 'PygameAssets.render', 'white')
    afont_rect = afont.get_rect(center=(300, 300))

    # render from within assetdict name, text, color
    bfont = assetdict.retrieve_asset('a font').render(
        'pygame.font.render', True, 'white')
    bfont_rect = bfont.get_rect(center=(300, 350))

    # render from within assetdict name, text, color
    cfont = assetdict.retrieve_asset('comicsans30').render(
        'using push_font', True, 'white')
    cfont_rect = cfont.get_rect(center=(300, 400))

    # retriece audio asset by name
    music = assetdict.retrieve_asset('some music')
    music.set_volume(0.10)
    music.play(loops=1)

    # pygame event loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        display.fill("black")  # background is grey

        # blit the retrieved assets
        display.blit(animage, animage_rect)  # display the image
        display.blit(afont, afont_rect)     # write the message
        display.blit(bfont, bfont_rect)     # write the message
        display.blit(cfont, cfont_rect)     # write the message

        # display screen
        pygame.display.flip()
        clock.tick(60)

    # pygame bye-bye
    pygame.quit()
