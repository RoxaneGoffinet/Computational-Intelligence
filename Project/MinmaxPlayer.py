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
        

    def minimax(self, game: "BetterGame", depth, is_maximizing):
        """ This function is designed to return the best move that can be done by the current player."""
        if game.check_winner() != -1 or depth >= self.depth:
            return self.heuristic(game)

        possible_moves = self.all_possible_moves(game.current_player_idx, game.get_board())
        if is_maximizing:
            best_score = float("-inf")
            for move in possible_moves:
                new_game = deepcopy(game)
                player = 1 - new_game.current_player_idx 
                new_game.move(move[0], move[1], player)
                score = self.minimax(new_game, depth + 1, False)
                best_score = max(score, best_score)
            return best_score
        else:
            best_score = float("inf")
            for move in possible_moves:
                new_game = deepcopy(game)
                player = 1 - new_game.current_player_idx 
                new_game.move(move[0], move[1], player)
                score = self.minimax(new_game, depth + 1, True)
                best_score = min(score, best_score)
            return best_score


    def make_move(self, game: "BetterGame") -> tuple[tuple[int, int], Move]:
        """ This function is designed to return the best move that can be done by the current player."""
        best_score = float("-inf")
        best_m = None
        possible_moves = self.all_possible_moves(game.current_player_idx, game.get_board())
        for move in possible_moves:
            new_game = deepcopy(game)
            new_game.move(move[0], move[1], new_game.current_player_idx)
            score = self.minimax(new_game, 0, False)
            if score > best_score:
                best_score = score
                best_m = move

        return best_m[0], best_m[1]