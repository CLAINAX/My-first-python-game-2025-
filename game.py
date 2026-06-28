import pygame
import input
import os, sys
from player import  Player
from player import sprites, Sprite, projectiles
from map import TileKind, Map
from camera import create_screen
from npc import NPC
from crown import Crown
import fight as combat
from menu import show_menu
from lore import intro_animation

music_state = None

# --- CONFIGURACIÓN PARA TESTEO ---
current_world = "world2"  # Cambia a "world2" para probar el Nivel 2 directamente
current_state = "world2"    # Pon "world" para saltarte el menú en las pruebas
# ---------------------------------

pygame.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(16)     # más canales
pygame.mixer.set_reserved(1)          # reserva 1 canal exclusivo
SFX_CH = pygame.mixer.Channel(0)

# Setup
#screen = create_screen(800, 600, "CROWNLESS")
screen = create_screen(1920, 1000, "CROWNLESS(test)")
color_bg = (0, 0, 0)
running = True
combat.init_swords()

pygame.joystick.init()
js = None
if pygame.joystick.get_count() > 0:
    js = pygame.joystick.Joystick(0)
    js.init()

# Sounds
sound_default = pygame.mixer.Sound("sounds/default.mp3")
sound_default.set_volume(1)
sound_battle = pygame.mixer.Sound("sounds/battle.mp3")
sound_battle.set_volume(1)
sound_attack = pygame.mixer.Sound("sounds/sword.ogg")
sound_attack.set_volume(5)

# Limpiamos las listas globales por seguridad antes de configurar los mundos
sprites.clear()
objects = []
npcs = []

# Proyectiles (Componentes persistentes del sistema de combate)
proj = [
    Sprite("ride/big_boy.png", 300, 0, None, None, True),
    Sprite("ride/box_fight.png", 130, 230, None, None, True)
]

tile_kilds = [
    TileKind("grass", "images/grass.png", True),
    TileKind("stone_floor", "images/stone.png", False),
    TileKind("stone_floor_2", "images/terre_2.png", False),
    TileKind("field", "images/cultivo.png", False),
    TileKind("water", "images/water.png", False),
    TileKind("wall_invisible", "images/transparent.png", True)
]
tile_kilds_2 = [
    TileKind("callejones", "images/stone.png", False),          ## 0 
    TileKind("cases", "images/floor_2.png", True),                ## 1 
    TileKind("avingudes", "images/terre_2.png", False),              ## 2 
    TileKind("edificis_alts", "images/floor_2.png", True),       ## 3 
    TileKind("edificis_alts", "images/floor_2.png", True),             ## 4 
    TileKind("places", "images/terre_2.png", False)               ## 5 - 
]


# GESTOR DE MUNDOS INICIALES antes del "while"

