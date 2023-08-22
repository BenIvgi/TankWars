import pygame
from Tank import Tank, WINDOW_HEIGHT,WINDOW_WIDTH
from Bullet import Bullet, BLACK
from Wall import Wall, WALL_HEIGHT, WALL_WIDTH
from sprites import all_sprites
BG_PATH = r"Background.jpeg"
if __name__ == '__main__':
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Tank Wars")
    tanks = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    walls = pygame.sprite.Group()

#1 left -1 right
    tank1 = Tank(120, 400, [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_z], 1)
    tank2 = Tank(600, 400, [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_SPACE], -1)
    # Add tanks to sprite groups
    all_sprites.add(tank1)
    all_sprites.add(tank2)
    tanks.add(tank1)
    tanks.add(tank2)

    maze_walls = []

    for x in range(0, 30):
        if x % 5 == 3:
            maze_walls += [Wall(x * WALL_WIDTH, i * WALL_HEIGHT) for i in range(6) if i != x % 4]
    # Add maze walls to sprite groups
    all_sprites.add(*maze_walls)
    walls.add(*maze_walls)

    running = True
    clock = pygame.time.Clock()

    # Load the background image
    background_image = pygame.image.load(BG_PATH).convert()

    # Resize the background image to match the window dimensions
    background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update all sprites
        all_sprites.update(walls, bullets)  # Update walls as well
        Bullet.handle_bullet_wall_collision(bullets, walls)

        # Check for collision between bullets and tanks
        for bullet in bullets:
            bullet_hit_tank = bullet.rect.collidelist([tank.rect for tank in tanks])
            if bullet_hit_tank != -1:
                tanks.sprites()[bullet_hit_tank].health -= 10  # Reduce tank's health by 10
                if tanks.sprites()[bullet_hit_tank].health <= 0:
                    tanks.sprites()[bullet_hit_tank].kill()  # Eliminate tank when health reaches 0

                bullets.remove(bullet)
                all_sprites.remove(bullet)

        # Clear the screen
        window.fill(BLACK)
        window.blit(background_image, (0, 0))

        # Draw all sprites
        all_sprites.draw(window)

        # Draw health bars
        for tank in tanks:
            tank.update_healthbar()
            window.blit(tank.healthbar, (tank.rect.x, tank.rect.y - 10))

        # Update the display
        pygame.display.flip()

        # Limit the frame rate
        clock.tick(60)

    # Quit the game
    pygame.quit()