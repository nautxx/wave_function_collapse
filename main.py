import pygame

# constants
WIDTH, HEIGHT = 800, 800
DIM = 2

def load_image(path, dim, padding=0):
    img = pygame.image.load(path).convert_alpha()
    img = pygame.transform.scale(img, (dim - padding, dim - padding))
    return img

def preload():
    pass

def draw(screen, tiles, grid):
    screen.blit(tiles[0], (0, 0))
    screen.blit(tiles[1], (50, 0))
    screen.blit(tiles[2], (100, 0))
    screen.blit(tiles[3], (150, 0))
    screen.blit(tiles[4], (0, 50))

    w = WIDTH / DIM
    h = HEIGHT / DIM

    for j in range(DIM):
        for i in range(DIM):
            cell = grid[i + j * DIM]
            if cell['collapsed']:
                index = cell['options'][0]
                img = tiles[index]
                scaled_img = pygame.transform.scale(img, (w, h)) # scale the img
                screen.blit(scaled_img, (i * w, j * h))
            else:
                pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(i * w, j * h, w, h))

    # Pick cell with least entropy
    grid_copy = [cell for cell in grid if not cell['collapsed']]

    if not grid_copy:
        return  # If there are no cells with options, exit the function

    # grid_copy sorted based on the length of options
    grid_copy.sort(key=lambda cell: len(cell['options']))

    print(grid)
    print(grid_copy)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    preload()

    tiles = []

    tiles.append(load_image("./tiles/test/0.png", DIM))
    tiles.append(load_image("./tiles/test/1.png", DIM))
    tiles.append(load_image("./tiles/test/2.png", DIM))
    tiles.append(load_image("./tiles/test/3.png", DIM))
    tiles.append(load_image("./tiles/test/4.png", DIM))

    grid = [{
        'collapsed': False,
        'options': [0, 1, 2, 3, 4]
    } for _ in range(DIM * DIM)]

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