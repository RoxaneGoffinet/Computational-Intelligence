import random
from itertools import combinations
from collections import namedtuple
from copy import deepcopy

State = namedtuple('State', ['x', 'o'])
MAGIC = [2, 7, 6, 9, 5, 1, 4, 3, 8]
NB_TEST = 1000 # number of games to play for the statistics
NB_TRAIN = 10000 # number of episodes to play for the training
player = 'x' # player that will be trained, x is the first player, o is the second one


def check_win(elements):
    """Checks the grid to see if there is a winner."""
    win = any(sum(c) == 15 for c in combinations(elements, 3))
    return win
    
def game(agent, player): 
    """Play a game of tic-tac-toe. The player x is played by the agent while the o player uses a random strategy. """

    trajectory = list()
    state = State(set(), set())
    available = list(range(1, 10))
    if player == 'x':
        while available:
            x = agent.choose_action(state, available)
            state.x.add(x)
            trajectory.append(deepcopy(state))
            available.remove(x)
            if check_win(state.x) or not available:
                break

            o = random.choice(list(available))
            state.o.add(o)
            trajectory.append(deepcopy(state))
            available.remove(o)
            if check_win(state.o) or not available:
                break
    else:
        while available:
            x = random.choice(list(available))
            state.x.add(x)
            trajectory.append(deepcopy(state))
            available.remove(x)
            if check_win(state.x) or not available:
                break

            o = agent.choose_action(state,available)
            state.o.add(o)
            trajectory.append(deepcopy(state))
            available.remove(o)
            if check_win(state.o) or not available:
                break
    return trajectory


def count_win(agent, player, fitness):
    win_agent = 0
    win_random = 0
    no_win = 0
    for i in range(NB_TEST):
        trajectory = game(agent, player)
        fit = fitness(trajectory[-1], player)
        if fit == 1:
            win_agent += 1
        elif fit == -1:
            win_random += 1
        else:
            no_win+=1
    return win_agent, win_random, no_win





def stats(win_agent, win_random, num_draw):
    """Returns the statistics of a game."""
    total_games =  win_agent + win_random + num_draw
    percent_win_agent = (win_agent / total_games) * 100
    percent_win_random = (win_random / total_games) * 100
    percent_draw = (num_draw / total_games) * 100
    percent_win_agent_vs_random= (win_agent/(win_agent + win_random))*100
    print("The agent wins {} % of time: ".format(percent_win_agent))
    print(f"Percentage wins of the random player: {percent_win_random}%")
    print(f"Percentage of draws: {percent_draw}%")
    print(f"Percentage wins of the agent with respect to the random player: {percent_win_agent_vs_random}%")
    #return percent_win_agent, percent_win_random, percent_draw, percent_win_agent_vs_random