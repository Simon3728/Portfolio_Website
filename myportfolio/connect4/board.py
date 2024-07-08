ROWS = 6
COLUMNS = 7

class Board:
    def __init__(self, board=None):
        if board is None:
            self.board = self.create_board()
        else:
            self.board = board

    def create_board(self):
        return [[0 for _ in range(COLUMNS)] for _ in range(ROWS)]

    def drop_piece(self, col, piece):
        for row in range(ROWS-1, -1, -1):
            if self.board[row][col] == 0:
                self.board[row][col] = piece
                return row, col
        raise ValueError("Column is full")

    def is_valid_move(self, col):
        return self.board[0][col] == 0

    def check_winner(self, piece):
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
        for row in self.board:
            if 0 in row:
                return False
        return True

    def to_serializable(self):
        return {
            'board': self.board
        }

    @classmethod
    def from_serializable(cls, data):
        return cls(board=data['board'])