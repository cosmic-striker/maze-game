import pygame
import random

# Initialize Pygame
pygame.init()

# Define constants
WIDTH, HEIGHT = 600, 600  # Size of the window
ROWS, COLS = 50, 50  # Number of rows and columns in the maze
CELL_SIZE = WIDTH // COLS  # Size of each cell in the grid
FPS = 60  # Frames per second

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Generator with Pathfinding")
clock = pygame.time.Clock()

# Maze generator class
class MazeGenerator:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [['#' for _ in range(cols)] for _ in range(rows)]
        self.path = []

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
            self.draw_maze()
        
        # Set the start and end points
        self.grid[0][0] = ' '
        self.grid[self.rows - 1][self.cols - 1] = ' '

        # Find and mark the path from start to end
        self.find_path(0, 0, [])

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

    def find_path(self, x, y, visited):
        if (x, y) == (self.cols - 1, self.rows - 1):
            self.path = visited + [(x, y)]
            return True

        visited.append((x, y))

        neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        random.shuffle(neighbors)

        for nx, ny in neighbors:
            if 0 <= nx < self.cols and 0 <= ny < self.rows and self.grid[ny][nx] == ' ' and (nx, ny) not in visited:
                if self.find_path(nx, ny, visited):
                    return True

        visited.pop()
        return False

    def draw_maze(self):
        screen.fill(BLACK)
        for y in range(self.rows):
            for x in range(self.cols):
                color = WHITE if self.grid[y][x] == ' ' else BLACK
                pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        for (px, py) in self.path:
            pygame.draw.rect(screen, GREEN, (px * CELL_SIZE, py * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        pygame.display.update()
        clock.tick(FPS)

# Main loop
def main():
    maze_gen = MazeGenerator(ROWS, COLS)
    maze_gen.generate_maze()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        maze_gen.draw_maze()

    pygame.quit()

if __name__ == "__main__":
    main()
