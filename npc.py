# npc.py
import pygame
from player import Sprite  # assuming Sprite is defined in player.py
import fight

class NPC(Sprite):
    def __init__(self, image_path, x, y, use_e_key=False, pad=10):
        # Llamada al padre SOLO con lo que necesita
        super().__init__(image_path, x, y)

        self.use_e_key = use_e_key
        self.pad = pad
        self.conversation_done = False

        # Key tracking
        self._key_states = {}
        self._e_was_down = False
        self._x_was_down = False
        self._in_range = False

        # UI
        self.font = pygame.font.Font(None, 28)
        self.prompt_font = pygame.font.Font(None, 24)

        # Dialogue
        self.dialogue_lines = [
            "Annie: Hi, nice to meet you!",
            "You: Hi, nice to meet you too!",
            "Annie: Welcome to our village.",
            "You: Thanks! It’s beautiful."
        ]

        self.speaker_turns = ["npc", "player", "npc", "player"]

        self.talking = False
        self.current_line = 0
        self.type_index = 0
        self.char_delay_ms = 18
        self.last_char_time = 0

    def _key_was_down(self, key):
        return self._key_states.get(key, False)

    def _update_key_state(self, key):
        self._key_states[key] = key in self._keys_down

    def set_lines(self, lines):
        self.dialogue_lines = list(lines)

    def _talk_zone(self):
        zone = self.rect.inflate(self.pad, self.pad)
        zone.center = self.rect.center
        return zone

    def _start_talking(self):
        if self.conversation_done == False:
            self.talking = True
            self.current_line = 0
            self.type_index = 0
            self.last_char_time = pygame.time.get_ticks()

    def _advance_or_close(self, keys_down):
        # Detecta teclado y mando sin cambiar firma del método
        BUTTON_X = 0  # índice botón X en tu mando

        # Chequea si hay algún mando y si el botón está presionado
        pad_pressed = False
        if pygame.joystick.get_count() > 0:
            joy = pygame.joystick.Joystick(0)
            if joy.get_button(BUTTON_X):
                pad_pressed = True

        if self.current_line >= len(self.dialogue_lines):
            self.talking = False
            self.conversation_done = True
            return

        line_full = self.dialogue_lines[self.current_line]
        speaker = "player" if line_full.startswith("You:") else "npc"
        required_key = pygame.K_e if speaker == "npc" else pygame.K_c

        # Flanco de subida con teclado o con botón X
        if ((required_key in keys_down and not self._key_was_down(required_key))
            or (pad_pressed and not self._x_was_down)):

            if self.type_index < len(line_full):
                self.type_index = len(line_full)
            else:
                self.current_line += 1
                if self.current_line >= len(self.dialogue_lines):
                    self.talking = False
                    self.conversation_done = True
                    if line_full.startswith("you:"):
                        fight.fight = True
                else:
                    self.type_index = 0
                    self.last_char_time = pygame.time.get_ticks()

        # Actualiza estados
        self._update_key_state(required_key)
        self._x_was_down = pad_pressed

    def update(self, player_rect, keys_down):
        self._keys_down = keys_down
        self._in_range = self._talk_zone().colliderect(player_rect)

        # También detecta inicio de conversación con botón X
        BUTTON_X = 0
        pad_pressed = False
        if pygame.joystick.get_count() > 0:
            joy = pygame.joystick.Joystick(0)
            if joy.get_button(BUTTON_X):
                pad_pressed = True

        if self.use_e_key:
            e_down = pygame.K_e in keys_down
            if self._in_range and not self.talking and (
                (e_down and not self._e_was_down)
                or (pad_pressed and not self._x_was_down)
            ):
                self._start_talking()
            self._e_was_down = e_down
            self._x_was_down = pad_pressed
        else:
            if self._in_range and not self.talking:
                self._start_talking()
            if self.talking and not self._in_range:
                self.talking = False

        if self.talking:
            self._advance_or_close(keys_down)

        # typing effect
        if self.talking and self.current_line < len(self.dialogue_lines):
            line_full = self.dialogue_lines[self.current_line]
            now = pygame.time.get_ticks()
            if self.type_index < len(line_full) and now - self.last_char_time >= self.char_delay_ms:
                self.type_index += 1
                self.last_char_time = now

    def draw(self, screen):
        super().draw(screen)  # draw the NPC sprite

        if self.use_e_key and self._in_range and not self.talking:
            self._draw_prompt(screen, "Press E or X to talk")

        if self.talking:
            text = self.dialogue_lines[self.current_line][:self.type_index]
            self._draw_speech_bubble(screen, text)

            if self.type_index >= len(self.dialogue_lines[self.current_line]):
                speaker = "npc" if self.dialogue_lines[self.current_line].startswith("Annie:") else "player"
                prompt_text = "Press E/X to continue" if speaker == "npc" else "Press C/X to continue"
                self._draw_prompt(screen, prompt_text)

    def _draw_prompt(self, surface, text):
        prompt = self.prompt_font.render(text, True, (255, 255, 255))
        padding = 6
        bg = prompt.get_rect()
        bg.inflate_ip(padding * 2, padding * 2)
        bg.midbottom = (self.rect.centerx, self.rect.top - 8)
        bg.clamp_ip(surface.get_rect())
        pygame.draw.rect(surface, (0, 0, 0), bg, border_radius=6)
        surface.blit(prompt, (bg.x + padding, bg.y + padding))

    def _draw_speech_bubble(self, surface, text):
        screen_width, screen_height = surface.get_size()
        bubble_w, bubble_h = screen_width - 40, 100
        bubble = pygame.Rect(20, screen_height - bubble_h - 20, bubble_w, bubble_h)

        pygame.draw.rect(surface, (255, 255, 255), bubble, border_radius=10)
        pygame.draw.rect(surface, (0, 0, 0), bubble, width=2, border_radius=10)

        rendered = self._wrap_text(self.font, text, bubble_w - 24)
        y = bubble.y + 12
        for line in rendered:
            surface.blit(line, (bubble.x + 12, y))
            y += line.get_height() + 2

    @staticmethod
    def _wrap_text(font, text, max_width):
        if not text:
            return []
        words = text.split(" ")
        lines = []
        current = ""
        for w in words:
            test = (current + " " + w).strip()
            if font.size(test)[0] <= max_width or not current:
                current = test
            else:
                lines.append(font.render(current, True, (0, 0, 0)))
                current = w
        if current:
            lines.append(font.render(current, True, (0, 0, 0)))
        return lines
