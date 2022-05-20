import pickle
import sys
import pygame
import os
from me_pong import Game
import neat


def test_ai( genome, config,game):
    net = neat.nn.FeedForwardNetwork.create(genome, config)

    run = True
    clock = pygame.time.Clock()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        output = net.activate(
            (game.paddleR.rect.center[1], game.puck.rect.center[1],
             abs(game.paddleL.rect.center[0] - game.puck.rect.center[0])))
        decision = output.index(max(output))


        pygame.display.flip()
        screen.blit(surface, (0, 0))
        game.puck_group.draw(game.screen)
        game.paddle_group.draw(game.screen)
        game.puck_group.update()
        game.draw(game.screen, [game.paddleL, game.paddleR], game.puck, game.puck.left_score, game.puck.right_score,
                  game.WHITE, game.SCORE_FONT)
        game.paddle_group.update(R=decision, L=0)
        game.collide(game.puck, game.paddleL, game.paddleR)
        pygame.display.update()
        game.clock.tick(60)

    pygame.quit()
def train_ai(game, genome1, genome2, config):
    net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
    net2 = neat.nn.FeedForwardNetwork.create(genome2, config)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        output1 = net1.activate(
            (game.paddleL.rect.center[1], game.puck.rect.center[1],
             abs(game.paddleL.rect.center[0] - game.puck.rect.center[0])))
        decisionL = output1.index(max(output1))
        output2 = net2.activate(
            (game.paddleR.rect.center[1], game.puck.rect.center[1],
             abs(game.paddleR.rect.center[0] - game.puck.rect.center[0])))
        decisionR = output2.index(max(output2))
        #pygame.display.flip()
        screen.blit(surface, (0, 0))
        game.puck_group.draw(game.screen)
        game.paddle_group.draw(game.screen)
        game.puck_group.update()
        game.draw(game.screen, [game.paddleL, game.paddleR], game.puck, game.puck.left_score, game.puck.right_score,
                  game.WHITE, game.SCORE_FONT)
        game.paddle_group.update(R=decisionR, L=decisionL)
        game.collide(game.puck, game.paddleL, game.paddleR)
        pygame.display.update()
        #game.clock.tick(200)
        if game.puck.left_score >= 1 or game.puck.right_score >= 1:
            calculate_fitness(genome1, genome2, game)
            break


def calculate_fitness( genome1, genome2, game):
    genome1.fitness += game.paddleL.hits
    genome2.fitness += game.paddleR.hits
    if game.paddleL.hits >= 10 or game.paddleR.hits >= 10:
        print ("here")

def eval_genomes(genomes, config):
    for i, (genome_id1, genome1) in enumerate(genomes):
        if i == len(genomes) - 1:
            break
        genome1.fitness = 0
        for genome_id2, genome2 in genomes[i + 1:]:
            genome2.fitness = 0 if genome2.fitness == None else genome2.fitness
            game = Game(1000, 700)
            train_ai(game, genome1, genome2, config)


def train_NEAT(config):
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1))
    winner = p.run(eval_genomes, 50)
    with open("best.pickle", "wb") as f:
        pickle.dump(winner, f)
def test_NEAT(config):
    width, height = 1000, 700
    window = pygame.display.set_mode((width, height))

    with open("best.pickle", "rb") as f:
        winner = pickle.load(f)

    game = Game(1000, 700)
    test_ai(winner, config,game)

if __name__ == "__main__":
    pygame.init()
    game = Game(1000, 700)
    screen = pygame.display.set_mode((1000, 700))
    surface = pygame.Surface((1000, 700))
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    #train_NEAT(config)
    test_NEAT(config)