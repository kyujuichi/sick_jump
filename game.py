import pygame
import random

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Stickman Jump")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Platforms
platforms = [pygame.Rect(random.randint(0, WIDTH - 60), i * 100, 60, 10) for i in range(6)]

# Stickman settings
initial_platform = platforms[0]
stickman = pygame.Rect(initial_platform.centerx - 15, initial_platform.top - 50, 30, 50)
velocity_y = 0
GRAVITY = 0.5
JUMP_STRENGTH = -20

# Bullets
bullets = []

# Monsters
monsters = [pygame.Rect(random.randint(0, WIDTH - 30), random.randint(-HEIGHT, 0), 30, 30) for _ in range(3)]

# Score
score = 0
high_score = 0
font = pygame.font.Font(None, 36)

def draw_stickman(surface, rect, high_score):
    if high_score >= 40:
        # Draw the word  "stickman "
        text = font.render("stickman", True, BLACK)
        surface.blit(text, (rect.centerx - text.get_width() // 2, rect.top))
    else:
        # Draw head
        pygame.draw.circle(surface, BLACK, (rect.centerx, rect.top + 10), 10)
        # Draw body
        pygame.draw.line(surface, BLACK, (rect.centerx, rect.top + 20), (rect.centerx, rect.bottom - 10), 2)
        # Draw arms
        pygame.draw.line(surface, BLACK, (rect.centerx, rect.top + 30), (rect.centerx - 15, rect.top + 20), 2)
        pygame.draw.line(surface, BLACK, (rect.centerx, rect.top + 30), (rect.centerx + 15, rect.top + 20), 2)
        # Draw legs
        pygame.draw.line(surface, BLACK, (rect.centerx, rect.bottom - 10), (rect.centerx - 10, rect.bottom), 2)
        pygame.draw.line(surface, BLACK, (rect.centerx, rect.bottom - 10), (rect.centerx + 10, rect.bottom), 2)

def draw_gradient(surface, color1, color2):
    for y in range(HEIGHT):
        color = (
            color1[0] + (color2[0] - color1[0]) * y // HEIGHT,
            color1[1] + (color2[1] - color1[1]) * y // HEIGHT,
            color1[2] + (color2[2] - color1[2]) * y // HEIGHT
        )
        pygame.draw.line(surface, color, (0, y), (WIDTH, y))

# Game loop
running = True
clock = pygame.time.Clock()
while running:
    if high_score >= 40:
        draw_gradient(screen, RED, YELLOW)
    else:
        draw_gradient(screen, BLUE, WHITE)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet = pygame.Rect(stickman.centerx - 5, stickman.top, 10, 20)
                bullets.append(bullet)
    
    # Stickman movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        stickman.x -= 5
    if keys[pygame.K_RIGHT]:
        stickman.x += 5
    
    # Apply gravity
    velocity_y += GRAVITY
    stickman.y += velocity_y
    
    # Check collision with platforms
    for platform in platforms:
        if stickman.colliderect(platform) and velocity_y > 0:
            velocity_y = JUMP_STRENGTH
            score += 1
            if score > high_score:
                high_score = score
    
    # Move bullets
    for bullet in bullets:
        bullet.y -= 10
        if bullet.y < 0:
            bullets.remove(bullet)
    
    # Check collision with monsters
    for monster in monsters:
        if stickman.colliderect(monster):
            running = False
        for bullet in bullets:
            if bullet.colliderect(monster):
                bullets.remove(bullet)
                monsters.remove(monster)
                score += 5
                if score > high_score:
                    high_score = score
    
    # Scroll screen
    if stickman.y < HEIGHT // 2:
        for platform in platforms:
            platform.y += abs(velocity_y)
        for monster in monsters:
            monster.y += abs(velocity_y)
        stickman.y += abs(velocity_y)
    
    # Remove old platforms and add new ones
    platforms = [p for p in platforms if p.y < HEIGHT]
    while len(platforms) < 6:
        platforms.append(pygame.Rect(random.randint(0, WIDTH - 60), 0, 60, 10))
    
    # Remove old monsters and add new ones
    monsters = [m for m in monsters if m.y < HEIGHT]
    while len(monsters) < 3:
        monsters.append(pygame.Rect(random.randint(0, WIDTH - 30), random.randint(-HEIGHT, 0), 30, 30))
    
    # Draw platforms
    for platform in platforms:
        pygame.draw.rect(screen, GREEN, platform)
    
    # Draw bullets
    for bullet in bullets:
        pygame.draw.rect(screen, BLACK, bullet)
    
    # Draw monsters
    for monster in monsters:
        pygame.draw.circle(screen, BLACK, monster.center, 15)
    
    # Draw stickman
    draw_stickman(screen, stickman, high_score)
    
    # Draw score
    if high_score >= 40:
        score_text = font.render(f"Punktzahl: {score}", True, BLACK)
        high_score_text = font.render(f"Rekord: {high_score}", True, BLACK)
    else:
        score_text = font.render(f"Score: {score}", True, BLACK)
        high_score_text = font.render(f"High Score: {high_score}", True, BLACK)
    screen.blit(score_text, (10, 10))
    screen.blit(high_score_text, (10, 40))
    
    # Game over condition
    if stickman.y > HEIGHT:
        score = 0
        initial_platform = platforms[0]
        stickman = pygame.Rect(initial_platform.centerx - 15, initial_platform.top - 50, 30, 50)
        platforms = [pygame.Rect(random.randint(0, WIDTH - 60), i * 100, 60, 10) for i in range(6)]
        monsters = [pygame.Rect(random.randint(0, WIDTH - 30), random.randint(-HEIGHT, 0), 30, 30) for _ in range(3)]
        bullets = []
        velocity_y = 0
    
    # Update screen
    pygame.display.flip()
    clock.tick(30)
    
pygame.quit()