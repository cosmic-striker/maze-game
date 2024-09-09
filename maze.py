import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants for screen and grid size
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
GRID_SIZE = 100  # 20x20 grid for the maze
CELL_SIZE = SCREEN_WIDTH // GRID_SIZE
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (50, 50, 50)  # Darker border color
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WALL = '#'

# Set up the display (initially windowed)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Maze Generation and Solver Visualization")

# Clock for frame control
clock = pygame.time.Clock()

# Font setup for text inside cells
font = pygame.font.SysFont(None, 24)

def toggle_fullscreen():
    if screen.get_flags() & pygame.FULLSCREEN:
        pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    else:
        pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)

class MazeGenerator:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [['#' for _ in range(cols)] for _ in range(rows)]

    def generate_maze(self):
        start_x = random.randint(0, self.cols // 2) * 2
        start_y = random.randint(0, self.rows // 2) * 2
        self.grid[start_y][start_x] = ' '
        walls = self.get_walls(start_x, start_y)

        while walls:
            wall = random.choice(walls)
            wx, wy = wall
            if self.is_valid_wall(wx, wy):
                self.grid[wy][wx] = ' '
                self.connect_cells(wx, wy)
                new_walls = self.get_walls(wx, wy)
                walls.extend(new_walls)
            walls.remove(wall)
            self.draw_maze_step()

        # Set the start and end points
        self.grid[0][0] = ' '
        self.grid[self.rows - 1][self.cols - 1] = ' '

    def get_walls(self, x, y):
        walls = []
        if x > 1:
            walls.append((x - 2, y))
        if x < self.cols - 2:
            walls.append((x + 2, y))
        if y > 1:
            walls.append((x, y - 2))
        if y < self.rows - 2:
            walls.append((x, y + 2))
        return walls

    def is_valid_wall(self, x, y):
        passage_count = 0
        if x > 1 and self.grid[y][x - 2] == ' ':
            passage_count += 1
        if x < self.cols - 2 and self.grid[y][x + 2] == ' ':
            passage_count += 1
        if y > 1 and self.grid[y - 2][x] == ' ':
            passage_count += 1
        if y < self.rows - 2 and self.grid[y + 2][x] == ' ':
            passage_count += 1
        return passage_count == 1

    def connect_cells(self, x, y):
        if x > 1 and self.grid[y][x - 2] == ' ':
            self.grid[y][x - 1] = ' '
        if x < self.cols - 2 and self.grid[y][x + 2] == ' ':
            self.grid[y][x + 1] = ' '
        if y > 1 and self.grid[y - 2][x] == ' ':
            self.grid[y - 1][x] = ' '
        if y < self.rows - 2 and self.grid[y + 2][x] == ' ':
            self.grid[y + 1][x] = ' '

    def draw_maze_step(self):
        screen.fill(BLACK)
        for y in range(self.rows):
            for x in range(self.cols):
                color = WHITE if self.grid[y][x] == ' ' else BLACK
                pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.display.update()

    def draw_maze(self, offset_x, offset_y):
        screen.fill(BLACK)
        for y in range(self.rows):
            for x in range(self.cols):
                color = WHITE if self.grid[y][x] == ' ' else BLACK
                pygame.draw.rect(screen, color, (offset_x + x * CELL_SIZE, offset_y + y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.display.update()

class MazeSolver:
    def __init__(self, maze):
        self.maze = maze
        self.visited = [[False for _ in range(len(maze[0]))] for _ in range(len(maze))]
        self.solution = []

    def solve_maze(self, start_x, start_y, end_x, end_y, screen, offset_x, offset_y):
        if self.dfs(start_x, start_y, end_x, end_y, screen, offset_x, offset_y):
            print("Maze Solved! Path:")
            print(self.solution)
        else:
            print("No solution found.")

    def dfs(self, x, y, end_x, end_y, screen, offset_x, offset_y):
        # Check if out of bounds or visited or it's a wall
        if x < 0 or y < 0 or x >= len(self.maze[0]) or y >= len(self.maze) or self.visited[y][x] or self.maze[y][x] == WALL:
            return False

        # Mark the current position as visited and add to the solution path
        self.visited[y][x] = True
        self.solution.append((x, y))

        # Visualize the current position being visited
        pygame.draw.rect(screen, GREEN, (offset_x + x * CELL_SIZE, offset_y + y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.display.update()
        pygame.time.delay(50)

        # Check if we reached the end
        if x == end_x and y == end_y:
            return True

        # Explore the neighbors (North, South, East, West)
        if (self.dfs(x + 1, y, end_x, end_y, screen, offset_x, offset_y) or  # Right
            self.dfs(x - 1, y, end_x, end_y, screen, offset_x, offset_y) or  # Left
            self.dfs(x, y + 1, end_x, end_y, screen, offset_x, offset_y) or  # Down
            self.dfs(x, y - 1, end_x, end_y, screen, offset_x, offset_y)):   # Up
            return True

        # Backtrack if no solution found
        self.solution.pop()
        pygame.draw.rect(screen, RED, (offset_x + x * CELL_SIZE, offset_y + y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.display.update()
        pygame.time.delay(50)

        return False

# Main loop
def main():
    maze_gen = MazeGenerator(GRID_SIZE, GRID_SIZE)
    maze_gen.generate_maze()

    # Set up solver for the generated maze
    solver = MazeSolver(maze_gen.grid)

    running = True
    fullscreen = False

    # Player starting position (top-left corner)
    player_pos = [0, 0]

    # Set a speed for movement delay (in milliseconds)
    move_delay = 150  # 150ms delay between movements
    last_move_time = 0

    # Solve the maze and display the solution path
    solver.solve_maze(0, 0, GRID_SIZE - 1, GRID_SIZE - 1, screen, 0, 0)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    # Toggle fullscreen when 'f' is pressed
                    toggle_fullscreen()

        # Get the current time in milliseconds
        current_time = pygame.time.get_ticks()

        # Get current screen size
        current_width, current_height = screen.get_size()

        # Calculate offsets to center the grid in fullscreen mode
        offset_x = (current_width - SCREEN_WIDTH) // 2
        offset_y = (current_height - SCREEN_HEIGHT) // 2

        # Handle key presses for continuous movement
        keys = pygame.key.get_pressed()

        if current_time - last_move_time > move_delay:  # Check if enough time has passed since the last move
            if (keys[pygame.K_w] or keys[pygame.K_UP]) and player_pos[1] > 0:  # Move up
                if maze_gen.grid[player_pos[1] - 1][player_pos[0]] == ' ':
                    player_pos[1] -= 1
                    last_move_time = current_time
            elif (keys[pygame.K_s] or keys[pygame.K_DOWN]) and player_pos[1] < GRID_SIZE - 1:  # Move down
                if maze_gen.grid[player_pos[1] + 1][player_pos[0]] == ' ':
                    player_pos[1] += 1
                    last_move_time = current_time
            elif (keys[pygame.K_a] or keys[pygame.K_LEFT]) and player_pos[0] > 0:  # Move left
                if maze_gen.grid[player_pos[1]][player_pos[0] - 1] == ' ':
                    player_pos[0] -= 1
                    last_move_time = current_time
            elif (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and player_pos[0] < GRID_SIZE - 1:  # Move right
                if maze_gen.grid[player_pos[1]][player_pos[0] + 1] == ' ':
                    player_pos[0] += 1
                    last_move_time = current_time

        # Fill the screen with white
        screen.fill(WHITE)

        # Draw the maze
        maze_gen.draw_maze(offset_x, offset_y)

        # Draw the player (red square)
        player_rect = pygame.Rect(offset_x + player_pos[0] * CELL_SIZE, offset_y + player_pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, RED, player_rect)

        # Update the display
        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
