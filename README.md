# Senet Board Game

Senet is one of the oldest known board games, originating in ancient Egypt. This project aims to recreate Senet in a digital format, providing a playable version of the game with a focus on historical accuracy and modern playability.

## Description

Senet is one of the oldest known board games, with origins tracing back to ancient Egypt around 3100 BC. The game is believed to have been a favorite among Pharaohs and commoners alike. Senet is played on a grid of thirty squares, arranged in three rows of ten, each square adorned with symbolic markings. The game’s historical significance extends beyond mere entertainment; it is thought to possess a religious aspect, symbolizing the journey of the soul to the afterlife.

This implementation of Senet seeks to bridge the gap between an ancient game and modern players by providing a digital version that is both historically accurate and accessible. Players can experience this traditional game through a modern graphical user interface, which includes detailed graphics that reflect the aesthetic of ancient Egypt. 

### Gameplay Mechanics
The game combines elements of strategy and luck, introduced through the roll of sticks or bones, which serve as ancient dice. Players move their pieces according to the rolls, navigating a path that is both strategic and symbolic, attempting to safely reach the game’s final square, which signifies the end of the journey.

### Multiple Game Modes
- **Human vs. Human:** Challenge a friend in a face-to-face match, promoting social interaction and strategic play. This mode is perfect for players who enjoy competitive gameplay with family or friends.

- **Human vs. Random Agent:** Test your skills against an AI opponent that makes moves randomly. This mode is suitable for beginners looking to understand the basics of the game without overwhelming strategic complexity.

- **Human vs. Heuristic Agent:** Engage with a more challenging AI that utilizes heuristic-based decision-making. This agent analyzes the game state to make smarter moves based on common strategic principles of Senet. Ideal for intermediate players who seek to improve their gameplay through practice against a competent opponent.

- **Human vs. MCTS (Monte Carlo Tree Search) Agent:** Compete against our most advanced AI, which employs the Monte Carlo Tree Search algorithm to simulate possible outcomes and determine the best moves. This mode offers a high level of difficulty and is designed for experienced players who want to experience a strong strategic challenge.

## Getting Started

These instructions will guide you through setting up the project on your local machine for development and playing. Follow these steps to get a copy of the Senet game up and running.

### Prerequisites

Before you can run the game, you'll need to install Python and Pygame. Here's how to install these essential components:

- **Python 3:** Senet is developed using Python 3. If you don't already have Python 3 installed, you can download it from the [official Python website](https://www.python.org/downloads/). Make sure to download a version that is 3.6 or higher.

- **Pygame:** This project uses Pygame for handling graphics and game dynamics. Once Python is installed, you can install Pygame using pip, Python's package installer. Run the following command in your terminal:

    ```bash
    pip install pygame
    ```

### Downloading the Game

Clone the repository to your local machine using git. If you have git installed, you can clone the repository by running:

```bash
git clone https://github.com/Lindsay-00/senet-python.git
cd senet-python
```

### Running the Game

Once you have Python and Pygame installed and have obtained the source code, you can start the game by navigating to the project directory and running the main script. Here's how to execute the game:
```bash
python3 main.py
```

This command starts the Senet game using Python 3. Ensure you are in the correct directory where main.py is located when you execute this command.

## Rules of Senet

The game board consists of 30 squares, arranged in three rows of ten. The squares are numbered from 1 to 30, and the movement is typically in a reverse "S" pattern, starting from the bottom left, moving to the right, and then zigzagging back to the top. Each player has a set of pawns (7 in this version), which they move according to the rolls of throwing sticks or, in some modern recreations, dice.

### Objective
The main objective of Senet is to move all your pawns off the board before your opponent. This represents a journey through the underworld in the context of ancient Egyptian beliefs, culminating in the afterlife.

### Setup
- Each player starts with 7 pawns placed alternately on the first 14 squares of the board.
- Player with black pawns goes first.

### Game Play
1. **Turns**: Players take turns, each casting the sticks (dice in this version) to determine their move. The sticks have one side marked and one side unmarked, and the number of marked sides facing up determines the number of spaces a player can move their pawn.
2. **Movement**: Players move their pawns along the squares starting from the first square, moving towards the 30th square in a reversed "S" or zigzag pattern. Players must move a pawn when a valid move is available. If no valid moves are possible on a player's turn due to the outcome of the casting sticks or the position of pawns on the board, the turn automatically passes to the opponent.
3. **Swapping Places**: If a player lands on a square occupied by an opponent's pawn, the two pawns swap positions, except in the following cases:
   - **Blocked by Two**: If the opponent's pawns are in two consecutive squares leading up to the square landed on, the swap does not occur as the path is blocked.
   - **Blocked by Three**: If the opponent's pawns occupy three consecutive squares leading up to the square landed on, the player cannot swap positions or jump over these pawns. This creates a barrier that must be navigated around through other moves or strategic plays.
4. **Safe squares**: Some squares are marked as "safe," where pawns cannot be swapped.
   - **The House of Rebirth (Square 15)**
   - **The House of Happiness (Square 26)**
   - **The House of Three Truths (Square 28)**
   - **The House of the Re-Atoum (Square 29)**
5. **Special squares**:
   - The 15th square is the "House of Rebirth": Landing on this square allows a player's pawn to be "reborn." It's a safe square where pawns cannot be swapped.
   - The 26th square is the "House of Happiness," players must land on this square in order to proceed.
   - The 27th square is the "House of Water," and landing on this square will send the player's pawn back The House of Rebirth (Square 15). If The House of Rebirth is already occupied by another pawn, the arriving pawn will be sent to the first unoccupied square before Square 15.
   - The 28th square is the "House of Three Truths," which requires a roll of three to leave.
   - The 29th square is the "House of Two Truths," requiring a roll of two to advance.


### Winning the Game

- The first player to successfully move all of their pawns off the board, by landing exactly on the 31st square with each, wins the game.


### Casting the sticks

In this digital version of Senet, instead of casting sticks, players will click on a "Roll Dice" button to determine their moves. The simulated dice roll mimics the probability distribution of the casting sticks with the following chances for each outcome:
- **1 move**: 1/4 chances
- **2 moves**: 3/8 chances
- **3 moves**: 1/4 chances
- **4 moves**: 1/16 chance
- **5 moves**: 1/16 chance

