import sys
import neat
import pygame
import os
from me_pong import Game
import neat

pygame.init()
game = Game(1000, 700)
screen = pygame.display.set_mode((1000, 700))
surface = pygame.Surface((1000, 700))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
    pygame.display.flip()
    screen.blit(surface, (0, 0))
    game.puck_group.draw(game.screen)
    game.paddle_group.draw(game.screen)
    game.puck_group.update()
    game.draw(game.screen, [game.paddleL, game.paddleR], game.puck, game.puck.left_score, game.puck.right_score,
              game.WHITE, game.SCORE_FONT)
    game.paddle_group.update(L=0,R=0)
    game.collide(game.puck, game.paddleL, game.paddleR)
    pygame.display.update()

    game.clock.tick()
