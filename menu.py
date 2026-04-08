import pygame

def show_menu(screen):
    global current_state
    # Colores y fuentes
    screen.fill((0, 0, 0))
    font_title = pygame.font.Font(None, 80)
    font_opt = pygame.font.Font(None, 40)

    title = font_title.render("CROWNLESS", True, (255, 215, 0))
    start = font_opt.render("Press ENTER / START to Start", True, (200, 200, 200))
    quit_game = font_opt.render("Press ESC / SELECT to Quit", True, (200, 200, 200))
    crown_png = pygame.image.load("ride/crown.png").convert_alpha()
    crown_jpg = pygame.transform.smoothscale(crown_png, (160, 130))

    crown_rect = crown_jpg.get_rect(center=(400, 100))


    # Centrado básico
    screen.blit(crown_jpg, crown_rect)
    screen.blit(title, title.get_rect(center=(400, 200)))
    screen.blit(start, start.get_rect(center=(400, 350)))
    screen.blit(quit_game, quit_game.get_rect(center=(400, 400)))

    pygame.display.flip()
