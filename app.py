from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
import os
import json

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', os.urandom(24))

LEADERBOARD_FILE = 'leaderboard.json'

# --- JSON Leaderboard Management Functions ---
def load_leaderboard():
    """Loads leaderboard data from the JSON file."""
    if not os.path.exists(LEADERBOARD_FILE):
        return {}
    try:
        with open(LEADERBOARD_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading leaderboard file: {e}. Starting with empty leaderboard.")
        return {}

def save_leaderboard(leaderboard_data):
    """Saves leaderboard data to the JSON file."""
    try:
        with open(LEADERBOARD_FILE, 'w') as f:
            json.dump(leaderboard_data, f, indent=4)
    except IOError as e:
        print(f"Error saving leaderboard file: {e}")

def get_or_create_player_stats(leaderboard_data, player_name):
    """Gets or creates a player's stats entry in the leaderboard data."""
    if player_name not in leaderboard_data:
        leaderboard_data[player_name] = {
            'player_name': player_name,
            'wins': 0,
            'losses': 0,
            'draws': 0,
            'total_matches': 0
        }
    return leaderboard_data[player_name]

# --- Game Logic Functions ---
def initialize_game_state():
    # This function is called when a *new game session* starts
    # or when the server restarts, thus resetting session-specific counts.
    return {
        'board': [''] * 9,
        'current_player': 'X',
        'game_over': False,
        'winner': None,
        'draw': False,
        'move_history': [],
        'player_x_name': None,
        'player_o_name': None,
        'session_x_wins': 0, # New: Track wins for X in this session
        'session_o_wins': 0, # New: Track wins for O in this session
        'session_draws': 0,
        'session_total_matches': 0
    }

def check_win(board):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8], # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8], # Columns
        [0, 4, 8], [2, 4, 6]             # Diagonals
    ]
    for condition in win_conditions:
        if board[condition[0]] == board[condition[1]] == board[condition[2]] != '':
            return board[condition[0]]
    return None

def check_draw(board):
    return all(cell != '' for cell in board)

# --- Routes ---

@app.route('/')
def index():
    # Clear game state from session on landing page to ensure fresh start for new players/games
    session.pop('game_state', None)
    session.pop('players', None)
    return render_template('index.html')

@app.route('/start_game', methods=['POST'])
def start_game():
    player1_name = request.form.get('player1_name', '').strip()
    player2_name = request.form.get('player2_name', '').strip()

    if not player1_name or not player2_name:
        flash('Both player names are required.', 'error')
        return redirect(url_for('index'))
    if player1_name == player2_name:
        flash('Player names must be different.', 'error')
        return redirect(url_for('index'))
    if len(player1_name) > 50 or len(player2_name) > 50:
        flash('Player names cannot exceed 50 characters.', 'error')
        return redirect(url_for('index'))

    session['players'] = {'X': player1_name, 'O': player2_name}
    # Initialize game state for the session, resetting all session-specific counts including wins
    session['game_state'] = initialize_game_state()
    session['game_state']['player_x_name'] = player1_name
    session['game_state']['player_o_name'] = player2_name

    return redirect(url_for('game_board'))

@app.route('/game')
def game_board():
    if 'game_state' not in session or 'players' not in session:
        flash('Please enter player names to start a new game.', 'info')
        return redirect(url_for('index'))

    game_state = session['game_state']
    players = session['players']

    # For displaying stats on game.html, we now ONLY use session-specific counts.
    # The global leaderboard is updated in the background but not displayed here.
    current_game_stats = {
        'X_name': players['X'],
        'O_name': players['O'],
        'session_x_wins': game_state['session_x_wins'], # Use session-specific wins
        'session_o_wins': game_state['session_o_wins'], # Use session-specific wins
        'session_draws': game_state['session_draws'],
        'session_total_matches': game_state['session_total_matches']
    }

    return render_template('game.html',
                           game=game_state,
                           players=players,
                           current_game_stats=current_game_stats
                           )

