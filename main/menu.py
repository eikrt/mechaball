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
    stdscr.addstr(int(scr.margin_y) + 2, int(scr.margin_x) + 30,' MECHABALL ')

    stdscr.addstr(int(scr.margin_y) + 8,int(scr.margin_x) + 36, '\u2588', curses.color_pair(Color.YELLOW.value))
    stdscr.addstr(int(scr.margin_y) + 8,int(scr.margin_x) + 54, powerups[0], curses.color_pair(Color.GREEN.value))
    stdscr.addstr(int(scr.margin_y) + 10,int(scr.margin_x) + 54, powerups[1], curses.color_pair(Color.GREEN.value))
    stdscr.addstr(int(scr.margin_y) + 12,int(scr.margin_x) + 54, powerups[2], curses.color_pair(Color.GREEN.value))

    stdscr.addstr(int(scr.margin_y) + 14,int(scr.margin_x) + 54, powerups[3], curses.color_pair(Color.GREEN.value))

    stdscr.addstr(int(scr.margin_y) + 16,int(scr.margin_x) + 54, powerups[4], curses.color_pair(Color.GREEN.value))

    stdscr.addstr(int(scr.margin_y) + 18,int(scr.margin_x) + 54, badpowerups[0], curses.color_pair(Color.RED.value))
    stdscr.addstr(int(scr.margin_y) + 20,int(scr.margin_x) + 54, badpowerups[1], curses.color_pair(Color.RED.value))
    stdscr.addstr(int(scr.margin_y) + 22,int(scr.margin_x) + 54, badpowerups[2], curses.color_pair(Color.RED.value))
    stdscr.addstr(int(scr.margin_y) + 8,int(scr.margin_x) + 66, badpowerups[3], curses.color_pair(Color.RED.value))


    stdscr.addstr(int(scr.margin_y) + 6,int(scr.margin_x) + 22, ' BRICKS ')
    stdscr.addstr(int(scr.margin_y) + 6,int(scr.margin_x) + 40, ' POWERUPS ')
    stdscr.addstr(int(scr.margin_y) + 8,int(scr.margin_x) + 22, ' HARD BRICK')

    stdscr.addstr(int(scr.margin_y) + 8,int(scr.margin_x) + 40, ' EXTRA BALL ')
    stdscr.addstr(int(scr.margin_y) + 10,int(scr.margin_x) + 40, ' HALF SPEED ')
    stdscr.addstr(int(scr.margin_y) + 12,int(scr.margin_x) + 40, ' PEW PEW ')
    stdscr.addstr(int(scr.margin_y) + 14,int(scr.margin_x) + 40, ' PENETRATION ')
    stdscr.addstr(int(scr.margin_y) + 16,int(scr.margin_x) + 40, ' EXPLOSION ')
    stdscr.addstr(int(scr.margin_y) + 18,int(scr.margin_x) + 40, ' 2x SPEED ')
    stdscr.addstr(int(scr.margin_y) + 20,int(scr.margin_x) + 40, ' BALL RESET ')
    
    stdscr.addstr(int(scr.margin_y) + 22,int(scr.margin_x) + 40, ' DEATH ')
    stdscr.addstr(int(scr.margin_y) + 8,int(scr.margin_x) + 56, ' FALLING ')
    mute = 'ON ' if settings['mute'] else 'OFF'
    stdscr.addstr(int(scr.margin_y) + 6,int(scr.margin_x) +3,f' MUTE: {mute}',curses.color_pair(Color.BLACK.value) if menu_selection == 0 else curses.color_pair(Color.WHITE.value))
    stdscr.addstr(int(scr.margin_y) + 8,int(scr.margin_x) + 3,' LEVEL SELECT ', curses.color_pair(Color.BLACK.value) if menu_selection == 1 else curses.color_pair(Color.WHITE.value))


    stdscr.addstr(int(scr.margin_y) + 10,int(scr.margin_x) + 22, ' CONTROLS ')
    stdscr.addstr(int(scr.margin_y) + 12,int(scr.margin_x) + 15, ' SPACE - SHOOT, REQUIRES ')


    stdscr.addstr(int(scr.margin_y) + 14,int(scr.margin_x) + 22, ' ARROWS - MOVE ')
    stdscr.addstr(int(scr.margin_y) + 16,int(scr.margin_x) + 22, ' Q - EXIT ')
