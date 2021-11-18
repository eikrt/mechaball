import os
import curses
from .settings import Color

from .utils import powerups
from .utils import badpowerups
from .settings import settings
from .settings import scr
menu_selection = 0
level_selection = 0

title = '''__  __ _____ ____ _   _    _    ____    _    _     _     
|  \/  | ____/ ___| | | |  / \  | __ )  / \  | |   | |    
| |\/| |  _|| |   | |_| | / _ \ |  _ \ / _ \ | |   | |    
| |  | | |__| |___|  _  |/ ___ \| |_) / ___ \| |___| |___ 
|_|  |_|_____\____|_| |_/_/   \_\____/_/   \_\_____|_____|'''

def draw(stdscr,x,y,msg:str, color):
    try:
        stdscr.addstr(int(scr.margin_y) + y, int(scr.margin_x) + x,msg, curses.color_pair(color))
    except:
        pass
def menu_show(main,stdscr, key):
    global menu_selection
    if key == curses.KEY_UP:
        if menu_selection >= 1:
            menu_selection -= 1
    elif key == curses.KEY_DOWN:
        if menu_selection <= 0:
            menu_selection += 1
    elif key == 10:
        if menu_selection == 0:
            settings['mute'] = not settings['mute']
        elif menu_selection == 1: 
            main.levelselect_on = True
    draw(stdscr,30,2,' MECHABALL ', Color.YELLOW.value)
    draw(stdscr,36,8, '\u2588',Color.YELLOW.value)
    draw(stdscr,54,8,powerups[0],Color.GREEN.value)

    draw(stdscr, 54, 10, powerups[1], Color.GREEN.value)
    draw(stdscr, 54, 12, powerups[2], Color.GREEN.value)
    draw(stdscr, 54, 14, powerups[3], Color.GREEN.value)
    draw(stdscr, 54, 16, powerups[4], Color.GREEN.value)
    draw(stdscr, 54, 18, badpowerups[0], Color.RED.value)
    draw(stdscr, 54, 20, badpowerups[1], Color.RED.value)
    draw(stdscr, 54, 22, badpowerups[2], Color.RED.value)
    draw(stdscr, 66, 8, badpowerups[3], Color.RED.value)


    draw(stdscr, 22,6,' BRICKS ', Color.MAGENTA.value)
    draw(stdscr, 22,8,' HARD BRICK ', Color.WHITE.value)
    draw(stdscr, 40,6,' POWERUPS ', Color.MAGENTA.value)
    draw(stdscr, 40,8,' EXTRA BALL ', Color.WHITE.value)
    draw(stdscr, 40,10,' HALF SPEED ', Color.WHITE.value)
    draw(stdscr, 40,12,' PEW PEW ', Color.WHITE.value)

    draw(stdscr, 40,14,' PENETRATION ', Color.WHITE.value)
    draw(stdscr, 40,16,' EXPLOSION ', Color.WHITE.value)
    draw(stdscr, 40,18,' 2x SPEED ', Color.WHITE.value)
    draw(stdscr, 40,20,' BALL RESET ', Color.WHITE.value)

    draw(stdscr, 40,22,' DEATH ', Color.WHITE.value)
    draw(stdscr, 56,8,' FALLING ', Color.WHITE.value)
    mute = 'ON ' if settings['mute'] else 'OFF'
    draw(stdscr, 3,6,f' MUTE: {mute}',Color.BLACK.value if menu_selection == 0 else curses.color_pair(Color.WHITE.value))

    draw(stdscr, 3,8,' LEVEL SELECT ', Color.BLACK.value if menu_selection == 1 else curses.color_pair(Color.WHITE.value))



    draw(stdscr, 22,10,' CONTROLS ', Color.MAGENTA.value)

    draw(stdscr, 15,12,' SPACE - SHOOT, REQUIRES ', Color.WHITE.value)
    draw(stdscr, 22,14,' ARROWS - MOVE ', Color.WHITE.value)
    draw(stdscr, 22,16,' Q - EXIT ', Color.WHITE.value)


def levelselect_show(main,stdscr,key):
    global level_selection


    draw(stdscr, 3,3,' LEVEL SELECT ', Color.WHITE.value)

    draw(stdscr,3,6,f' LEVEL 1 - Warm Up ',Color.BLACK.value if level_selection == 0 else Color.WHITE.value)
    draw(stdscr,3,8,f' LEVEL 2 - Pyramid ',Color.BLACK.value if level_selection == 1 else Color.WHITE.value)
    draw(stdscr,3,10,f' LEVEL 3 - Ping Pong ',Color.BLACK.value if level_selection == 2 else Color.WHITE.value)
    draw(stdscr,3,12,f' LEVEL 4 - El Lissitzky ',Color.BLACK.value if level_selection == 3 else Color.WHITE.value)
    draw(stdscr,3,14,f' LEVEL 5 - Where No Man Has Gone Before ',Color.BLACK.value if level_selection == 4 else Color.WHITE.value)
    draw(stdscr,3,16,f' LEVEL 6 - Perished By The Sword ',Color.BLACK.value if level_selection == 5 else Color.WHITE.value)
    draw(stdscr,3,18,f' LEVEL 7 - Vingilote ',Color.BLACK.value if level_selection == 6 else Color.WHITE.value)
    draw(stdscr,3,20,f' MENU ',Color.BLACK.value if level_selection == 7 else Color.WHITE.value)

    if key == curses.KEY_UP:
        if level_selection > 0:
            level_selection -= 1
    elif key == curses.KEY_DOWN:
        if level_selection < 7:
            level_selection += 1

    elif key == 10:
        if level_selection == 0:
            main.select_level(os.path.abspath('levels/level1.txt'))
            main.levelselect_on = False
            main.menu_on = False
        elif level_selection == 1:
            main.select_level(os.path.abspath('levels/level2.txt'))
            main.levelselect_on = False
            main.menu_on = False
        elif level_selection == 2: 
            main.select_level(os.path.abspath('levels/level3.txt'))
            main.levelselect_on = False
            main.menu_on = False
        elif level_selection == 3:
            main.select_level(os.path.abspath('levels/level4.txt'))
            main.levelselect_on = False
            main.menu_on = False
        elif level_selection == 4:
            main.select_level(os.path.abspath('levels/level5.txt'))
            main.levelselect_on = False
            main.menu_on = False
        elif level_selection == 5: 
            main.select_level(os.path.abspath('levels/level6.txt'))
            main.levelselect_on = False
            main.menu_on = False
        elif level_selection == 6: 
            main.select_level(os.path.abspath('levels/level7.txt'))
            main.levelselect_on = False
            main.menu_on = False
        elif level_selection == 7: 
            main.levelselect_on = False
            main.menu_on = True
