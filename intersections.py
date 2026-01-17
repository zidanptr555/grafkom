import pygame
import os

pygame.init()

# =============================
# KONFIGURASI
# =============================
BASE_DIR = "images"
DIRECTIONS = ["right", "left", "up", "down"]

os.makedirs(BASE_DIR, exist_ok=True)
for d in DIRECTIONS:
    os.makedirs(f"{BASE_DIR}/{d}", exist_ok=True)

# =============================
# HELPER
# =============================
def draw_shadow(surf, rect):
    shadow = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.ellipse(shadow, (0, 0, 0, 60), shadow.get_rect())
    surf.blit(shadow, (rect.x, rect.y + 4))

def rotate(img, d):
    if d == "up":
        return img
    if d == "right":
        return pygame.transform.rotate(img, -90)
    if d == "down":
        return pygame.transform.rotate(img, 180)
    if d == "left":
        return pygame.transform.rotate(img, 90)


# =============================
# VEHICLE (TOP VIEW)
# =============================
def draw_car():
    s = pygame.Surface((34, 60), pygame.SRCALPHA)
    draw_shadow(s, pygame.Rect(6, 8, 22, 44))
    pygame.draw.rect(s, (180, 0, 0), (6, 6, 22, 48), border_radius=6)
    pygame.draw.rect(s, (220, 80, 80), (8, 12, 18, 18), border_radius=4)
    pygame.draw.rect(s, (180, 220, 255), (9, 14, 16, 10), border_radius=2)
    pygame.draw.circle(s, (255, 255, 120), (11, 8), 2)
    pygame.draw.circle(s, (255, 255, 120), (23, 8), 2)
    pygame.draw.circle(s, (255, 80, 80), (11, 52), 2)
    pygame.draw.circle(s, (255, 80, 80), (23, 52), 2)
    return s

def draw_bus():
    s = pygame.Surface((40, 90), pygame.SRCALPHA)
    draw_shadow(s, pygame.Rect(8, 10, 24, 70))
    pygame.draw.rect(s, (255, 170, 0), (6, 6, 28, 78), border_radius=6)
    for y in range(14, 70, 14):
        pygame.draw.rect(s, (190, 220, 255), (9, y, 22, 10), border_radius=2)
    return s

def draw_truck():
    s = pygame.Surface((42, 100), pygame.SRCALPHA)
    draw_shadow(s, pygame.Rect(10, 12, 22, 75))
    pygame.draw.rect(s, (90, 90, 90), (8, 8, 26, 24), border_radius=4)
    pygame.draw.rect(s, (150, 150, 150), (8, 32, 26, 50), border_radius=4)
    pygame.draw.rect(s, (170, 210, 255), (11, 12, 20, 10), border_radius=2)
    return s

def draw_bike():
    s = pygame.Surface((18, 40), pygame.SRCALPHA)
    draw_shadow(s, pygame.Rect(4, 8, 10, 24))
    pygame.draw.rect(s, (200, 0, 0), (6, 10, 6, 20), border_radius=3)
    pygame.draw.circle(s, (30, 30, 30), (9, 8), 4)
    pygame.draw.circle(s, (30, 30, 30), (9, 32), 4)
    return s

# =============================
# GENERATE ASSETS
# =============================
vehicles = {
    "car": draw_car(),
    "bus": draw_bus(),
    "truck": draw_truck(),
    "bike": draw_bike()
}

for name, img in vehicles.items():
    for d in DIRECTIONS:
        pygame.image.save(
            rotate(img, d),
            f"{BASE_DIR}/{d}/{name}.png"
        )

pygame.quit()
print("✅ Asset kendaraan TOP-DOWN berhasil dibuat (siap simulasi)")