def levelselect_show(main,stdscr,key):
    global level_selection
    stdscr.addstr(int(scr.margin_y + 3),int(scr.margin_x + 3)," LEVEL SELECT ")
    stdscr.addstr(int(scr.margin_y) + 6,int(scr.margin_x) + 3,f' LEVEL 1 - Warm Up ',curses.color_pair(Color.BLACK.value) if level_selection == 0 else curses.color_pair(Color.WHITE.value))
    stdscr.addstr(int(scr.margin_y) + 8,int(scr.margin_x) + 3,f' LEVEL 2 - Pyramid ',curses.color_pair(Color.BLACK.value) if level_selection == 1 else curses.color_pair(Color.WHITE.value))
    stdscr.addstr(int(scr.margin_y) + 10,int(scr.margin_x) + 3,f' LEVEL 3 - Ping Pong',curses.color_pair(Color.BLACK.value) if level_selection == 2 else curses.color_pair(Color.WHITE.value))
    stdscr.addstr(int(scr.margin_y) + 12,int(scr.margin_x) + 3,f' LEVEL 4 - El Lissitzky ',curses.color_pair(Color.BLACK.value) if level_selection == 3 else curses.color_pair(Color.WHITE.value))
    stdscr.addstr(int(scr.margin_y) + 14,int(scr.margin_x) + 3,f' LEVEL 5 - Where No Man Has Gone Before',curses.color_pair(Color.BLACK.value) if level_selection == 4 else curses.color_pair(Color.WHITE.value))
    stdscr.addstr(int(scr.margin_y) + 16,int(scr.margin_x) + 3,f' LEVEL 6 - Perished By The Sword ',curses.color_pair(Color.BLACK.value) if level_selection == 5 else curses.color_pair(Color.WHITE.value))
    stdscr.addstr(int(scr.margin_y) + 18,int(scr.margin_x) + 3,f' LEVEL 7 - Vingilote ',curses.color_pair(Color.BLACK.value) if level_selection == 6 else curses.color_pair(Color.WHITE.value))
    stdscr.addstr(int(scr.margin_y) + 20,int(scr.margin_x) + 3,f' MENU ',curses.color_pair(Color.BLACK.value) if level_selection == 7 else curses.color_pair(Color.WHITE.value))

    if key == curses.KEY_UP:
        if level_selection > 0:
            level_selection -= 1
    elif key == curses.KEY_DOWN:
        if level_selection < 7:
            level_selection += 1

    elif key == 10:
        if level_selection == 0:
            main.select_level('levels/level1.txt')
            main.levelselect_on = False
            main.menu_on = False
        elif level_selection == 1:
            main.select_level('levels/level2.txt')
            main.levelselect_on = False
            main.menu_on = False
        elif level_selection == 2: 
            main.select_level('levels/level3.txt')
            main.levelselect_on = False
            main.menu_on = False
        elif level_selection == 3:
            main.select_level('levels/level4.txt')
            main.levelselect_on = False
            main.menu_on = False
        elif level_selection == 4:
            main.select_level('levels/level5.txt')
            main.levelselect_on = False
            main.menu_on = False
        elif level_selection == 5: 
            main.select_level('levels/level6.txt')
            main.levelselect_on = False
            main.menu_on = False
        elif level_selection == 6: 
            main.select_level('levels/level7.txt')
            main.levelselect_on = False
            main.menu_on = False
        elif level_selection == 7: 
            main.levelselect_on = False
            main.menu_on = True
