# Author: Jericho Arizala
# GitHub username: earthlydev
# Date: 12/08/2024
# Description:

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
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'] ]
        self._white_pieces = ['P','R','N','B','Q','K']
        self._black_pieces = ['p','r','n','b','q','k']

    def convert_position(self, pos):
        """
        Convert the position into board indices
        :return: A tuple for the row and the column
        """
        columns = ['a','b','c','d','e','f','g','h']
        rows = ['8','7','6','5','4','3','2','1']
        col = columns.index(pos[0])
        row = rows.index(pos[1])
        return row, col

    # USE A 2D LIST THAT CONTAINS ALL OF THE BOARD'S POSITIONS, NO PIECES ARE SHOWN.
    # WHEN THE POSITION MATCHES ONE ON THE BOARD RETURN THE POSITION INTO A TUPLE.
    def king_is_check(self):
        """
        Check if the king is in check
        :return: True if an opposing piece can capture the king, otherwise False
        """
# Find the position of the king on the board by looping through. After finding the king,
    # using the list of the opponents pieces iterate through the board and find matching pieces
    # when a piece matches one from the list check their valid_moves() and if a valid_move() falls within range
    # of the king's position (king_pos) then return True
    # If the loop ends then return False

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

    def get_board(self, perspective): #### ADD PERSPECTIVE AT END ####
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

    def make_move(self, current_pos, new_pos):
        """
        Moves the indicated piece to the new spot position
        :param current_pos: A string where the piece is currently on
        :param new_pos: A string where the piece will move to
        :return: True for a valid move, when true moves piece and captures any pieces.
            False otherwise
        """
        if self.get_game_state() != 'UNFINISHED': # The game is finished
            return False
        if self.is_in_bounds(new_pos): # If out of bounds
            return False
        current_row, current_col = self.convert_position(current_pos)
        new_row, new_col = self.convert_position(new_pos)
        piece = self._board[current_row][current_col]
        self._board[current_row][current_col] = ' ' # Replaces the old position as empty
        self._board[new_row][new_col] = piece # Captures any pieces that is there
        return True
