import time
from datetime import datetime
from playsound import playsound
import curses
import math
from curses import wrapper
import random
import re
w = 70
h = 25
debug_message = ""
score = 0
settings = {'mute':True,'auto_mode':False}
def psound(url: str, block: bool):
    global settings
    if not settings['mute']:
        playsound(url, block)
class Entity:
    def __init__(self, x: float, y: float, color: hex, symbol: str, id: str, cbox_w: float, cbox_h: float):
        self.x = x
        self.y = y
        self.color = color
        self.symbol = symbol
        self.id = id
        self.dir = -math.pi/4
        self.speed = 10
        self.ball_speed_time = 1000
        self.ball_change = 0
        self.dead = False
        self.cbox_w=cbox_w
        self.cbox_h=cbox_h
        self.tickcd = 25
        self.ticktime = 0
    def draw(self, stdscr):
        try:
            stdscr.addstr((int)(self.y), (int)(self.x), self.symbol, curses.color_pair(self.color))
        except curses.error:
            pass
    def move(self, delta):
        self.ticktime -= 1
        self.ball_change += 10
        if self.ball_change > self.ball_speed_time:
            self.ball_change = 0
            self.speed += 0.0
        self.move_step(delta,self.speed)
    def move_step(self, delta, step):
        self.x += (math.cos(self.dir)* step * delta) / 1000
        self.y += (math.sin(self.dir)* step * delta) / 1000
    def collision(self, other):
        pass
class Ball(Entity):
    def __init__(self, x: float, y: float, color: hex, symbol: chr, id: str):
        super().__init__(x,y,color,symbol,id, 1,1)

    def move(self,delta):

        super().move(delta)
        global settings
        if self.ticktime < 0:
            if self.x <= 1:

                self.ticktime = self.tickcd
                if math.sin(self.dir) > 0:
                    self.dir = self.dir - math.pi/2
                else:
                    self.dir = self.dir + math.pi/2
                psound("sound/wall.wav", False)
            elif self.y <= 1:

                self.ticktime = self.tickcd
                self.dir = -self.dir

                psound("sound/wall.wav", False)
            elif self.x >= w-1:

                self.ticktime = self.tickcd
                if math.sin(self.dir) > 0:
                    self.dir = self.dir + math.pi/2
                else:
                    self.dir = self.dir - math.pi/2

                psound("sound/wall.wav", False)
            if self.y >= h: # death
                psound("sound/death.wav", True)
                return True
    def draw(self, stdscr):
        #stdscr.addstr(4,4, str(math.sin(self.dir)))
        super().draw(stdscr)
    def collision(self,delta,other):
        selfhitboxb = self.cbox_w/2
        otherhitboxb = other.cbox_w/2
        if self.x +  (math.cos(self.dir)*self.speed * delta) / 1000 > other.x - otherhitboxb- selfhitboxb and self.x +  (math.cos(self.dir)*self.speed * delta) / 1000 < other.x +otherhitboxb + selfhitboxb and self.y +  (math.sin(self.dir)*self.speed * delta) / 1000 > other.y -otherhitboxb - selfhitboxb and self.y +  (math.sin(self.dir)*self.speed * delta) / 1000 < other.y + selfhitboxb + otherhitboxb and self.ticktime < 0:
            self.ticktime=self.tickcd
            if self.y > other.y:
                self.dir += math.pi/2
            elif self.y <= other.y:
                if math.cos(self.dir) > 0:
                    self.dir -= math.pi/2
                elif math.cos(self.dir) < 0:
                    self.dir += math.pi/2
            if other.id == 'brick':
                global score
                score += 250
                other.dead = True

                psound('sound/brick.wav', False)
            elif other.id == 'paddle':

                psound('sound/bounce.wav', False)
                #self.dir += random.uniform(-0.2,0.2)
class Brick(Entity):
    def __init__(self, x: float, y: float, color: hex, symbol: chr, id: id):
        super().__init__(x,y,color,symbol,id,0,0)
class Paddle(Entity):
    def __init__(self, x: float, y: float, color: hex, symbol: chr, id: id):
        super().__init__(x,y,color,symbol,id,0,0)
    def move(self, delta):
        pass
