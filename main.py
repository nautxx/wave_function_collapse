import pygame
import random
from tile import Tile
from cell import Cell

# constants
WIDTH, HEIGHT = 800, 800
DIM = 10

tiles = []
tile_images = []

grid = []

def load_image(path):
    img = pygame.image.load(path).convert_alpha()
    return img

def preload():
    path = "./tiles/circuit"
    for i in range(13):
        tile_images.append(load_image(f"{path}/{i}.png"))

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

def make_grid():
    # Create cell for each spot on the grid
    for i in range(DIM * DIM):
        grid.append(Cell(len(tiles)))

def remove_duplicated_tiles(tiles):
    unique_tiles_map = {}
    for tile in tiles:
        key = ','.join(tile.edges)  # ex: "ABB,BCB,BBA,AAA"
        unique_tiles_map[key] = tile
    return list(unique_tiles_map.values())

def draw(screen, tiles, grid):
    w = WIDTH / DIM
    h = HEIGHT / DIM

    # draw the grid
    for j in range(DIM):
        for i in range(DIM):
            cell = grid[i + j * DIM]
            if cell.collapsed:
                index = cell.options[0]
                img = tiles[index].img
                scaled_img = pygame.transform.scale(img, (w, h)) # scale the img
                screen.blit(scaled_img, (i * w, j * h))
            else:
                pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(i * w, j * h, w, h), 1)

    # make a copy of the grid and removed any collapsed cells
    grid_copy = [cell for cell in grid if not cell.collapsed]

    # algorithm has completed if everything is collapsed
    if len(grid_copy) == 0:
        return

    # pick a cell with least entropy
    # sort by entropy
    grid_copy.sort(key=lambda cell: len(cell.options))

    # keep only the lowest entropy cells
    length = len(grid_copy[0].options)
    stop_index = 0
    for i in range(1, len(grid_copy)):
        if len(grid_copy[i].options) > length:
            stop_index = i
            break
    if stop_index > 0:
        grid_copy = grid_copy[:stop_index]

    # collapse a cell
    if grid_copy:
        cell = random.choice(grid_copy)
        cell.collapsed = True
        pick = random.choice(cell.options)
        if pick == None:
            make_grid()
            return
        cell.options = [pick]

    # print(grid)
    # print(grid_copy)

    # calculate entropy
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
                        valid = tiles[option].down
                        valid_options.extend(valid)
                    check_valid(options, valid_options)
                # Look right
                if i < DIM - 1:
                    right = grid[i + 1 + j * DIM]
                    valid_options = []
                    for option in right.options:
                        valid = tiles[option].left
                        valid_options.extend(valid)
                    check_valid(options, valid_options)
                # Look down
                if j < DIM - 1:
                    down = grid[i + (j + 1) * DIM]
                    valid_options = []
                    for option in down.options:
                        valid = tiles[option].up
                        valid_options.extend(valid)
                    check_valid(options, valid_options)
                # Look left
                if i > 0:
                    left = grid[i - 1 + j * DIM]
                    valid_options = []
                    for option in left.options:
                        valid = tiles[option].right
                        valid_options.extend(valid)
                    check_valid(options, valid_options)

                next_grid.append(Cell(options))
    grid = next_grid

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    preload()

    tiles.append(Tile(tile_images[0], ['AAA', 'AAA', 'AAA', 'AAA'], 0))
    tiles.append(Tile(tile_images[1], ['BBB', 'BBB', 'BBB', 'BBB'], 1))
    tiles.append(Tile(tile_images[2], ['BBB', 'BCB', 'BBB', 'BBB'], 2))
    tiles.append(Tile(tile_images[3], ['BBB', 'BDB', 'BBB', 'BDB'], 3))
    tiles.append(Tile(tile_images[4], ['ABB', 'BCB', 'BBA', 'AAA'], 4))
    tiles.append(Tile(tile_images[5], ['ABB', 'BBB', 'BBB', 'BBA'], 5))
    tiles.append(Tile(tile_images[6], ['BBB', 'BCB', 'BBB', 'BCB'], 6))
    tiles.append(Tile(tile_images[7], ['BDB', 'BCB', 'BDB', 'BCB'], 7))
    tiles.append(Tile(tile_images[8], ['BDB', 'BBB', 'BCB', 'BBB'], 8))
    tiles.append(Tile(tile_images[9], ['BCB', 'BCB', 'BBB', 'BCB'], 9))
    tiles.append(Tile(tile_images[10], ['BCB', 'BCB', 'BCB', 'BCB'], 10))
    tiles.append(Tile(tile_images[11], ['BCB', 'BCB', 'BBB', 'BBB'], 11))
    tiles.append(Tile(tile_images[12], ['BBB', 'BCB', 'BBB', 'BCB'], 12))

    # tiles.append(tiles[1].rotate(1))
    # tiles.append(tiles[1].rotate(2))
    # tiles.append(tiles[1].rotate(3))

    initial_tile_count = len(tiles)
    for i in range(initial_tile_count):
        temp_tiles = []
        for j in range(4):
            temp_tiles.append(tiles[i].rotate(j))
        temp_tiles = remove_duplicated_tiles(temp_tiles)  # Assuming this function is defined elsewhere
        tiles.extend(temp_tiles)
    print(f"Total tiles: {len(tiles)}")

    # generate the adjacency rules based on edges
    for i in range(len(tiles)):
        tile = tiles[i]
        tile.analyze(tiles)
                 
    make_grid()

    loop = True
    while loop:
        # event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False

        # default background color
        screen.fill((0, 0, 0))

        # draw elements on the screen
        draw(screen, tiles, grid)

        # update the display
        pygame.display.flip()

        # cap the frame rate
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()