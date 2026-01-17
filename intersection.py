import pygame
import os
import random

pygame.init()

# ================= CANVAS =================
WIDTH, HEIGHT = 1400, 800   # SAMA DENGAN SEBELUMNYA
surface = pygame.Surface((WIDTH, HEIGHT))

# ================= COLORS =================
GRASS_1 = (70, 150, 70)
GRASS_2 = (60, 140, 60)
ROAD = (65, 65, 65)
SIDEWALK = (175, 175, 175)
WHITE = (245, 245, 245)

TREE_DARK = (30, 100, 40)
TREE_LIGHT = (40, 130, 60)
TREE_TRUNK = (90, 70, 50)

# ================= PARAMETERS =================
LANE_WIDTH = 60
LANE_COUNT = 4
ROAD_WIDTH = LANE_WIDTH * LANE_COUNT
SIDEWALK_WIDTH = 28

CENTER_X = WIDTH // 2 - 20
CENTER_Y = HEIGHT // 2

# ================= DRAW MAP =================

# Grass
TILE = 80
for x in range(0, WIDTH, TILE):
    for y in range(0, HEIGHT, TILE):
        color = GRASS_1 if (x//TILE + y//TILE) % 2 == 0 else GRASS_2
        pygame.draw.rect(surface, color, (x, y, TILE, TILE))

# Roads
pygame.draw.rect(
    surface, ROAD,
    (0, CENTER_Y - ROAD_WIDTH//2, WIDTH, ROAD_WIDTH)
)
pygame.draw.rect(
    surface, ROAD,
    (CENTER_X - ROAD_WIDTH//2, 0, ROAD_WIDTH, HEIGHT)
)

# Sidewalk
pygame.draw.rect(
    surface, SIDEWALK,
    (0, CENTER_Y - ROAD_WIDTH//2 - SIDEWALK_WIDTH,
     WIDTH, SIDEWALK_WIDTH)
)
pygame.draw.rect(
    surface, SIDEWALK,
    (0, CENTER_Y + ROAD_WIDTH//2,
     WIDTH, SIDEWALK_WIDTH)
)

pygame.draw.rect(
    surface, SIDEWALK,
    (CENTER_X - ROAD_WIDTH//2 - SIDEWALK_WIDTH, 0,
     SIDEWALK_WIDTH, HEIGHT)
)
pygame.draw.rect(
    surface, SIDEWALK,
    (CENTER_X + ROAD_WIDTH//2, 0,
     SIDEWALK_WIDTH, HEIGHT)
)

# Lane lines
for i in range(1, LANE_COUNT):
    offset = -ROAD_WIDTH//2 + i * LANE_WIDTH

    for x in range(0, WIDTH, 60):
        pygame.draw.rect(
            surface, WHITE,
            (x, CENTER_Y + offset - 2, 30, 4)
        )

    for y in range(0, HEIGHT, 60):
        pygame.draw.rect(
            surface, WHITE,
            (CENTER_X + offset - 2, y, 4, 30)
        )

# Center double line
gap = 6
pygame.draw.rect(surface, WHITE, (0, CENTER_Y - gap, WIDTH, 4))
pygame.draw.rect(surface, WHITE, (0, CENTER_Y + gap, WIDTH, 4))
pygame.draw.rect(surface, WHITE, (CENTER_X - gap, 0, 4, HEIGHT))
pygame.draw.rect(surface, WHITE, (CENTER_X + gap, 0, 4, HEIGHT))

# ================= TREES =================
def draw_tree(x, y, r):
    pygame.draw.circle(surface, TREE_DARK, (x, y), r)
    pygame.draw.circle(surface, TREE_LIGHT, (x - r//4, y - r//4), r - 6)
    pygame.draw.rect(surface, TREE_TRUNK, (x - 4, y + r - 4, 8, 10))

SAFE = ROAD_WIDTH//2 + SIDEWALK_WIDTH + 30

for _ in range(220):
    x = random.randint(20, WIDTH - 20)
    y = random.randint(20, HEIGHT - 20)
    if abs(x - CENTER_X) > SAFE and abs(y - CENTER_Y) > SAFE:
        draw_tree(x, y, random.randint(14, 22))

# ================= SAVE =================
os.makedirs("images", exist_ok=True)
pygame.image.save(surface, "images/intersection_4lane_1400x800.png")

pygame.quit()
print("✅ PNG 1400x800 berhasil dibuat")