if current_world == "world1":
    map = Map("maps/start.map", tile_kilds, 32)
    player = Player("images/male_front.png", 2200, 430, joystick=js)
    
    objects = [
        # Bordes delimitantes del mundo
        Sprite("images/border.png", 2250, 0),
        Sprite("images/border.png", -20, 0),
        Sprite("images/border_2.png", -20, -20),
        Sprite("images/border_2.png", -20, 1390),
        
        # Casas
        Sprite("images/house_1.png", 1330, 240),
        Sprite("images/house_1.png", 1730, 240),
        Sprite("images/house_1.png", 1850, 240),
        Sprite("images/house_2.png", 1520, 190),
        Sprite("images/house_2.png", 1597, 190),
        Sprite("images/house_2.png", 2000, 190),
        Sprite("images/house_3.png", 1380, 400),
        Sprite("images/house_3.png", 1530, 400),
        Sprite("images/house_3.png", 1680, 400),
        
        
        # Varios Caminos e Iniciales
        Sprite("images/death.png", 300, 0),
        Sprite("images/leave.png", 1010, 290),
        Sprite("images/leave.png", 1000, 300),
        Sprite("images/leave.png", 1030, 320),
        Sprite("images/leave.png", 1025, 320),
        Sprite("images/tree.png", 1000, 200),
        Sprite("images/armory.png", 920, 10),
        Sprite("images/house4.png", 800, 200),
        Sprite("images/house4.png", 800, 440),
        Sprite("images/house4.png", 1200, 600),
        Sprite("images/house_5.png", 1200, 250),
        Sprite("images/house_5.png", 1200, 435),
        Sprite("images/fuente.png", 800, 1070),
        Sprite("images/table.png", 800, 1170),
        Sprite("images/chair.png", 810, 1150),
        Sprite("images/chair.png", 837, 1188),
        Sprite("images/chair.png", 810, 1148),
        Sprite("images/chair.png", 817, 1208),
        Sprite("images/tenda_1.png", 770, 1300),
        Sprite("images/foc.png", 750, 1170),
        Sprite("images/carro.png", 1000, 500),
        Sprite("images/carpes.png", 530, 830),
        Sprite("images/pancartes.png", 830, 830),
        Sprite("images/roof.png", 950, 1100),
        Sprite("images/roof_2.png", 950, 1100),
        Sprite("images/roof_2.png", 870, 1200),
        Sprite("images/fence_3.png", 469, 1090),

        # Muralla y Alrededores
        Sprite("images/muralla.png", -750, -400),
        Sprite("images/planta_1.png", 450, 700),
        Sprite("images/planta_1.png", 550, 700),
        Sprite("images/planta_1.png", 650, 700),
        Sprite("images/planta_1.png", 740, 700),
        Sprite("images/flag.png", 190, 657),
        Sprite("images/flag.png", 290, 440),
        Sprite("images/flag.png", 320, 570),
        Sprite("images/caseta.png", 190, 450),

        # NPC Bases Estáticas (Visuales)
        Sprite("npc/Female_1.png", 2000, 360),
        Sprite("npc/trash.png", 825, 1300),

        # Pous
        Sprite("images/pou.png", 710, 490),
        Sprite("images/pou.png", 570, 800)
    ]

    # Configuración de diálogos de NPCs del Mundo 1
    npc_test = NPC("npc/Female_1.png", 0, 0, use_e_key=False)  
    npc_test.set_lines([
        "Annie: Hi budy!",
        "You: Hi?",
        "Annie: Are you ok? I saw that you were swimming on that river",
        "You: Uh, yes, I whant to train",
        "Annie: In Dalqady's arrounds, we try to care of everybady. So, don't do it again!"
    ])

    npc_manolo = NPC("npc/Female_1.png", 2000, 360, use_e_key=False)  
    npc_manolo.set_lines([
        "Annie: Hi buddy!",
        "You: Hi?",
        "Annie: Are you ok? I saw that you were swimming on the river",
        "You: Uh... yes, I wanted to practice my swimming",
        "Annie: That river is full of trash. In Dalqady's surroundings, we care about everybody. So, don't do it again!",
        "Annie: It's dangerous!!!",
        "Annie: By the way, you don't seem from here. If you want to enter the city, I recommend you go to the square and then, take the left path."
    ])

    npc_trash = NPC("npc/trash.png", 825, 1300, use_e_key=False)  
    npc_trash.set_lines([
        "Rudi: Whats up boy!",
        "You: Hello",
        "Rudi: Are you looking for good stuff at low price?",
        "Rudi: Come in please, I have everything you need",
        "You: Not really, but thanks for the offer",
        "Rudi: Are you sure?",
        "You: I don't have money",
        "Rudi: Wow",
        "Rudi: Ok, let's make a deal: I'll give you an advice if you promise to come back and buy something",
        "You: Deal",
        "Rudi: So, I saw that you weren't running. Here, everybody runs to get to places. If you don't know how to do it, just press R or F2"
    ])

    npc_knight = NPC("npc/Soldier.png", 200, 570, use_e_key=False)  
    npc_knight.set_lines([
        "Knight Wido: Hold it right there, peasant. These gates don’t swing open for just anyone. Baron’s orders, you know…",
        "You: I need to get inside. Isn't this how it works?",
        "Knight Wido: Don't you know? Well, that’s unfortunate. The privilege to get inside the city comes at a cost",
        "You: What!",
        "Knight Wido: Hey! Easy, man!",
        "Knight Wido: If you talk to me this way, I'll hit you!",
        "you: Just try!"
    ])

    npcs = [npc_test, npc_manolo, npc_trash, npc_knight]
