import pygame
from Bullet import Bullet
from sprites import all_sprites
TANK1_PNG_PATH = r"BlueTank.png"
TANK2_PNG_PATH = r"RedTank.png"

# Define tank dimensions
TANK_WIDTH = 80
TANK_HEIGHT = 80
# Define health bar dimensions
HEALTHBAR_WIDTH = TANK_WIDTH
HEALTHBAR_HEIGHT = 5
# Define RGB colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
# Define window dimensions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

class Tank(pygame.sprite.Sprite):
    def __init__(self, x, y, controls, direction):
        super().__init__()
        path = TANK1_PNG_PATH if direction == 1 else TANK2_PNG_PATH
        #convert alpha makes tank background transperent
        self.image = pygame.transform.scale(pygame.image.load(path).convert_alpha(), (TANK_WIDTH, TANK_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.controls = controls
        self.shoot_delay = 500  # Delay between consecutive shots (in milliseconds)
        self.last_shot_time = pygame.time.get_ticks()
        self.health = 100  # Initial health value - hp hit point
        self.direction = direction

        # Create health bar
        self.healthbar = pygame.Surface([HEALTHBAR_WIDTH, HEALTHBAR_HEIGHT])
        self.healthbar.fill(GREEN)

    # 4 horizontal speed 2 vertical speed
    def update(self, walls, bullets):
        keys = pygame.key.get_pressed()
        dx = 0
        dy = 0
        if keys[self.controls[0]]:
            dy = -2
        if keys[self.controls[1]]:
            dy = 2
        if keys[self.controls[2]]:
            dx = -4
        if keys[self.controls[3]]:
            dx = 4

        #this rect after it will be drawn it'll be in the new place
        new_rect = self.rect.move(dx, dy)

        # Check screen boundaries
        if new_rect.left < 0:
            dx = max(dx, 0)
        if new_rect.right > WINDOW_WIDTH:
            dx = min(dx, 0)
        if new_rect.top < 0:
            dy = max(dy, 0)
        if new_rect.bottom > WINDOW_HEIGHT:
            dy = min(dy, 0)

        # Check for collision with walls
        for wall in walls:
            if new_rect.colliderect(wall.rect):
                dx = 0
                dy = 0
                break

        self.rect.x += dx
        self.rect.y += dy

        #if  player shoots
        if keys[self.controls[-1]]:
            current_time = pygame.time.get_ticks()
            #enough delay between shots
            if current_time - self.last_shot_time > self.shoot_delay:
                bullet = Bullet(self.rect.x + TANK_WIDTH * self.direction / (1 if self.direction == 1 else 10),
                                self.rect.y + TANK_HEIGHT // 2, self.direction)
                bullets.add(bullet)
                all_sprites.add(bullet)
                self.last_shot_time = current_time

    def update_healthbar(self):
        # Update the health bar based on the tank's health value
        health_percentage = self.health / 100
        healthbar_width = int(HEALTHBAR_WIDTH * health_percentage)
        self.healthbar = pygame.Surface([healthbar_width, HEALTHBAR_HEIGHT])
        if health_percentage > 0.5:
            self.healthbar.fill(GREEN)
        elif health_percentage > 0.2:
            self.healthbar.fill(ORANGE)
        else:
            self.healthbar.fill(RED)