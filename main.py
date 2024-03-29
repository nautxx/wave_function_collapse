import pygame
import random
from tile import Tile
from cell import Cell

# constants
WIDTH, HEIGHT = 800, 800
DIM = 20

def load_image(path, dim, padding=0):
    img = pygame.image.load(path).convert_alpha()
    img = pygame.transform.scale(img, (dim - padding, dim - padding))
    return img

def preload():
    images = []
    path = "./tiles/tetris"
    images.append(load_image(f"{path}/blank.png", DIM))
    images.append(load_image(f"{path}/up.png", DIM))
    return images

def check_valid(arr, valid):
    # VALID: [BLANK, RIGHT]
    # ARR: [BLANK, UP, RIGHT, DOWN, LEFT]
    # result in removing UP, DOWN, LEFT
    i = len(arr) - 1
    while i >= 0:
        element = arr[i]
        if element not in valid:
            arr.pop(i)
        i -= 1

def draw(screen, tiles, grid):
    screen.blit(tiles[0].img, (0, 0))
    screen.blit(tiles[1].img, (50, 0))
    screen.blit(tiles[2].img, (100, 0))
    screen.blit(tiles[3].img, (150, 0))
    screen.blit(tiles[4].img, (0, 50))

    w = WIDTH / DIM
    h = HEIGHT / DIM

    for j in range(DIM):
        for i in range(DIM):
            cell = grid[i + j * DIM]
            if cell.collapsed:
                index = cell.options[0]
                img = tiles[index].img
                scaled_img = pygame.transform.scale(img, (w, h)) # scale the img
                screen.blit(scaled_img, (i * w, j * h))
            else:
                pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(i * w, j * h, w, h))

    # Pick cell with least entropy
    grid_copy = [cell for cell in grid if not cell.collapsed]

    if not grid_copy:
        return  # If there are no cells with options, exit the function

    grid_copy.sort(key=lambda cell: len(cell.options))

    # Find the stop index
    len_options = len(grid_copy[0].options)
    stop_index = next((i for i, cell in enumerate(grid_copy) if len(cell.options) > len_options), 0)

    if stop_index > 0:
        grid_copy = grid_copy[:stop_index]

    if grid_copy:
        cell = random.choice(grid_copy)
        cell.collapsed = True
        pick = random.choice(cell.options)
        if pick is None:
            start_over()
            return
        cell.options = [pick]

    print(grid)
    print(grid_copy)

    next_grid = []
    for j in range(DIM):
        for i in range(DIM):
            index = i + j * DIM
            if grid[index].collapsed:
                next_grid.append(grid[index])
            else:
                options = list(range(len(tiles)))  # List of options
                # Look up
                if j > 0:
                    up = grid[i + (j - 1) * DIM]
                    valid_options = []
                    for option in up.options:
                        valid_options.extend(tiles[option].down)
                    check_valid(options, valid_options)
                # Look right
                if i < DIM - 1:
                    right = grid[i + 1 + j * DIM]
                    valid_options = []
                    for option in right.options:
                        valid_options.extend(tiles[option].left)
                    check_valid(options, valid_options)
                # Look down
                if j < DIM - 1:
                    down = grid[i + (j + 1) * DIM]
                    valid_options = []
                    for option in down.options:
                        valid_options.extend(tiles[option].up)
                    check_valid(options, valid_options)
                # Look left
                if i > 0:
                    left = grid[i - 1 + j * DIM]
                    valid_options = []
                    for option in left.options:
                        valid_options.extend(tiles[option].right)
                    check_valid(options, valid_options)

                next_grid.append({
                    'collapsed': True,
                    'options': options
                })
    grid = next_grid

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    tile_images = preload()

    tiles = []
    tiles.append(Tile(tile_images[0], [0, 0, 0 ,0]))
    tiles.append(Tile(tile_images[1], [1, 1, 0 ,1]))
    tiles.append(tiles[1].rotate(1))
    tiles.append(tiles[1].rotate(2))
    tiles.append(tiles[1].rotate(3))

    # Generate the adjacency rules based on edges
    for i in range(len(tiles)):
        tile = tiles[i]
        tile.analyze(tiles)
                 
    # Create cell for each spot on the grid
    grid = []
    for i in range(DIM * DIM):
        grid.append(Cell(len(tiles)))

    loop = True
    while loop:
        # event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False

        # default background color
        screen.fill((255, 255, 255))

        # draw elements on the screen
        draw(screen, tiles, grid)

        # update the display
        pygame.display.flip()

        # cap the frame rate
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()