class Main:
    def __init__(self):
        self.running = True
        stdscr = curses.initscr()
        curses.curs_set(0)
        curses.noecho()
        curses.cbreak()
        stdscr.nodelay(1)
        curses.endwin()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(7, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(8, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(9, curses.COLOR_WHITE, curses.COLOR_BLACK)
        stdscr.keypad(1)
        curses.mousemask(1)
        global settings
        self.entities = []
        self.bricks = []
        self.menu_on = True
        self.levelselect_on = False
        self.paddles = [Paddle(30,22, 1, '\u2581', "paddle"), Paddle(31,22, 1, '\u2581', "paddle"), Paddle(29,22, 1, '\u2581', "paddle")]
        if settings.get('auto_mode'):
            self.paddles = [Paddle(29,22, 1, '\u2581', "paddle")]
        self.ball = Ball(30,15, 2, '\u25CF', "ball")
        #for x in range(10):
        #    for y in range(40):
        #        self.bricks.append(Brick(y + w/2-16,x + 5, random.randint(3,7), '\u2588', 'brick'))
        self.entities.extend(self.bricks)
        self.entities.extend(self.paddles)
        self.entities.append(self.ball)
        self.loop(stdscr)
        wrapper(self.loop)

    def select_level(self, path: str):
        self.bricks.clear()
        lines = ""
        level = []
        with open(path, "r") as f:
            lines = f.readlines()
        for x in lines:
            x.replace('\\', '')
            x.replace('n', '')
        for x in range(len(lines[0])):
            for y in range(len(lines)):

                if lines[y][x] == '1':
                    self.bricks.append(Brick(x,y, random.randint(3,7), '\u2588', 'brick'))
        
        self.entities.extend(self.bricks)
    def loop(self, stdscr):
        global settings
        title = '''  __  __ _____ ____ _   _    _    ____    _    _     _     
  |  \/  | ____/ ___| | | |  / \  | __ )  / \  | |   | |    
  | |\/| |  _|| |   | |_| | / _ \ |  _ \ / _ \ | |   | |    
  | |  | | |__| |___|  _  |/ ___ \| |_) / ___ \| |___| |___ 
  |_|  |_|_____\____|_| |_/_/   \_\____/_/   \_\_____|_____|'''

        old_time = None


        menu_selection = 0
        level_selection = 0
        while(self.running):

            stdscr.clear()
            stdscr.border('|')
            global settings


            new_time = datetime.now()
            
            if old_time != None:
                delta = (new_time.microsecond - old_time.microsecond) /10
            else:
                delta = 10
            key = stdscr.getch() 
            if key == ord('q'):
                self.running = False
            if self.menu_on:
                if not self.levelselect_on: 
                    if key == curses.KEY_UP:
                        menu_selection -= 1
                    elif key == curses.KEY_DOWN:
                        menu_selection += 1
                    elif key == 10:
                        if menu_selection == 0:
                            settings['mute'] = not settings['mute']
                        elif menu_selection == 1: 
                            self.levelselect_on = True
                        elif menu_selection == 2: 
                            self.menu_on = False
                    stdscr.addstr(1,1,title)
                    mute = 'ON ' if settings['mute'] else 'OFF'
                    stdscr.addstr(8,1,f' MUTE: {mute}',curses.color_pair(8) if menu_selection == 0 else curses.color_pair(9))
                    stdscr.addstr(10,1,' LEVEL SELECT ', curses.color_pair(8) if menu_selection == 1 else curses.color_pair(9))
                    stdscr.addstr(12,1,' PLAY ', curses.color_pair(8) if menu_selection == 2 else curses.color_pair(9))

                elif self.levelselect_on:
                    stdscr.addstr(2,2,"LEVEL SELECT")


                    stdscr.addstr(8,1,f' LEVEL 1 - Warm Up ',curses.color_pair(8) if level_selection == 0 else curses.color_pair(9))
                    stdscr.addstr(10,1,f' LEVEL 2 - Pyramid ',curses.color_pair(8) if level_selection == 1 else curses.color_pair(9))
                    stdscr.addstr(12,1,f' LEVEL 3 - Ping Pong',curses.color_pair(8) if level_selection == 2 else curses.color_pair(9))
                    stdscr.addstr(14,1,f' LEVEL 4 - El Lissitzky ',curses.color_pair(8) if level_selection == 3 else curses.color_pair(9))
                    stdscr.addstr(16,1,f' LEVEL 5 - Where No Man Has Gone Before',curses.color_pair(8) if level_selection == 4 else curses.color_pair(9))
                    stdscr.addstr(18,1,f' LEVEL 6 - Perished By The Sword ',curses.color_pair(8) if level_selection == 5 else curses.color_pair(9))
                    stdscr.addstr(20,1,f' LEVEL 7 - Evil Dead ',curses.color_pair(8) if level_selection == 6 else curses.color_pair(9))
                    stdscr.addstr(22,1,f' MENU ',curses.color_pair(8) if level_selection == 7 else curses.color_pair(9))

                    if key == curses.KEY_UP:
                        level_selection -= 1
                    elif key == curses.KEY_DOWN:
                        level_selection += 1

                    elif key == 10:
                        if level_selection == 0:
                            self.select_level('levels/level1.txt')
                            self.levelselect_on = False
                            self.menu_on = False
                        elif level_selection == 1:
                            self.select_level('levels/level2.txt')
                            self.levelselect_on = False
                            self.menu_on = False
                        elif level_selection == 2: 
                            self.select_level('levels/level3.txt')
                            self.levelselect_on = False
                            self.menu_on = False

                        elif level_selection == 3:
                            self.select_level('levels/level4.txt')
                            self.levelselect_on = False
                            self.menu_on = False
                        elif level_selection == 4:
                            self.select_level('levels/level5.txt')
                            self.levelselect_on = False
                            self.menu_on = False
                        elif level_selection == 5: 
                            self.select_level('levels/level6.txt')
                            self.levelselect_on = False
                            self.menu_on = False
                        elif level_selection == 6: 
                            self.select_level('levels/level7.txt')
                            self.levelselect_on = False
                            self.menu_on = False
                        elif level_selection == 7: 
                            self.levelselect_on = False
                            self.menu_on = True
            elif not self.menu_on:


                if key == curses.KEY_LEFT:
                    for paddle in self.paddles:
                        paddle.x -= 3
                elif key == curses.KEY_RIGHT:
                    for paddle in self.paddles:
                        paddle.x += 3

            #    stdscr.addstr(0,0,str(self.ball.x))
                for paddle in self.paddles:
                    self.ball.collision(delta, paddle)
                for b in self.bricks:
                    self.ball.collision(delta, b)
                if self.ball.move(delta):
                    self.running=False
                if settings.get('auto_mode'):
                    self.paddles[0].x = self.ball.x
                for e in self.entities:
                    if e.dead:
                        self.entities.remove(e)
                        if e in self.bricks:
                            self.bricks.remove(e)
                for e in self.entities:
                    e.draw(stdscr)
                stdscr.addstr(1,2,f"Score: {score}", curses.A_BOLD)
            stdscr.refresh()
            time.sleep(0.01)
            old_time = datetime.now()
        curses.endwin()


def main():
        main = Main()

