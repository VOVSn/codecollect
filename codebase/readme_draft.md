# Project Overview

This Python project consists of a script (`src/larva01.py`) designed to demonstrate various functionalities through command-line arguments. The program can enhance its code, draw ASCII art, play a simple snake game using Pygame, and simulate a tic-tac-toe game in the console.

## Key Functionalities

1. **Code Improvement**: The `make` argument allows you to pass instructions for improving the script's functionality. This utilizes an AI model via the `ollama` library.
2. **ASCII Art Drawing**: Use the `draw_sun` command to print a sun drawn with ASCII art.
3. **Snake Game**: The `snake_game` command starts a basic snake game using Pygame, where you control the movement of the snake on a grid.
4. **Tic-Tac-Toe**: Run the program with `tic_tac_toe` to play a console-based tic-tac-toe game against another player.

# Installation

To set up and run this project, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```

2. **Set Up a Virtual Environment (Optional but Recommended)**:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   ```

3. **Install Dependencies**:
   Install Pygame and the required libraries specified in any `requirements.txt` file, or directly:
   ```bash
   pip install pygame ollama
   ```

4. **Run the Program**:
   Execute the script with desired arguments:
   ```bash
   python src/larva01.py <command>
   ```
   Replace `<command>` with one of `make`, `draw_sun`, `snake_game`, or `tic_tac_toe`.

# Tech Stack

- **Python**: The core programming language used for developing functionalities.
- **Pygame**: A library to create the snake game.
- **Ollama**: Used for AI-driven code improvement.

# Usage Guide

## Code Improvement (`make`)

```bash
python src/larva01.py make "<your instructions>"
```

This command uses the `ollama` library to attempt improving the script's functionality based on provided instructions. The improved code is saved as a new version of the script.

## ASCII Art Drawing (`draw_sun`)

```bash
python src/larva01.py draw_sun
```

Prints an ASCII representation of the sun to the console.

## Snake Game

```bash
python src/larva01.py snake_game
```

Starts a basic snake game. Use arrow keys for navigation.

## Tic-Tac-Toe

```bash
python src/larva01.py tic_tac_toe
```

Play a console-based tic-tac-toe game with another player, taking turns to input moves via the command line.

# Development Guidelines

- **Code Style**: Follow PEP 8 guidelines.
- **Line Length**: Limit lines to a maximum of 79 characters.
- **String Quotes**: Use single quotes for strings unless necessary otherwise.
- **Structure**: Maintain two blank lines between classes and functions.

Ensure all contributions adhere to these standards. Refactor code where necessary for compliance with formatting rules.

# Git Workflow

- **Branch Naming**: Follow the pattern `feature/your-feature-name` or `bugfix/your-bug-fix`.
- **Pull Requests**: Create a PR for each feature or bug fix, detailing changes and their impact.
- **Code Reviews**: Ensure code reviews are conducted to maintain quality standards.

# License

This project is licensed under MIT. See the [LICENSE](LICENSE) file for more details.

---

Feel free to contribute! Follow the guidelines outlined above to ensure consistency across the codebase. If you have any questions or need assistance, reach out through our communication channels.

## Folder Structure:
```
codecollect/
├── README.md
├── requirements.txt
├── setup.cfg
├── src
│   └── larva01.py
```