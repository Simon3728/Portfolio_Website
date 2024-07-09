$(document).ready(function() {
    $('#PopulationForm').submit(function(event) {
        event.preventDefault();  // Prevent the form from submitting the traditional way
        $.ajax({
            url: $(this).attr('action'),
            type: $(this).attr('method'),
            data: $(this).serialize(),
            success: function(data) {
                const updateSection = $(data).find('#updateSection').html();
                $('#updateSection').html(updateSection);
            }
        });
    });
    $('#ElectionYearForm').submit(function(event) {
        event.preventDefault();  // Prevent the form from submitting the traditional way
        $.ajax({
            url: $(this).attr('action'),
            type: $(this).attr('method'),
            data: $(this).serialize(),
            success: function(data) {
                const electionResultSection = $(data).find('#electionResultSection').html();
                $('#electionResultSection').html(electionResultSection);
            }
        });
    });
});

// JS for Connect4

document.addEventListener('DOMContentLoaded', () => {
    const board = document.getElementById('connect4-board');
    const resetButton = document.getElementById('reset-button');
    const currentPlayerBox = document.getElementById('current-player');
    let gameOver = false;

    function updateCurrentPlayer(player) {
        if (!currentPlayerBox) {
            return;
        }
        if (player === 1) {
            currentPlayerBox.textContent = `Player 1`;
            currentPlayerBox.style.backgroundColor = 'red';
            currentPlayerBox.style.color = 'white';
        } else if (player === 2) {
            currentPlayerBox.textContent = `AI`;
            currentPlayerBox.style.backgroundColor = 'yellow';
            currentPlayerBox.style.color = 'black';
        }
    }

    if (board) {
        board.addEventListener('click', (event) => {
            if (gameOver) return;
            const cell = event.target.closest('td');
            const column = cell ? cell.dataset.column : undefined;

            if (column !== undefined) {
                makeMove(column);
            }
        });
    }

    if (resetButton) {
        resetButton.addEventListener('click', () => {
            resetGame();
        });
    }

    function makeMove(column) {
        fetch('', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ column: column })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
                return;
            }
            updateBoard(data.board);
            updateCurrentPlayer(data.current_player);
            checkGameState(data);
            if (!data.winner && !data.draw && data.current_player === 2) {
                makeAIMove();
            }
        })
        .catch(error => console.error('Error:', error));
    }

    function makeAIMove() {
        fetch('', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ column: null })
        })
        .then(response => response.json())
        .then(data => {
            updateBoard(data.board);
            updateCurrentPlayer(data.current_player);
            checkGameState(data);
        })
        .catch(error => console.error('Error:', error));
    }

    function updateBoard(board) {
        const cells = document.querySelectorAll('#connect4-board td');
        cells.forEach(cell => {
            const row = cell.dataset.row;
            const col = cell.dataset.column;
            const div = cell.querySelector('div');
            div.className = '';

            if (board[row][col] === 1) {
                div.classList.add('player1');
            } else if (board[row][col] === 2) {
                div.classList.add('player2');
            } else {
                div.classList.add('empty');
            }
        });
    }

    function checkGameState(data) {
        if (data.winner) {
            document.getElementById('game-messages').innerText = data.winner === 1 ? 'Player 1 wins!' : 'Player 2 wins!';
            gameOver = true;
        } else if (data.draw) {
            document.getElementById('game-messages').innerText = 'It\'s a draw!';
            gameOver = true;
        }
    }

    function resetGame() {
        fetch('', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ reset: true })
        })
        .then(response => response.json())
        .then(data => {
            updateBoard(data.board);
            document.getElementById('game-messages').innerText = '';
            updateCurrentPlayer(data.current_player);
            gameOver = false;
        })
        .catch(error => console.error('Error:', error));
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Initialize the board with the starting state
    if (board && resetButton) {
        resetGame();
    }
});
