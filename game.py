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
current_world = "world1"  # o un número si prefieres: 1, 2, etc.
current_state = "menu"



pygame.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(16)     # más canales
pygame.mixer.set_reserved(1)          # reserva 1 canal exclusivo
SFX_CH = pygame.mixer.Channel(0)



# Setup
screen = create_screen(800, 600, "CROWNLESS")
color_bg = (0, 0, 0)
running = True
combat.init_swords()

pygame.joystick.init()
js = None
if pygame.joystick.get_count() > 0:
    js = pygame.joystick.Joystick(0)
    js.init()





#Sounds


sound_default = pygame.mixer.Sound("sounds/default.mp3")
sound_default.set_volume(1)
sound_battle = pygame.mixer.Sound("sounds/battle.mp3")
sound_battle.set_volume(1)

sound_attack = pygame.mixer.Sound("sounds/sword.ogg")
sound_attack.set_volume(5)

#player = Player("images/male_front.png", 0, 480)
#Materials
house_1 = pygame.image.load("images/house_1.png")
house_2 = pygame.image.load("images/house_2.png")
house_3 = pygame.image.load("images/house_3.png")
fence = pygame.image.load("images/fence.png")
fence_2 = pygame.image.load("images/fence_2.png")
black = pygame.image.load("images/black.png")
lake_original = pygame.image.load("images/lake.png")
lake = pygame.transform.scale(lake_original, (250, 200))

player = Player("images/male_front.png", 2200, 430, joystick=js)






proj = [

    Sprite("ride/big_boy.png", 300, 0, None, None, True),
    Sprite("ride/box_fight.png",130 , 230, None, None, True)

]


objects = [
########################################How actualy you need to add materials


#Bordes delimitantes del mundo

Sprite("images/border.png", 2250, 0),
Sprite("images/border.png", -20, 0),
Sprite("images/border_2.png", -20, -20),
Sprite("images/border_2.png", -20, 1390),
# Print houses

Sprite("images/house_1.png", 1330, 240),
Sprite("images/house_1.png", 1730, 240),
Sprite("images/house_1.png", 1850, 240),
Sprite("images/house_2.png", 1520, 190),
Sprite("images/house_2.png", 1597, 190),
Sprite("images/house_2.png", 2000, 190),
Sprite("images/house_3.png", 1380, 400),
Sprite("images/house_3.png", 1530, 400),
Sprite("images/house_3.png", 1680, 400),




#Print lake
#Sprite("images/lake.png", 1830, 430)

#Print death
Sprite("images/death.png", 300, 0),

#Varis escena camins inicials
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


#Varis escena muralla
Sprite("images/muralla.png", -750, -400),
Sprite("images/planta_1.png", 450, 700),
Sprite("images/planta_1.png", 550, 700),
Sprite("images/planta_1.png", 650, 700),
Sprite("images/planta_1.png", 740, 700),
Sprite("images/flag.png", 190, 657),
Sprite("images/flag.png", 290, 440),
Sprite("images/flag.png", 320, 570),
Sprite("images/caseta.png", 190, 450),





#NPC's body
Sprite("npc/Female_1.png", 2000, 360),
Sprite("npc/trash.png", 825, 1300),

#Pous
Sprite("images/pou.png", 710, 490),
Sprite("images/pou.png", 570, 800)

#NPC



#Print borders
#Sprite("images/black.png", 1250, 500)
#Sprite("images/black.png", 0, -150)
#Sprite("images/black.png", 800, 200)
]
#Npc
npc_test = NPC("npc/Female_1.png", 0, 0, use_e_key=False)  # set True for E-to-talk
npc_test.set_lines(["Annie: Hi budy!",
            "You: Hi?",
            "Annie: Are you ok? I saw that you were swimming on that river",
            "You: Uh, yes, I whant to train",
            "Annie: In Dalqady's arrounds, we try to care of everybady. So, don't do it again!",])


