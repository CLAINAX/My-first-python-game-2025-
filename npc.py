import pygame
from player import Sprite  # Asumiendo que Sprite está en player.py
import fight

class NPC(Sprite):
    # Añadimos width=32 y height=32 como valores por defecto
    def __init__(self, image_path, x, y, use_e_key=False, pad=10, width=32, height=32):
        # Se los pasamos a la clase Sprite para que cambie el tamaño de la imagen
        super().__init__(image_path, x, y, width=width, height=height)
        
        self.use_e_key = use_e_key
        self.pad = pad
        self.conversation_done = False

        # Key tracking para evitar repeticiones rápidas
        self._e_was_down = False
        self._a_was_down = False
        self._d_was_down = False
        self._space_was_down = False
        self._in_range = False

        # UI
        self.font = pygame.font.Font(None, 28)
        self.prompt_font = pygame.font.Font(None, 24)

        # Diálogo por defecto
        self.dialogue_lines = ["Annie: Hi, nice to meet you!"]

        # Estado del NPC
        self.talking = False
        self.current_line = 0
        self.type_index = 0
        self.char_delay_ms = 18
        self.last_char_time = 0
        
        # --- VARIABLES PARA ELEGIR (LUCHAR / IRSE) ---
        self.can_fight = False    
        self.force_fight = False  # Obliga a pelear directo sin menú
        self.choosing = False     
        self.choice_index = 0     # 0: Luchar, 1: Irse
        self.choosing_cooldown = 0 # Temporizador para evitar saltar el menú por accidente

    def set_lines(self, lines):
        self.dialogue_lines = lines

    def update(self, player_rect, keys_down):
        self.update_rect()
        
        # Distancia para saber si el jugador está cerca
        dx = self.rect.centerx - player_rect.centerx
        dy = self.rect.centery - player_rect.centery
        dist = (dx**2 + dy**2)**0.5
        self._in_range = dist <= 60

        # Manejo de teclas PULSADAS (solo cuentan 1 vez al bajarlas)
        e_down = pygame.K_e in keys_down
        e_pressed = e_down and not self._e_was_down
        self._e_was_down = e_down

        a_down = pygame.K_a in keys_down
        a_pressed = a_down and not self._a_was_down
        self._a_was_down = a_down

        d_down = pygame.K_d in keys_down
        d_pressed = d_down and not self._d_was_down
        self._d_was_down = d_down
        
        space_down = pygame.K_SPACE in keys_down
        space_pressed = space_down and not self._space_was_down
        self._space_was_down = space_down

        # ==========================================
        # MODO ELECCIÓN (Luchar o Irse)
        # ==========================================
        if self.choosing:
            if a_pressed:
                self.choice_index = 0  # Izquierda (Luchar)
            elif d_pressed:
                self.choice_index = 1  # Derecha (Irse)
                
            # Confirma la selección solo si ha pasado medio segundo (500 ms) 
            # para evitar que la pulsación del chat cierre esto accidentalmente.
            if e_pressed or space_pressed:
                if pygame.time.get_ticks() > self.choosing_cooldown:
                    self.choosing = False
                    self.conversation_done = True
                    if self.choice_index == 0:
                        fight.fight = True  # ¡Inicia el combate!
            return # Termina para no entrar al código de chat inferior

        # ==========================================
        # LÓGICA DE CONVERSACIÓN NORMAL
        # ==========================================
        if not self.conversation_done:
            if not self.talking:
                if self._in_range:
                    if not self.use_e_key or e_pressed:
                        self.talking = True
                        self.current_line = 0
                        self.type_index = 0
                        self.last_char_time = pygame.time.get_ticks()
            else:
                current_text = self.dialogue_lines[self.current_line]
                now = pygame.time.get_ticks()
                
                # Efecto máquina de escribir
                if self.type_index < len(current_text):
                    if now - self.last_char_time > self.char_delay_ms:
                        self.type_index += 1
                        self.last_char_time = now
                
                # Avanzar diálogo
                if e_pressed or space_pressed:
                    if self.type_index < len(current_text):
                        self.type_index = len(current_text) # Saltamos animación
                    else:
                        self.current_line += 1
                        self.type_index = 0
                        # ¿Se acabó el diálogo?
                        # ¿Se acabó el diálogo?
                        if self.current_line >= len(self.dialogue_lines):
                            self.talking = False
                            
                            # --- CAMBIO MÍNIMO: ¿Te obliga a luchar? ---
                            if self.force_fight:
                                fight.fight = True  # Inicia combate de golpe
                                self.conversation_done = True
                                
                            # Si no obliga, abre el menú normal (Jefe Nivel 2)
                            elif self.can_fight:
                                self.choosing = True
                                self.choice_index = 0 
                                self.choosing_cooldown = pygame.time.get_ticks() + 500 
                            else:
                                self.conversation_done = True

    def draw(self, surface):
        super().draw(surface)
        
        if self.talking:
            text = self.dialogue_lines[self.current_line][:self.type_index]
            self._draw_speech_bubble(surface, text)
            
        elif self.choosing:
            # Dibujamos las opciones de una manera clara y sin errores de espacio
            if self.choice_index == 0:
                texto_opciones = "Decide: [ > FIGHT < ]    o    [  Evaporate (leave)  ]\n(Use A / D to select and space for confirm)"
            else:
                texto_opciones = "Decide: [  Fight  ]    o    [ > Evaporate (leave) < ]\n(Use A / D to select and space for confirm)"
            
            
            self._draw_speech_bubble(surface, texto_opciones)
            
        elif self._in_range and not self.conversation_done and self.use_e_key:
            self._draw_e_prompt(surface)

    def _draw_e_prompt(self, surface):
        prompt = self.prompt_font.render("[E] Talk", True, (255, 255, 255))
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

        # Fondo y borde de la caja
        pygame.draw.rect(surface, (255, 255, 255), bubble, border_radius=10)
        pygame.draw.rect(surface, (0, 0, 0), bubble, width=2, border_radius=10)

        # Texto renderizado
        rendered = self._wrap_text(self.font, text, bubble_w - 24)
        y = bubble.y + 12
        for line in rendered:
            surface.blit(line, (bubble.x + 12, y))
            y += line.get_height() + 2

    @staticmethod
    def _wrap_text(font, text, max_width):
        if not text:
            return []
            
        # Separar por saltos de línea ("\n")
        manual_lines = text.split("\n")
        final_surfaces = []
        
        for manual_line in manual_lines:
            words = manual_line.split(" ")
            lines = []
            current_line = []
            
            for word in words:
                current_line.append(word)
                fw, fh = font.size(" ".join(current_line))
                if fw > max_width:
                    current_line.pop()
                    lines.append(" ".join(current_line))
                    current_line = [word]
                    
            if current_line:
                lines.append(" ".join(current_line))
                
            for string_line in lines:
                final_surfaces.append(font.render(string_line, True, (0, 0, 0)))
                
        return final_surfaces