"""
    The 'state machine' portion is from:
        YouTube Tutorial: https://www.youtube.com/watch?v=PZTqfag3T7M&t=16s
        "incompetent_ian" on YouTube: https://www.youtube.com/channel/UCmRJyLjnQ035ng6XP295zXg
        Github Respository: https://github.com/ianrufus/youtube/pygame-state

    The 'Space Invaders' game is (with enhancements and changes) cribbed from:
		YouTube Tutorial: https://www.youtube.com/watch?v=o-6pADy5Mdg&t=3219s 
		"Clear Code" on YouTube: https://www.youtube.com/channel/UCznj32AM2r98hZfTxrRo9bQ
		Github Respository: https://github.com/clear-code-projects/Space-invaders

    I needed something to add pizzazz to a Space Invaders game.  I wanted a splash 
    screen, menu, parameter mod screen, Game Start, Level screen, and Game End screen.
    Should be straight forward as there is no win or loss screen, in the end you 
    either leave the game in the middle or lose.  What matters is points scored when 
    you finally die.  That's the 70s for you.  Play until you die.

    The idea behind this is to process from:
    Splash Screen ==> Main Menu. You then have four choices to either  GamePlay, 
    ModifyParameters, ShowCredits, Quit.  GamePlay goes to GameStart and into the 
    actual game. That takes you to either LevelComplete or GameEnd when you finally die.  
    From there you can restart the game, go back to the Main Menu, or end the program.
    
    I truely do invite you to examine 'state machine' by "incompetent_ian".  It's almost perfect.  It's 
    only issue is that it does not execute the 'startup' function for the first state.  I fixed a lot of
    stuff, this one is up to you.
"""

import pygame
from game import Game
from states.pygameassets import PygameAssets
from states.splash import Splash
from states.game_over import GameOver
from states.gameplay import GamePlay
from states.intermission import GameIntermission, GameStart
from states.sound import Sound
from states.credits import Credits
from states.menu import Menu


# initialize pygame and display screen
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Space Invaders")

# list of assets and where they are - goes into PygameAssets class
game_assets_list = {
    "alien/red": ("i", "graphics/red.png"),
    "alien/yellow": ("i", "graphics/yellow.png"),
    "alien/green": ("i", "graphics/green.png"),
    "playerOK": ("i", "graphics/player_ok.png"),
    "playerHIT": ("i", "graphics/player_hit.png"),
    "extra": ("i", "graphics/extra.png"),
    "titlefont": ("f", "font/StarcruiserExpandedSemiItalic-gKeY.ttf", "50"),
    "subtitlefont": ("f", "font/SwordskullPersonalUse-axqz5.ttf", "50"),
    "music": ("s", "audio/music.wav"),
    "pewpew": ("s", "audio/laser.wav"),
    "boom": ("s", "audio/explosion.wav"),
}

# make asset dictionary
game_assets = PygameAssets(game_assets_list)
# add system fonts to asset dictionary... just for convenience
game_assets.push_font("sysfont60", pygame.font.SysFont(None, 60))
game_assets.push_font("sysfont50",  pygame.font.SysFont(None, 50))
game_assets.push_font("comicsans65", pygame.font.SysFont("comicsans", 65))
game_assets.push_font("comicsans25", pygame.font.SysFont("comicsans", 25))

# these are available states for the Space Invaders game system.
states = {
    "SPLASH": Splash(game_assets),   # Startup Splash Screen
    "MENU": Menu(game_assets),  # Main Menu
    "SOUND": Sound(game_assets),  # Game Parameter Adjustments
    "CREDITS": Credits(game_assets),  # Game etc. credits screen
    "GAMESTART": GameStart(game_assets),  # Game start screen
    "GAMEPLAY": GamePlay(game_assets),  # The Space Invaders game itself    
    "GAMELEVEL": GameIntermission(game_assets),  # Game between levels break
    "GAMEOVER": GameOver(game_assets),  # Game over/you lose screen
}

game = Game(screen, states, "SPLASH")
game.run()

pygame.quit()
