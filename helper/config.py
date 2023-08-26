
import os
home = os.getcwd()


STATIC_DIR = "./static/"
WYRS_PATH = STATIC_DIR + "dataset.json"
FONT_PATH = STATIC_DIR + "font.ttf"


SOUNDS_DIR = STATIC_DIR + "sounds/"
START_SOUND_PATH = SOUNDS_DIR + "start.mp3"
TIMER_SOUND_PATH = SOUNDS_DIR + "timer.mp3"
END_SOUND_PATH = SOUNDS_DIR + "end.mp3"



WIDTH = 500
HEIGHT = 500

class CustomEvent:
    start = 0
    timer = 1
    end = 2