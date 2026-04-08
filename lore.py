import pygame, sys

def run_scene(screen, font, clock, bg_path, pic_path, lines,
              pic_size=(700, 400),
              advice_text="Press SPACE or START to continue || To exit, any other key    ",
              advice_color=(209, 182, 27), margin=(16, 12)):

    white = (255, 255, 255)

    # Carga y escala
    bg = pygame.image.load(bg_path).convert()
    bg = pygame.transform.smoothscale(bg, screen.get_size())

    pic = pygame.image.load(pic_path).convert()
    pic = pygame.transform.smoothscale(pic, pic_size)

    # Texto aviso
    advice_surf = font.render(advice_text, True, advice_color)

    text_index = 0
    pygame.event.clear()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    text_index += 1
                else:
                    return False  # cualquier otra tecla -> salir

            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button == 9:  # Botón específico del mando
                    text_index += 1
                else:
                    return False  # cualquier otro botón -> salir

        # ¿Se acabaron las líneas?
        if text_index >= len(lines):
            return True

        # Dibujado
        screen.blit(bg, (0, 0))
        screen.blit(pic, (50, 50))

        full_text = lines[text_index]

        # Renderizado multilínea
        max_width = screen.get_width() - 100
        words = full_text.split(" ")
        line = ""
        y_text = screen.get_height() - 140
        line_height = font.get_linesize()

        for word in words:
            test_line = line + word + " "
            if font.size(test_line)[0] <= max_width:
                line = test_line
            else:
                line_surface = font.render(line, True, white)
                line_rect = line_surface.get_rect(centerx=screen.get_width() // 2, y=y_text)
                screen.blit(line_surface, line_rect)
                y_text += line_height
                line = word + " "

        if line:
            line_surface = font.render(line, True, white)
            line_rect = line_surface.get_rect(centerx=screen.get_width() // 2, y=y_text)
            screen.blit(line_surface, line_rect)

        # Aviso
        w, h = screen.get_size()
        advice_rect = advice_surf.get_rect(bottomright=(w - margin[0], h - margin[1]))
        screen.blit(advice_surf, advice_rect)

        pygame.display.flip()
        clock.tick(60)



def intro_animation(screen):
    # Config común
    font = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()

    # Escena 1
    lines_1 = [
        "Since ancient times, Dalqady has excelled because of its honest kings.",
        "This strength spared the kingdom from corruption many times...",
        "until yesterday."
    ]
    finished = run_scene(screen, font, clock,
        bg_path="maps/bg.png",
        pic_path="maps/image.png",
        lines=lines_1
    )
    if not finished:
        return  # el jugador saltó

    # Escena 2
    lines_2 = [
        "King Leonardo, known for his intellect, died suddenly at the age of 20.",
        "There is no one, nor any doubt.",
        "The seven ministers whom the king trusted most",
        "say nothing out of fear."

    ]
    finished = run_scene(screen, font, clock,
        bg_path="maps/bg.png",
        pic_path="maps/scene_2.png",
        lines=lines_2
    )

    # Escena 3
    lines_3 = [
        "You wake up crownless, drenched, and unrecognized,",
        "by the city’s river.",
        "Before you can gather your thoughts, survival is already a battle.",
        "Shivering and wet, you realize you’ve never left the city’s edge.",
        "Desperate for answers, you head to the castle."

    ]
    finished = run_scene(screen, font, clock,
        bg_path="maps/bg.png",
        pic_path="maps/scene_3.png",
        lines=lines_3
    )

