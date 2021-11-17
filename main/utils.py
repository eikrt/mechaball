from playsound import playsound
from .settings import settings
import os
from sys import platform
powerups = ['8','<','\'','/','*'] # extra ball, half speed, shooting, penetrating, exploding, speedup, reset, death, closing blocks
badpowerups = ['>','o','X','=']
def psound(url: str, block: bool):
    if not settings['mute']:
        try:
            if platform == "linux" or platform == "linux2":
                os.system("play " + os.path.abspath(url) + " > /dev/null 2>&1 &")
            elif platform == "darwin":
                os.system("play " + os.path.abspath(url) + " > /dev/null 2>&1 &")
            elif platform == "win32":
                playsound(os.path.abspath(url), block)
        except:
            pass
