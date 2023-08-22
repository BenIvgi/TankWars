import pygame
from sprites import all_sprites
BLACK = (0, 0, 0)
BULLET_WIDTH = 5
BULLET_HEIGHT = 5

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.Surface([BULLET_WIDTH, BULLET_HEIGHT])
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = direction

    #overriding update function in sprite
    def update(self, bullets, walls):
        self.rect.x += 5*self.direction

    def handle_bullet_wall_collision(bullets, walls):
        for bullet in bullets:
            bullet_hit_wall = bullet.rect.collidelist([wall.rect for wall in walls])
            if bullet_hit_wall != -1:
                bullets.remove(bullet)
                all_sprites.remove(bullet)