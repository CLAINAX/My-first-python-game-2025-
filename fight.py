import pygame
import random

# --- Estado Global ---
sword_queue = []
swords = []
next_launch_time = 0
fight = False
change_world = 0

# Variables de ritmo dinámicas
initial_delay = 4000
time_reduction = 300
min_delay = 300
current_delay = initial_delay

# 1 = Corona (Original), 2 = Guardia (Agobiante)
boss_type = 1 

class Sword:
    def __init__(self, x, y, target_x, target_y, speed=5, image_path=None):
        img_file = image_path or "ride/sword_normal.png"
        self.image = pygame.image.load(img_file).convert_alpha()
        self.x = x
        self.y = y
        self.target_x = target_x
        self.target_y = target_y
        self.speed = speed
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def update(self):
        if self.x < self.target_x: self.x += self.speed
        elif self.x > self.target_x: self.x -= self.speed
        if self.y < self.target_y: self.y += self.speed
        elif self.y > self.target_y: self.y -= self.speed
        self.rect.topleft = (self.x, self.y)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))


def init_swords():
    global swords, sword_queue, current_delay, next_launch_time
    swords.clear()
    sword_queue.clear()
    
    if boss_type == 1:
        # --- PERFIL 1: EL ORIGINAL QUE YA TENÍAS ---
        sword_queue = [
            Sword(850, 200, 300, 400, speed=5, image_path="ride/sword_normal.png"),
            Sword(-50, 500, 300, 400, speed=5, image_path="ride/sword_normal.png"),
            Sword(400, -50, 300, 400, speed=5, image_path="ride/sword_normal.png"),
            Sword(400, 850, 300, 400, speed=5, image_path="ride/sword_normal.png"),
        ]
        current_delay = 4000
    else:
        # --- PERFIL 2: EL NUEVO JEFE AGOBIANTE ---
        current_delay = 1500

    next_launch_time = pygame.time.get_ticks() + current_delay


def start_fight():
    global fight
    fight = True
    init_swords()

def end_fight():
    global fight
    fight = False
    sword_queue.clear()
    swords.clear()

def death():
    global swords, sword_queue
    swords = []
    sword_queue = []
    print("He, he, you died!")


def update_swords(sound_attack, sfx_channel):
    global next_launch_time, current_delay, fight, change_world

    if not fight:
        return

    current_time = pygame.time.get_ticks()

    if current_time >= next_launch_time:
        
        if boss_type == 1:
            # Lógica original: solo dispara si hay espadas en la cola
            if sword_queue:
                sfx_channel.play(sound_attack)
                swords.append(sword_queue.pop(0))
                current_delay = max(300, current_delay - 300)
                next_launch_time = current_time + current_delay
                
        elif boss_type == 2:
            # Lógica nueva: Espadas infinitas, aleatorias y rápidas
            sfx_channel.play(sound_attack)
            x_start = random.choice([-50, 850])
            y_start = random.randint(-50, 650)
            target_x = random.randint(100, 700)
            target_y = random.randint(100, 500)
            swords.append(Sword(x_start, y_start, target_x, target_y, speed=6, image_path="ride/sword_normal.png"))
            
            current_delay = max(100, current_delay - 100) # Se vuelve loco muy rápido
            next_launch_time = current_time + current_delay

    for s in swords:
        s.update()

    # Mantener solo espadas en movimiento
    swords[:] = [s for s in swords if (abs(s.x - s.target_x) > 5 or abs(s.y - s.target_y) > 5)]

    if change_world == 1:
        end_fight()