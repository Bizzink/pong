import pygame as pg
from sys import exit
from time import sleep
from random import randrange
from math import pi, cos, sin


class Paddle:
    def __init__(self, side):
        self.pos = height // 2
        self.rect = pg.Rect(0, 0, 10, height // 6)
        self.height = height // 6

        if side == "left":
            self.rect.centerx = 20
        elif side == "right":
            self.rect.centerx = width - 20
        else:
            raise ValueError

        self.draw()

    def __str__(self):
        return str(self.pos) + "(" + str(self.rect) + ")"

    def draw(self):
        self.rect.centery = int(self.pos)
        pg.draw.rect(screen, (255, 255, 255), self.rect)

    def move(self, direction):
        self.pos += direction

        if self.pos > height - (self.height // 2):
            self.pos = height - (self.height // 2)

        if self.pos < self.height // 2:
            self.pos = self.height // 2

        self.draw()


class Ball:
    def __init__(self):
        self.rect = pg.Rect(0, 0, 10, 10)
        self.x, self.y = 0, 0
        self.vx, self.vy = 0, 0

        self.move(width // 2, height // 2)

    def __str__(self):
        return "pos = (" + str(self.x) + "," + str(self.y) + "), vel = (" + str(self.vx) + "," + str(self.vy) + ")"

    def draw(self):
        pg.draw.ellipse(screen, (255, 255, 255), self.rect)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

        self.rect.centerx = int(self.x)
        self.rect.centery = int(self.y)

        self.draw()

    def update(self):
        global left, right

        #  Ball hits left paddle
        if self.rect.colliderect(left.rect):
            self.vx = abs(self.vx)
        #  Ball hits right paddle
        if self.rect.colliderect(right.rect):
            self.vx = abs(self.vx) * -1
        #  Ball hits top
        if self.rect.top < 0:
            self.vy = abs(self.vy)
        #  Ball hits bottom
        if self.rect.bottom > height:
            self.vy = abs(self.vy) * -1
        #  Ball leaves sides
        if self.rect.left > width or self.rect.right < 0:
            game_over()

        self.move(self.vx, self.vy)


class Title:
    def __init__(self, text, x, y, size):
        self.pos = (x, y)
        self.font = pg.font.Font("Retro_Gaming.ttf", size)
        self.update(text)
        titles.append(self)

    def draw(self):
        screen.blit(self.text, self.rect)

    def update(self, text):
        self.text = self.font.render(text, True, (200, 200, 200))
        self.rect = self.text.get_rect()
        self.rect.center = self.pos

        self.draw()


def init():
    """setup paddles and ball"""
    global left, right, ball
    left = Paddle("left")
    right = Paddle("right")
    ball = Ball()

    angle = randrange(360) * (pi / 180)

    ball.vy = cos(angle) * speed * 1.5
    ball.vx = sin(angle) * speed * 1.5

    Title("test", 50, width // 2, 20)


def game_over():
    """reset game"""
    global ball
    ball = None

    sleep(0.5)
    init()


def play(paddle):
    """for when computer is playing a paddle"""
    if ball.y > paddle.pos:
        paddle.move(speed)
    elif ball.y < paddle.pos:
        paddle.move(-speed)


width, height = (900, 800)
left, right, ball = None, None, None
pressed_keys = []
titles = []
speed = 0.2

pg.init()
screen = pg.display.set_mode((width, height))

init()

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
            break
        if event.type == pg.KEYDOWN:
            pressed_keys.append(event.key)
        if event.type == pg.KEYUP:
            pressed_keys.remove(event.key)

    for key in pressed_keys:
        #print(key)
        if key == 119:  # W
            left.move(-speed)

        if key == 115:  # S
            left.move(speed)

        if key == 273:  # Up arrow
            right.move(-speed)

        if key == 274:  # Down arrow
            right.move(speed)

        if key == 27:  # Escape
            game_over()

    for title in titles:
        title.draw()

    play(right)

    screen.fill((0, 0, 0))
    left.draw()
    right.draw()

    ball.update()

    pg.display.flip()
