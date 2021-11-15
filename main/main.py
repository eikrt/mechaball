import time
from datetime import datetime
import curses
from curses import wrapper
import math
import random
import re
from .utils import psound
from .world import Entity
from .world import Paddle
from .world import Ball
from .world import Projectile
from .world import Powerup 
from .world import Brick
from .settings import Color 
from .settings import settings
from .state import state
from .utils import powerups
from .utils import badpowerups
from .menu import menu_show
from .menu import levelselect_show
from .settings import scr
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
                    self.bricks.append(Brick(x,y, Color.YELLOW.value, '\u2588', 'hard_brick'))
        
        self.entities.extend(self.bricks)
    def loop(self, stdscr):
        global settings

        old_time = None


        menu_selection = 0
        level_selection = 0
        while(self.running):

            stdscr.clear()
            

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
                if self.levelselect_on:
                    levelselect_show(self,stdscr,key)
                else:
                    menu_show(self, stdscr, key)
            elif not self.menu_on:


                if key == curses.KEY_LEFT:
                    for paddle in self.paddles:
                        if self.paddles[-1].x > len(self.paddles):
                            paddle.x -= 2
                elif key == curses.KEY_RIGHT:
                    for paddle in self.paddles:
                        if self.paddles[len(self.paddles)-1].x < settings['w']-2:
                            paddle.x += 3
                elif key == ord(' '):
                    for p in self.paddles:
                        p.shoot(self.entities, self.projectiles)

                for p in self.paddles:
                    for b in self.balls:
                        b.collision(delta, p, self.bricks)
                for b in self.bricks:
                    for ba in self.balls:
                        ba.collision(delta, b, self.bricks)
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
                                b.color = Color.CYAN.value 
                        elif power == 4:
                            for b in self.balls:
                                b.exploding = True
                                b.color = Color.YELLOW.value
                        elif power == 5:
                            for b in self.balls:
                                b.speed *= 2
                        elif power == 6:
                            for b in self.balls:
                                b.penetrating = False
                                b.exploding = False
                                b.color = Color.RED.value 
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
                                i = random.randint(0,4)
                                powerup = Powerup(e.x,e.y, Color.GREEN.value, powerups[i], "powerup", i)
                            elif bad == 1:

                                i = random.randint(0,3)
                                powerup = Powerup(e.x,e.y, Color.RED.value, badpowerups[i], "powerup", i+5)
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
                    self.menu_on = True
                    self.levelselect_on = True
                if len(self.bricks) <= 0:
                    self.menu_on = True
                    self.levelselect_on = True
                for e in self.entities:
                    e.draw(stdscr)
                stdscr.addstr(int(scr.margin_y+2),int(scr.margin_x + 3),f"Score: {state['score']}", curses.A_BOLD)

            for x in range(settings['w']):
                try:
                    stdscr.addstr(int(scr.margin_y),int(x + scr.margin_x),'\u2593')
                except:
                    pass

            for y in range(settings['h']):
                try:
                    stdscr.addstr(int(y + scr.margin_y),int(scr.margin_x),'\u2593')
                except:
                    pass

            for x in range(settings['w']):
                try: 
                    stdscr.addstr(int(scr.margin_y + settings['h']),int(x + scr.margin_x),'\u2593')
                except:
                    pass

            for y in range(settings['h']+1):
                try: 
                    stdscr.addstr(int(scr.margin_y+y),int(scr.margin_x + settings['w']),'\u2593')
                except:
                    pass

            scr.update_margins(stdscr)
            stdscr.refresh()
            time.sleep(0.01)
            old_time = datetime.now()
        curses.endwin()


def main():
        main = Main()

