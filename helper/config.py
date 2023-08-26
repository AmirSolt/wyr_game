
import os
home = os.getcwd()


STATIC_DIR = "./static/"
WYRS_PATH = STATIC_DIR + "dataset.json"
FONT_PATH = STATIC_DIR + "font.ttf"
IMAGE_DIR = STATIC_DIR + "imgs/"
BG_TEMPLATE_PATH = IMAGE_DIR + "wyr_template.png"
DONO_FLOWER_PATH = IMAGE_DIR + "dono_flower.png"
DONO_TIKTOK_PATH = IMAGE_DIR + "dono_tiktok.png"

SOUNDS_DIR = STATIC_DIR + "sounds/"
START_SOUND_PATH = SOUNDS_DIR + "start.mp3"
TIMER_SOUND_PATH = SOUNDS_DIR + "timer.mp3"
END_SOUND_PATH = SOUNDS_DIR + "end.mp3"
MUSIC_SOUND_PATH = SOUNDS_DIR + "music.mp3"



WIDTH = 703
HEIGHT = 1250

class CustomEvent:
    start = 0
    timer = 1
    end = 2