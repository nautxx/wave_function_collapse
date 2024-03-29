import pygame

def reverse_string(s):
    return s[::-1]

def compare_edge(a, b):
    return a == reverse_string(b)

class Tile:
    def __init__(self, img, edges):
        self.img = img
        self.edges = edges
        self.up = []
        self.right = []
        self.down = []
        self.left = []

    def rotate(self, num):
        w, h = self.img.get_size()
        new_img = pygame.Surface((w, h), pygame.SRCALPHA)
        new_img.blit(self.img, (0, 0))
        new_img = pygame.transform.rotate(new_img, -90 * num)

        new_edges = []
        length = len(self.edges)
        for i in range(length):
            new_edges.append(self.edges[(i - num + length) % length])

        return Tile(new_img, new_edges)
    
    def analyze(self, tiles):
        for i in range(len(tiles)):
            tile = tiles[i]

            # UP
            if compare_edge(tile.edges[2], self.edges[0]):
                self.up.append(tile)
            # RIGHT
            if compare_edge(tile.edges[3], self.edges[1]):
                self.right.append(tile)
            # DOWN
            if compare_edge(tile.edges[0], self.edges[2]):
                self.down.append(tile)
            # LEFT
            if compare_edge(tile.edges[1], self.edges[3]):
                self.left.append(tile)