# (670)
elif current_world == "world2":
    map = Map("maps/level_2.map", tile_kilds_2, 32)
    player = Player("images/male_front.png", 1170, 650, joystick=js)
    
    # Marcadores limpios para poblar el Nivel 2 en tus pruebas futuras
    objects = [

    # Casas 
        Sprite("images/fence_6.png", 180, 0),

        Sprite("images/house9.png", 90, 450),
        Sprite("images/house9.png", 90, 700),

        Sprite("images/house5.png", -160, 550),
        Sprite("images/house5.png", -150, 550),
        Sprite("images/house5.png", -140, 550),
        Sprite("images/house5.png", -130, 550),
        Sprite("images/house5.png", -120, 550),
        Sprite("images/house5.png", -110, 550),
        Sprite("images/house5.png", -100, 550),

    #P ack
        Sprite("images/house0.png", 500, 450),
        Sprite("images/house2.png", 300, 450),
        Sprite("images/house3.png", 900, 410),
        Sprite("images/house8.png", 1100, 430),
        Sprite("images/house6.png", 1300, 450),
        Sprite("images/house7.png", 1500, 450),

    #Chunk
# ==========================================# ========================================================
    # CHUNK: DISTRITO URBANO MEDIEVAL DENSO (Caos Orgánico)
    # ========================================================
# ========================================================
    # MURO DENSO DE TEJADOS (CAMINS 700, 1700, 2200 ESBORRATS)
    # ========================================================

    # --- CAPA 1: Y = -90 ---
        Sprite("images/house10.png", 327, -90),
        Sprite("images/house0.png", 581, -90),
        Sprite("images/house0.png", 849, -90),
        Sprite("images/house2.png", 1121, -90),
        Sprite("images/house2.png", 1438, -90),
        Sprite("images/house10.png", 2011, -90),

    # --- CAPA 2: Y = -71 ---
        Sprite("images/house2.png", 183, -71),
        Sprite("images/house6.png", 457, -71),
        Sprite("images/house2.png", 1039, -71),
        Sprite("images/house6.png", 1361, -71),
        Sprite("images/house2.png", 1917, -71),

    # --- CAPA 3: Y = -52 ---
        Sprite("images/house0.png", 261, -52),
        Sprite("images/house0.png", 517, -52),
        Sprite("images/house6.png", 1083, -52),
        Sprite("images/house2.png", 1319, -52),
        Sprite("images/house0.png", 1891, -52),

    # --- CAPA 4: Y = -33 ---
        Sprite("images/house10.png", 327, -33),
        Sprite("images/house0.png", 581, -33),
        Sprite("images/house0.png", 849, -33),
        Sprite("images/house2.png", 1121, -33),
        Sprite("images/house2.png", 1438, -33),
        Sprite("images/house10.png", 2011, -33),

    # --- CAPA 5: Y = -14 ---
        Sprite("images/house2.png", 183, -14),
        Sprite("images/house6.png", 457, -14),
        Sprite("images/house2.png", 1039, -14),
        Sprite("images/house6.png", 1361, -14),
        Sprite("images/house2.png", 1917, -14),

    # --- CAPA 6: Y = 5 ---
        Sprite("images/house0.png", 261, 5),
        Sprite("images/house0.png", 517, 5),
        Sprite("images/house6.png", 1083, 5),
        Sprite("images/house2.png", 1319, 5),
        Sprite("images/house0.png", 1891, 5),

    # --- CAPA 7: Y = 24 ---
        Sprite("images/house10.png", 327, 24),
        Sprite("images/house0.png", 581, 24),
        Sprite("images/house0.png", 849, 24),
        Sprite("images/house2.png", 1121, 24),
        Sprite("images/house2.png", 1438, 24),
        Sprite("images/house10.png", 2011, 24),

    # --- CAPA 8: Y = 43 ---
        Sprite("images/house2.png", 183, 43),
        Sprite("images/house6.png", 457, 43),
        Sprite("images/house2.png", 1039, 43),
        Sprite("images/house6.png", 1361, 43),
        Sprite("images/house2.png", 1917, 43),

    # --- CAPA 9: Y = 62 ---
        Sprite("images/house0.png", 261, 62),
        Sprite("images/house0.png", 517, 62),
        Sprite("images/house6.png", 1083, 62),
        Sprite("images/house2.png", 1319, 62),
        Sprite("images/house0.png", 1891, 62),

    # --- CAPA 10: Y = 81 ---
        Sprite("images/house10.png", 327, 81),
        Sprite("images/house0.png", 581, 81),
        Sprite("images/house0.png", 849, 81),
        Sprite("images/house2.png", 1121, 81),
        Sprite("images/house2.png", 1438, 81),
        Sprite("images/house10.png", 2011, 81),

    # --- CAPA 11: Y = 100 ---
        Sprite("images/house2.png", 183, 100),
        Sprite("images/house6.png", 457, 100),
        Sprite("images/house2.png", 1039, 100),
        Sprite("images/house6.png", 1361, 100),
        Sprite("images/house2.png", 1917, 100),

    # --- CAPA 12: Y = 119 ---
        Sprite("images/house0.png", 261, 119),
        Sprite("images/house0.png", 517, 119),
        Sprite("images/house6.png", 1083, 119),
        Sprite("images/house2.png", 1319, 119),
        Sprite("images/house0.png", 1891, 119),

    # --- CAPA 13: Y = 138 ---
        Sprite("images/house10.png", 327, 138),
        Sprite("images/house0.png", 581, 138),
        Sprite("images/house0.png", 849, 138),
        Sprite("images/house2.png", 1121, 138),
        Sprite("images/house2.png", 1438, 138),
        Sprite("images/house10.png", 2011, 138),

    # --- CAPA 14: Y = 157 ---
        Sprite("images/house2.png", 183, 157),
        Sprite("images/house6.png", 457, 157),
        Sprite("images/house2.png", 1039, 157),
        Sprite("images/house6.png", 1361, 157),
        Sprite("images/house2.png", 1917, 157),

    # --- CAPA 15: Y = 176 ---
        Sprite("images/house0.png", 261, 176),
        Sprite("images/house0.png", 517, 176),
        Sprite("images/house6.png", 1083, 176),
        Sprite("images/house2.png", 1319, 176),
        Sprite("images/house0.png", 1891, 176),

    # --- CAPA 16: Y = 195 ---
        Sprite("images/house10.png", 327, 195),
        Sprite("images/house0.png", 581, 195),
        Sprite("images/house0.png", 849, 195),
        Sprite("images/house2.png", 1121, 195),
        Sprite("images/house2.png", 1438, 195),
        Sprite("images/house10.png", 2011, 195),

    # --- CAPA 17: Y = 214 ---
        Sprite("images/house2.png", 183, 214),
        Sprite("images/house6.png", 457, 214),
        Sprite("images/house2.png", 1039, 214),
        Sprite("images/house6.png", 1361, 214),
        Sprite("images/house2.png", 1917, 214),

    # --- CAPA 18: Y = 233 ---
        Sprite("images/house0.png", 261, 233),
        Sprite("images/house0.png", 517, 233),
        Sprite("images/house6.png", 1083, 233),
        Sprite("images/house2.png", 1319, 233),
        Sprite("images/house0.png", 1891, 233),

    # --- CAPA 19: Y = 252 ---
        Sprite("images/house10.png", 327, 252),
        Sprite("images/house0.png", 581, 252),
        Sprite("images/house0.png", 849, 252),
        Sprite("images/house2.png", 1121, 252),
        Sprite("images/house2.png", 1438, 252),
        Sprite("images/house10.png", 2011, 252),

    # --- CAPA 20: Y = 271 ---
        Sprite("images/house2.png", 183, 271),
        Sprite("images/house6.png", 457, 271),
        Sprite("images/house2.png", 1039, 271),
        Sprite("images/house6.png", 1361, 271),
        Sprite("images/house2.png", 1917, 271),

    # --- CAPA 21: Y = 290 ---
        Sprite("images/house0.png", 261, 290),
        Sprite("images/house0.png", 517, 290),
        Sprite("images/house6.png", 1083, 290),
        Sprite("images/house2.png", 1319, 290),
        Sprite("images/house0.png", 1891, 290),

    # --- CAPA 22: Y = 309 ---
        Sprite("images/house10.png", 327, 309),
        Sprite("images/house0.png", 581, 309),
        Sprite("images/house0.png", 849, 309),
        Sprite("images/house2.png", 1121, 309),
        Sprite("images/house2.png", 1438, 309),
        Sprite("images/house10.png", 2011, 309),

    # --- CAPA 23: Y = 328 ---
        Sprite("images/house2.png", 183, 328),
        Sprite("images/house6.png", 457, 328),
        Sprite("images/house2.png", 1039, 328),
        Sprite("images/house6.png", 1361, 328),
        Sprite("images/house2.png", 1917, 328),

    # --- CAPA 24: Y = 347 ---
        Sprite("images/house0.png", 261, 347),
        Sprite("images/house0.png", 517, 347),
        Sprite("images/house6.png", 1083, 347),
        Sprite("images/house2.png", 1319, 347),
        Sprite("images/house0.png", 1891, 347),

    # --- CAPA 25: Y = 366 ---
        Sprite("images/house10.png", 327, 366),
        Sprite("images/house0.png", 581, 366),
        Sprite("images/house0.png", 849, 366),
        Sprite("images/house2.png", 1121, 366),
        Sprite("images/house2.png", 1438, 366),
        Sprite("images/house10.png", 2011, 366),

    # --- CAPA 26: Y = 385 ---
        Sprite("images/house2.png", 183, 385),
        Sprite("images/house6.png", 457, 385),
        Sprite("images/house2.png", 1039, 385),
        Sprite("images/house6.png", 1361, 385),
        Sprite("images/house2.png", 1917, 385),

    # --- CAPA 27: Y = 404 ---
        Sprite("images/house0.png", 261, 404),
        Sprite("images/house0.png", 517, 404),
        Sprite("images/house6.png", 1083, 404),
        Sprite("images/house2.png", 1319, 404),
        Sprite("images/house0.png", 1891, 404),

    # --- CAPA 28: Y = 423 ---
        Sprite("images/house10.png", 327, 423),
        Sprite("images/house0.png", 581, 423),
        Sprite("images/house0.png", 849, 423),
        Sprite("images/house2.png", 1121, 423),
        Sprite("images/house2.png", 1438, 423),
        Sprite("images/house10.png", 2011, 423),

    # --- CAPA 29: Y = 442 ---
        Sprite("images/house2.png", 183, 442),
        Sprite("images/house6.png", 457, 442),
        Sprite("images/house2.png", 1039, 442),
        Sprite("images/house6.png", 1361, 442),
        Sprite("images/house2.png", 1917, 442),

    # --- CAPA 30: Y = 461 ---
        Sprite("images/house0.png", 261, 461),
        Sprite("images/house0.png", 517, 461),
        Sprite("images/house6.png", 1083, 461),
        Sprite("images/house2.png", 1319, 461),
        Sprite("images/house0.png", 1891, 461),


    #Correcting_bug based 
        #Sprite("images/house10.png", 450, 600),       
       # Sprite("images/house10.png", 700, 600),    
        #Sprite("images/house10.png", 1400, 600),

    #Extra sprintes 
        Sprite("images/house_121.png", 1832, 0), 
        Sprite("images/house_121.png", 1832, 110),   
        Sprite("images/house32.png", 1560, 30),
        Sprite("images/armory2.png", 1600, 300),

        Sprite("images/farola.png", 1850, 300),
        Sprite("images/pou.png", 1800, 220),
        Sprite("images/farola.png", 1845, 395),
        Sprite("images/farola.png", 1840, 480),
        Sprite("images/carro_2.png", 1650, 220),
        Sprite("images/house800.png", 2360, -15),
        Sprite("images/house800.png", 2360, 80),
        Sprite("images/house900.png", 2130, 10),
        Sprite("images/house8000.png", 2130, 320),
        Sprite("images/house9.png", 2400, 440),
        Sprite("images/house9.png", 2400, 700),

        Sprite("images/pou.png", 1830, 700),
        Sprite("images/pou.png", 1925, 700),
        Sprite("images/pou.png", 2025, 700),
        Sprite("images/pou.png", 2125, 700),
        Sprite("images/pou.png", 2225, 700),

        Sprite("images/carpes_2.png", 2190, 845),
        Sprite("images/carpes_3.png", 1890, 845),
        Sprite("images/carpes_3.png", 2190, 925),
        Sprite("images/carpes_2.png", 1890, 925),

        Sprite("images/tenda_dreta.png", 1840, 1070),
        Sprite("images/tenda_esquerra.png", 2190, 1050),
        Sprite("images/tenda_1.png", 1975, 1200),
        Sprite("images/tenda_1.png", 2079, 1200),
        
        Sprite("images/foc.png", 2020, 1130),
        Sprite("images/foc.png", 2140, 1056),
        Sprite("images/fuente.png", 2070, 1094),

        Sprite("images/farola.png", 1850, 970),
        Sprite("images/farola.png", 1853, 850),


        Sprite("images/flag.png", 2365, 310),
        Sprite("images/flag.png", 2425, 315),
        Sprite("images/flag.png", 2320, 297),

        Sprite("images/magatzem.png", 1506, 695),
        Sprite("images/magatzem.png", 1506, 795),
        Sprite("images/magatzem.png", 1506, 1095),
        Sprite("images/magatzem.png", 1506, 1195),
        Sprite("images/magatzem.png", 1506, 1295),
        Sprite("images/magatzem.png", 1506, 1395),


        Sprite("images/house_di.png", 1570, 700),
        Sprite("images/house_di.png", 1570, 865),
        Sprite("images/house_di.png", 1570, 1030),
        Sprite("images/house_did.png", 1570, 1195),
        Sprite("images/house_did.png", 1570, 1360),
        Sprite("images/house_dins.png", 1370, 695),
        Sprite("images/house3.png", 1350, 825),


        Sprite("images/tree.png", 1380, 1060),
        Sprite("images/tree.png", 1240, 1200),
        Sprite("images/fuente.png", 1307, 1150),

    # --- CAPA 30000: Y = 461 ---


        Sprite("images/house0.png", 261, 861),
        Sprite("images/house2.png", 400, 861),
        Sprite("images/house6.png", 457, 900),

        Sprite("images/house0.png", 200, 861),
        Sprite("images/house2.png", 340, 861),
        Sprite("images/house6.png", 180, 900),
        Sprite("images/house0.png", 261, 961),
        Sprite("images/house2.png", 400, 961),
        Sprite("images/house6.png", 457, 1000),

        Sprite("images/house0.png", 620, 1120),

        Sprite("images/house0.png", 200, 961),
        Sprite("images/house2.png", 340, 961),
        Sprite("images/house6.png", 180, 1000),
        Sprite("images/house0.png", 261, 1061),
        Sprite("images/house2.png", 400, 1061),
        Sprite("images/house6.png", 457, 1100),

        Sprite("images/house0.png", 200, 1061),
        Sprite("images/house2.png", 340, 1061),
        Sprite("images/house6.png", 180, 1100),

        Sprite("images/house0.png", 480, 1181),
        Sprite("images/house6.png", 620, 1181),
        Sprite("images/house0.png", 540, 1271),




        Sprite("images/house0.png", 261, 861),
        Sprite("images/house2.png", 400, 861),
        Sprite("images/house6.png", 457, 900),


        Sprite("images/taverna2.png", 610, 750),
        Sprite("images/taverna2.png", 610, 920),

        Sprite("images/taverna.png", 850, 700),
        Sprite("images/taverna.png", 850, 881),
        Sprite("images/taverna.png", 850, 1062),
        Sprite("images/taverna.png", 850, 1243),
        Sprite("images/taverna.png", 850, 1380),

        Sprite("images/magatzem.png", 500, 700),
        Sprite("images/magatzem.png", 400, 700),
        Sprite("images/magatzem.png", 300, 700),

        Sprite("images/magatzem2.png", 500, 800),
        Sprite("images/magatzem2.png", 400, 800),
        Sprite("images/magatzem2.png", 300, 800),
        Sprite("images/magatzem3.png", 230, 740),



        Sprite("images/carpes_2.png", 1290, 1480),
        Sprite("images/caseta.png", 1000, 1491),
        Sprite("images/caseta.png", 1110, 1491),
        Sprite("images/caseta.png", 1110, 1391),

        Sprite("images/corral.png", 1050, 1210),
        Sprite("images/planta_1.png", 1410, 1340),
        Sprite("images/flag.png", 1210, 1370),
        Sprite("images/farola.png", 1410, 1240),

        Sprite("images/table.png", 1150, 1060),
        Sprite("images/chair.png", 1165, 1040),

        Sprite("images/table.png", 1050, 960),
        Sprite("images/chair.png", 1065, 940),

        Sprite("images/table.png", 1180, 960),
        Sprite("images/chair.png", 1195, 940),

        Sprite("images/table.png", 1230, 1060),
        Sprite("images/chair.png", 1235, 1040),

        Sprite("images/table.png", 1230, 860),
        Sprite("images/chair.png", 1235, 840),


        Sprite("images/planta_1.png", 1070, 1060),
        Sprite("images/carro_2.png", 1070, 800),
        Sprite("images/carro_2.png", 1070, 700),
        Sprite("images/carro_3.png", 1100, 1095),

        Sprite("images/leave.png", 1600, 1600),
        Sprite("images/carro.png", 1800, 1250),

        Sprite("images/foc.png", 1870, 1450),
        Sprite("images/foc.png", 1840, 1420),
        Sprite("images/foc.png", 1910, 1440),
        Sprite("images/foc.png", 1910, 1490),
        Sprite("images/foc_2.png", 1910, 1545),


#muralla
        Sprite("images/muralla2.png", -100, -690),



    ]


    npc_guardia_2 = NPC("images/guard.png", 200, 670, use_e_key=False)  
    npc_guardia_2.set_lines([
        "Knight Leonardo: ¡Wow! Hold your horses your man!.",
        "Knight Leonardo: I saw you entering this area really decided.",
        "You: Yeah. You know that is said that who has a directo goal, achives it?.",
        "Knight Leonardo: Not too sure wether that is a thread or not but still, you can't pass. You need to have a recomedation letter.",
        "You: I don't have one. If you let me pass, I promise that I will pay you back when my task is acomplised.",
        "Knight Leonardo: You know what's funny of this talk?...",
        "Knight Leonardo: That it's going to end with your ass kicked!."
    ])
    npc_guardia_2.can_fight = True

    proj = [
        Sprite("ride/big_boy_2.png", 300, 0, None, None, True),
        Sprite("ride/box_fight.png", 130, 230, None, None, True)
    ]

    npc_ciudadano = NPC("images/foc_2.png", 1910, 1545, use_e_key=False)  
    npc_ciudadano.set_lines([
        "Ronaldinyo: Hey guy!.",
        "Ronaldinyo: Come over hear please! I beg you!.",
        "You: Why shoud I? I don't even know you.",
        "Ronaldinyo: If you come here, I sear that I will tel you something you don't know...",
        "You: Ok then.",
        "Ronaldinyo: Oh, thanks for it. It seems so pointless but...",
        "Ronaldinyo: You can't imagine how it feels to be near somebody since a long time... So theraphyst."
        "You: So..."
        "Ronaldinyo: Ho, yea. I forgot."
        "You: I will ki..."
        "Ronaldinyo: Chill men; I was joking."
        "Ronaldinyo: There are rumors that this new king didn't acces the power on a legal way but by killing the last one."
        "You: OH."
        "Ronaldinyo: Hey, don't cry. It's just a rumour okay?."
    ])
    npc_ciudadano.can_fight = False  
    
    ##################################################################################################
    npc_ciudadano2 = NPC("images/Female_1.png", 2330, 150, use_e_key=False)  
    npc_ciudadano2.set_lines([
        "Clara: Nice place to observe you know?.",
        "You: What is this street?.",
        "Clara: Well...",
        "Clara: Besides being a street, it's where you find job as a fighter and you can even gain real-time moley!.",
        "Clara: I am C tear. Do you whant to try it? I can arrange ev...",
        "You: No thanks. I can't loose time here.",
        "You: But...",
        "You: Thanks anyway.",
    ])
    npc_ciudadano2.can_fight = False  
    
    
    npc_ciudadano3 = NPC("images/su.png", 2030, 780, use_e_key=False)  
    npc_ciudadano3.set_lines([
        "Micha: Hi!.",
        "You: Hello.",
        "Micha: I'm taking water for my sick child.",
        "You: So sorry!.",
    ])
    npc_ciudadano3.can_fight = False  

 
    npc_ciudadano4 = NPC("images/priest.png", 1800, 150, use_e_key=False)  
    npc_ciudadano4.set_lines([
        "Alfonso: Bess you.",
        "You: Thanks?.",
        "Alfonso: For Luminou's sake, pray tomorrow please.",
        "You: I promise nothing.",
    ])
    npc_ciudadano4.can_fight = False  


    npc_ciudadano5 = NPC("images/shee.png", 1800, 1100, use_e_key=False)  
    npc_ciudadano5.set_lines([
        "Beeee!: I just got out of prison. If steve asks, can u say you haven't seen me please?.",
        "You: Sure buddy.",
    ])
    npc_ciudadano5.can_fight = False  


    npc_ciudadano6 = NPC("images/fine.png", 830, 1100, use_e_key=False)  
    npc_ciudadano6.set_lines([
        "Steve: Dude, have you seen a white sheep in the middle of some path?.",
        "You: Yes, it told me not to told you.",
        "Steve: Bless you dude!.",
    ])
    npc_ciudadano6.can_fight = False  

    npc_ciudadano7 = NPC("images/ok.png", 1170, 780, use_e_key=False)  
    npc_ciudadano7.set_lines([
        "Hugo: Kid, would you want some of my fresh fruit?.",
        "You: Is it free?.",
        "Steve: 50 rupees each!.",
        "You: Ehm... No thanks!.",
    ])

    npc_ciudadano8 = NPC("images/drunk.png", 830, 900, use_e_key=False)  
    npc_ciudadano8.set_lines([
        "RCEI: jdhadbowe bewdfjw ebsja bj!.",
        "You: Are you okey?.",
        "RCEI: ojnew.",
        "You: Are you drunk?!.",
    ])
    npc_ciudadano8.can_fight = False  
    npcs = [npc_guardia_2, npc_ciudadano, npc_ciudadano2, npc_ciudadano3, npc_ciudadano4, npc_ciudadano5, npc_ciudadano6, npc_ciudadano7, npc_ciudadano8]

