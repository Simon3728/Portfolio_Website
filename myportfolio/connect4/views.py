from django.shortcuts import render
from django.http import JsonResponse
import json
from .board import Board
from .minimax import MinimaxPlayer


def get_initial_game_state():
    board = Board()
    return {
        'board': board.to_serializable(),
        'current_player': 1,  # Player 1 starts
        'winner': None,
        'draw': False,
        'move_sequence': ""  # Track the sequence of moves
    }

def connect4(request):
    if 'game_state' not in request.session:
        request.session['game_state'] = get_initial_game_state()

    if request.method == 'POST':
        data = json.loads(request.body)
        if 'reset' in data and data['reset']:
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
                    row, col = board.drop_piece(column, current_player)
                    move_sequence += str(column+1)
                except ValueError as e:
                    return JsonResponse({'error': str(e)})

                winner = board.check_winner(current_player)
                draw = board.check_draw()
            else:  # AI player
                ai_player = MinimaxPlayer("AI", 2)
                column = ai_player.get_move(board, move_sequence)
                row, col = board.drop_piece(column, 2)
                move_sequence += str(column+1)
                winner = board.check_winner(2)
                draw = board.check_draw()

            if winner or draw:
                game_state['winner'] = current_player if winner else None
                game_state['draw'] = draw
                request.session.modified = True
            else:
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
            request.session['game_state'] = game_state
            return JsonResponse(response)

    return render(request, 'projects/connect4.html')
