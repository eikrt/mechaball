from playsound import playsound
from .settings import settings
import os
from sys import platform
powerups = ['8','<','\'','/','*'] # extra ball, half speed, shooting, penetrating, exploding, speedup, reset, death, closing blocks
badpowerups = ['>','o','X','=']
def psound(url: str, block: bool):
    if not settings['mute']:

        if platform == "linux" or platform == "linux2":
            os.system("play " + url + " &")
        elif platform == "darwin":
            os.system("play " + url + " &")
        elif platform == "win32":
            playsound(url, block)
