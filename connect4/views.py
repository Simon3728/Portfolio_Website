"""
Views for the Connect4 app.

This file defines the view function for the Connect4 game, handling game state management,
calculating moves, and returning updated game data.
"""

from django.shortcuts import render
from django.http import JsonResponse
import json
from .board import Board
from .minimax import MinimaxPlayer

def get_initial_game_state():
    """
    Initialize a new game state.
    """
    board = Board()
    return {
        'board': board.to_serializable(),
        'current_player': 1,  # Player 1 starts
        'winner': None,
        'draw': False,
        'move_sequence': ""  # Track the sequence of moves
    }

def connect4(request):
    """
    Handle requests to the Connect4 game page.

    This view initializes the game state, processes moves, and handles game resets.
    It returns updated game data as a JSON response for AJAX requests or renders the game page.
    """
    if 'game_state' not in request.session:
        # Initialize game state if not already present in the session
        request.session['game_state'] = get_initial_game_state()

    if request.method == 'POST':
        data = json.loads(request.body)

        if 'reset' in data and data['reset']:
            # Handle game reset
            request.session['game_state'] = get_initial_game_state()
            request.session.modified = True
            return JsonResponse({
                'message': 'Game reset',
                'board': request.session['game_state']['board']['board'],
                'current_player': request.session['game_state']['current_player']
            })
        
        if 'column' in data:
            game_state = request.session['game_state']
            board = Board.from_serializable(game_state['board'])
            current_player = game_state['current_player']
            move_sequence = game_state['move_sequence']

            if current_player == 1:  # Human player
                column = int(data['column'])
                try:
                    # Attempt to drop a piece in the selected column
                    row, col = board.drop_piece(column, current_player)
                    move_sequence += str(column + 1)  # Track the move
                except ValueError as e:
                    return JsonResponse({'error': str(e)})

                # Check for a winner or a draw after the move
                winner = board.check_winner(current_player)
                draw = board.check_draw()
            else:  # AI player
                ai_player = MinimaxPlayer("AI", 2)
                # Calculate the AI's move using the minimax algorithm
                column = ai_player.get_move(board, move_sequence)
                row, col = board.drop_piece(column, 2)
                move_sequence += str(column + 1)  # Track the move
                winner = board.check_winner(2)
                draw = board.check_draw()

            if winner or draw:
                # Update the game state if there's a winner or a draw
                game_state['winner'] = current_player if winner else None
                game_state['draw'] = draw
                request.session.modified = True
            else:
                # Switch to the next player if the game is still ongoing
                game_state['current_player'] = 2 if current_player == 1 else 1
                request.session.modified = True

            game_state['move_sequence'] = move_sequence
            game_state['board'] = board.to_serializable()
            response = {
                'board': game_state['board']['board'],
                'current_player': game_state['current_player'],
                'winner': game_state.get('winner'),
                'draw': game_state.get('draw')
            }
            # Update the session with the new game state
            request.session['game_state'] = game_state
            return JsonResponse(response)

    # Render the Connect4 game page
    return render(request, 'projects/connect4.html')
