from collections import deque  # Helps us use a special queue for BFS

# 1. Load the maze from a text file
def load_maze(filename):
    with open(filename, "r") as file:
        return [list(line.strip()) for line in file.readlines()]

# 2. Find the start (S) and end (E) points
def find_points(maze):
    start = end = None
    for y, row in enumerate(maze):          # y is the row number
        for x, cell in enumerate(row):      # x is the column number
            if cell == "S":
                start = (x, y)               # Save start position
            elif cell == "E":
                end = (x, y)                 # Save end position
    return start, end

# 3. Solve maze using BFS (shortest path)
def bfs(maze, start, end):
    queue = deque([(start, [start])])       # Each item: (current_pos, path_so_far)
    visited = set([start])                  # Keep track of visited spots

    while queue:
        (x, y), path = queue.popleft()      # Get the first item from queue

        if (x, y) == end:                   # If we reach the end
            return path

        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:  # Try 4 directions
            nx, ny = x + dx, y + dy
            if (0 <= ny < len(maze) and 0 <= nx < len(maze[0]) and
                maze[ny][nx] != "#" and (nx, ny) not in visited):
                visited.add((nx, ny))
                queue.append(((nx, ny), path + [(nx, ny)]))  # Add to queue

    return None  # No path found

# 4. Solve maze using DFS (might not be shortest)
def dfs(maze, start, end):
    stack = [(start, [start])]
    visited = set([start])

    while stack:
        (x, y), path = stack.pop()          # Get the last item (DFS style)

        if (x, y) == end:
            return path

        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = x + dx, y + dy
            if (0 <= ny < len(maze) and 0 <= nx < len(maze[0]) and
                maze[ny][nx] != "#" and (nx, ny) not in visited):
                visited.add((nx, ny))
                stack.append(((nx, ny), path + [(nx, ny)]))

    return None

from PIL import Image, ImageDraw  # Add to the top of your file

def draw_maze_path(maze, path, filename="maze_path.png"):
    cell_size = 20  # size of each cell in pixels
    width = len(maze[0]) * cell_size
    height = len(maze) * cell_size

    # Create a white canvas
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)

    # Draw maze
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            top_left = (x * cell_size, y * cell_size)
            bottom_right = ((x+1) * cell_size, (y+1) * cell_size)

            if cell == "#":
                draw.rectangle([top_left, bottom_right], fill="black")
            elif cell == "S":
                draw.rectangle([top_left, bottom_right], fill="green")
            elif cell == "E":
                draw.rectangle([top_left, bottom_right], fill="red")

    # Draw path
    for x, y in path:
        top_left = (x * cell_size + 5, y * cell_size + 5)
        bottom_right = ((x+1) * cell_size - 5, (y+1) * cell_size - 5)
        draw.rectangle([top_left, bottom_right], fill="blue")

    # Save image
    img.save(filename)
    print(f"Image saved as {filename}")


# 5. Run the program
maze = load_maze("complex_maze.txt")  # Your maze file
start, end = find_points(maze)        # Find S and E

# Solve using both BFS and DFS
bfs_path = bfs(maze, start, end)
dfs_path = dfs(maze, start, end)

# Solve using both methods
bfs_path = bfs(maze, start, end)
dfs_path = dfs(maze, start, end)

# Draw image for BFS path
if bfs_path:
    draw_maze_path(maze, bfs_path, "bfs_path.png")
    print("✅ BFS path image saved as bfs_path.png")

# Draw image for DFS path
if dfs_path:
    draw_maze_path(maze, dfs_path, "dfs_path.png")
    print("✅ DFS path image saved as dfs_path.png")

# draw maze with path
def draw_maze(maze, path, start, end, filename='maze_path.png'):
    import matplotlib.pyplot as plt

    rows = len(maze)
    cols = len(maze[0])
    fig, ax = plt.subplots(figsize=(cols, rows))

    # Draw maze: blue for wall, white for open path
    for y in range(rows):
        for x in range(cols):
            if maze[y][x] == '#':
                ax.add_patch(plt.Rectangle((x, rows - y - 1), 1, 1, color='blue'))   # wall
            else:
                ax.add_patch(plt.Rectangle((x, rows - y - 1), 1, 1, color='white'))  # path

    # Draw red path if available
    if path:
        px, py = zip(*[(x + 0.5, rows - y - 1 + 0.5) for x, y in path])
        ax.plot(px, py, color='red', linewidth=2)

    # Draw Start point (green with 'S')
    ax.plot(start[0] + 0.5, rows - start[1] - 0.5, 'go')
    ax.text(start[0] + 0.3, rows - start[1] - 0.8, 'S', fontsize=12, color='black')

    # Draw End point (red with 'E')
    ax.plot(end[0] + 0.5, rows - end[1] - 0.5, 'ro')
    ax.text(end[0] + 0.3, rows - end[1] - 0.8, 'E', fontsize=12, color='black')

    # Finish up
    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows)
    ax.set_aspect('equal')
    ax.axis('off')
    plt.savefig(filename, bbox_inches='tight', pad_inches=0.1)
    plt.close()

draw_maze(maze, dfs_path, start, end, filename='dfs_path.png')
draw_maze(maze, bfs_path, start, end, filename='bfs_path.png')



