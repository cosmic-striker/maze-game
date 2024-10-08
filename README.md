# 🎮 Maze Generation and Solver Visualization 🧩

This project is a Python-based maze generation and solver visualization built using the Pygame library. The application generates a random maze 🏞️ and solves it step by step using Depth-First Search (DFS), providing a real-time visualization of both processes. Players can also navigate the maze manually using the arrow keys 🎯.

## 🚀 Features

- **Maze Generation**: The maze is generated using randomized Prim's algorithm, creating a 20x20 grid 🧱.
- **Maze Solving**: Uses the Depth-First Search (DFS) algorithm to solve the maze and visualizes the process 🧑‍💻.
- **Player Navigation**: The player can move through the maze manually using the keyboard (W, A, S, D or Arrow keys) 🏃‍♂️.
- **Responsive Window**: The window is resizable 🖥️, and the game can be toggled between fullscreen and windowed mode 🔄.
- **Smooth Animations**: Maze generation and solving processes are visually animated 🎨 for better understanding.

## 🎮 Controls

- `W`, `A`, `S`, `D` or Arrow keys: Move the player around the maze.
- `F`: Toggle fullscreen mode 🖥️↔️.
- `Esc` or close button: Exit the program 🚪.

## 🧠 How It Works

1. **Maze Generation**:
   - The maze is generated in a grid where cells can either be walls (`#`) or empty spaces (` `) 🔲.
   - Randomized Prim's algorithm is used to carve out paths 🪓 by picking random walls and ensuring no cycles are formed.
   
2. **Maze Solving**:
   - DFS is employed to find the path from the start (top-left corner) to the end (bottom-right corner) 🏁.
   - As the algorithm explores different paths, it visualizes successful moves in green 🍀 and backtracks in red ❌.
   
3. **Player Movement**:
   - After the maze is generated, you can manually move the player (represented as a red square 🔴) from the starting point to the end using the keyboard.

## 🛠️ Requirements

Ensure you have the following dependencies installed:

- Python 3.7+
- Pygame 🎮

### 💻 Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/maze-generator-solver.git
   cd maze-generator-solver
   ```

2. Install dependencies:

   ```bash
   pip install pygame
   ```

3. Run the game:

   ```bash
   python maze_game.py
   ```

## 📂 Project Structure

```
├── maze_game.py      # Main script containing the game logic 🧠
└── README.md         # Project documentation 📄
```

## ✏️ How to Modify

- **Change Maze Size**: Modify the `GRID_SIZE` variable to generate a larger or smaller maze 📏.
- **Adjust Animation Speed**: Change the delay values ⏳ in the `MazeGenerator` and `MazeSolver` classes to control how fast the maze is generated and solved.

## 🚧 Future Enhancements

- Add more algorithms for maze generation and solving (e.g., Dijkstra, A*) 🤖.
- Implement pathfinding visualizations for different maze solving algorithms 🗺️.
- Introduce obstacles and more interactive gameplay elements 🏹.

## 📜 License

This project is licensed under the MIT License. See `LICENSE` for more details 📝.

