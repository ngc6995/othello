import numpy as np
import math
import random

class Othello:
    # Class constants
    # Black disc, white disc and empty square
    BLACK, WHITE, EMPTY = 1, -1, 0
    # If ai plays first, pick the move randomly
    FIRST_MOVE = {1:"d3", 2:"c4", 3:"f5", 4:"e6"}
    # Eight directions
    DIRECTIONS = ((0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1))
    # Infinity number
    INFINITY = math.inf
    # Computer win score
    WIN = 10000
    # Computer lost score
    LOST = -10000
    # Draw score
    DRAW = 0
    # Maximum search depth
    MAX_DEPTH = 5
    # Calculate the score of a giving position
    SCORE_MATRIX = (( 99, -25, 10, 5, 5, 10, -25,  99,),
                    (-25, -25,  1, 1, 1,  1, -25, -25,),
                    ( 10,   1,  5, 2, 2,  5,   1,  10,),
                    (  5,   1,  2, 1, 1,  2,   1,   5,),
                    (  5,   1,  2, 1, 1,  2,   1,   5,),
                    ( 10,   1,  5, 2, 2,  5,   1,  10,),
                    (-25, -25,  1, 1, 1,  1, -25, -25,),
                    ( 99, -25, 10, 5, 5, 10, -25,  99))

    def __init__(self):
        self.board = np.full((8, 8), self.EMPTY)
        self.board[3][3] = self.BLACK
        self.board[4][4] = self.BLACK
        self.board[3][4] = self.WHITE
        self.board[4][3] = self.WHITE
        self.player_turn = self.BLACK
        self.move_counter = 1
        self.flip_discs = []

    def __str__(self):
        # char = {Othello.BLACK:u"\u25CB", Othello.WHITE:u"\u25CF", Othello.EMPTY:u"\u25A1"}
        char = {self.BLACK:u"\u25CB", self.WHITE:u"\u25CF", self.EMPTY:u"\u2592"}
        board_str = ""
        row_num = 0
        for row in range(7, -1, -1):
            row_num += 1
            board_str += " " + str(row_num) + " "
            for col in range(8):
                board_str += char[self.board[row][col]]
            board_str += "\n"
        board_str += "    a b c d e f g h"
        return board_str

    @property
    def black_discs(self):
        discs = 0
        for row in range(8):
            for col in range(8):
                if self.board[row][col] == self.BLACK:
                    discs += 1
        return discs

    @property
    def white_discs(self):
        discs = 0
        for row in range(8):
            for col in range(8):
                if self.board[row][col] == self.WHITE:
                    discs += 1
        return discs

    @property
    def game_over(self):
        who_play = self.player_turn
        self.player_turn = self.BLACK
        black_legal_moves = len(self.legal_moves)
        self.player_turn = self.WHITE
        white_legal_moves = len(self.legal_moves)
        self.player_turn = who_play
        if black_legal_moves == 0 and white_legal_moves == 0:
            self.player_turn = None
            return True
        else:
            return False

    @property
    def legal_moves(self):
        return self.__get_legal_moves(self.board, self.player_turn)

    def __get_legal_moves(self, position, player):
        moves = []
        for row in range(8):
            for col in range(8):
                if self.__is_legal_move(position, player, row, col):
                    moves.append([row, col])
        return moves

    def __is_legal_move(self, position, player, row, col):
        if position[row][col] == self.EMPTY:
            for direction in self.DIRECTIONS:
                adj_row, adj_col = row, col  # Adjacent row and column.
                opp_discs = 0  # Opponent's disc counter.
                while True:
                    adj_row += direction[0]
                    adj_col += direction[1]
                    if adj_row < 0 or adj_row > 7 or adj_col < 0 or adj_col > 7:
                        break  # Out of bounds!
                    if position[adj_row][adj_col] == self.EMPTY:
                        break  # Adjacent square is empty.
                    if position[adj_row][adj_col] == player and opp_discs == 0:
                        break  # Not opponent's disc.
                    if position[adj_row][adj_col] == player and opp_discs > 0:
                        return True  # One valid move found.
                    opp_discs += 1
            # No valid move found, after checking eight directions.
            return False
        # Is not an empty square.
        return False

    def move(self, row, col):
        if self.__is_legal_move(self.board, self.player_turn, row, col):
            self.board, self.flip_discs = self.__make_move(self.board, self.player_turn, [row, col])
            self.__switch_player_turn()
            if len(self.legal_moves) == 0:
                self.__switch_player_turn()
            return True
        else:
            return False

    def __make_move(self, position, player, move):
        self.move_counter += 1
        row, col = move[0], move[1]
        new_position = position.copy()
        flip_discs = []  # All discs to flip.
        for direction in self.DIRECTIONS:
            adj_row, adj_col = row, col  # Adjacent row and column.
            new_flip_discs = []  # Discs to flip of one direction.
            opp_discs = 0  # Opponent's disc counter.
            while True:
                adj_row += direction[0]
                adj_col += direction[1]
                if adj_row < 0 or adj_row > 7 or adj_col < 0 or adj_col > 7:
                    break  # Out of bounds!
                if new_position[adj_row][adj_col] == self.EMPTY:
                    break  # Adjacent square is empty.
                if new_position[adj_row][adj_col] == player and opp_discs == 0:
                    break  # Not opponent's disc.
                if new_position[adj_row][adj_col] == player and opp_discs > 0:
                    flip_discs += new_flip_discs  # Store the opponent's discs to flip.
                    break  # Search next direction.
                new_flip_discs.append([adj_row, adj_col])
                opp_discs += 1
        # Update board.
        new_position[row][col] = player
        for flip_disc in flip_discs:
            new_position[flip_disc[0]][flip_disc[1]] = player
        return new_position, flip_discs

    def __switch_player_turn(self):
        self.player_turn *= -1
        
    def ai(self):
        self.__max_player = self.player_turn
        self.__min_player = self.__max_player * -1
        if self.move_counter == 1:
            move = self.notation_to_rc(self.FIRST_MOVE[random.randint(1, 4)])
        else:
            _, move = self.__alphabeta(self.board, self.MAX_DEPTH, -self.INFINITY, +self.INFINITY, True)
        return move

    def __alphabeta(self, node, depth, alpha, beta, maximizingPlayer):
        if depth == 0 or self.__terminal(node):
            return self.__evaluation(node), None
        if maximizingPlayer:
            max_player_moves = self.__get_legal_moves(node, self.__max_player)
            if len(max_player_moves) == 0:
                return self.__alphabeta(node, depth-1, alpha, beta, not maximizingPlayer)
            value = -self.INFINITY
            best_move = None
            for move in max_player_moves:
                child_node, _ = self.__make_move(node, self.__max_player, move)
                max_temp, _ = self.__alphabeta(child_node, depth-1, alpha, beta, False)
                if max_temp > value:
                    value = max_temp
                    best_move = move
                alpha = max(alpha, value)
                if alpha >= beta:
                    break  # Beta cut off
            return value, best_move
        else:
            min_player_moves = self.__get_legal_moves(node, self.__min_player)
            if len(min_player_moves) == 0:
                return self.__alphabeta(node, depth-1, alpha, beta, not maximizingPlayer)
            value = +self.INFINITY
            best_move = None
            for move in min_player_moves:
                child_node, _ = self.__make_move(node, self.__min_player, move)
                min_temp, _ = self.__alphabeta(child_node, depth-1, alpha, beta, True)
                if min_temp < value:
                    value = min_temp
                    best_move = move
                beta = min(beta, value)
                if beta <= alpha:
                    break  # Alpha cut off
            return value, best_move 

    def __terminal(self, position):
        max_legal_moves = self.__get_legal_moves(position, self.__max_player)
        min_legal_moves = self.__get_legal_moves(position, self.__min_player)
        if max_legal_moves == 0 and min_legal_moves == 0:
            max_discs, min_discs = 0, 0
            for row in range(8):
                for col in range(8):
                    if position[row][col] == self.__max_player:
                        max_discs += 1
                    elif position[row][col] == self.__min_player:
                        min_discs += 1
            if max_discs > min_discs:
                self.__terminal_state = self.WIN
            elif min_discs > max_discs:
                self.__terminal_state = self.LOST
            else:
                self.__terminal_state = self.DRAW
            return True
        else:
            self.__terminal_state = None
            return False

    def __evaluation(self, position):
        if self.__terminal_state is None:
            max_score, min_score = 0, 0
            for row in range(8):
                for col in range(8):
                    if not(position[row][col] == self.EMPTY):
                        if position[row][col] == self.__max_player:
                            max_score += self.SCORE_MATRIX[row][col]
                        else:
                            min_score += self.SCORE_MATRIX[row][col]
            return max_score - min_score
        else:
            return self.__terminal_state

    @staticmethod
    # Convert Othello notation to row and column
    def notation_to_rc(move):
        if len(move) == 2:
            move = move.upper()
            # ASCII value 'A' to 'H'
            if ord(move[0]) in range(65, 73):
                # ASCII value '1' to '8'
                if ord(move[1]) in range(49, 57):
                    row = 8 - int(move[1])
                    col = abs(65 - ord(move[0]))
                    return [row, col]
        # Invalid notation.
        return []

    @staticmethod
    # Convert row and column to Othello notation
    def rc_to_notation(row, col):
        return chr(97 + col) + str(8 - row)
