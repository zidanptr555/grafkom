import pygame, sys, random, math, threading, time

# ================= SETUP =================
pygame.init()
WIDTH, HEIGHT = 1400, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Traffic Intersection Simulation")
clock = pygame.time.Clock()


# ================= IMAGES =================
bg = pygame.image.load("images/intersection.png")

signals_img = {
    "red": pygame.image.load("images/signals/red.png"),
    "yellow": pygame.image.load("images/signals/yellow.png"),
    "green": pygame.image.load("images/signals/green.png")
}

# ================= SIGNAL CONFIG =================
GREEN = 12
YELLOW = 3

currentGreen = 0
currentYellow = False

signalPos = [
    (500,160),  # atas kiri
    (825,160),  # atas kanan
    (825,540),  # bawah kanan
    (500,540)   # bawah kiri
]

signalTimerPos = [
    (500,140),
    (825,140),
    (825,520),
    (500,520)
]
signalDir = ['right','down','left','up']

signals = []
for i in range(4):
    signals.append({"green":GREEN,"yellow":YELLOW,"red":0})

# Tambahkan timer untuk setiap sinyal
signalTimers = [GREEN, GREEN, GREEN, GREEN]

# ================= VEHICLE CONFIG =================
speeds = {'car':1.3,'bus':1.1,'truck':1.1,'bike':1.5}

startPos = {
    'right':(-120,370),
    'left':(WIDTH+120,450),
    'down':(720,-120),
    'up':(640,HEIGHT+120)
}

TURN_TRIGGER = 12   # jarak setelah stopline agar mulai belok

stopLine = {
    'right':535,
    'left':840,
    'down':285,
    'up':540
}

turnChance = 0.3
vehicles = pygame.sprite.Group()

# ================= VEHICLE CLASS =================
class Vehicle(pygame.sprite.Sprite):
    def __init__(self, vtype, direction):
        super().__init__()
        self.type = vtype
        self.direction = direction
        self.speed = speeds[vtype]

        self.image_original = pygame.image.load(
            f"images/{direction}/{vtype}.png"
        )
        self.image = self.image_original
        self.rect = self.image.get_rect(center=startPos[direction])
        self.zoom_offset = 0

        self.crossed = False
        self.turned = False
        self.turn = random.random() < turnChance
        self.scale = 1.0
        self.angle = 0
        self.target_angle = 0
        self.rotating = False
        self.rotation_speed = 0.5 if direction != 'down' else 0.35
        self.passed_stopline = False
        self.next_direction = self.direction
        if self.direction == 'up':
            self.rotation_speed = 0.35


        

    def move(self):
        global currentGreen, currentYellow

        # ===== COLLISION DETECTION =====
        # Cek jika ada kendaraan lain di depan
        collision = False
        SAFE = 18

        for other in vehicles:
            if other == self:
                continue

            if self.direction != other.direction:
                continue

            if self.direction == 'right':
                if 0 < other.rect.left - self.rect.right < SAFE:
                    collision = True

            elif self.direction == 'left':
                if 0 < self.rect.left - other.rect.right < SAFE:
                    collision = True

            elif self.direction == 'down':
                if 0 < other.rect.top - self.rect.bottom < SAFE:
                    collision = True

            elif self.direction == 'up':
                if 0 < self.rect.top - other.rect.bottom < SAFE:
                    collision = True

            

                    # ===== FORCE CROSSED AFTER STOPLINE (FIX DOWN ISSUE) =====
            if not self.crossed:
                if self.direction == 'down' and self.rect.top > stopLine['down'] + TURN_TRIGGER:
                    self.crossed = True
                elif self.direction == 'right' and self.rect.left > stopLine['right'] + TURN_TRIGGER:
                    self.crossed = True
                elif self.direction == 'up' and self.rect.bottom < stopLine['up'] - TURN_TRIGGER:
                    self.crossed = True
                elif self.direction == 'left' and self.rect.right < stopLine['left'] - TURN_TRIGGER:
                    self.crossed = True


            self.angle -= min(self.rotation_speed, abs(self.angle - self.target_angle))
            center = self.rect.center
            self.image = pygame.transform.rotate(self.image_original, self.angle)
            self.rect = self.image.get_rect(center=center)
        else:
            self.angle = self.target_angle
            self.rotating = False
            self.direction = self.next_direction

                    # ===== PASS STOPLINE (FINAL FIX) =====
            if not self.passed_stopline:
                if self.direction == 'right' and self.rect.left > stopLine['right']:
                    self.passed_stopline = True
                elif self.direction == 'left' and self.rect.right < stopLine['left']:
                    self.passed_stopline = True
                elif self.direction == 'down' and self.rect.top > stopLine['down']:
                    self.passed_stopline = True
                elif self.direction == 'up' and self.rect.bottom < stopLine['up']:
                    self.passed_stopline = True



        # ===== STOP LOGIC (FINAL REALISTIC FIX) =====
        stop = False

        if not self.passed_stopline:
            lampu_stop = (self.direction != signalDir[currentGreen])

            if lampu_stop:
                if self.direction == 'right':
                    if self.rect.centerx + self.rect.width//2 >= stopLine['right']:
                        stop = True

                elif self.direction == 'left':
                    if self.rect.centerx - self.rect.width//2 <= stopLine['left']:
                        stop = True

                elif self.direction == 'down':
                    if self.rect.centery + self.rect.height//2 >= stopLine['down']:
                        stop = True

                elif self.direction == 'up':
                    if self.rect.centery - self.rect.height//2 <= stopLine['up']:
                        stop = True


        if not stop and not collision:
            if self.direction == 'right': self.rect.x += self.speed
            if self.direction == 'left': self.rect.x -= self.speed
            if self.direction == 'down': self.rect.y += self.speed
            if self.direction == 'up': self.rect.y -= self.speed


        # ===== TURN =====
        # ===== TURN (SMOOTH) =====
        if self.crossed and self.turn and not self.turned and not self.rotating:
            self.rotating = True
            self.turned = True

            if self.direction == 'right':
                self.next_direction = 'down'
            elif self.direction == 'down':
                self.next_direction = 'left'
            elif self.direction == 'left':
                self.next_direction = 'up'
            elif self.direction == 'up':
                self.next_direction = 'right'

            self.target_angle = self.angle - 90

        # ===== ZOOM OUT (AMAN) =====
        if self.crossed:
            cx, cy = WIDTH // 2, HEIGHT // 2
            dist = math.hypot(self.rect.centerx - cx, self.rect.centery - cy)
            self.scale = max(0.65, 1 - dist / 1600)
        else:
            self.scale = 1.0


