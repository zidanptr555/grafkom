import pygame
import sys

# Inisialisasi pygame
pygame.init()

# Ukuran layar
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Mobil Pygame")

# Warna
WHITE = (255, 255, 255)

# Load aset PNG
car_img = pygame.image.load("assets/car.png")
road_img = pygame.image.load("assets/road.png")

# Resize gambar mobil
car_img = pygame.transform.scale(car_img, (60, 120))

# Posisi mobil
car_x = WIDTH // 2 - 30
car_y = HEIGHT - 150
speed = 5

clock = pygame.time.Clock()

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Input keyboard
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and car_x > 0:
        car_x -= speed
    if keys[pygame.K_RIGHT] and car_x < WIDTH - 60:
        car_x += speed

    # Gambar background
    screen.blit(road_img, (0, 0))

    # Gambar mobil
    screen.blit(car_img, (car_x, car_y))

    pygame.display.update()
    clock.tick(60)