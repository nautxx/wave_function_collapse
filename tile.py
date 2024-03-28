import pygame

class Tile:
    def __init__(self, img, edges):
        self.img = img
        self.edges = edges

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