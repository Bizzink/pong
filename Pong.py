import pygame as pg
from sys import exit
from time import sleep, time
from random import randrange
from math import pi, cos, sin


class Paddle:
    def __init__(self, side):
        self.pos = height // 2
        self.rect = pg.Rect(0, 0, 10, height // 10)
        self.height = height // 10
        self.moving = None

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
        self.moving = direction

        if self.pos > height - (self.height // 2):
            self.pos = height - (self.height // 2)
            self.moving = None

        if self.pos < self.height // 2:
            self.pos = self.height // 2
            self.moving = None

        self.draw()


class Ball:
    def __init__(self, debug):
        self.rect = pg.Rect(0, 0, 20, 20)
        self.x, self.y = width // 2, height // 2
        self.rect.center = (self.x, self.y)
        self.debug = debug

        self.v = 0

        self.angle = randrange(360)

        while self.angle % 90 > 70 or self.angle % 90 < 20:
            self.angle = randrange(360)

        self.angle -= 180
        self.angle *= (pi / 180)

    def __str__(self):
        return "pos = (" + str(self.x) + "," + str(self.y) + "), vel = (" + str(self.v) + "," + str(self.angle) + "deg)"

    def draw(self):
        pg.draw.ellipse(screen, (255, 255, 255), self.rect)

        if self.debug:
            pg.draw.line(screen, (255, 0, 0), (self.x, self.y), (self.x + cos(self.angle) * 50, self.y + sin(self.angle) * 50))

    def move(self, dist):
        self.x += cos(self.angle) * dist
        self.y += sin(self.angle) * dist

        self.rect.center = (int(self.x), int(self.y))

        self.draw()

    def check_collide(self):
        global left, right, first_bounce

        if self.rect.colliderect(left):
            self.x = left.rect.right + self.rect.width // 2
            self.angle += ((pi / 2) - self.angle) * 2
            first_bounce = False

            if left.moving is not None:
                if randrange(20) > 10:
                    self.angle += left.moving * 0.5

        if self.rect.colliderect(right):
            self.x = right.rect.left - self.rect.width // 2
            self.angle += ((pi / 2) - self.angle) * 2
            first_bounce = False
# TODO: fix this
            if right.moving is not None:
                if randrange(20) > 10:
                    self.angle += right.moving * 0.5

        #  Ball hits top
        if self.rect.top < 0:
            self.rect.top = 1
            self.angle -= 2 * self.angle
        #  Ball hits bottom
        if self.rect.bottom > height:
            self.rect.bottom = height - 1
            self.angle -= 2 * self.angle


class Title:
    def __init__(self, text, x, y, size):
        self.text, self.rect = None, None
        self.string = text
        self.pos = (x, y)
        self.font = pg.font.Font("Retro_Gaming.ttf", size)
        self.update(text)
        titles.append(self)

    def draw(self):
        screen.blit(self.text, self.rect)

    def update(self, text):
        text = str(text)
        self.text = self.font.render(text, True, (200, 200, 200))
        self.rect = self.text.get_rect()
        self.rect.center = self.pos

        self.string = text

        self.draw()


def init():
    """setup paddles and ball"""
    global left, right, ball, first_bounce
    left = Paddle("left")
    right = Paddle("right")
    ball = Ball(True)

    first_bounce = True

    Title("Player 1", width // 4, 50, 25)

    if pc_play:
        Title("PC", width // 4 * 3, 50, 25)
    else:
        Title("Player 2", width // 4 * 3, 50, 25)


def game_over():
    """reset game"""
    global ball
    ball = None

    sleep(0.5)
    init()


def play(paddle):
    """for when computer is playing a paddle"""
    global ball
    if ball.y > paddle.pos:
        paddle.move((curr_tick - prev_tick) * speed)
    elif ball.y < paddle.pos:
        paddle.move((curr_tick - prev_tick) * -speed)


def tick(curr_time, prev_time):
    """runs calculations based on time since last frame, so movement isn't tied to framerate"""
    global ball, left, right
    dist = curr_time - prev_time

    if 119 in pressed_keys:  # W
        left.move(dist * -speed)

    if 115 in pressed_keys:  # S
        left.move(dist * speed)

    if 273 in pressed_keys:  # Up arrow
        right.move(dist * -speed)

    if 274 in pressed_keys:  # Down arrow
        right.move(dist * speed)

    ball.check_collide()

    if first_bounce:
        ball.move(dist * speed * 0.9)
    else:
        ball.move(dist * speed * 1.25)

    #  Ball leaves sides
    if ball.rect.left > width:
        scores[0].update(int(scores[0].string) + 1)
        game_over()

    elif ball.rect.right < 0:
        scores[1].update(int(scores[1].string) + 1)
        game_over()

    left.moving = None
    right.moving = None

    ball.draw()
    left.draw()
    right.draw()


width, height = (900, 800)
left, right, ball = None, None, None
pressed_keys = []
titles = []
speed = 300
first_bounce = True
pc_play = True

curr_tick = time()
prev_tick = 0

pg.init()
screen = pg.display.set_mode((width, height))

init()
scores = [Title("0", width // 4, 90, 20), Title("0", width // 4 * 3, 90, 20)]

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
            break
        if event.type == pg.KEYDOWN:
            pressed_keys.append(event.key)
        if event.type == pg.KEYUP:
            pressed_keys.remove(event.key)

    if 27 in pressed_keys:  # Escape
        game_over()

    screen.fill((0, 0, 0))

    pg.draw.rect(screen, (150, 150, 150), ((width // 2) - 2, 0, 4, height))

    for title in titles:
        title.draw()

    prev_tick = curr_tick
    curr_tick = time()

    tick(curr_tick, prev_tick)

    if pc_play:
        play(right)

    pg.display.flip()
