from .settings import settings
def psound(url: str, block: bool):
    if not settings['mute']:
        playsound(url, block)
