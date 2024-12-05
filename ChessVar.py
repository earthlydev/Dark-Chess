# Author: Jericho Arizala
# GitHub username: earthlydev
# Date: 12/08/2024
# Description: This program runs a game of dark chess. Two players can compete, where
# the pieces movements are tracked, when a piece is captured. Additionally, when a player views
# the board, hides the opponent pieces except when an opponent piece can be captured.

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
        self._current_turn = 'WHITE'

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

    def set_current_turn(self):
        """
        Switches the current turn depending on the previous turn
        """
        self._current_turn = 'WHITE' if self._current_turn == 'BLACK' else 'BLACK'

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

    def is_opponent(self, piece, new_row, new_col):
        """
        Checks if the piece being captured is an opponent
        :param piece: A string for the color chess piece
        :param new_row: An int for the current row
        :param new_col: An int for the current col
        :return: True if the player is capturing the opponent piece, otherwise False
        """
        second_piece = self._board[new_row][new_col]
        if (piece.isupper() and second_piece.isupper()) or (piece.islower() and second_piece.islower()):
            return False
        return True

    def is_straight_path(self, current_row, current_col, new_row, new_col):
        """
        Returns true if the path indicated is straight and contains no obstacles blocking the path
        :param current_row, current_col: Ints for the current position of piece.
        :param new_row, new_col: Ints for the destination position.
        :return: True if the path contains no obstacles and is a straight path.
        """
        if new_row == current_row or new_col == current_col: # at least one needs to be true
            if new_row != current_row: # Checking the vertical path
                index = 1 if new_row > current_row else -1
                for row in range(current_row + index, new_row, index):
                    if self._board[row][new_col] != ' ': # if the row reaches an obstacle
                        return False # return False
            elif current_col != new_col: # otherwise check the horizontal path
                index = 1 if new_col > current_col else -1
                for col in range(current_col + index, new_col, index):
                    if self._board[new_row][col] != ' ':
                        return False
            else:
                return True

    def is_diagonal_path(self, current_row, current_col, new_row, new_col):
        """
        Checks that the diagonal path is valid and contains no obstacles.
        :param current_row, current_col: Ints for the current position
        :param new_row, new_col: Ints for the destination position
        :return: Return True if the path contains no obstacles and is correctly calculated.
        """
        x_path = abs(new_col - current_col)
        y_path = abs(new_row - current_row)
        if x_path == y_path:
            row_step = 1 if new_row > current_row else -1
            col_step = 1 if new_col > current_col else -1
            check_row = current_row + row_step
            check_col = current_col + col_step
            while check_row != new_row and check_col != new_col:
                if self._board[check_row][check_col] != ' ':
                    return False
                check_row += row_step
                check_col += col_step
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
            if new_row >= current_row - 2 and self._board[new_row][new_col] == ' ':
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
        if self.is_straight_path(current_row, current_col, new_row, new_col):
            if self._board[new_row][new_col] == ' ':  # if destination is empty
                print("checked if the space is empty")
                return True
            elif self.is_opponent(piece,new_row,new_col):  # Checks if piece is opponent
                return True
        else:
            return False

    def validate_knight_move(self, piece, current_pos, new_pos):
        """
        Checks if new_position is a valid knight move and makes sure any opponent captures are valid.
        :param piece: string for the color knight piece - lowercase for black, uppercase for white
        :param current_pos: int for the current knight position
        :param new_pos: int for the destination knight position
        :return: True if the move is valid, otherwise False
        """
        current_row, current_col = self.convert_position(current_pos)
        new_row, new_col = self.convert_position(new_pos)
        if new_row != current_row and new_col != current_col: # Checks if it is an L path
            if ((abs(new_row - current_row) == 2 and abs(new_col - current_col) == 1)
                or (abs(new_row - current_row) == 1 and abs(new_col - current_col) == 2)):
                    if self.is_opponent(piece,new_row,new_col) or self._board[new_row][new_col] == ' ':
                        return True
        return False

    def validate_bishop_move(self, piece, current_pos, new_pos):
        """
        Checks if new_position is a valid bishop move and makes sure any opponent captures are valid.
        :param piece: string for the color bishop piece - lowercase for black, uppercase for white
        :param current_pos: int for the current bishop position
        :param new_pos: int for the destination bishop position
        :return: True if the move is valid, otherwise False
        """
        current_row, current_col = self.convert_position(current_pos)
        new_row, new_col = self.convert_position(new_pos)
        if not self.is_diagonal_path(current_row, current_col, new_row, new_col):
            return False
        elif self.is_opponent(piece,new_row,new_col):
            return True

    def validate_queen_move(self, piece, current_pos, new_pos):
        """
        Checks if the new position is a valid queen move, any opponent captures are valid, and
        if path along does not contain any obstacles.
        :param piece: String for the color queen piece
        :param current_pos: int for the current queen position
        :param new_pos: int for the destination queen position
        :return: True if the move is valid, otherwise False
        """
        current_row, current_col = self.convert_position(current_pos)
        new_row, new_col = self.convert_position(new_pos)
        if not self.is_diagonal_path(current_row, current_col, new_row, new_col):
            return False
        elif not self.is_straight_path(current_row, current_col, new_row, new_col):
            return False
        elif self.is_opponent(piece,new_row,new_col):
            return True

    def validate_king_move(self, piece, current_pos, new_pos):
        """
        Checks if new_position is a valid king move and makes sure any opponent captures are valid.
        :param piece: string for the color king piece - lowercase for black, uppercase for white
        :param current_pos: int for the current king position
        :param new_pos: int for the destination king position
        :return: True if the move is valid, otherwise False
        """
        current_row, current_col = self.convert_position(current_pos)
        new_row, new_col = self.convert_position(new_pos)
        if abs(new_row - current_row) > 1 or abs(new_col - current_col) > 1:
            return False # because king can move one space around
        elif self.is_opponent(piece,new_row,new_col) or self._board[new_row][new_col] == ' ':
            return True

    def validate_move(self, piece, current_pos, new_pos):
        """
        A helper method to call the correct chess piece function for validating moves
        :param piece: A string for the piece
        :param current_pos: An int for the current position
        :param new_pos: An int for the new position
        :return: True or false depending on the result of the called function
        """
        if piece == 'p' or piece == 'P':
            return self.validate_pawn_move(piece, current_pos, new_pos)
        elif piece == 'r' or piece == 'R':
            return self.validate_rook_move(piece, current_pos, new_pos)
        elif piece == 'n' or piece == 'N':
            return self.validate_knight_move(piece, current_pos, new_pos)
        elif piece == 'b' or piece == 'B':
            return self.validate_bishop_move(piece, current_pos, new_pos)
        elif piece == 'q' or piece == 'Q':
            return self.validate_queen_move(piece, current_pos, new_pos)
        elif piece == 'k' or piece == 'K':
            return self.validate_king_move(piece, current_pos, new_pos)

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
        if self.get_game_state() != 'UNFINISHED':
            return False # The game is finished
        elif piece.islower() and self._current_turn == 'WHITE':
            return False # piece attempting to move is black
        elif piece.isupper() and self._current_turn == 'BLACK':
            return False # piece attempting to move is white
        elif not self.is_in_bounds(current_pos) and not self.is_in_bounds(new_pos):
            return False # If starting position and destination position is within bounds
        elif self._board[current_row][current_col] == ' ':
            return False # There is no piece at this position
        elif not self.validate_move(piece, current_pos, new_pos):
            return False
        else:
            self._board[current_row][current_col] = ' ' # Replaces the old position as empty
            self._board[new_row][new_col] = piece # Captures any pieces that is there
            self.set_current_turn() # Switches turns for current player
            return True

# TODO: Implement a feature to allow the player to view what piece is allowed to be captured
# Does this entail utilizing the validate_piece_move()
# how would I loop through available positions?