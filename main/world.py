import time
from datetime import datetime
from playsound import playsound
import curses
import math
from curses import wrapper
import random
import re
from .settings import settings
from .state import state
from .utils import psound
from .settings import Color
from .settings import scr
class Entity:
    def __init__(self, x: float, y: float, color: hex, symbol: str, id: str, cbox_w: float, cbox_h: float):
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.color = color
        self.symbol = symbol
        self.id = id
        self.dir = -math.pi/4
        self.speed = 10
        self.speed_cap = 10
        self.ball_speed_time = 1000
        self.ball_change = 0
        self.dead = False
        self.cbox_w=cbox_w
        self.cbox_h=cbox_h
        self.tickcd = 15
        self.ticktime = 0
        self.buffer_size = 0.2
    def draw(self, stdscr):
        rows, cols = stdscr.getmaxyx()
        try:
            stdscr.addstr(int(scr.margin_y+self.y), int(scr.margin_x+self.x), self.symbol, curses.color_pair(self.color))
        except curses.error:
            pass
    def move(self, delta):
        self.ticktime -= 1
        self.ball_change += 10
        if self.ball_change > self.ball_speed_time:
            self.ball_change = 0
            if self.speed < self.speed_cap:
                self.speed += 0.3
        self.x += (math.cos(self.dir) * self.speed * delta) / 1000
        self.y += (math.sin(self.dir) * self.speed * delta) / 1000
        if self.x > settings['w'] + 5 or self.x < -5 or self.y > settings['h'] + 1 or self.y < -1:
            self.dead = True
    def collision(self, other):
        pass
class Powerup(Entity):
    def __init__(self, x: float, y: float, color: int, symbol: chr, id: str, power: int):
        super().__init__(x,y,color,symbol,id, 1,1)
        self.cbox_w = 1
        self.cbox_h = 1
        self.power = power
        self.speed = 5
        self.dir = math.pi/2 + random.uniform(-0.4,0.4)
    def collision(self,delta,other):
        super().collision(other)
        selfhitboxb = self.cbox_w
        otherhitboxb = other.cbox_w
        step_x = (math.cos(self.dir) * self.speed * delta) / 1000
        step_y = (math.sin(self.dir) * self.speed * delta) / 1000
        hx = self.x + selfhitboxb / 2
        hy = self.y + selfhitboxb / 2
        if self.x + step_x >= other.x and self.x + step_x <= other.x + otherhitboxb and self.y + step_y >= other.y and self.y + step_y <= other.y + otherhitboxb and self.ticktime < 0:
            if other.id == 'paddle':
                self.ticktime=self.tickcd
                self.dead = True
                return self.power
        return -1
    def move(self,delta):
        super().move(delta)
        
class Ball(Entity):
    def __init__(self, x: float, y: float, color: hex, symbol: chr, id: str):
        super().__init__(x,y,color,symbol,id, 1,1)
        self.penetrating = False
        self.explosive = False
        self.explosion_size = 2
        self.speed = 4
        self.speed_cap = 15
    def move(self,delta):

        super().move(delta)
        
        if self.ticktime < 0:
            if self.x <= 1:
                self.dir = math.pi - self.dir
                self.ticktime = self.tickcd
                psound("sound/wall.wav", False)
            elif self.y <= 1:
                self.dir = -self.dir
                self.ticktime = self.tickcd

                psound("sound/wall.wav", False)
            elif self.x >= settings['w']-1:
                self.dir = math.pi - self.dir
                self.ticktime = self.tickcd

                psound("sound/wall.wav", False)
            if self.y >= settings['h']: # death
                self.dead = True
    def draw(self, stdscr):
        super().draw(stdscr)
    def collision(self,delta,other,bricks):
        selfhitboxb = self.cbox_w
        otherhitboxb = other.cbox_w
        step_x = (math.cos(self.dir) * self.speed * delta) / 1000
        step_y = (math.sin(self.dir) * self.speed * delta) / 1000
        hx = self.x + selfhitboxb / 2
        hy = self.y + selfhitboxb / 2
        if self.x + step_x >= other.x and self.x + step_x <= other.x + otherhitboxb and self.y + step_y >= other.y and self.y + step_y <= other.y + otherhitboxb and self.ticktime < 0:
            self.ticktime=self.tickcd
            if other.id != 'paddle':
                if self.explosive:
                    psound('sound/explosion.wav', False)
                    for b in bricks:

                        if b.x > hx - self.explosion_size and b.x < hx +self.explosion_size and  b.y > hy - self.explosion_size and b.y < hy +self.explosion_size:
                            b.dead = True
                if not self.penetrating:
                     if math.cos(self.dir) > 0: # right
                         if math.sin(self.dir) > 0: # down
                             
                             self.dir = (math.pi/4)*4
                         if math.sin(self.dir) < 0: # up
                             self.dir = (math.pi/4)*3
                     if math.cos(self.dir) < 0: # left

                         if math.sin(self.dir) < 0: # down
                             
                             self.dir = (math.pi/4)*1
                         if math.sin(self.dir) > 0: # up
                              
                             self.dir = (math.pi/4)*2
                     self.dir += random.uniform(0,(math.pi/4)*3)
            else:
                if other.align == -1:

                    self.dir = -self.dir + random.uniform(-math.pi/12,0.0)
                elif other.align == 0:

                    self.dir = -self.dir
                elif other.align == 1:
                    self.dir =  -self.dir + random.uniform(-0.0,math.pi/12)
                else:
                    self.dir = -self.dir
            if other.id == 'brick' and not self.explosive:
                
                state['score'] += 250
                other.dead = True
                psound('sound/brick.wav', False)

            elif other.id == 'hard_brick' and not self.explosive:
                if self.penetrating:
                    other.dead = True
                psound('sound/wall.wav', False)
            elif other.id == 'paddle':
                psound('sound/bounce.wav', False)
class Brick(Entity):
    def __init__(self, x: float, y: float, color: hex, symbol: chr, id: id):
        super().__init__(x,y,color,symbol,id,0.9,0.9)
        self.buffer_size = 0.2
class Projectile(Entity):
    def __init__(self, x: float, y: float, color: hex, symbol: chr, id: id, cbox_w: float, cbox_h: float):

        super().__init__(x,y,color,symbol,id,0.9,0.9)

        self.speed = 30
    def move(self,delta):
        super().move(delta)
    def collision(self, delta, other):
        selfhitboxb = self.cbox_w
        otherhitboxb = other.cbox_w
        step_x = (math.cos(self.dir) * self.speed * delta) / 1000
        step_y = (math.sin(self.dir) * self.speed * delta) / 1000
        hx = self.x + selfhitboxb / 2
        hy = self.y + selfhitboxb / 2
        if self.x + step_x >= other.x and self.x + step_x <= other.x + otherhitboxb and self.y + step_y >= other.y and self.y + step_y <= other.y + otherhitboxb and self.ticktime < 0:
            self.ticktime=self.tickcd
            if other.id != 'hard_brick':
                other.dead = True
            self.dead = True
class Paddle(Entity):
    def __init__(self, x: float, y: float, color: hex, symbol: chr, id: id, align: int):
        super().__init__(x,y,color,symbol,id,1,1)
        self.align = align
        self.shooting = False
    def shoot(self, entities: list, projectiles: list):
        if self.shooting:
            projectile = Projectile(self.x,self.y,1,'\'','laser',1,1)
            projectile.dir = -math.pi/2
            entities.append(projectile)
            projectiles.append(projectile)
            psound('sound/laser.wav', False)
    def collision(self, other,delta):
        super().collision(other)

    def move(self, delta):
        pass