crown = None

# Game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

        if current_state == "intro":
            intro_animation(screen)
            current_state = "world"
            continue  

        # Route events by state
        if current_state == "menu":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    current_state = "intro"
                elif event.key == pygame.K_ESCAPE:
                    running = False

            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button in (7, 9):      # START
                    current_state = "intro"
                elif event.button in (6, 8):    # BACK/SELECT
                    running = False
            continue

        # Not in menu: normal gameplay input tracking
        if event.type == pygame.KEYDOWN:
            input.keys_down.add(event.key)
        elif event.type == pygame.KEYUP:
            input.keys_down.discard(event.key)
        elif event.type == pygame.JOYBUTTONDOWN:
            pass

    if current_state == "menu":
        show_menu(screen)
        continue  
        
    elif combat.change_world == 1:
        sound_battle.stop()
        print("First level passed! Loading World 2...")
            
        # 1. Limpiamos por completo el mundo anterior
        sprites.clear()
        objects.clear()
        npcs.clear()
        pantalla.fill("black")
        # 2. Re-inyectamos los proyectiles y al jugador en la lista global de dibujado
        for p in proj:
            sprites.append(p)
        sprites.append(player)
            
        # 3. Cargamos el mapa real de destino
        map = Map("maps/level_2.map", tile_kilds_2, 32)
            
        # 4. Modificamos posición lógica real (Fijación correcta anti-bucles)
        player.x = 200  
        player.y = 300  
        player.update_rect()
            
        # 5. Listas listas para añadir contenido propio del nivel 2 en caliente
        objects = []
        npcs = []
            
        # 6. Restablecemos banderas de combate y estado global del mapa
        combat.change_world = 0   
        combat.fight = False      
        crown = None              
            
        current_world = "world2"
        current_state = "world"   
        continue

    if combat.change_world == 0:
        if not combat.fight:
            # Update
            if music_state != "default":
                pygame.mixer.music.load("sounds/default.mp3")
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(-1)
                music_state = "default"

            player.update(objects)
            for npc in npcs:
                npc.update(player.rect, input.keys_down)

            # Draw
            screen.fill(color_bg)
            map.draw(screen)

            for s in sprites:
                s.draw(screen)

            for npc in npcs:
                npc.draw(screen)

        else:
            if music_state != "battle":
                pygame.mixer.music.load("sounds/battle.mp3")
                pygame.mixer.music.set_volume(0.1)
                pygame.mixer.music.play(-1)
                music_state = "battle"

            screen.fill("black")

            # 1. CARGAMOS AL JEFE SEGÚN EL MUNDO
            if crown is None:  # first frame of fight
                combat.start_fight()
                if current_world == "world1":
                    crown = Crown("ride/crown.png", 300, 400, joystick=js)
                elif current_world == "world2":
                    crown = Crown("images/guard.png", 300, 400, joystick=js)
                    # Vaciamos la cola normal para ignorar el patrón del Nivel 1
                    combat.sword_queue = []
                    combat.current_delay = 1500
                    combat.next_launch_time = pygame.time.get_ticks() + 1500

            # 2. MAGIA: GESTIÓN DE ESPADAS SEGÚN EL MUNDO
            if current_world == "world1":
                combat.update_swords(sound_attack, SFX_CH)
            elif current_world == "world2":
                import random
                current_time = pygame.time.get_ticks()
                
                # Crear espadas agobiantes infinitas
                if current_time >= combat.next_launch_time:
                    SFX_CH.play(sound_attack)
                    
                    x_start = random.choice([-50, 850])
                    y_start = random.randint(-50, 650)
                    t_x = random.randint(100, 700)
                    t_y = random.randint(100, 500)
                    
                    # Usa la clase Sword original, pero la creamos directamente aquí
                    # (Puedes cambiar "ride/sword_normal.png" por otra imagen si quieres otro obstáculo)
                    combat.swords.append(combat.Sword(x_start, y_start, t_x, t_y, speed=6))
                    
                    # Hacemos que cada vez dispare más rápido (agobiante)
                    combat.current_delay = max(100, combat.current_delay - 100)
                    combat.next_launch_time = current_time + combat.current_delay

                # Actualizar movimiento y borrar las que llegan al destino
                for s in combat.swords:
                    s.update()
                combat.swords[:] = [s for s in combat.swords if (abs(s.x - s.target_x) > 5 or abs(s.y - s.target_y) > 5)]

            # 3. DIBUJAR ESPADAS Y COMPROBAR DAÑO
            for sword in combat.swords:
                sword.draw(screen)
                
                offset_x = sword.rect.x - crown.rect.x
                offset_y = sword.rect.y - crown.rect.y
                if crown.mask.overlap(sword.mask, (offset_x, offset_y)):
                    crown.take_damage(1)

            crown.draw(screen)
            crown.update(proj)
            crown.draw_health_bar(screen)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                crown.take_damage(1)

            if crown.defeat:
                defeat_img = pygame.image.load("ride/defeat.png").convert()
                screen.blit(defeat_img, (0, 3))
                pygame.display.flip()
                pygame.time.delay(5000)
                combat.end_fight()
                pygame.quit()
                os.execl(sys.executable, sys.executable, *sys.argv)
           

            for p in proj:
                p.draw(screen)

    pygame.display.flip()
    pygame.time.delay(17)