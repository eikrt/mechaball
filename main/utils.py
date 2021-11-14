from .settings import settings
powerups = ['8','<','\'','/','*'] # extra ball, half speed, shooting, penetrating, exploding, speedup, reset, death, closing blocks
badpowerups = ['>','o','X','=']
def psound(url: str, block: bool):
    if not settings['mute']:
        playsound(url, block)
