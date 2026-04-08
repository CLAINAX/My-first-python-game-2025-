import pygame

# --- Estado ---
sword_queue = []
swords = []
initial_delay = 4000
time_reduction = 300
min_delay = 300
next_launch_time = 0
current_delay = initial_delay
fight = False
change_world = 0


class Sword:
    def __init__(self, x, y, target_x, target_y, speed=5, image_path=None):
        img_file = image_path or "ride/sword_normal.png"
        self.image = pygame.image.load(img_file).convert_alpha()

        self.x = x
        self.y = y
        self.target_x = target_x
        self.target_y = target_y
        self.speed = speed

        # Pixel-perfect collision mask
        self.mask = pygame.mask.from_surface(self.image)

        # Rect for position + bounding box
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def update(self):
        # Move toward target
        if self.x < self.target_x:
            self.x += self.speed
        elif self.x > self.target_x:
            self.x -= self.speed
        if self.y < self.target_y:
            self.y += self.speed
        elif self.y > self.target_y:
            self.y -= self.speed

        # Keep rect synced
        self.rect.topleft = (self.x, self.y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


def init_swords():
    """Prepara espadas y reinicia tiempos/colas."""
    global sword_queue, swords, next_launch_time, current_delay
    sword_queue = [
        Sword(-800, 300, 1100, 300, image_path="ride/sword_normal.png"),
        Sword(-800, 200, 1100, 200, image_path="ride/sword_normal.png"),
        Sword(-800, 400, 1100, 400, image_path="ride/sword_normal.png"),
        Sword(-800, 300, 1100, 300, image_path="ride/sword_normal.png"),
        Sword(300, -700, 300, 800, image_path="ride/sword_not_normal.png"),
        Sword(400, -700, 400, 800, image_path="ride/sword_not_normal.png"),
        Sword(200, -700, 200, 800, image_path="ride/sword_not_normal.png"),
    ]
    swords.clear()
    current_delay = initial_delay
    next_launch_time = pygame.time.get_ticks() + current_delay


def start_fight():
    """Entrar en combate y reiniciar patrón."""
    global fight
    fight = True
    init_swords()


def end_fight():
    """Salir de combate y limpiar."""
    global fight
    fight = False
    sword_queue.clear()
    swords.clear()


def death():
    """Acciones al morir (ejemplo)."""
    global swords, sword_queue
    swords = []
    sword_queue = []
    print("He, he, you died!")


def update_swords(sound_attack, sfx_channel):
    """Lanza espadas con delay decreciente (solo si hay combate)."""
    global next_launch_time, current_delay, fight, change_world

    if not fight:
        return

    current_time = pygame.time.get_ticks()

    if sword_queue and current_time >= next_launch_time:
        # Paso 2: usar canal reservado para asegurar que suena
        sfx_channel.play(sound_attack)
        swords.append(sword_queue.pop(0))
        current_delay = max(min_delay, current_delay - time_reduction)
        next_launch_time = current_time + current_delay

    for s in swords:
        s.update()

    # Mantener solo espadas en movimiento
    swords[:] = [
        s for s in swords
        if (abs(s.x - s.target_x) > s.speed or abs(s.y - s.target_y) > s.speed)
    ]

    print("queue:", len(sword_queue), "actives:", len(swords))

    if not swords and not sword_queue:
        end_fight()
        change_world += 1