# ================= SIGNAL LOOP =================
def signalLoop():
    global currentGreen, currentYellow, signalTimers
    while True:
        # Green phase
        for t in range(GREEN, 0, -1):
            signalTimers[currentGreen] = t
            time.sleep(1)
        # Yellow phase
        currentYellow = True
        for t in range(YELLOW, 0, -1):
            signalTimers[currentGreen] = t
            time.sleep(1)
        currentYellow = False
        currentGreen = (currentGreen+1)%4
        # Set red for others
        for i in range(4):
            if i != currentGreen:
                signalTimers[i] = "---"  # Atau hitung red time jika perlu

# ================= VEHICLE GENERATOR =================
def spawnVehicles():
    while True:
        vtype = random.choice(['car','bus','truck','bike'])
        direction = random.choice(['right','left','up','down'])
        vehicles.add(Vehicle(vtype,direction))
        time.sleep(3)

threading.Thread(target=signalLoop,daemon=True).start()
threading.Thread(target=spawnVehicles,daemon=True).start()

# ================= MAIN LOOP =================
font = pygame.font.Font(None,28)

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.blit(bg,(0,0))

    # Draw signals and timers
    for i,pos in enumerate(signalPos):
        if i == currentGreen:
            img = signals_img["yellow"] if currentYellow else signals_img["green"]
        else:
            img = signals_img["red"]
        screen.blit(img,pos)
        # Tampilkan timer
        timer_text = font.render(str(signalTimers[i]), True, (255,255,255), (0,0,0))
        screen.blit(timer_text, signalTimerPos[i])

    for v in vehicles:
        v.move()
        img = pygame.transform.rotozoom(v.image_original, v.angle, v.scale)
        rect = img.get_rect(center=v.rect.center)
        screen.blit(img, rect)



    pygame.display.update()
    clock.tick(60)