import pygame
import sys
import random

# Inicializálás
pygame.init()

# Ablak beállításai
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

# Színek
WHITE = (255, 255, 255)
BLUE = (135, 206, 250)
GREEN = (0, 200, 0)
RED = (255, 0, 0)

# Madár beállításai
bird_x, bird_y = 50, 300
bird_radius = 15
bird_velocity = 0
gravity = 0.5
jump_height = -10

# Csövek beállításai
pipe_width = 70
pipe_gap = 150
pipe_velocity = 3
pipes = []

# Pontszám
score = 0
font = pygame.font.SysFont("Arial", 24)

# Cső létrehozása
def create_pipe():
    pipe_height = random.randint(100, 400)
    pipes.append([WIDTH, pipe_height])

# Játék vége
def game_over():
    text = font.render(f"Game Over! Score: {score}", True, RED)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
    pygame.display.update()
    pygame.time.delay(2000)
    pygame.quit()
    sys.exit()

# Fő ciklus
running = True
while running:
    screen.fill(BLUE)

    # Események figyelése
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bird_velocity = jump_height

    # Madár mozgása
    bird_velocity += gravity
    bird_y += bird_velocity

    # Csövek mozgatása
    if not pipes or pipes[-1][0] < WIDTH - 200:
        create_pipe()

    for pipe in pipes:
        pipe[0] -= pipe_velocity
        pygame.draw.rect(screen, GREEN, (pipe[0], 0, pipe_width, pipe[1]))
        pygame.draw.rect(screen, GREEN, (pipe[0], pipe[1] + pipe_gap, pipe_width, HEIGHT))

        # Pontszám növelése
        if pipe[0] + pipe_width == bird_x:
            score += 1

    # Csövek eltávolítása
    pipes = [pipe for pipe in pipes if pipe[0] + pipe_width > 0]

    # Madár megjelenítése
    pygame.draw.circle(screen, RED, (bird_x, bird_y), bird_radius)

    # Ütközésellenőrzés
    if bird_y - bird_radius < 0 or bird_y + bird_radius > HEIGHT:
        game_over()

    for pipe in pipes:
        if bird_x + bird_radius > pipe[0] and bird_x - bird_radius < pipe[0] + pipe_width:
            if bird_y - bird_radius < pipe[1] or bird_y + bird_radius > pipe[1] + pipe_gap:
                game_over()

    # Pontszám megjelenítése
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.update()
    clock.tick(30)
