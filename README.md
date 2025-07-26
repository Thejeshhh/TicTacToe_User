# Tic Tac Toe Web Game

A simple, interactive Tic Tac Toe game built with Flask, HTML, CSS, and JavaScript. This game allows two players to compete against each other, tracks their performance for the current session, and also maintains a persistent global record of all players' overall wins, losses, and draws.

## ✨ Features

* **Player Name Input:** Start each game by entering names for Player X and Player O.
* **Interactive Game Board:** A classic 3x3 grid for engaging gameplay.
* **Dynamic UI Updates:** Real-time display of the current player, game status (win/draw), and move history.
* **Session-Based Stats:** Tracks wins for Player X, wins for Player O, draws, and total matches for the *current playing session*. These statistics reset when a new game session is initiated (e.g., by returning to the home page).
* **Persistent Global Leaderboard (Backend):** A `leaderboard.json` file on the server keeps a permanent record of all players' lifetime wins, losses, and draws across all games played, even if the server restarts. This data is updated with each game's outcome but is not directly displayed on the `game.html` page to emphasize session-specific tracking.
* **Reset Board:** Easily clear the board to play another round with the same players, continuing to accumulate session-specific stats.
* **Start New Game:** Option to return to the player name input screen, which effectively resets all session-based statistics for a fresh start.
* **Responsive Design:** Optimized for play on various screen sizes, from desktops to mobile devices.
* **Sound Effects:** Engaging audio cues for moves and game outcomes.
* **User Feedback:** Flash messages provide clear notifications for successful actions, errors, and important game information.

## 📁 Project Structure

tic-tac-toe/
├── app.py
├── leaderboard.json  (auto-generated on first run)
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── script.js
│   └── sounds/
│       ├── move.mp3
│       └── win.mp3
└── templates/
├── game.html
└── index.html

## 🚀 Getting Started

Follow these instructions to set up and run the Tic Tac Toe game on your local machine.

### Prerequisites

* Python 3.x
* `pip` (Python package installer, usually comes with Python)

### Installation

1.  **Clone the repository or create the files:**
    Ensure you have all the project files (`app.py`, `static/`, `templates/`, etc.) organized as shown in the `Project Structure`.

2.  **Navigate to the project directory:**

    ```bash
    cd tic-tac-toe
    ```

3.  **Create a Python virtual environment (recommended):**

    ```bash
    python -m venv venv
    ```

4.  **Activate the virtual environment:**

    * **On Windows (Command Prompt):**
        ```bash
        .\venv\Scripts\activate
        ```
    * **On Windows (PowerShell):**
        ```bash
        $env:FLASK_SECRET_KEY="your_super_secret_key_here" # Set this before running
        .\venv\Scripts\activate
        ```
    * **On macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```

5.  **Install Flask:**

    ```bash
    pip install Flask
    ```

6.  **Set the Flask Secret Key:**
    Flask uses a secret key to secure sessions. It's crucial for security.
    **Before running `app.py`**, set an environment variable with a strong, random string. Replace `your_super_secret_key_here` with your actual key.

    * **On Windows (Command Prompt):**
        ```bash
        set FLASK_SECRET_KEY=your_super_secret_key_here
        ```
    * **On Windows (PowerShell):**
        ```bash
        $env:FLASK_SECRET_KEY="your_super_secret_key_here"
        ```
    * **On macOS/Linux:**
        ```bash
        export FLASK_SECRET_KEY='your_super_secret_key_here'
        ```
    For production environments, consider more robust ways to manage environment variables.

### Running the Application

1.  **From the project root directory, with your virtual environment activated, run:**

    ```bash
    python app.py
    ```

2.  **Open your web browser** and navigate to:
    ```
    [http://127.0.0.1:5000/](http://127.0.0.1:5000/)
    ```

## 🎮 How to Play

1.  **Enter Names:** On the welcome page, type in the names for Player X and Player O.
2.  **Start Game:** Click the "Start Game" button.
3.  **Make Moves:** Click on any empty cell on the 3x3 board to place your mark (X or O).
4.  **Game Outcome:** The game will automatically announce the winner or if it's a draw.
5.  **Player Stats:** The left panel will show the current session's wins for each player, draws, and total matches.
6.  **Move History:** The right panel will display a chronological list of all moves made in the current game.
7.  **Reset Board:** Click the "Reset Board" button to clear the grid and start a new round with the *same players*, continuing to accumulate stats for the current session.
8.  **Start New Game:** Click the "Start New Game" link (next to the Reset button) to return to the player name input screen. This action will completely reset all session-based statistics.

## 🛠️ Technologies Used

* **Backend:**
    * [Flask](https://flask.palletsprojects.com/) - Python web framework
* **Frontend:**
    * HTML5
    * CSS3
    * JavaScript (ES6+)
* **Data Persistence:**
    * JSON (`leaderboard.json`) for global player statistics

## 💡 Future Enhancements

* **Dedicated Leaderboard Page:** Create a separate page to display the persistent global leaderboard from `leaderboard.json`.
* **AI Opponent:** Implement an artificial intelligence player for single-player mode.
* **Customization:** Add options for theme selection or custom board colors.
* **User Authentication:** For more robust player tracking across devices/sessions.
* **Real-time Multi-player:** Use WebSockets for live online play between remote users.