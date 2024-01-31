from game import *
import random
from tqdm import tqdm
from scipy.special import softmax
import numpy as np
import pickle
from utils import *
from RandomPlayer import *




class RLPlayer(Player):
    def __init__(self) -> None:
        super().__init__()
        self.moves = [Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT] # available moves
        self.col = range(5) #size of the game
        self.row = self.col
        self.len_move = 16 #number of pieces on the border (playable)
        self.ind = [[(i,j) for i in self.row] for j in self.col] # coordinates of each position
        self.last_move: [[Move]] # last move chosen for each position
        self.picks: [[int]] # number of times each position was chosen to play
        self.pos_proba: [[float]] #probability of choosing each position
        self.move_proba: [[[float]]] # probability pf each move for each position
        self.id = -1 #actual player
        self.training_size = 15000 
        self.testing_size = 3000
        self.lr = 0.2 #learning_rate
        self.wins = 0 # number of wins achieved
        self.nb_games = 0 # number of training games played
        self.last_reward = 0 # last reward obtained on a training game
        self.epsilon = 1.0 #exploration parameter
        self.decay_rate = 0.05 # rate of decay for the epsilon parameter


    def is_playable(self, position: tuple[int, int], player_id: int, board) -> bool:
        '''This function check that the piece we want to use is within the border limit and is not occupied by the opponent'''

        border = False
        available = False
        # Check error of position
        if (position[0] >=5 or position[1]>=5 or position[0]<0 or position[1]<0):
            print("There is an error the row/col cannot be greater or equal to 5 ")
            border = False
        # Check border
        elif (position[0] == 0 or position[0] == 4 or position[1] == 0 or position[1] == 4):
            border = True
        # Check availability
        if (board[position] == player_id or board[position] == -1):
            available = True
        return (border and available) 
          

    
    def get_move(self):
            """ This function predict the best piece and move with respect to the probability"""
            flat_proba = [item for row in self.pos_proba for item in row]
            proba = softmax(flat_proba) # we want them to sum up to one
            flat_ind = [item for row in self.ind for item in row]
            valid_idx = [0, 1, 2, 3, 4, 5, 9, 10, 14, 15, 19, 20, 21, 22, 23, 24] # we can only move pieces on the border
            table_idx = [i for i in  range(len(flat_proba))]          
            ind = np.random.choice(table_idx, p=proba)
            while ind not in valid_idx:
                ind = np.random.choice(table_idx, p=proba)

            row = flat_ind[ind][0]
            col = flat_ind[ind][1]
            moves = [Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT]
            move = np.random.choice(moves, p = softmax(self.move_proba[row][col]))
            return row, col, move
    



    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        """ This function is determining the next move"""

        self.id = game.get_current_player() #update the actual player
        if random.uniform(0,1) < self.epsilon:   #random exploration
            row = random.randint(0,4)
            col = random.randint(0,4)
            while not self.is_playable((row,col),self.id, game.get_board()): 
                row = random.randint(0,4)
                col = random.randint(0,4)

            if (row == 0 and col == 0):
                move =  random.choice([Move.BOTTOM, Move.RIGHT]) 
            elif (row == 0 and col == 4):
                move = random.choice([Move.BOTTOM, Move.LEFT]) 
            elif (row == 4 and col == 0):
                move = random.choice([Move.TOP, Move.RIGHT]) 
            elif (row == 4 and col == 4):
                move = random.choice([Move.TOP, Move.LEFT]) 
            elif (row == 0):
                move = random.choice([Move.BOTTOM, Move.LEFT, Move.RIGHT]) 
            elif (row == 4):
                 move = random.choice([Move.TOP, Move.LEFT, Move.RIGHT]) 
            elif (col == 0):
                move = random.choice([Move.TOP, Move.BOTTOM, Move.RIGHT]) 
            elif (col == 4):
                move = random.choice([Move.TOP, Move.BOTTOM, Move.LEFT]) 

            self.picks[row][col] += 1 #1
            self.last_move[row][col] = move
        
        else:
            row, col, move = self.get_move()
            while game.get_board()[row][col] == 1 - self.id:
                row, col, move = self.get_move()  
            self.picks[row][col] += 1
            self.last_move[row][col] = move

        return (col,row), move
 




    def init_proba(self):
        """ This function initialize every attributs"""
        self.pos_proba = [[0 for _ in self.col] for _ in self.row] # proba of each position
        self.picks = [[0 for i in self.row] for j in self.col] # Number of picks for each position
        self.last_move = [[0 for i in self.row] for j in self.col] # last move of each position
        self.move_proba = [[[0 for _ in range(4)] for _ in self.col] for _ in self.row] # proba of TOP, BOTTOM, LEFT, RIGHT for each position
              
        for i in range(5):
            self.pos_proba[0][i] = 1/self.len_move
            self.pos_proba[4][i] = 1/self.len_move
            self.pos_proba[i][0] = 1/self.len_move
            self.pos_proba[i][4] = 1/self.len_move

        # if we are in a corner there is only two directions where we can move 
        self.move_proba[0][0] = [0, 0.5, 0, 0.5] 
        self.move_proba[0][4] = [0, 0.5, 0.5, 0]
        self.move_proba[4][0] = [0.5, 0, 0, 0.5]
        self.move_proba[4][4] = [0.5, 0, 0.5, 0]

        self.last_move[0][0] = random.choice([Move.BOTTOM, Move.RIGHT])
        self.last_move[0][4] = random.choice([Move.BOTTOM, Move.LEFT])
        self.last_move[4][0] = random.choice([Move.TOP, Move.RIGHT])
        self.last_move[4][4] = random.choice([Move.TOP, Move.LEFT])

        # when we on the border but not in the corner, we can move in 3 directions
        for i in range(1,4):
                self.move_proba[0][i] = [0, 1/3, 1/3, 1/3] # we can't move to the top
                self.move_proba[4][i] = [1/3, 0, 1/3, 1/3] # we can't move to the bottom
                self.move_proba[i][0] = [1/3, 1/3, 0, 1/3] # we can't move to the left
                self.move_proba[i][4] = [1/3, 1/3, 1/3, 0] # we can't move to the right
        
                self.last_move[0][i] = random.choice([Move.BOTTOM, Move.LEFT, Move.RIGHT])
                self.last_move[4][i] = random.choice([Move.TOP, Move.LEFT, Move.RIGHT])
                self.last_move[i][0] = random.choice([Move.TOP, Move.BOTTOM, Move.RIGHT])
                self.last_move[i][4] = random.choice([Move.TOP, Move.BOTTOM, Move.LEFT])



    def init_random(self):
        """ This function initialize every attributs randomly"""
        self.pos_proba = [[0 for _ in self.col] for _ in self.row] # proba of each position
        self.picks = [[0 for i in self.row] for j in self.col] # Number of picks for each position
        self.ind = [[(i,j) for i in self.row] for j in self.col] # coordinates of each position
        self.last_move = [[0 for i in self.row] for j in self.col] # last move of each position
        self.move_proba = [[[0 for _ in range(4)] for _ in self.col] for _ in self.row] #proba of TOP, BOTTOM, LEFT, RIGHT for each position
        
        for i in range(5):
            self.pos_proba[0][i] = random.random()
            self.pos_proba[4][i] = random.random()
            self.pos_proba[i][0] = random.random()
            self.pos_proba[i][4] = random.random()

        self.last_move[0][0] = random.choice([Move.BOTTOM, Move.RIGHT])
        self.last_move[0][4] =  random.choice([Move.BOTTOM, Move.LEFT])
        self.last_move[4][0] = random.choice([Move.TOP, Move.RIGHT])
        self.last_move[4][4] = random.choice([Move.TOP, Move.LEFT])

        self.move_proba[0][0] = [0,random.random(),0,random.random()]
        self.move_proba[0][4] = [0,random.random(),random.random(),0]
        self.move_proba[4][0] = [random.random(),0,0,random.random()]
        self.move_proba[4][4] = [random.random(),0,random.random(),0]

        for i in range(1,4):

            self.last_move[0][i] = random.choice([Move.BOTTOM, Move.LEFT, Move.RIGHT])
            self.last_move[4][i] = random.choice([Move.TOP, Move.LEFT, Move.RIGHT])
            self.last_move[i][0] = random.choice([Move.TOP, Move.BOTTOM, Move.RIGHT])
            self.last_move[i][4] = random.choice([Move.TOP, Move.BOTTOM, Move.LEFT])      

            self.move_proba[0][i] = [0, random.random(), random.random(), random.random()] # we can't move to the top
            self.move_proba[4][i] = [random.random(), 0, random.random(), random.random()] # we can't move to the bottom
            self.move_proba[i][0] = [random.random(), random.random(), 0, random.random()] # we can't move to the left
            self.move_proba[i][4] = [random.random(), random.random(), random.random(), 0] # we can't move to the right


    def clear_picks(self):
        """This functions serves to clean all the picks (ie. set it back to 0)"""
        for i in self.row:
            for j in self.col:
                self.picks[i][j] = 0 



    def training(self):
        """ This function serves for the training of the weights"""
        self.init_proba()
        self.epsilon=1
        win_count = 0
        for _ in  tqdm(range(self.training_size)):
            g = Game()
            player1 = self
            player2 = RandomPlayer()
            winner = g.play(player1, player2)
            self.update_weights(winner)
            rew = self.reward_function(winner)
            self.update_epsilon(rew)
            if winner == 0:
                win_count+=1
                    
        self.save_weights()
        return (win_count/self.training_size)*100


    def update_weights(self, winner): 
        """ This function modify the proba in order to take into account the reward after the game"""
        if winner == 0: 
            los = 1
        else :
            los = 0 
        for i in self.row:
            for j in self.col:
                if  self.picks[i][j] >= 1: # if the piece was used
                    reward = ((los - self.pos_proba[i][j])*self.lr)/self.picks[i][j]
                    self.pos_proba[i][j] = self.pos_proba[i][j] + reward
                    index_moves = self.moves.index(self.last_move[i][j])
                    self.move_proba[i][j][index_moves] = self.move_proba[i][j][index_moves] + reward
                    self.picks[i][j]= 0 # we put it back to 0
        return reward

    def reward_function(self, winner):
        """ This function serves as a reward/fitness function that evolves after each game (it stays between 0 and 1)"""
        self.nb_games +=1    
        if winner == 0:
            self.wins +=1

        return self.wins/self.nb_games
            
    def update_epsilon(self, reward):
        """ This function adapt epsilon the exploration parameter based on the reward obtained"""
        if reward > self.last_reward : # Decrease epsilon for better performance
            epsilon = self.epsilon - self.decay_rate
        else :
            epsilon = self.epsilon - self.decay_rate
        
        epsilon = max(0.1, epsilon) 
        self.epsilon = min (1, epsilon)




    def save_weights(self):
        """ This function saves the weights after training"""

        fw = open('proba_pos', 'wb')
        pickle.dump(self.pos_proba, fw)
        fw.close()
        fw = open('proba_move', 'wb')
        pickle.dump(self.move_proba, fw)
        fw.close()


    def load_weights(self, file1, file2):
            """ This function use file to initialize weights"""
            self.init_proba()
            self.epsilon = 0
            fr = open(file1, 'rb')
            self.pos_proba = pickle.load(fr)
            fr.close()

            fr = open(file2, 'rb')
            self.move_proba = pickle.load(fr)
            fr.close()



    def test_random(self):
        """ This function serves to play against a random player"""
        print("RL vs. Random")
        self.init_proba()
        self.epsilon = 0.1 # we want it mainly to use the weights trained when playing
        win_count = 0
        self.load_weights("proba_pos", "proba_move")
        for _ in tqdm(range(self.testing_size)):
            self.clear_picks()
            g = Game()
            alea = random.randint(0,1)
            player = [self, RandomPlayer()]
            winner = g.play(player[alea], player[1-alea])
            if winner == self.id:
                win_count+=1

        ratio = (win_count/self.testing_size)*100
        print("The winning ratio of RL vs. Random is : {} %".format(ratio))
        return ratio







