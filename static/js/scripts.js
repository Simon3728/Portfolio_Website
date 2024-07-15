// jQuery document ready function to ensure the DOM is fully loaded before executing the script
$(document).ready(function() {
    // Handle form submission for PopulationForm using AJAX
    $('#PopulationForm').submit(function(event) {
        event.preventDefault();  // Prevent the form from submitting the traditional way
        $.ajax({
            url: $(this).attr('action'),  // Use the form's action attribute as the URL
            type: $(this).attr('method'),  // Use the form's method attribute for the request type
            data: $(this).serialize(),  // Serialize the form data for submission
            success: function(data) {
                // Update the #updateSection with the response data
                const updateSection = $(data).find('#updateSection').html();
                $('#updateSection').html(updateSection);
            }
        });
    });

    // Handle form submission for ElectionYearForm using AJAX
    $('#ElectionYearForm').submit(function(event) {
        event.preventDefault();  // Prevent the form from submitting the traditional way
        $.ajax({
            url: $(this).attr('action'),  // Use the form's action attribute as the URL
            type: $(this).attr('method'),  // Use the form's method attribute for the request type
            data: $(this).serialize(),  // Serialize the form data for submission
            success: function(data) {
                // Update the #electionResultSection with the response data
                const electionResultSection = $(data).find('#electionResultSection').html();
                $('#electionResultSection').html(electionResultSection);
            }
        });
    });
});

// JS for Connect4 game functionality
document.addEventListener('DOMContentLoaded', () => {
    const board = document.getElementById('connect4-board');
    const resetButton = document.getElementById('reset-button');
    const currentPlayerBox = document.getElementById('current-player');
    let gameOver = false;

    // Function to update the current player display
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

    // Add click event listener to the game board
    if (board) {
        board.addEventListener('click', (event) => {
            if (gameOver) return;  // Prevent actions if the game is over
            const cell = event.target.closest('td');  // Get the clicked cell
            const column = cell ? cell.dataset.column : undefined;  // Get the column of the clicked cell

            if (column !== undefined) {
                makeMove(column);  // Make a move in the specified column
            }
        });
    }

    // Add click event listener to the reset button
    if (resetButton) {
        resetButton.addEventListener('click', () => {
            resetGame();  // Reset the game when the button is clicked
        });
    }

    // Function to make a move in the specified column
    function makeMove(column) {
        fetch('', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')  // Include the CSRF token for security
            },
            body: JSON.stringify({ column: column })  // Send the column index in the request body
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);  // Display an error message if there is an error
                return;
            }
            updateBoard(data.board);  // Update the game board with the new state
            updateCurrentPlayer(data.current_player);  // Update the current player display
            checkGameState(data);  // Check the game state for win/draw conditions
            if (!data.winner && !data.draw && data.current_player === 2) {
                makeAIMove();  // Make a move for the AI if applicable
            }
        })
        .catch(error => console.error('Error:', error));
    }

    // Function to make a move for the AI
    function makeAIMove() {
        fetch('', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')  // Include the CSRF token for security
            },
            body: JSON.stringify({ column: null })  // Send a null column to indicate AI should move
        })
        .then(response => response.json())
        .then(data => {
            updateBoard(data.board);  // Update the game board with the new state
            updateCurrentPlayer(data.current_player);  // Update the current player display
            checkGameState(data);  // Check the game state for win/draw conditions
        })
        .catch(error => console.error('Error:', error));
    }

    // Function to update the game board
    function updateBoard(board) {
        const cells = document.querySelectorAll('#connect4-board td');
        cells.forEach(cell => {
            const row = cell.dataset.row;
            const col = cell.dataset.column;
            const div = cell.querySelector('div');
            div.className = '';  // Reset the cell's class

            // Set the cell's class based on the board state
            if (board[row][col] === 1) {
                div.classList.add('player1');
            } else if (board[row][col] === 2) {
                div.classList.add('player2');
            } else {
                div.classList.add('empty');
            }
        });
    }

    // Function to check the game state for win/draw conditions
    function checkGameState(data) {
        if (data.winner) {
            document.getElementById('game-messages').innerText = data.winner === 1 ? 'Player 1 wins!' : 'Player 2 wins!';
            gameOver = true;  // Set the game over flag
        } else if (data.draw) {
            document.getElementById('game-messages').innerText = 'It\'s a draw!';
            gameOver = true;  // Set the game over flag
        }
    }

    // Function to reset the game
    function resetGame() {
        fetch('', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')  // Include the CSRF token for security
            },
            body: JSON.stringify({ reset: true })  // Send a reset command in the request body
        })
        .then(response => response.json())
        .then(data => {
            updateBoard(data.board);  // Update the game board with the new state
            document.getElementById('game-messages').innerText = '';  // Clear the game messages
            updateCurrentPlayer(data.current_player);  // Update the current player display
            gameOver = false;  // Reset the game over flag
        })
        .catch(error => console.error('Error:', error));
    }

    // Function to get the CSRF token from cookies
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
        resetGame();  // Reset the game to its initial state
    }
});
