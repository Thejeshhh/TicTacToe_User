document.addEventListener('DOMContentLoaded', () => {
    const gameBoardDiv = document.getElementById('game-board');
    const cells = document.querySelectorAll('.cell');
    const currentPlayerSpan = document.getElementById('current-player');
    const gameStatusHeading = document.getElementById('game-info-heading');
    const gameResultDiv = document.getElementById('game-result');
    const resetBoardButton = document.getElementById('reset-board-button');
    const moveSound = document.getElementById('move-sound');
    const winSound = document.getElementById('win-sound');
    const moveHistoryList = document.getElementById('move-history');
    const flashMessagesDiv = document.querySelector('.flash-messages');

    // Leaderboard elements for current game players (now includes session-specific counts)
    const currentXWinsSpan = document.getElementById('current-x-wins'); // Now displays session_x_wins
    const currentOWinsSpan = document.getElementById('current-o-wins'); // Now displays session_o_wins
    const sessionDrawsSpan = document.getElementById('session-draws');
    const sessionTotalMatchesSpan = document.getElementById('session-total-matches');

    // If gameBoardDiv doesn't exist, we are on the index.html page.
    // No game logic needed for index.html.
    if (!gameBoardDiv) {
        return;
    }

    // Function to display flash messages dynamically
    function showFlashMessage(message, category = 'info') {
        const flashDiv = document.createElement('div');
        flashDiv.className = `flash flash-${category}`;
        flashDiv.textContent = message;
        flashMessagesDiv.appendChild(flashDiv);
        setTimeout(() => {
            flashDiv.remove();
        }, 5000); // Remove after 5 seconds
    }

    cells.forEach(cell => {
        cell.addEventListener('click', () => {
            const cellIndex = cell.dataset.index;
            // Prevent move if cell is already filled or game is over
            if (cell.textContent === '' && !gameResultDiv.textContent.includes('wins') && !gameResultDiv.textContent.includes('Draw')) {
                makeMove(cellIndex);
            } else if (cell.textContent !== '') {
                showFlashMessage('This cell is already taken!', 'error');
            } else {
                showFlashMessage('The game is over. Please reset to play again.', 'info');
            }
        });
    });

    resetBoardButton.addEventListener('click', () => {
        resetBoard();
    });

    function updateUI(game, players, current_game_stats) {
        // Update Board
        cells.forEach((cell, index) => {
            cell.textContent = game.board[index];
            cell.classList.remove('filled');
            cell.removeAttribute('aria-disabled');

            if (game.board[index] !== '') {
                cell.classList.add('filled');
                cell.setAttribute('aria-disabled', 'true');
            }
        });

        // Update Current Player / Game Status
        gameStatusHeading.textContent = `${players['X']} (X) vs ${players['O']} (O)`;

        if (game.game_over) {
            if (game.winner) {
                gameResultDiv.textContent = `${players[game.winner]} (${game.winner}) wins!`;
                gameResultDiv.style.color = 'var(--primary-color)'; // Green for win (dark theme)
                currentPlayerSpan.textContent = '';
                winSound.play();
                showFlashMessage(`${players[game.winner]} (${game.winner}) wins!`, 'success');
            } else if (game.draw) {
                gameResultDiv.textContent = 'It\'s a Draw!';
                gameResultDiv.style.color = 'var(--light-text-color)'; // Light gray for draw (dark theme)
                currentPlayerSpan.textContent = '';
                showFlashMessage('The game is a Draw!', 'info');
            }
        } else {
            gameResultDiv.textContent = '';
            gameResultDiv.style.color = ''; // Reset color
            currentPlayerSpan.textContent = `${players[game.current_player]} (${game.current_player})`;
        }

        // Update Move History
        moveHistoryList.innerHTML = '';
        game.move_history.forEach(move => {
            const li = document.createElement('li');
            li.textContent = move;
            moveHistoryList.appendChild(li);
        });

        // Update Current Player Stats (using session-specific wins now)
        currentXWinsSpan.textContent = current_game_stats.session_x_wins; // Updated to session-specific
        currentOWinsSpan.textContent = current_game_stats.session_o_wins; // Updated to session-specific
        sessionDrawsSpan.textContent = current_game_stats.session_draws;
        sessionTotalMatchesSpan.textContent = current_game_stats.session_total_matches;
    }

    async function makeMove(cellIndex) {
        try {
            const response = await fetch('/make_move', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ cell_index: cellIndex })
            });

            const data = await response.json();

            if (data.success) {
                updateUI(data.game, data.players, data.current_game_stats);
                if (!data.game.game_over) {
                    moveSound.currentTime = 0;
                    moveSound.play().catch(e => console.error("Move sound play failed:", e));
                }
            } else {
                console.error('Error making move:', data.error);
                showFlashMessage(data.error || 'An unknown error occurred.', 'error');
            }
        } catch (error) {
            console.error('Network error during move:', error);
            showFlashMessage('Network error: Could not connect to the server.', 'error');
        }
    }

    async function resetBoard() {
        try {
            const response = await fetch('/reset_board', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            const data = await response.json();

            if (data.success) {
                updateUI(data.game, data.players, data.current_game_stats);
                showFlashMessage('Board has been reset!', 'info');
            } else {
                console.error('Error resetting board:', data.error);
                showFlashMessage(data.error || 'An error occurred while resetting the board.', 'error');
            }
        } catch (error) {
            console.error('Network error during reset:', error);
            showFlashMessage('Network error: Could not connect to the server for reset.', 'error');
        }
    }
});