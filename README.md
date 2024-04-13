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

