import pygame
from input import is_key_pressed
from camera import camera
import math
defeat = False


# Sprites y caché
sprites = []
loaded = {}
location_x = [2, 3]
location_y = [3, 3]

def load_image(path):
    if path in loaded:
        return loaded[path]
    img = pygame.image.load(path).convert_alpha()
    loaded[path] = img
    return img

class Sprite:
    def __init__(self, image, x, y, width=None, height=None):
        # Imágenes para direcciones del jugador/NPC
        self.images = {
            "down": load_image("ride/crown.png"),
            "up": load_image("ride/crown.png"),
            "left": load_image("ride/crown.png"),
            "right": load_image("ride/crown.png")
        }
        self.facing = "down"
        self.image = self.images[self.facing]

        self.max_health = 100
        self.health = 100

        if image in loaded:
            self.image = loaded[image]
        else:
            img = pygame.image.load(image).convert_alpha()
            if width and height:
                img = pygame.transform.scale(img, (width, height))
            loaded[image] = img
            self.image = img

        self.mask = pygame.mask.from_surface(self.image)

        self.x = x
        self.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        sprites.append(self)

    def update_rect(self):
        self.rect.topleft = (self.x, self.y)

    def pixel_collides_with(self, other):
        offset_x = other.rect.x - self.rect.x
        offset_y = other.rect.y - self.rect.y
        return self.mask.overlap(other.mask, (offset_x, offset_y)) is not None

    def delete(self):
        if self in sprites:
            sprites.remove(self)

    def draw(self, screen):
        self.update_rect()
        screen.blit(self.image, (self.x, self.y))

class Crown(Sprite):
    def __init__(self, image, x, y, joystick=None):
        super().__init__(image, x, y)
        self.movement_speed = 1.2
        self.joystick = joystick  # ahora el mando está asociado al jugador
        self.defeat = False


    def set_joystick(self, joystick):
        """Permite cambiar o asignar el mando en caliente."""
        self.joystick = joystick

    def draw_health_bar(self, screen):
        bar_width = 800
        bar_height = 100
        x = 0
        y = 550



        # fondo rojo
        pygame.draw.rect(screen, (255, 0, 0), (x, y, bar_width, bar_height))
        # barra verde proporcional
        current_width = int(bar_width * (self.health / self.max_health))
        pygame.draw.rect(screen, (0, 255, 0), (x, y, current_width, bar_height))

    def take_damage(self, amount=10):
        self.health = max(0, self.health - amount)
        if self.health == 0:
            self.defeat = True

    def update(self, obstacles):
        # Guardamos posición anterior para colisiones
        location_x.append(self.x)
        location_y.append(self.y)

        old_list_x = location_x[-2]
        old_list_y = location_y[-2]

        move_x, move_y = 0, 0

        # ============================
        #   MOVIMIENTO WASD FUNCIONAL
        # ============================
        if is_key_pressed(pygame.K_w):
            move_y -= 1
            self.facing = "up"
        if is_key_pressed(pygame.K_s):
            move_y += 1
            self.facing = "down"
        if is_key_pressed(pygame.K_a):
            move_x -= 1
            self.facing = "left"
        if is_key_pressed(pygame.K_d):
            move_x += 1
            self.facing = "right"

        # Aplicar movimiento WASD si NO hay joystick moviéndose
        if (move_x != 0 or move_y != 0) and not (self.joystick and self.joystick.get_init()):
            # DASH con SHIFT
            keys = pygame.key.get_pressed()
            velocidad_wasd = self.movement_speed
            if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                velocidad_wasd *= 2

            self.x += move_x * velocidad_wasd
            self.y += move_y * velocidad_wasd

        # ============================
        #   Mando Mafiti GP100
        # ============================
        if self.joystick and self.joystick.get_init():
            ax = self.joystick.get_axis(0) if self.joystick.get_numaxes() > 0 else 0.0
            ay = self.joystick.get_axis(1) if self.joystick.get_numaxes() > 1 else 0.0

            DEADZONE = 0.25
            ax = 0 if abs(ax) < DEADZONE else ax
            ay = 0 if abs(ay) < DEADZONE else ay

            hx, hy = (0, 0)
            if self.joystick.get_numhats() > 0:
                hx, hy = self.joystick.get_hat(0)

            if ax != 0 or ay != 0 or hx != 0 or hy != 0:
                move_x = ax if ax != 0 else float(hx)
                move_y = ay if ay != 0 else float(-hy)

                # Facing
                if abs(move_y) > abs(move_x):
                    self.facing = "down" if move_y > 0 else "up"
                elif abs(move_x) > 0:
                    self.facing = "right" if move_x > 0 else "left"

            # Velocidad base
            velocidad_actual = self.movement_speed

            # Duplicar con botón 5
            if self.joystick.get_numbuttons() > 5 and self.joystick.get_button(5):
                velocidad_actual = self.movement_speed * 2

            # Aplicar movimiento del joystick
            self.x += move_x * velocidad_actual
            self.y += move_y * velocidad_actual

        # ============================
        #   Actualizar sprite
        # ============================
        self.image = self.images[self.facing]
        self.update_rect()

        # Colisiones
        for obstacle in obstacles:
            obstacle.update_rect()
            if self.pixel_collides_with(obstacle):
                self.x, self.y = old_list_x, old_list_y
                self.update_rect()
                break

            #Como usar una tecla


        # Actualizar sprite
        self.image = self.images[self.facing]
        self.update_rect()

        # Colisiones
        for obstacle in obstacles:
            obstacle.update_rect()
            if self.pixel_collides_with(obstacle):
                self.x, self.y = old_list_x, old_list_y
                self.update_rect()
                break

        # Cámara sigue al jugador