@app.route('/make_move', methods=['POST'])
def make_move():
    if 'game_state' not in session:
        return jsonify({'success': False, 'error': 'Game not started. Please go back to the home page.'}), 400

    game_state = session['game_state']
    players = session['players']

    if game_state['game_over']:
        return jsonify({'success': False, 'error': 'Game is already over. Please reset the board or start a new game.'}), 400

    try:
        cell_index = int(request.json['cell_index'])
    except (KeyError, ValueError):
        return jsonify({'success': False, 'error': 'Invalid cell index provided.'}), 400

    if not (0 <= cell_index < 9) or game_state['board'][cell_index] != '':
        return jsonify({'success': False, 'error': 'Invalid move. Cell is already taken or out of bounds.'}), 400

    current_player_symbol = game_state['current_player']
    game_state['board'][cell_index] = current_player_symbol
    player_name = players[current_player_symbol]
    game_state['move_history'].append(f"{player_name} ({current_player_symbol}) played at cell {cell_index + 1}")

    winner = check_win(game_state['board'])

    # Load persistent leaderboard data to update global stats (happens in background)
    leaderboard_data = load_leaderboard()
    player_x_global_stats = get_or_create_player_stats(leaderboard_data, players['X'])
    player_o_global_stats = get_or_create_player_stats(leaderboard_data, players['O'])

    if winner:
        game_state['winner'] = winner
        game_state['game_over'] = True

        # Update global persistent stats
        if winner == 'X':
            player_x_global_stats['wins'] += 1
            player_o_global_stats['losses'] += 1
            game_state['session_x_wins'] += 1 # Update session-specific X wins
        else: # winner == 'O'
            player_o_global_stats['wins'] += 1
            player_x_global_stats['losses'] += 1
            game_state['session_o_wins'] += 1 # Update session-specific O wins

        player_x_global_stats['total_matches'] += 1
        player_o_global_stats['total_matches'] += 1
        save_leaderboard(leaderboard_data)

        game_state['session_total_matches'] += 1 # Update session-specific total matches

    elif check_draw(game_state['board']):
        game_state['draw'] = True
        game_state['game_over'] = True

        # Update global persistent stats
        player_x_global_stats['draws'] += 1
        player_o_global_stats['draws'] += 1
        player_x_global_stats['total_matches'] += 1
        player_o_global_stats['total_matches'] += 1
        save_leaderboard(leaderboard_data)

        game_state['session_draws'] += 1 # Update session-specific draws
        game_state['session_total_matches'] += 1 # Update session-specific total matches
    else:
        game_state['current_player'] = 'O' if current_player_symbol == 'X' else 'X'

    session['game_state'] = game_state

    # Prepare data for JSON response, using ONLY session-specific counts
    current_game_stats_response = {
        'X_name': players['X'],
        'O_name': players['O'],
        'session_x_wins': game_state['session_x_wins'], # Use session-specific wins
        'session_o_wins': game_state['session_o_wins'], # Use session-specific wins
        'session_draws': game_state['session_draws'],
        'session_total_matches': game_state['session_total_matches']
    }

    return jsonify({
        'success': True,
        'game': game_state,
        'players': players,
        'current_game_stats': current_game_stats_response
    })

@app.route('/reset_board', methods=['POST'])
def reset_board():
    if 'game_state' not in session or 'players' not in session:
        return jsonify({'success': False, 'error': 'Game not started. Cannot reset.'}), 400

    current_game_state = session['game_state']
    players = session['players']

    # Create a new game board state, but preserve the *session-specific cumulative* counts
    new_board_state = {
        'board': [''] * 9,
        'current_player': 'X',
        'game_over': False,
        'winner': None,
        'draw': False,
        'move_history': [],
        'player_x_name': players['X'],
        'player_o_name': players['O'],
        # Preserve session-specific counts from the current state across board resets
        'session_x_wins': current_game_state['session_x_wins'],
        'session_o_wins': current_game_state['session_o_wins'],
        'session_draws': current_game_state['session_draws'],
        'session_total_matches': current_game_state['session_total_matches']
    }
    session['game_state'] = new_board_state

    # Prepare data for JSON response, using the *preserved* session-specific counts
    current_game_stats_response = {
        'X_name': players['X'],
        'O_name': players['O'],
        'session_x_wins': new_board_state['session_x_wins'],
        'session_o_wins': new_board_state['session_o_wins'],
        'session_draws': new_board_state['session_draws'],
        'session_total_matches': new_board_state['session_total_matches']
    }

    return jsonify({
        'success': True,
        'game': session['game_state'],
        'players': players,
        'current_game_stats': current_game_stats_response
    })

if __name__ == '__main__':
    app.run(debug=True)