npc_manolo = NPC("npc/Female_1.png", 2000, 360, use_e_key=False)  # set True for E-to-talk
npc_manolo.set_lines(["Annie: Hi buddy!",
            "You: Hi?",
            "Annie: Are you ok? I saw that you were swimming on the river",
            "You: Uh... yes, I wanted to practice my swimming",
            "Annie: That river is full of trash. In Dalqady's surroundings, we care about everybody. So, don't do it again!",
            "Annie: It's dangerous!!!",
            "Annie: By the way, you don't seem from here. If you want to enter the city, I recommend you go to the square and then, take the left path.",])



npc_trash = NPC("npc/trash.png", 825, 1300, use_e_key=False)  # set True for E-to-talk
npc_trash.set_lines(["Rudi: Whats up boy!",
            "You: Hello",
            "Rudi: Are you looking for good stuff at low price?",
            "Rudi: Come in please, I have everything you need",
            "You: Not really, but thanks for the offer",
            "Rudi: Are you sure?",
            "You: I don't have money",
            "Rudi: Wow",
            "Rudi: Ok, let's make a deal: I'll give you an advice if you promise to come back and buy something",
            "You: Deal",
            "Rudi: So, I saw that you weren't running. Here, everybody runs to get to places. If you don't know how to do it, just press R or F2",

                     ])

npc_knight = NPC("npc/Soldier.png", 200, 570, use_e_key=False)  # set True for E-to-talk
npc_knight.set_lines([
            "Knight Wido: Hold it right there, peasant. These gates don’t swing open for just anyone. Baron’s orders, you know…",
            "You: I need to get inside. Isn't this how it works?",
            "Knight Wido: Don't you know? Well, that’s unfortunate. The privilege to get inside the city comes at a cost",
            "You: What!",
            "Knight Wido: Hey! Easy, man!",
            "Knight Wido: If you talk to me this way, I'll hit you!",
            "you: Just try!",

                     ])


npcs = [npc_test, npc_manolo, npc_trash, npc_knight]


# Player placeholder

# Lake
screen.blit(lake, (620, 450))

screen.blit(black, (0, 500))
screen.blit(black, (0, -150))


#Invisible walls



tile_kilds = [
    TileKind("grass", "images/grass.png", True),
    TileKind("stone_floor", "images/stone.png", False),
    TileKind("stone_floor_2", "images/terre_2.png", False),
    TileKind("field", "images/cultivo.png", False),
    TileKind("water", "images/water.png", False),
    TileKind("wall_invisible", "images/transparent.png", True)
]
map = Map("maps/start.map", tile_kilds, 32)


crown = None
# Game loop

while running:
    print("Top of loop, current_state:", current_state)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

        if current_state == "intro":
            intro_animation(screen)
            current_state = "world"
            continue  # Evita que se ejecute el resto del juego durante la intro

        # Route events by state
        if current_state == "menu":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    current_state = "intro"
                elif event.key == pygame.K_ESCAPE:
                    running = False

            elif event.type == pygame.JOYBUTTONDOWN:
                # SDL mappings vary: START is often 7, sometimes 9
                if event.button in (7, 9):      # START
                    current_state = "intro"

                elif event.button in (6, 8):    # BACK/SELECT
                    running = False


            # Don't let menu events fall through into gameplay input
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
        continue  # evita que ejecute el resto del loop

    elif combat.change_world == 1:
        sound_battle.stop()
        screen.fill("yellow")
        print("Thanks for playing the demo, hope you had fun")
        pygame.display.flip()
        pygame.time.delay(17)
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

            # (mueve flip/delay fuera del bucle)
        else:
            if music_state != "battle":
                pygame.mixer.music.load("sounds/battle.mp3")
                pygame.mixer.music.set_volume(0.1)
                pygame.mixer.music.play(-1)
                music_state = "battle"

            screen.fill("black")

            if crown is None:  # first frame of fight
                combat.start_fight()
                crown = Crown("ride/crown.png", 300, 400, joystick=js)

            combat.update_swords(sound_attack, SFX_CH)

            for sword in combat.swords:
                sword.draw(screen)

            for sword in combat.swords:
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
                pygame.quit()  # close window, cleanup
                os.execl(sys.executable, sys.executable, *sys.argv)

            for p in proj:
                p.draw(screen)

    pygame.display.flip()
    pygame.time.delay(17)


