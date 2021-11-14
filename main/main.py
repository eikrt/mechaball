import time
from datetime import datetime
import curses
from curses import wrapper
import math
import random
import re
from playsound import playsound
from .world import Entity
from .world import Paddle
from .world import Ball
from .world import Projectile
from .world import Powerup 
from .world import Brick
from .settings import Color 
from .settings import settings
from .state import state
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
        curses.init_pair(Color.YELLOW.value, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(Color.RED.value, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(Color.YELLOW.value, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(Color.CYAN.value, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(Color.MAGENTA.value, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(Color.BLUE.value, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(Color.GREEN.value, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(Color.BLACK.value, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(Color.WHITE.value, curses.COLOR_WHITE, curses.COLOR_BLACK)
        stdscr.keypad(1)
        curses.mousemask(1)
        global settings
        self.entities = []
        self.bricks = []
        self.powerups = []
        self.projectiles = []
        self.menu_on = True
        self.levelselect_on = False
        self.paddles = [Paddle(28,22, Color.YELLOW.value, '\u2581', "paddle"), Paddle(29,22, Color.YELLOW.value, '\u2581', "paddle"),Paddle(30,22, Color.YELLOW.value, '\u2581', "paddle"), Paddle(31,22, Color.YELLOW.value, '\u2581', "paddle"),Paddle(32,22, Color.YELLOW.value, '\u2581', "paddle")]
        self.balls = [Ball(25,18, Color.RED.value, '\u25CF', "ball")]
        self.entities.extend(self.bricks)
        self.entities.extend(self.paddles)
        self.entities.extend(self.balls)
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
                    self.bricks.append(Brick(x,y, random.randint(4,7), '\u2588', 'brick'))

                elif lines[y][x] == '2':
                    self.bricks.append(Brick(x,y, 3, '\u2588', 'hard_brick'))
        
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
            if delta > 100:
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
                    stdscr.addstr(8,40, '\u2588', curses.color_pair(Color.YELLOW.value))
                    stdscr.addstr(8,41, ' = HARD BRICK')
                    mute = 'ON ' if settings['mute'] else 'OFF'
                    stdscr.addstr(8,1,f' MUTE: {mute}',curses.color_pair(Color.BLACK.value) if menu_selection == 0 else curses.color_pair(Color.WHITE.value))
                    stdscr.addstr(10,1,' LEVEL SELECT ', curses.color_pair(Color.BLACK.value) if menu_selection == 1 else curses.color_pair(Color.WHITE.value))
                    stdscr.addstr(12,1,' PLAY ', curses.color_pair(Color.BLACK.value) if menu_selection == 2 else curses.color_pair(Color.WHITE.value))

                elif self.levelselect_on:
                    stdscr.addstr(2,2,"LEVEL SELECT")
                    stdscr.addstr(8,1,f' LEVEL 1 - Warm Up ',curses.color_pair(Color.BLACK.value) if level_selection == 0 else curses.color_pair(Color.WHITE.value))
                    stdscr.addstr(10,1,f' LEVEL 2 - Pyramid ',curses.color_pair(Color.BLACK.value) if level_selection == 1 else curses.color_pair(Color.WHITE.value))
                    stdscr.addstr(12,1,f' LEVEL 3 - Ping Pong',curses.color_pair(Color.BLACK.value) if level_selection == 2 else curses.color_pair(Color.WHITE.value))
                    stdscr.addstr(14,1,f' LEVEL 4 - El Lissitzky ',curses.color_pair(Color.BLACK.value) if level_selection == 3 else curses.color_pair(Color.WHITE.value))
                    stdscr.addstr(16,1,f' LEVEL 5 - Where No Man Has Gone Before',curses.color_pair(Color.BLACK.value) if level_selection == 4 else curses.color_pair(Color.WHITE.value))
                    stdscr.addstr(18,1,f' LEVEL 6 - Perished By The Sword ',curses.color_pair(Color.BLACK.value) if level_selection == 5 else curses.color_pair(Color.WHITE.value))
                    stdscr.addstr(20,1,f' LEVEL 7 - Evil Dead ',curses.color_pair(Color.BLACK.value) if level_selection == 6 else curses.color_pair(Color.WHITE.value))
                    stdscr.addstr(22,1,f' MENU ',curses.color_pair(Color.BLACK.value) if level_selection == 7 else curses.color_pair(Color.WHITE.value))

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
                elif key == ord(' '):
                    for p in self.paddles:
                        p.shoot(self.entities, self.projectiles)
                for p in self.paddles:
                    for b in self.balls:
                        b.collision(delta, p)
                for b in self.bricks:
                    for ba in self.balls:
                        ba.collision(delta, b)
                for p in self.projectiles:
                    for b in self.bricks:
                        p.collision(delta,b)
                for p in self.powerups:
                    for pa in self.paddles:
                        power = p.collision(delta, pa)
                        if power == 0:
                            new_ball = Ball(self.balls[0].x,self.balls[0].y, 2, '\u25CF', "ball")
                            new_ball.dir = math.pi - new_ball.dir
                            self.balls.append(new_ball)
                            self.entities.append(new_ball)
                        elif power == 1:
                            for b in self.balls:
                                b.speed /= 2
                        elif power == 2:
                            self.paddles[0].shooting = True
                            self.paddles[len(self.paddles)-1].shooting = True
                        elif power == 3:
                            for b in self.balls:
                                b.penetrating = True
                        elif power == 4:
                            for b in self.balls:
                                b.exploding = True
                                b.color = 3 
                        elif power == 5:
                            for b in self.balls:
                                b.speed *= 2
                        elif power == 6:
                            for b in self.balls:
                                b.penetrating = False
                                b.exploding = False

                        elif power == 7:
                            for b in self.balls:
                                b.dead = True
                        elif power == 8:
                            for b in self.bricks:
                                b.y += 2

                    p.move(delta)
                for p in self.projectiles:
                    p.move(delta)
                for b in self.balls:
                    b.move(delta)
                for e in self.entities:
                    if e.dead:
                        if e.id == 'brick':
                            bad = random.randint(0,1)
                            if bad == 0:
                                powerup = Powerup(e.x,e.y, 1, '+', "powerup", random.randint(0,4))
                            elif bad == 1:
                                powerup = Powerup(e.x,e.y, 2, 'X', "powerup", random.randint(4,8))
                            if random.randint(0,4) == 0: 
                                self.entities.append(powerup)
                                self.powerups.append(powerup)
                        self.entities.remove(e)
                        if e in self.bricks:
                            self.bricks.remove(e)
                        if e in self.powerups:
                            self.powerups.remove(e)
                        if e in self.balls:
                            self.balls.remove(e)
                        if e in self.projectiles:
                            self.projectiles.remove(e)
                if len(self.balls) <= 0:
                    psound('sound/death.wav', True)
                    exit()
                for e in self.entities:
                    e.draw(stdscr)
                stdscr.addstr(1,2,f"Score: {state['score']}", curses.A_BOLD)
            stdscr.refresh()
            time.sleep(0.01)
            old_time = datetime.now()
        curses.endwin()


def main():
        main = Main()

