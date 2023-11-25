import pygame
from pygame.locals import *
import time
import random

import asyncio

print("KITCHUMITCHU WANTS FOOD!!!!!")

SIZE = 71
WHITE = (237, 250, 252)
PINK = (247, 200, 235)
RED = (255, 17, 0)
BLACK = (0, 0, 0)
WIDTH = 400
HEIGHT = 400

def start():
    font = pygame.font.Font(None, 39)
    pygame.fill(PINK)
    text = font.render("START TO EAT CHERRYS", True, RED, PINK)
    textReact = text.get_rect()
    textReact.center = [WIDTH // 2 // 2]
    pygame.blit(text, textReact)
    pygame.display.update()
    pygame.time.wait(1200)
    pygame.fill(WHITE)


class Cherry:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("Resources/Cherry.png").convert()
        self.x = 140
        self.y = 140

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1, 10) * SIZE
        self.y = random.randint(1, 10) * SIZE


class Snake:
    def __init__(self, surface, length):
        self.parent_screen = surface
        self.block = pygame.image.load("Resources/Snake.jpg").convert()
        self.length = length
        self.x = [40] * length
        self.y = [40] * length
        self.direction = 'down'

    def walk(self):
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]
        if self.direction == 'left':
            self.x[0] -= SIZE
        elif self.direction == 'right':
            self.x[0] += SIZE
        elif self.direction == 'up':
            self.y[0] -= SIZE
        elif self.direction == 'down':
            self.y[0] += SIZE
        self.draw()

    def draw(self):
        self.parent_screen.fill((3, 202, 252))
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def move_right(self):
        self.direction = 'right'

    def move_left(self):
        self.direction = 'left'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def increase_Len(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)


def is_collision(x1, y1, x2, y2):
    if x2 <= x1 <= x2 + SIZE:
        if y2 <= y1 <= y2 + SIZE:
            return True
    return False


class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((800, 800))
        pygame.display.set_caption("Kitchumitchu Eats")

        pygame.mixer.init()
        self.snakeObj = Snake(self.surface, 1)
        self.snakeObj.draw()
        self.CherryObj = Cherry(self.surface)
        self.CherryObj.draw()

    def play_sound(self, sound):
        if sound == "drama":
            sound = pygame.mixer.Sound("Resources/drama.mp3")
        elif sound == "Magicend":
            sound = pygame.mixer.Sound("Resources/Magicend.mp3")

        pygame.mixer.Sound.play(sound)

    def Play(self):
        self.snakeObj.walk()
        self.CherryObj.draw()
        self.Display_Score()
        self.Money()
        pygame.display.flip()

       #snake collide with CHERRY
        if is_collision(self.snakeObj.x[0], self.snakeObj.y[0], self.CherryObj.x, self.CherryObj.y):
            self.play_sound("drama")
            self.snakeObj.increase_Len()
            self.CherryObj.move()
            print("Give me more food!!!!!! :)")

        #snake collide with itself
        for i in range(3, self.snakeObj.length):
            if is_collision(self.snakeObj.x[0],  self.snakeObj.y[0],  self.snakeObj.x[i],  self.snakeObj.y[i]):
                self.play_sound("Magicend")
                raise "The cat got KILLED! :)"

        if not(0 <= self.snakeObj.x[0] <= 800 and self.snakeObj.y[0] <= 800):
            self.play_sound('Snake Crash')
            raise "Hit the boundary error"

    def Display_Score(self):
        font = pygame.font.SysFont('Fantasy', 35, "italic")
        score = font.render(f"Tokens:{self.snakeObj.length}", True, (255, 255, 255))
        self.surface.blit(score, (650, 20))

    def Money(self):
        font = pygame.font.SysFont('Fantasy', 40, "Fantasy")
        score = font.render(f"Money:{self.snakeObj.length*4}", True, (251, 255, 0))
        self.surface.blit(score, (20, 20))

    def show_game_over(self):
        self.surface.fill((0, 191, 255))
        font = pygame.font.SysFont('arial', 36)
        line1 = font.render(f"Eating time is over your score is  {self.snakeObj.length}", True, (255, 0, 0))
        self.surface.blit(line1, (311, 311))
        line2 = font.render(f"Cardboard coins earned : {self.snakeObj.length*4}", True, (251, 255, 0))
        self.surface.blit(line2, (211, 211))
        line3 = font.render("PRESS ENTER TO PLAY!", True, (255, 255, 255))
        self.surface.blit(line3, (111, 111))

        pygame.display.flip()

    def reset(self):
        self.snakeObj = Snake(self.surface, 1)
        self.CherryObj = Cherry(self.surface)

    def speed(self):
        if self.snakeObj.length >= 5:
            time.sleep(0.2)
        elif self.snakeObj.length >= 12:
            time.sleep(0.1)

        else:
            time.sleep(0.3)





    def run(self):
        running = True
        pause = False
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RETURN:
                        pause = False

                    if not pause:
                        if event.key == K_LEFT:
                            self.snakeObj.move_left()
                        if event.key == K_RIGHT:
                            self.snakeObj.move_right()
                        if event.key == K_UP:
                            self.snakeObj.move_up()
                        if event.key == K_DOWN:
                            self.snakeObj.move_down()
                elif event.type == QUIT:
                    running = False
            try:
                if not pause:
                    self.Play()

            except Exception:
                self.show_game_over()
                pause = True
                self.reset()
            self.speed()

if __name__ == '__main__':
    game = Game()
    game.run()
