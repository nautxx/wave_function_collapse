import pygame

def reverse_string(s):
    return s[::-1]

def compare_edge(a, b):
    return a == reverse_string(b)

class Tile:
    def __init__(self, img, edges, i=None):
        self.img = img
        self.edges = edges
        self.up = []
        self.right = []
        self.down = []
        self.left = []

        if i != None:
            self.index = i

    def rotate(self, num):
        """Rotate a tile and its edges to create a new one"""

        w, h = self.img.get_width(), self.img.get_height(),
        new_img = pygame.Surface((w, h), pygame.SRCALPHA)
        new_img.blit(self.img, (0, 0))
        new_img = pygame.transform.rotate(new_img, -90 * num)

        # rotate edges
        new_edges = []
        length = len(self.edges)
        for i in range(length):
            new_edges.append(self.edges[(i - num + length) % length])
        # print(new_edges)
        return Tile(new_img, new_edges, self.index)
    
    def analyze(self, tiles):
        """Finds valid neighbors."""

        for i in range(len(tiles)):
            tile = tiles[i]

            # tile 5 can't match itself
            if (tile.index == 5 and self.index == 5):
                continue
            # up
            if compare_edge(tile.edges[2], self.edges[0]):
                self.up.append(i)

            # right
            if compare_edge(tile.edges[3], self.edges[1]):
                self.right.append(i)

            # down
            if compare_edge(tile.edges[0], self.edges[2]):
                self.down.append(i)

            # left
            if compare_edge(tile.edges[1], self.edges[3]):
                self.left.append(i)