# Libraries
import matplotlib.pyplot as plt



def print_stats(win, lost, nb_games, title):
    """ This functions is designed to print the stats of the current game."""
    ratio_win = win / nb_games * 100
    ratio_draw = (nb_games - win - lost) / nb_games * 100
    ratio_lost = lost / nb_games * 100

    print("Stats:")
    print("  - Total number of plays: {}".format(nb_games))
    print("  - Number of wins: {}".format(win))
    print("  - Number of losts: {}".format(lost))
    print("  - Number of draws: {}".format(nb_games - win - lost))
    print("  - Percentage of winning: {:.2f}%".format(ratio_win))
 
    plt.pie([ratio_win, ratio_draw, ratio_lost], labels=["Wins", "Losses", "Draws"], explode = [0.15, 0,  0], autopct="%1.1f%%")
    plt.title(title)
    plt.show()




def print_statsMMRL(win_RL, win_MM, nb_games, title):
    """ This functions is designed to print the stats of the current game."""
    ratio_win_RL = win_RL / nb_games * 100
    ratio_draw = (nb_games - win_RL - win_MM) / nb_games * 100
    ratio_win_MM = win_MM / nb_games * 100

    print("Stats:")
    print("  - Total number of plays: {}".format(nb_games))
    print("  - Number of wins of RL Player: {}".format(win_RL))
    print("  - Number of wins of MinMax Player: {}".format(win_MM))
    print("  - Number of draws: {}".format(nb_games - win_MM - win_RL))
 
    plt.pie([ratio_win_RL, ratio_draw, ratio_win_MM], labels=["Wins RL", "Draws", "Wins MM"])
    plt.title(title)
    plt.show()