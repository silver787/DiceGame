BLUE = ["#b2dfde", "#5cbdbc"]
GREEN = ["#9ec98f", "#5f914d"]
BLACK = ["#4d4d4d", "#363636"]
WHITE = ["#f7f7f7", "#dbdbdb"]
# constants for game GUI themes, changes depending on theme selected

FONT = "PT Serif"
TITLE_FONT_SIZE = 30
# font specific constants, PT Serif is used for all font, size 30 is only used for titles, font size otherwize is variable

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 600
# constants for how high and wide the main window will be, needs to be lesser than device screen dimensions to work

LOGINS_FILE = "data/logins.txt"
HIGH_SCORES_FILE = "data/high_scores.txt"
# constants for the files that contains the players' scores and login credentials

BLUE_DICE = ["images/blue_die_12.jpg", "images/blue_die_22.jpg",
             "images/blue_die_32.jpg", "images/blue_die_42.jpg", "images/blue_die_52.jpg", "images/blue_die_62.jpg"]
GREEN_DICE = ["images/green_die_12.jpg", "images/green_die_22.jpg",
              "images/green_die_32.jpg", "images/green_die_42.jpg", "images/green_die_52.jpg", "images/green_die_62.jpg"]
BLACK_DICE = ["images/black_die_12.jpg", "images/black_die_22.jpg",
              "images/black_die_32.jpg", "images/black_die_42.jpg", "images/black_die_52.jpg", "images/black_die_62.jpg"]
WHITE_DICE = ["images/white_die_12.jpg", "images/white_die_22.jpg",
              "images/white_die_32.jpg", "images/white_die_42.jpg", "images/white_die_52.jpg", "images/white_die_62.jpg"]
# constants for locations of dice images in project, chanages between themes hence four different types

ALL_DICE = [BLUE_DICE, GREEN_DICE, BLACK_DICE, WHITE_DICE]
# constant list that contains all dice image types, used in "main.py" to iterate through all of them and load them in

MUSIC_FILE = "music/bensound-thejazzpiano_2.mp3"
# constant gives the location of the music file for the project

