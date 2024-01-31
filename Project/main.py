### LIBRARIES ###
from tqdm import tqdm
from utils import *
from game import *
from RandomPlayer import RandomPlayer
from RLPlayer import RLPlayer
from MinmaxPlayer import MinmaxPlayer


### GLOBAL PARAMETERS ###

TRAINING = False
TESTING = True


if __name__ == '__main__':

    playerRL = RLPlayer()


    if TRAINING :
        print(" Training of RL agent")
        playerRL.training()


    if TESTING:
        print("Testing")
        playerRL.test_random()


    PlayerMM = MinmaxPlayer(2)
    PlayerR = RandomPlayer()

    NB_GAMES = 10
    DEPTH = 2
    wins = 0
    losses = 0
    for _ in tqdm(range(NB_GAMES)):
        g = BetterGame()
        player1 = MinmaxPlayer(DEPTH)  # put the depth as parameter
        player2 = RandomPlayer()
        winner = g.play(player1, player2)  #player1 plays as 0 and player2 plays as 1
        if winner == 0:
            wins += 1
        if winner == 1:
            losses += 1
            
    print_stats(wins, losses, NB_GAMES," Results of MinMaxPlayer({}) vs RandomPlayer on {} games".format(DEPTH, NB_GAMES))



        

