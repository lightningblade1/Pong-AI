import random
import sys

import pygame


class Paddle(pygame.sprite.Sprite):
    def __init__(self, player, window_width, window_height):
        if player == "L":
            self.Player = player
            self.pos_x = 0 + 12
            self.pos_y = window_height / 2
        if player == "R":
            self.Player = player
            self.pos_x = window_width - 12
            self.pos_y = window_height / 2
        super().__init__()
        self.hits = 0
        self.width = window_width
        self.height = window_height
        self.paddle_speed = 4
        self.image = pygame.Surface((12, 100))
        self.rect = self.image.get_rect(center=(50, 50))
        # self.image.fill(color)
        pygame.draw.rect(self.image, "White", (0, 0, 12, 100))
        self.rect.center = (self.pos_x, self.pos_y)

    def update(self, *args, **kwargs):
        keys = pygame.key.get_pressed()
        if self.Player == "L":
            if (keys[pygame.K_UP] and self.rect.center[1] > 0 + self.image.get_size()[1] / 2) or (
                    kwargs["L"] == 1 and self.rect.center[1] > 0 + self.image.get_size()[1] / 2):
                self.rect.center = (self.rect.center[0], self.rect.center[1] - self.paddle_speed)
            if (keys[pygame.K_DOWN] and self.rect.center[1] < self.height - 50) or (
                    kwargs["L"] == 2 and self.rect.center[1] < self.height - 50):
                self.rect.center = (self.rect.center[0], self.rect.center[1] + self.paddle_speed)
        if self.Player == "R":
            if (keys[pygame.K_w] and self.rect.center[1] > 0 + self.image.get_size()[1] / 2) or (
                    kwargs["R"] == 1 and self.rect.center[1] > 0 + self.image.get_size()[1] / 2):
                self.rect.center = (self.rect.center[0], self.rect.center[1] - self.paddle_speed)
            if (keys[pygame.K_s] and self.rect.center[1] < self.height - 50) or (
                    kwargs["R"] == 2 and self.rect.center[1] < self.height - 50):
                self.rect.center = (self.rect.center[0], self.rect.center[1] + self.paddle_speed)


class Puck(pygame.sprite.Sprite):
    def __init__(self, window_width, window_height):
        super().__init__()
        self.image = pygame.image.load("ball.png")  # loads image
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()  # get the rectangular area of the image or suface
        self.rect.center = (window_width / 2, window_height / 2)
        self.max_speed = 10
        choice_sign = random.choice([1, -1])
        choice_num = random.choice([1, 2, 3, 4, 5])
        self.xspeed = choice_num * choice_sign
        choice_num = random.choice([1, 2, 3, 4, 5])
        choice_sign = random.choice([1, -1])
        self.yspeed = choice_num * choice_sign  # 0self.max_speed
        self.left_score = 0
        self.right_score = 0
        self.width = window_width
        self.height = window_height

    def update(self):
        self.rect.center = (self.rect.center[0] + self.xspeed, self.rect.center[1] + self.yspeed)
        if self.rect.center[0] < 40:
            self.rect.center = (self.width / 2, self.height / 2)
            choice_sign = random.choice([1])
            choice_num = random.choice([1, 2, 3, 4, 5])
            self.xspeed = choice_num * choice_sign
            choice_num = random.choice([1, 2, 3, 4, 5])
            choice_sign = random.choice([1, -1])
            self.yspeed = choice_num * choice_sign
            self.right_score += 1
        elif self.rect.center[0] > self.width-40:
            self.rect.center = (self.width / 2, self.height / 2)
            choice_sign = random.choice([1, -1])
            choice_num = random.choice([4, 5,6,7])
            self.xspeed = choice_num * choice_sign
            choice_num = random.choice([1, 2, 3, 4, 5])
            choice_sign = random.choice([1, -1])
            self.yspeed = choice_num * choice_sign
            self.left_score += 1
        if self.rect.center[1] - (self.rect.height / 2) <= 0:
            self.yspeed = abs(self.yspeed)
            # better implementation could have been made but this solves the jitter problem
        elif self.rect.center[1] + (self.rect.height / 2) >= self.height:
            self.yspeed *= -1

        # if self.rect.center[1]

        # puck.yspeed = -1 * puck.yspeed


class Game():
    def __init__(self, width=1000, height=700):

        self.clock = pygame.time.Clock()
        self.window_width = width
        self.window_height = height
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.mouse.set_visible(False)
        self.surface = pygame.Surface((self.window_width, self.window_height))
        self.WHITE = (255, 255, 255)
        self.SCORE_FONT = pygame.font.SysFont("comicsans", 50)
        # surface.set_colorkey('White')

        self.puck = Puck(self.window_width, self.window_height)
        self.paddleL = Paddle("L", self.window_width, self.window_height)
        self.paddleR = Paddle("R", self.window_width, self.window_height)
        self.puck_group = pygame.sprite.Group()
        self.paddle_group = pygame.sprite.Group()
        self.puck_group.add(self.puck)
        self.paddle_group.add(self.paddleL)
        self.paddle_group.add(self.paddleR)

    def draw(self, win, paddles, ball, left_score, right_score, WHITE, SCORE_FONT):
        left_score_text = SCORE_FONT.render(f"{left_score}", 1, WHITE)
        right_score_text = SCORE_FONT.render(f"{right_score}", 1, WHITE)
        win.blit(left_score_text, (self.window_width // 4 - left_score_text.get_width() // 2, 20))
        win.blit(right_score_text, (self.window_width * (3 / 4) -
                                    right_score_text.get_width() // 2, 20))

        for i in range(10, self.window_height, self.window_height // 20):
            if i % 2 == 1:
                continue
            pygame.draw.rect(win, WHITE, (self.window_width // 2 - 5, i, 10, self.window_height // 20))

    def collide(self, puck, paddleL, paddleR):
        puck.rect.colliderect(paddleL.rect)
        if puck.rect.colliderect(paddleL.rect):
            # puck.yspeed = -1 * puck.yspeed
            puck.xspeed = puck.xspeed * (-1)

            paddleL.hits += 1
            # i want reduction factor "R" to be maximum velocity "Mv" when distance "D" between ball and mid of ball is max meaning: D/R=Mv
            # we know Mv and we know D so we can calculate R

        elif puck.rect.colliderect(paddleR.rect):
            puck.xspeed = puck.xspeed * (-1)

            paddleR.hits += 1
