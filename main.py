import pygame
import random
from tile import Tile
from cell import Cell

# constants
DIM = 40
WIDTH, HEIGHT = 800, 800

tiles = []
tile_images = []
grid = []

def load_image(path):
    img = pygame.image.load(path).convert_alpha()
    return img

def check_valid(arr, valid):
    """Check is any element in arr is valid."""

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
    """Create a cell for each spot on the grid"""

    for i in range(DIM * DIM):
        grid.append(Cell(len(tiles)))

def remove_duplicated_tiles(tiles):
    unique_tiles_map = {}
    for tile in tiles:
        key = ','.join(tile.edges)  # ex: "ABB,BCB,BBA,AAA"
        unique_tiles_map[key] = tile
    return list(unique_tiles_map.values())

def draw(screen):
    w = screen.get_width() / DIM
    h = screen.get_height() / DIM

    # draw the grid
    for j in range(DIM):
        for i in range(DIM):
            cell = grid[i + j * DIM]
            if cell.collapsed:
                index = cell.options[0]
                image = tiles[index].img
                scaled_img = pygame.transform.scale(image, (w, h)) # scale the img
                screen.blit(scaled_img, (i * w, j * h))
            else:
                # create blanks
                pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(i * w, j * h, w, h), 1)

    # make a copy of the grid and remove any collapsed cells
    grid_copy = [cell for cell in grid if not cell.collapsed]
    # print(grid)
    # print(grid_copy)

    # algorithm has completed if everything is collapsed
    if len(grid_copy) == 0:
        return

    # pick a cell with the least entropy
    # sort by entropy
    grid_copy.sort(key=lambda x: len(x.options))

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
                options = list(range(len(tiles)))
                # print(options)

                # look up
                if j > 0:
                    up = grid[i + (j - 1) * DIM]
                    valid_options = []
                    for option in up.options:
                        valid = tiles[option].down
                        valid_options.extend(valid)
                    check_valid(options, valid_options)

                # look right
                if i < DIM - 1:
                    right = grid[i + 1 + j * DIM]
                    valid_options = []
                    for option in right.options:
                        valid = tiles[option].left
                        valid_options.extend(valid)
                    check_valid(options, valid_options)

                # look down
                if j < DIM - 1:
                    down = grid[i + (j + 1) * DIM]
                    valid_options = []
                    for option in down.options:
                        valid = tiles[option].up
                        valid_options.extend(valid)
                    check_valid(options, valid_options)

                # look left
                if i > 0:
                    left = grid[i - 1 + j * DIM]
                    valid_options = []
                    for option in left.options:
                        valid = tiles[option].right
                        valid_options.extend(valid)
                    check_valid(options, valid_options)

                next_grid.append(Cell(options))
    
    # re-assign the grid value after cell evaluation
    grid[:] = next_grid

def main():
    # initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Wave Function Collapse")

    # preload images
    path = "./tiles/circuit"
    for i in range(13):
        tile_images.append(load_image(f"{path}/{i}.png"))

    # create and label the tiles
    tiles.append(Tile(tile_images[0], ['AAA', 'AAA', 'AAA', 'AAA']))
    tiles.append(Tile(tile_images[1], ['BBB', 'BBB', 'BBB', 'BBB']))
    tiles.append(Tile(tile_images[2], ['BBB', 'BCB', 'BBB', 'BBB']))
    tiles.append(Tile(tile_images[3], ['BBB', 'BDB', 'BBB', 'BDB']))
    tiles.append(Tile(tile_images[4], ['ABB', 'BCB', 'BBA', 'AAA']))
    tiles.append(Tile(tile_images[5], ['ABB', 'BBB', 'BBB', 'BBA']))
    tiles.append(Tile(tile_images[6], ['BBB', 'BCB', 'BBB', 'BCB']))
    tiles.append(Tile(tile_images[7], ['BDB', 'BCB', 'BDB', 'BCB']))
    tiles.append(Tile(tile_images[8], ['BDB', 'BBB', 'BCB', 'BBB']))
    tiles.append(Tile(tile_images[9], ['BCB', 'BCB', 'BBB', 'BCB']))
    tiles.append(Tile(tile_images[10], ['BCB', 'BCB', 'BCB', 'BCB']))
    tiles.append(Tile(tile_images[11], ['BCB', 'BCB', 'BBB', 'BBB']))
    tiles.append(Tile(tile_images[12], ['BBB', 'BCB', 'BBB', 'BCB']))

    # assign indexes to Tile objects
    for i in range(len(tiles)):
        tiles[i].index = i

    # create new tile duplicates from rotating and add to tiles list.
    for i in range(len(tiles)):
        temp_tiles = []
        for j in range(4):
            temp_tiles.append(tiles[i].rotate(j))
        temp_tiles = remove_duplicated_tiles(temp_tiles)  # Assuming this function is defined elsewhere
        tiles.extend(temp_tiles)
    # print(f"Total tiles: {len(tiles)}")

    # generate the adjacency rules based on edges
    for i in range(len(tiles)):
        tile = tiles[i]
        tile.analyze(tiles)
        # print(f"{i}: u{tile.up}, r{tile.right}, d{tile.down}, l{tile.left}")
                 
    make_grid()

    # game loop
    loop = True
    while loop:
        # event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    loop = False

        # set background color
        screen.fill((0, 0, 0))

        # draw elements on the screen
        draw(screen)

        # update the display
        pygame.display.flip()

        # cap the frame rate
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()