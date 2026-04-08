import pygame

pygame.init()
pygame.joystick.init()
screen = pygame.display.set_mode((400, 200))
clock = pygame.time.Clock()

js = None
if pygame.joystick.get_count() > 0:
    js = pygame.joystick.Joystick(0)
    js.init()
    print("Nombre:", js.get_name())
    print("Ejes:", js.get_numaxes(), "Botones:", js.get_numbuttons(), "Hats:", js.get_numhats())
else:
    print("Sin gamepad")

running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        elif e.type == pygame.JOYAXISMOTION:
            print(f"AXIS {e.axis}: {e.value:.2f}")
        elif e.type == pygame.JOYBUTTONDOWN:
            print(f"BTN DOWN {e.button}")
        elif e.type == pygame.JOYBUTTONUP:
            print(f"BTN UP {e.button}")
        elif e.type == pygame.JOYHATMOTION:
            print(f"HAT {e.hat}: {e.value}")

    screen.fill((30,30,30))
    pygame.display.flip()
    clock.tick(60)
