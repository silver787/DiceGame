from Game.game_constants import *
import tkinter as tk
import pygame


def switch_user(parent, colour, volume):
    if colour == 'blue':
        parent.colour = BLUE
        parent.font_colour = 'white'
        parent.dice = BLUE_DICE
        parent.configure(bg=parent.colour[0])
        pygame.mixer.music.set_volume(volume)

    elif colour == 'green':
        parent.colour = GREEN
        parent.font_colour = 'white'
        parent.dice = GREEN_DICE
        parent.configure(bg=parent.colour[0])
        pygame.mixer.music.set_volume(volume)

    elif colour == 'black':
        parent.colour = BLACK
        parent.font_colour = 'white'
        parent.dice = BLACK_DICE
        parent.configure(bg=parent.colour[0])
        pygame.mixer.music.set_volume(volume)

    elif colour == 'white':
        parent.colour = WHITE
        parent.font_colour = 'white'
        parent.dice = WHITE_DICE
        parent.configure(bg=parent.colour[0])
        pygame.mixer.music.set_volume(volume)

