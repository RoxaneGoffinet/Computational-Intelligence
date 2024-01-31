# Final Project fort the Computationnal Intelligence course

The goal of the project was to design our own players for the game of Quixo. Quixo is a strategic board game played on a 5x5 grid with 25 cubes, the objective is to be the first player to align five of their cubes in a row, either horizontally, vertically, or diagonally. However we can only access the cune on the border and decide to move them to top, bottom, left or right. 

The major comparison between the different models are visible either in **main.ipynb** or **main.py**. We also import some functions from utils to enhance the visualization.

## Random Player

This is an already implemented player that is in **RandomPlayer.py** it chooses randomly the piece to move and the direction of the move

## Reinforcement Learning Player

In order to design a player able to win against a random one I designed a RLPlayer class where I use reinforcement learning to choose the next move. This class is visible in the file **RLPlayer.py**, in **game.py** we have function that designed the board and the movement (it has not been touch and is the original one furnished by the professor), **main.ipynb** is only here to make it more easy to see the results at the first glance but this file doesn't contain any python functions. There is also 2 files called **proba_move** and **proba_pos** in the folder **weights** wich are binary files in wich we save the trained weights of the model (it is more convenient for testing). 

## MimMax Player

Contrary to the RLPlayer the MinMax Player doesn't require training. It is also very very efficient at playing Quixo. The implementation can be found in the file **MinmaxPlayer.py**

