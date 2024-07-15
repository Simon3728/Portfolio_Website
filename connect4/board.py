"""
This file contains the Board class, which represents the board of the Connect 4 game.
It includes methods for creating the board, dropping pieces, checking for valid moves,
determining the winner, checking for a draw, and serializing the board state.
"""

ROWS = 6
COLUMNS = 7

class Board:
    def __init__(self, board=None):
        """
        Initialize the board. If no board is provided, create a new one.
        """
        if board is None:
            self.board = self.create_board()
        else:
            self.board = board

    def create_board(self):
        """
        Create a new board.
        """
        return [[0 for _ in range(COLUMNS)] for _ in range(ROWS)]

    def drop_piece(self, col, piece):
        """
        Drop a piece into the specified column.
        """
        for row in range(ROWS-1, -1, -1):
            if self.board[row][col] == 0:
                self.board[row][col] = piece
                return row, col
        raise ValueError("Column is full")

    def is_valid_move(self, col):
        """
        Check if a move is valid (i.e., the column is not full).
        """
        return self.board[0][col] == 0

    def check_winner(self, piece):
        """
        Check if there is a winner.
        """
        # Check horizontal locations for win
        for c in range(COLUMNS-3):
            for r in range(ROWS):
                if self.board[r][c] == piece and self.board[r][c+1] == piece and self.board[r][c+2] == piece and self.board[r][c+3] == piece:
                    return True

        # Check vertical locations for win
        for c in range(COLUMNS):
            for r in range(ROWS-3):
                if self.board[r][c] == piece and self.board[r+1][c] == piece and self.board[r+2][c] == piece and self.board[r+3][c] == piece:
                    return True

        # Check positively sloped diagonals
        for c in range(COLUMNS-3):
            for r in range(ROWS-3):
                if self.board[r][c] == piece and self.board[r+1][c+1] == piece and self.board[r+2][c+2] == piece and self.board[r+3][c+3] == piece:
                    return True

        # Check negatively sloped diagonals
        for c in range(COLUMNS-3):
            for r in range(3, ROWS):
                if self.board[r][c] == piece and self.board[r-1][c+1] == piece and self.board[r-2][c+2] == piece and self.board[r-3][c+3] == piece:
                    return True

        return False

    def check_draw(self):
        """
        Check if the game is a draw (board is full).
        """
        for row in self.board:
            if 0 in row:
                return False
        return True

    def to_serializable(self):
        """
        Convert the board state to a serializable format.
        """
        return {
            'board': self.board
        }

    @classmethod
    def from_serializable(cls, data):
        """
        Create a Board instance from a serializable format.
        """
        return cls(board=data['board'])
