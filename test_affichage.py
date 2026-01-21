import pygame
import time

# Initialisation
pygame.init()
SCREEN_WIDTH = 64
SCREEN_HEIGHT = 32
SCALE = 10
screen = pygame.display.set_mode((SCREEN_WIDTH * SCALE, SCREEN_HEIGHT * SCALE))
pygame.display.set_caption("TEST AFFICHAGE CHIP-8")

# Créer un écran de test
display = [[0 for _ in range(32)] for _ in range(64)]

# Dessiner un rectangle
for x in range(20, 44):
    for y in range(10, 22):
        display[x][y] = 1

# Afficher
screen.fill((0, 0, 0))
for x in range(SCREEN_WIDTH):
    for y in range(SCREEN_HEIGHT):
        if display[x][y]:
            pygame.draw.rect(screen, (255, 255, 255),
                             (x * SCALE, y * SCALE, SCALE, SCALE))

pygame.display.flip()
print("✅ Fenêtre ouverte avec rectangle blanc")

# Attendre 5 secondes
time.sleep(5)
pygame.quit()
print("✅ Test terminé")
