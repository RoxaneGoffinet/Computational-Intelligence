from game2 import *
from copy import deepcopy

class MinmaxPlayer(Player):
    def __init__(self, depth) -> None:
        super().__init__()
        self.depth = depth
        self.board_size = 5

    def all_possible_moves(self, player_id: int, board) -> list[list[tuple[int, int], Move]]:
            '''This function returns all the possible moves that can be done by a player in a given board'''

            all_possible_moves = []
            for row in range(5):
                for col in range(5):
                    available = False
                    border = False
                    # Check border
                    if (row == 0 or row == 4 or col == 0 or col == 4):
                        border = True
                    # Check availability
                    if (board[(row, col)] == player_id or board[(row, col)] == -1):
                        available = True

                    if border and available:
                        if (row == 0 and col == 0):
                            all_possible_moves.append([(row, col), Move.BOTTOM])
                            all_possible_moves.append([(row, col), Move.RIGHT])
                        elif (row == 4 and col == 0):
                            all_possible_moves.append([(row, col), Move.BOTTOM])
                            all_possible_moves.append([(row, col), Move.LEFT])
                        elif (row == 0 and col == 4):
                            all_possible_moves.append([(row, col), Move.TOP])
                            all_possible_moves.append([(row, col), Move.RIGHT])
                        elif (row == 4 and col == 4):
                            all_possible_moves.append([(row, col), Move.TOP])
                            all_possible_moves.append([(row, col), Move.LEFT])
                        elif (col == 0):
                            all_possible_moves.append([(row, col), Move.BOTTOM])
                            all_possible_moves.append([(row, col), Move.LEFT])
                            all_possible_moves.append([(row, col), Move.RIGHT])
                        elif (col== 4):
                            all_possible_moves.append([(row, col), Move.TOP])
                            all_possible_moves.append([(row, col), Move.LEFT])
                            all_possible_moves.append([(row, col), Move.RIGHT])
                        elif (row == 0):
                            all_possible_moves.append([(row, col), Move.TOP])
                            all_possible_moves.append([(row, col), Move.BOTTOM])
                            all_possible_moves.append([(row, col), Move.RIGHT])
                        elif (row == 4):
                            all_possible_moves.append([(row, col), Move.TOP])
                            all_possible_moves.append([(row, col), Move.BOTTOM])
                            all_possible_moves.append([(row, col), Move.LEFT])
                        else:
                            all_possible_moves.append([(row, col), Move.TOP])
                            all_possible_moves.append([(row, col), Move.BOTTOM])
                            all_possible_moves.append([(row, col), Move.LEFT])
                            all_possible_moves.append([(row, col), Move.RIGHT])

            return all_possible_moves

    

    def heuristic(self, game: "BetterGame") -> int:
        """ This function is designed to return the heuristic value of the current board."""

        winner = game.check_winner()
        if winner == game.current_player_idx:
            return 1
        elif winner == 1 - game.current_player_idx:
            return -1
        else:
            return (game.best_sequence() - 2.5) / 5
        

    def minmax(self, game: "BetterGame", depth, is_max) -> int:
        """ This function is designed to return the best move that can be done by the current player."""

        if game.check_winner() != -1 or depth >= self.depth:
            return self.heuristic(game)

        possible_moves = self.all_possible_moves(game.current_player_idx, game.get_board())
        
        if is_max:  # Maximizer
            best_score = float("-inf")
            for move in possible_moves:
                game_new = deepcopy(game)
                player = 1 - game_new.current_player_idx 
                game_new.move(move[0], move[1], player)
                current_score = self.minmax(game_new, depth + 1, False)
                best_score = max(current_score, best_score)
            return best_score
        else:                # Minimizer
            best_score = float("inf")
            for move in possible_moves:
                game_new = deepcopy(game)
                player = 1 - game_new.current_player_idx 
                game_new.move(move[0], move[1], player)
                current_score = self.minmax(game_new, depth + 1, True)
                best_score = min(current_score, best_score)
            return best_score


    def make_move(self, game: "BetterGame") -> tuple[tuple[int, int], Move]:
        """ This function is designed to return the best move that can be done by the current player."""

        best_score = float("-inf")
        best_move = None
        possible_moves = self.all_possible_moves(game.current_player_idx, game.get_board())
        for move in possible_moves:
            game_new = deepcopy(game)
            game_new.move(move[0], move[1], game_new.current_player_idx)
            current_score = self.minmax(game_new, 0, False)
            if current_score > best_score: # we keep the move with the best minmax score
                best_score = current_score
                best_move = move

        return best_move[0], best_move[1]