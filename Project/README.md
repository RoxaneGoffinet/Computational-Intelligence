# Final Project fort the Computationnal Intelligence course

The goal of the project was to design ou own player for the game of Quixo. Quixo is a strategic board game played on a 5x5 grid with 25 cubes, the objective is to be the first player to align five of their cubes in a row, either horizontally, vertically, or diagonally. However we can only access the cune on the border and decide to move them to top, bottom, left or right. 


## RL Learning

In order to design a player able to win against a random one I designed a RLPlayer class where I use reinforcement learning to choose the next move. This class is visible in the file **main.py**, in **game.py** we have function that designed the board and the movement (it has not been touch and is the original one furnished by the professor), **main.ipynb** is only here to make it more easy to see the results at the first glance but this file doesn't contain any python functions. There is also 2 files called **proba_move** and **proba_pos** in the folder **weights** wich are binary files in wich we save the trained weights of the model (it is more convenient for testing). 