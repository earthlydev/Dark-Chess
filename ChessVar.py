# Author: Jericho Arizala
# GitHub username: earthlydev
# Date: 12/08/2024
# Description:

import pprint

class ChessVar:
    """
    A class to represent a game of dark chess. Uses Chess Piece class
    to gather chess piece moves.
    """
    def __init__(self):
        """
        takes no parameters, initializes the board, and places pieces into
        starting positions. all data members are private.
        """
        self._board = [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        ]

    def convert_position(self, pos):
        """
        Convert the position into board indices
        :param pos: A string for the position specified
        :return: A tuple for the row and the column
        """
        columns = ['a','b','c','d','e','f','g','h']
        rows = ['8','7','6','5','4','3','2','1']
        col = columns.index(pos[0])
        row = rows.index(pos[1])
        return row, col

    def get_game_state(self):
        """
        Gets the game state
        :return: 'UNFINISHED' for game currently player, 'WHITE_WON' for white is winner,
        'BlACK_WON' for black is winner.
        """
        if any('K' in row for row in self._board) and ('k' in row for row in self._board):
            return 'UNFINISHED'
        elif any('K' in row for row in self._board) and ('k' not in row for row in self._board):
            return 'WHITE_WON'
        elif any('k' in row for row in self._board) and ('K' not in row for row in self._board):
            return 'BlACK_WON'

    def get_board(self, perspective):
        """
        Displays the board where it's oriented for white perspective, for black,
        and the audience may view without any hidden information.
        :param perspective: A string containing indicating who's viewing the board
        :return: A nested list representing the board
        """
        oriented_board = [] # To orient the board without manipulating it
        for row in self._board:
            oriented_board.append(list(row))
        if perspective == 'audience':
            return oriented_board
        elif perspective == 'white':
            for i in range(len(self._board)):
                for j in range(len(self._board[i])):
                    if self._board[i][j].islower():
                        oriented_board[i][j] = '*'
        elif perspective == 'black':
            for i in range(len(self._board)):
                for j in range(len(self._board[i])):
                    if self._board[i][j].isupper():
                        oriented_board[i][j] = '*'
            oriented_board = oriented_board[::-1]
        return oriented_board

    def is_in_bounds(self, new_pos):
        """
        Checks if the new position in within the bounds of the board
        :param new_pos: A string where the piece wants to move.
        :return: True if the position is within bounds, otherwise False
        """
        new_row, new_col = self.convert_position(new_pos)
        if new_row > 7 or new_col > 7: # new position is out of boundaries
            return False
        return True

    def validate_pawn_move(self, piece, current_pos, new_pos):
        """
        Checks if new_position is a valid pawn move and makes sure any opponent captures are valid.
        :param piece: string for the color pawn piece - lowercase for black, uppercase for white
        :param current_pos: int for the current pawn position
        :param new_pos: int for the destination pawn position
        :return: True if the move is valid, otherwise False
        """
        current_row, current_col = self.convert_position(current_pos)
        new_row, new_col = self.convert_position(new_pos)
        if piece == 'p': # Black pawn logic
            if new_col == current_col: # a7 = [1][0] = [3][0]
                if ((new_row == current_row + 1 or new_row == current_row + 2)
                        and self._board[new_row][new_col] == ' '):
                    return True # If the pawn moves within 2 rows down and same column true
            if (new_row == current_row + 1
                    and (new_col == current_col + 1 or new_col == current_col - 1)
                    and self._board[current_row][current_col] != ' '):
                if self._board[new_row][new_col].isupper():
                    return True
        elif piece == 'P': # White pawn logic
            if new_row <= current_row - 2 and self._board[new_row][new_col] == ' ':
                    return True
            if (new_row == current_row - 1
                    and (new_col == current_col + 1 or new_col == current_col - 1)
                    and self._board[current_row][current_col] != ' '):
                if self._board[new_row][new_col].islower():
                    return True
        return False

    def validate_rook_move(self, piece, current_pos, new_pos):
        """
        Checks if new_position is a valid rook move and makes sure any opponent captures are valid.
        :param piece: string for the color rook piece - lowercase for black, uppercase for white
        :param current_pos: int for the current rook position
        :param new_pos: int for the destination rook position
        :return: True if the move is valid, otherwise False
        """
        current_row, current_col = self.convert_position(current_pos)
        new_row, new_col = self.convert_position(new_pos)
        row = current_row
        col = current_col
        # Checks horizontal/vertical paths for pieces in the way
        if new_row == current_row or new_col == current_col:
            if new_row != current_row:
                if new_row > current_row:
                    index = 1
                else:
                    index = -1
                for row in range(current_row + index, new_row, index):
                    if self._board[row][new_col] != ' ':
                        return False
            elif current_col != new_col:
                if new_col > current_col:
                    index = 1
                else:
                    index = -1
                for col in range(current_col + index, new_col, index):
                    if self._board[row][col] != ' ':
                        return False
        # if all passes checks if the piece to be captured is an opponent or if the space is empty
        if self._board[new_row][new_col] == ' ':  # if destination is empty
            return True
        elif (piece == 'r' and self._board[new_row][new_col].isupper()
              or (piece == 'R' and self._board[new_row][new_col].islower())):  # Checks if piece is opponent
            return True

    def validate_knight_move(self, piece, current_pos, new_pos):
        """
        Checks if new_position is a valid knight move and makes sure any opponent captures are valid.
        :param piece: string for the color knight piece - lowercase for black, uppercase for white
        :param current_pos: int for the current knight position
        :param new_pos: int for the destination knight position
        :return: True if the move is valid, otherwise False
        """
        pass

    def validate_bishop_moves(self, piece, current_pos, new_pos):
        """
        Checks if new_position is a valid bishop move and makes sure any opponent captures are valid.
        :param piece: string for the color bishop piece - lowercase for black, uppercase for white
        :param current_pos: int for the current bishop position
        :param new_pos: int for the destination bishop position
        :return: True if the move is valid, otherwise False
        """
        current_row, current_col = self.convert_position(current_pos)
        new_row, new_col = self.convert_position(new_pos)
        if current_row == new_row or current_col == new_col:
            return False # The move is not along a diagonal path
        pass

    def get_queen_moves(self):
        pass
    def get_king_moves(self):
        pass

    def validate_move(self, piece, current_pos, new_pos):
        if piece == 'p' or piece == 'P':
            return self.validate_pawn_move(piece, current_pos, new_pos)
        elif piece =='r' or piece == 'R':
            return self.validate_rook_move(piece, current_pos, new_pos)
        pass


    def make_move(self, current_pos, new_pos):
        """
        Moves the indicated piece to the new spot position
        :param current_pos: A string where the piece is currently on
        :param new_pos: A string where the piece will move to
        :return: True for a valid move, when true moves piece and captures any pieces.
            False otherwise
        """
        current_row, current_col = self.convert_position(current_pos)
        piece = self._board[current_row][current_col]
        new_row, new_col = self.convert_position(new_pos)
        if self.get_game_state() != 'UNFINISHED': # The game is finished
            return False
        elif not self.is_in_bounds(current_pos) and not self.is_in_bounds(new_pos): # If starting position and destination position is within bounds
            return False
        elif self._board[current_row][current_col] == ' ': # There is no piece at this position
            return False
        elif not self.validate_move(piece, current_pos, new_pos):
            return False
        else:
            self._board[current_row][current_col] = ' ' # Replaces the old position as empty
            self._board[new_row][new_col] = piece # Captures any pieces that is there
            return True

# game = ChessVar()
# pprint.pp(game.make_move('b2', 'b4'))
# print(game.validate_pawn_move('p', 'a7', 'a5'))
# pprint.pp(game.make_move('b7','b5'))
# pprint.pp(game.make_move('c1', 'b2')) # a valid move for bishop
#
# # pprint.pp(game.make_move('g7', 'g5'))
# # pprint.pp(game.make_move('c1', 'g5'))
# # pprint.pp(game.make_move('e7', 'e6'))
# # pprint.pp(game.make_move('g5', 'd8'))
# pprint.pp(game.get_board("audience"))
# # pprint.pp(game.get_board("white"))
# # pprint.pp(game.get_board("black"))