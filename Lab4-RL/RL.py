import random
from collections import defaultdict
from copy import deepcopy
from game_functions import *

class RLearning:
    def __init__(self, alpha, epsilon, d):
        self.Q = defaultdict(float)
        self.alpha = alpha
        self.epsilon = epsilon
        self.d = d 

    def get_Q(self, state, action):
        state_key = (tuple(state.x), tuple(state.o))
        return self.Q[(state_key, action)]


    def choose_action(self, state, available):
        if random.random() < self.epsilon:
            return random.choice(available)
        else:
            Q_vals= [self.get_Q(state, action) for action in available]
            max_Q = max(Q_vals)
            best_moves = [i for i in range(len(available)) if Q_vals[i] == max_Q]
            index = random.choice(best_moves)
            return available[index]

    def update_Q(self, state, action, reward, next_state, available):
        state_key = (tuple(state.x), tuple(state.o))
        next_Q_vals = [self.get_Q(next_state, next_action) for next_action in available]
        max_next_Q = max(next_Q_vals,default=0.0)
        self.Q[(state_key, action)] = (1 - self.alpha) * self.Q[(state_key, action)] + self.alpha * (reward + self.d * max_next_Q)



def fitness(pos: State, player):
    """ Evaluate state: +1 first player wins """
    if check_win(pos.x):
        if player == 'x':
            return 1
        else:
            return -1
    elif check_win(pos.o):
        if player == 'o':
            return 1
        else:
            return -1
    else:
        return 0
    

def train(nb_train, alpha, epsilon, d, player):
    agent = RLearning(alpha, epsilon, d)
    #player = 'x' #we assumed that x is starting always firstly in our games function
    for i in range(nb_train): 
        state = State(set(), set())
        available = list(range(1, 10))
        player_turn = 'x'
        while available and not check_win(state):
            if player_turn == player:
                action = agent.choose_action(state, available)
            else:
                action = random.choice(available)

            previous_state = deepcopy(state)
            if player_turn == 'x':
                state.x.add(action)
            else:
                state.o.add(action)
            available.remove(action)
            reward = fitness(state, player)
            agent.update_Q(previous_state, action, reward, state, available)
            player_turn = 'o' if player_turn == 'x' else 'x'
        player = 'x' if player == 'o' else 'o'

    return agent

def optimization(epsilons, alphas, ds, player,nb_train=NB_TRAIN):
    best_agent = None
    best_percentage_win_agent = 0

    for epsilon in epsilons:
        for alpha in alphas:
            for d in ds:
                agent = train(nb_train=nb_train, alpha=alpha, epsilon=epsilon, d=d, player=player)
                win_agent, win_random, no_win = count_win(agent, player,  fitness)
                tot_games = win_agent + win_random + no_win
                percentage_win_agent = (win_agent / tot_games) * 100

                if percentage_win_agent > best_percentage_win_agent: #if the current agent is better than the previous one, we update the best agent and the best percentage
                    best_percentage_win_agent = percentage_win_agent
                    best_agent = agent

    return best_agent

  
