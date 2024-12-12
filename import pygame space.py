import pygame
import random

# Initialize pygame
pygame.init()

# Define constants
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Load assets
player_img = pygame.Surface((50, 50))
player_img.fill(GREEN)  # Space ship as green
player_rect = player_img.get_rect(center=(WIDTH // 2, HEIGHT - 50))

alien_img = pygame.Surface((40, 40))
alien_img.fill(RED)  # Small alien as red square
alien_rects = []

bullet_img = pygame.Surface((5, 10))
bullet_img.fill(WHITE)
bullets = []

# Game variables
player_speed = 5
bullet_speed = 7
alien_speed = 2
alien_direction = 1
score = 0
level = 1
enemies_per_level = 5
game_over = False

# Font
font = pygame.font.SysFont('Arial', 30)

def draw_score():
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def draw_level():
    level_text = font.render(f"Level: {level}", True, WHITE)
    screen.blit(level_text, (WIDTH - 150, 10))

def move_aliens():
    global alien_direction
    for alien_rect in alien_rects:
        alien_rect.x += alien_speed * alien_direction
        if alien_rect.right >= WIDTH or alien_rect.left <= 0:
            alien_direction *= -1
            for rect in alien_rects:
                rect.y += 20

def check_collision():
    global score
    for bullet in bullets[:]:
        for alien_rect in alien_rects[:]:
            if bullet.colliderect(alien_rect):
                score += 10
                bullets.remove(bullet)
                alien_rects.remove(alien_rect)
                break

def spawn_aliens():
    global alien_speed, enemies_per_level
    for x in range(100, 700, 60):
        for y in range(50, 200, 60):
            if len(alien_rects) < enemies_per_level:
                alien_rects.append(alien_img.get_rect(center=(x, y)))

def level_up():
    global level, alien_speed, enemies_per_level
    level += 1
    alien_speed += 1  # Increase speed of aliens as levels increase
    enemies_per_level += 2  # Add more enemies per level

def main():
    global player_rect, bullets, alien_rects, score, level, game_over, enemies_per_level
    run = True
    clock = pygame.time.Clock()

    # Initial spawn of aliens
    spawn_aliens()

    while run:
        screen.fill(BLACK)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_rect.left > 0:
            player_rect.x -= player_speed
        if keys[pygame.K_RIGHT] and player_rect.right < WIDTH:
            player_rect.x += player_speed
        if keys[pygame.K_SPACE]:
            bullet_rect = bullet_img.get_rect(center=player_rect.center)
            bullets.append(bullet_rect)

        # Move bullets
        for bullet in bullets[:]:
            bullet.y -= bullet_speed
            if bullet.bottom < 0:
                bullets.remove(bullet)

        # Move aliens
        move_aliens()

        # Collision detection
        check_collision()

        # Check for level up condition (all aliens defeated)
        if len(alien_rects) == 0:
            level_up()
            spawn_aliens()

        # Draw player (space ship) and aliens
        screen.blit(player_img, player_rect)
        for alien_rect in alien_rects:
            screen.blit(alien_img, alien_rect)
        for bullet in bullets:
            screen.blit(bullet_img, bullet)

        # Draw score and level
        draw_score()
        draw_level()

        # Check if game over (aliens reach the bottom)
        for alien_rect in alien_rects:
            if alien_rect.bottom >= HEIGHT:
                game_over = True
                break

        if game_over:
            game_over_text = font.render("GAME OVER", True, WHITE)
            screen.blit(game_over_text, (WIDTH // 3, HEIGHT // 2))
            pygame.display.flip()
            pygame.time.wait(2000)
            break

        # Update the display
        pygame.display.flip()

        # Frame rate
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
