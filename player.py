import pygame
from input import is_key_pressed
from camera import camera
import math

# Sprites y caché
sprites = []
projectiles = []
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
    def __init__(self, image, x, y, width=None, height=None, isProjectile=False):
        # Imágenes para direcciones del jugador/NPC
        self.images = {
            "down": load_image("images/Male s.png"),
            "up": load_image("images/Male w.png"),
            "left": load_image("images/Male a.png"),
            "right": load_image("images/Male d.png")
        }
        self.facing = "down"
        self.image = self.images[self.facing]

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
        self.isProjectile = isProjectile

        if not self.isProjectile:
            sprites.append(self)
        else:

            projectiles.append(self)

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
        if self.isProjectile:
            screen.blit(self.image, (self.x, self.y))
        else:
            screen.blit(self.image, (self.x - camera.x, self.y - camera.y))

class Player(Sprite):
    def __init__(self, image, x, y, joystick=None):
        super().__init__(image, x, y)
        self.movement_speed = 4
        self.joystick = joystick  # ahora el mando está asociado al jugador

    def set_joystick(self, joystick):
        """Permite cambiar o asignar el mando en caliente."""
        self.joystick = joystick

    def update(self, obstacles):
        # Guardamos posición anterior para colisiones
        location_x.append(self.x)
        location_y.append(self.y)

        old_list_x = location_x[-2]
        old_list_y = location_y[-2]

        move_x, move_y = 0, 0

        # Teclado WASD
        if is_key_pressed(pygame.K_w):
            move_y -= 3
            self.facing = "up"
        if is_key_pressed(pygame.K_s):
            move_y += 3
            self.facing = "down"
        if is_key_pressed(pygame.K_a):
            move_x -= 3
            self.facing = "left"
        if is_key_pressed(pygame.K_d):
            move_x += 3
            self.facing = "right"

        # Mando Mafiti GP100
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

            # Aplicar
            self.x += move_x * velocidad_actual
            self.y += move_y * velocidad_actual

        # -------------------------------
        #   AÑADIDO: Movimiento con WASD
        # -------------------------------
        keys = pygame.key.get_pressed()

        move_x = 0
        move_y = 0

        if keys[pygame.K_a]:
            move_x = -1
        if keys[pygame.K_d]:
            move_x = 1
        if keys[pygame.K_w]:
            move_y = -1
        if keys[pygame.K_s]:
            move_y = 1

        # Actualizar facing (solo si hay movimiento)
        if move_x != 0 or move_y != 0:
            if abs(move_y) > abs(move_x):
                self.facing = "down" if move_y > 0 else "up"
            else:
                self.facing = "right" if move_x > 0 else "left"

        # Aumentar velocidad con SHIFT (dash del teclado)
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            velocidad_wasd = self.movement_speed * 2
        else:
            velocidad_wasd = self.movement_speed

        # Aplicar velocidad WASD
        self.x += move_x * velocidad_wasd
        self.y += move_y * velocidad_wasd

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
        camera.x = self.x - camera.width / 2
        camera.y = self.y - camera.height / 2
