import random
from django.conf import settings
import os
import time

ROWS = 6
COLUMNS = 7

class MinimaxPlayer:
    def __init__(self, name, piece, depth=5):
        self.name = name
        self.piece = piece
        self.depth = depth

    def minimax(self, board, depth, alpha, beta, maximizingPlayer):
        if depth == 0 or board.check_winner(1) or board.check_winner(2):
            return self.evaluate_board(board.board, depth)

        valid_moves = [col for col in range(COLUMNS) if board.is_valid_move(col)]

        if maximizingPlayer:
            max_eval = -float('inf')
            for col in valid_moves:
                row, _ = board.drop_piece(col, self.piece)
                eval = self.minimax(board, depth - 1, alpha, beta, False)
                board.board[row][col] = 0  
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  # Beta cut-off
            return max_eval
        else:
            min_eval = float('inf')
            opponent_piece = 2 if self.piece == 1 else 1
            for col in valid_moves:
                row, _ = board.drop_piece(col, opponent_piece)
                eval = self.minimax(board, depth - 1, alpha, beta, True)
                board.board[row][col] = 0  
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break  # Alpha cut-off
            return min_eval

    def get_move(self, board, sequence):
        turn = self.get_move_count(board.board)
        if turn == 0:
            return 3
        elif turn <= 5:
            last_digit = self.binary_search_ignore_last_digit(f'moves_{turn}.txt', sequence)
            if last_digit > 0 and last_digit < 8:
                time.sleep(0.7)
                return last_digit - 1            

        best_moves = []
        best_value = -float('inf')
        alpha = -float('inf')
        beta = float('inf')
        for col in range(COLUMNS):
            if board.is_valid_move(col):
                row, _ = board.drop_piece(col, self.piece)
                value = self.minimax(board, self.depth - 1, alpha, beta, False)
                board.board[row][col] = 0
                if value > best_value:
                    best_value = value
                    best_moves = [col]
                elif value == best_value:
                    best_moves.append(col)
                alpha = max(alpha, value)
        return random.choice(best_moves)

    def evaluate_board(self, board, depth):
        def score_position(board, piece):
            score = 0

            center_array = [board[row][COLUMNS // 2] for row in range(ROWS)]
            center_count = center_array.count(piece)
            score += center_count * 120

            for col in range(COLUMNS):
                for row in range(ROWS):
                    if board[row][col] == piece:
                        if col in [0, COLUMNS - 1]:
                            score += 40
                        elif col in [1, COLUMNS - 2]:
                            score += 70
                        elif col in [2, COLUMNS - 3]:
                            score += 120
                        else:
                            score += 200

            # Score Horizontal
            for row in range(ROWS):
                row_array = [board[row][col] for col in range(COLUMNS)]
                for col in range(COLUMNS - 3):
                    window = row_array[col:col + 4]
                    score += self.evaluate_window(window, piece)
            # Score Vertical
            for col in range(COLUMNS):
                col_array = [board[row][col] for row in range(ROWS)]
                for row in range(ROWS - 3):
                    window = col_array[row:row + 4]
                    score += self.evaluate_window(window, piece)

            # Score positive sloped diagonal
            for row in range(ROWS - 3):
                for col in range(COLUMNS - 3):
                    window = [board[row + i][col + i] for i in range(4)]
                    score += self.evaluate_window(window, piece)

            # Score negative sloped diagonal
            for row in range(ROWS - 3):
                for col in range(COLUMNS - 3):
                    window = [board[row + 3 - i][col + i] for i in range(4)]
                    score += self.evaluate_window(window, piece)

            return score

        score = score_position(board, self.piece)
        opponent_piece = 2 if self.piece == 1 else 1
        score -= score_position(board, opponent_piece)
        return score

    def evaluate_window(self, window, piece):
        score = 0
        opponent_piece = 2 if piece == 1 else 1

        if window.count(piece) == 4:
            score += 1000000000
        elif window.count(piece) == 3 and window.count(0) == 1:
            score += 900000 
        elif window.count(piece) == 2 and window.count(0) == 2:
            score += 50000
        elif window.count(piece) == 1 and window.count(0) == 3:
            score += 5000
        elif window.count(opponent_piece) == 3 and window.count(0) == 1:
            score -= 900000 
        return score

    def binary_search_ignore_last_digit(self, filename, target):
        file_path = os.path.join(settings.BASE_DIR, 'connect4', 'Possible_Moves', filename)
        with open(file_path, 'r') as file:
            lines = [line.strip() for line in file.readlines()]
            try:
                numbers = [int(line) for line in lines]
            except:
                return -1

            target_int = int(target)
            left, right = 0, len(numbers) - 1

            while left <= right:
                mid = (left + right) // 2
                mid_value = numbers[mid] // 10

                if mid_value == target_int:
                    last_digit = numbers[mid] % 10
                    return last_digit
                elif mid_value < target_int:
                    left = mid + 1
                else:
                    right = mid - 1
            return -1

    def get_move_count(self, board):
        count = 0
        for row in board:
            for cell in row:
                if cell != 0:
                    count += 1
        return count
