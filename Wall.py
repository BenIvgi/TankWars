import pygame
WALL_WIDTH = 30
WALL_HEIGHT = 100

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        path = r"Wall.jpeg"
        self.image = pygame.transform.scale(pygame.image.load(path).convert_alpha(), (WALL_WIDTH, WALL_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
