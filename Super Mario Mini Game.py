import pygame
import sys
import random

pygame.init()

# Screen and name
WIDTH, HEIGHT = 1400, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Super Mario Mini Game")
clock = pygame.time.Clock()

# Load images
bg = pygame.image.load(r"mario-web\lvl1\bgd.jpg")
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

mario_img = pygame.image.load(r"mario-web\lvl1\classic_mario.jpeg")
mario_img = pygame.transform.scale(mario_img, (40, 60))

goomba_img = pygame.image.load(r"mario-web\lvl1\goomba.jpg")
goomba_img = pygame.transform.scale(goomba_img, (40, 40))

flag_img = pygame.image.load(r"mario-web\lvl1\flag.jpeg")
flag_img = pygame.transform.scale(flag_img, (20, 60))

# Load music and sound
pygame.mixer.music.load(r"mario-web\lvl1\mario_theme_song.mp3")
die_sound = pygame.mixer.Sound(r"mario-web\sounds\mario_loses_life.mp3")
win_sound = pygame.mixer.Sound(r"mario-web\sounds\level_complete.mp3")
game_over_sound = pygame.mixer.Sound(r"mario-web\sounds\game_over.mp3")
pygame.mixer.music.play(-1)

# Colors
GREEN = (50, 205, 50)
YELLOW = (255, 255, 0)
BROWN = (139, 69, 19)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#Level 1
def level_1():
    print("➡️ Level 1 Starting...")
    global coin_collected, lives

    # Player
    player = pygame.Rect(50, 400, 40, 60)
    player_x_vel = 0
    player_y_vel = 0
    gravity = 0.5
    jump_power = -10
    speed = 3
    on_ground = False

    coin_collected = 0
    lives = 3

    ground = pygame.Rect(0, 660, WIDTH, 40)

    platforms = [
        pygame.Rect(200, 550, 120, 20),
        pygame.Rect(400, 480, 120, 20),
        pygame.Rect(600, 420, 120, 20),
        pygame.Rect(800, 480, 120, 20),
        pygame.Rect(1000, 550, 120, 20)
    ]

    coins = [
        pygame.Rect(250, 510, 20, 20),
        pygame.Rect(460, 440, 20, 20),
        pygame.Rect(650, 380, 20, 20),
        pygame.Rect(850, 440, 20, 20),
        pygame.Rect(1050, 510, 20, 20)
    ]

    enemies = []
    enemy_dirs = []
    for i in range(3):
        enemy_x = random.randint(200, 1300)
        enemies.append(pygame.Rect(enemy_x, 620, 40, 40))
        enemy_dirs.append(1)

    goal = pygame.Rect(1300, 600, 20, 60)

    while True:
        screen.blit(bg, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x_vel = -speed
        elif keys[pygame.K_RIGHT]:
            player_x_vel = speed
        else:
            player_x_vel = 0
        if keys[pygame.K_SPACE] and on_ground:
            player_y_vel = jump_power
            on_ground = False

        player.x += player_x_vel
        player_y_vel += gravity
        player.y += player_y_vel

        #Prevent Mario from going off-screen
        if player.x < 0:
            player.x = 0
        elif player.x + player.width > WIDTH:
            player.x = WIDTH - player.width

        on_ground = False
        for plat in platforms + [ground]:
            if player.colliderect(plat) and player_y_vel >= 0:
                player.y = plat.y - player.height
                player_y_vel = 0
                on_ground = True

        for i, enemy in enumerate(enemies):
            enemy.x += enemy_dirs[i] * 2
            if enemy.x < 100 or enemy.x > 1300:
                enemy_dirs[i] *= -1

        for enemy in enemies:
            if player.colliderect(enemy):
                pygame.mixer.music.stop()
                die_sound.play()
                lives -= 1
                print(f"💥 Hit by enemy! Lives left: {lives}")
                pygame.time.delay(1500)
                if lives == 0:
                    game_over_sound.play()
                    screen.fill(BLACK)
                    font = pygame.font.SysFont(None, 80)
                    text = font.render("GAME OVER", True, YELLOW)

                    # Add restart prompt
                    font_small = pygame.font.SysFont(None, 36)
                    restart_text = font_small.render("Press R to restart", True, WHITE)

                    screen.blit(text, (WIDTH // 2 - 200, HEIGHT // 2 - 40))
                    screen.blit(restart_text, (WIDTH // 2 - 100, HEIGHT // 2 + 50))
                    pygame.display.flip()

                    waiting = True
                    while waiting:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_r:  # Checks both 'r' and 'R'
                                    waiting = False

                    # Restart the level
                    player.x, player.y = 50, 400  # Reset player position
                    player_y_vel = 0
                    coin_collected = 0
                    lives = 3
                    pygame.mixer.music.play(-1)
                    continue  # Skip rest of the loop and continue level
                else:
                    player.x, player.y = 50, 400
                    player_y_vel = 0
                    coin_collected = 0
                    pygame.mixer.music.play(-1)

        for coin in coins[:]:
            if player.colliderect(coin):
                coins.remove(coin)
                coin_collected += 1
                print(f"✨ Coins collected: {coin_collected}")

        if player.colliderect(goal):
            if len(coins) == 0:
                # Allow level completion only if all coins are collected
                pygame.mixer.music.stop()
                win_sound.play()
                print("🎉 Level Complete!")
                screen.fill((0, 0, 0))
                font = pygame.font.SysFont(None, 60)
                message = font.render("   Level 1 Complete!", True, YELLOW)
                screen.blit(message, (400, HEIGHT // 2 - 40))
                pygame.display.flip()
                pygame.time.delay(3000)
                # Move to next level (adjust as needed)
                level_2()  # For level 1, or level_3() for level 2
                return
            else:
                # Optional: Display a message if coins are still left
                font = pygame.font.SysFont(None, 40)
                message = font.render("Collect all coins first!", True, (255, 0, 0))
                screen.blit(message, (player.x - 50, player.y - 30))

        pygame.draw.rect(screen, GREEN, ground)
        for plat in platforms:
            pygame.draw.rect(screen, BROWN, plat)
        for coin in coins:
            pygame.draw.circle(screen, YELLOW, coin.center, 10)
        for enemy in enemies:
            screen.blit(goomba_img, enemy)
        screen.blit(flag_img, goal)
        screen.blit(mario_img, player)

        font = pygame.font.SysFont(None, 36)
        hud_text = font.render(f"Lives: {lives}    Coins: {coin_collected}", True, YELLOW)
        screen.blit(hud_text, (20, 20))

        pygame.display.flip()
        clock.tick(60)

#Level 2
def level_2():
    # Setup
    bg2 = pygame.image.load(r"mario-web\lvl2\bgd2.jpg")
    bg2 = pygame.transform.scale(bg2, (WIDTH, HEIGHT))

    pygame.mixer.music.load(r"mario-web\lvl2\underwater_theme.mp3")
    pygame.mixer.music.play(-1)

    blooper_img = pygame.image.load(r"mario-web\lvl2\blooper.jpg")
    blooper_img = pygame.transform.scale(blooper_img, (40, 40))

    fish_img = pygame.image.load(r"mario-web\lvl2\fish.jpg")
    fish_img = pygame.transform.scale(fish_img, (40, 40))

    flag_img2 = pygame.image.load(r"mario-web\lvl1\flag.jpeg")
    flag_img2 = pygame.transform.scale(flag_img2, (20, 60))

    player = pygame.Rect(50, 400, 40, 60)
    player_x_vel = 0
    player_y_vel = 0
    gravity = 0.2
    jump_power = -7  # 🔺 Higher jump
    speed = 2
    on_ground = False
    coin_collected = 0
    lives = 3

    ground = pygame.Rect(0, 660, WIDTH, 40)

    # 🔁 Easier platforms
    # Example: Creating multiple vertical spaced platforms
    platforms = [
        pygame.Rect(200, 500, 120, 20),
        pygame.Rect(400, 400, 120, 20),
        pygame.Rect(600, 300, 120, 20),
        pygame.Rect(800, 200, 120, 20),
        pygame.Rect(1000, 100, 120, 20)
    ]

    # 🔁 Moving platforms at start and end
    moving_platforms = [
        pygame.Rect(50, 520, 100, 20),     # start
        pygame.Rect(1100, 300, 100, 20),   # middle
        pygame.Rect(1250, 500, 100, 20),   # end
    ]
    moving_dirs = [1, -1, 1]

    coins = [
        pygame.Rect(245, 460, 20, 20),  # above platform 1
        pygame.Rect(445, 360, 20, 20),  # above platform 2
        pygame.Rect(645, 260, 20, 20),  # above platform 3
        pygame.Rect(845, 160, 20, 20),  # above platform 4
        pygame.Rect(1040, 60, 20, 20)
        # floating between moving platforms
    ]

    goal = pygame.Rect(1300, 600, 20, 60)

    bloopers = []
    blooper_dirs = []
    for i in range(4):
        blooper = pygame.Rect(500 + i * 300, 500, 40, 40)
        bloopers.append(blooper)
        blooper_dirs.append([random.choice([-1, 1]), random.choice([-1, 1])])

    fish_enemies = []
    fish_dirs = []
    for i in range(4):
        fish_enemy = pygame.Rect(600 + i * 300, 620, 40, 40)
        fish_enemies.append(fish_enemy)
        fish_dirs.append([random.choice([-1, 1]), random.choice([-1, 1])])

    while True:
        screen.blit(bg2, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x_vel = -speed
        elif keys[pygame.K_RIGHT]:
            player_x_vel = speed
        else:
            if player_x_vel > 0:
                player_x_vel -= 0.1
            elif player_x_vel < 0:
                player_x_vel += 0.1

        if keys[pygame.K_SPACE] and on_ground:
            player_y_vel = jump_power
            on_ground = False

        player.x += player_x_vel
        player_y_vel += gravity
        player.y += player_y_vel

        #Prevent Mario from going off-screen
        if player.x < 0:
            player.x = 0
        elif player.x + player.width > WIDTH:
            player.x = WIDTH - player.width

        on_ground = False
        for plat in platforms + moving_platforms + [ground]:
            if player.colliderect(plat) and player_y_vel >= 0:
                player.y = plat.y - player.height
                player_y_vel = 0
                on_ground = True

        # Move moving platforms
        for i, plat in enumerate(moving_platforms):
            plat.x += moving_dirs[i] * 2
            if plat.x < 20 or plat.x > WIDTH - 120:
                moving_dirs[i] *= -1

        # Move enemies
        for i, blooper in enumerate(bloopers):
            blooper.x += blooper_dirs[i][0] * 2
            blooper.y += blooper_dirs[i][1] * 2
            if blooper.x < 0 or blooper.x > WIDTH - 40:
                blooper_dirs[i][0] *= -1
            if blooper.y < 0 or blooper.y > HEIGHT - 40:
                blooper_dirs[i][1] *= -1

        for i, fish in enumerate(fish_enemies):
            fish.x += fish_dirs[i][0] * 2
            fish.y += fish_dirs[i][1] * 2
            if fish.x < 0 or fish.x > WIDTH - 40:
                fish_dirs[i][0] *= -1
            if fish.y < 0 or fish.y > HEIGHT - 40:
                fish_dirs[i][1] *= -1

        # Collision with enemies
        for enemy in fish_enemies + bloopers:
            if player.colliderect(enemy):
                pygame.mixer.music.stop()
                die_sound.play()
                lives -= 1
                pygame.time.delay(1500)
                if lives == 0:
                    game_over_sound.play()
                    screen.fill(BLACK)
                    font = pygame.font.SysFont(None, 80)
                    text = font.render("GAME OVER", True, YELLOW)
                    screen.blit(text, (WIDTH // 2 - 200, HEIGHT // 2 - 40))
                    pygame.display.flip()
                    pygame.time.delay(4000)
                    pygame.quit()
                    sys.exit()
                else:
                    player.x, player.y = 50, 400
                    player_y_vel = 0
                    coin_collected = 0
                    pygame.mixer.music.play(-1)

        for coin in coins[:]:
            if player.colliderect(coin):
                coins.remove(coin)
                coin_collected += 1
                print(f"✨ Coins collected: {coin_collected}")

        if player.colliderect(goal):
            if len(coins) == 0:
                # Allow level completion only if all coins are collected
                pygame.mixer.music.stop()
                win_sound.play()
                print("🎉 Level Complete!")
                screen.fill((0, 0, 0))
                font = pygame.font.SysFont(None, 60)
                message = font.render("            Level 2 Complete!", True, YELLOW)
                screen.blit(message, (400, HEIGHT // 2 - 40))
                pygame.display.flip()
                pygame.time.delay(3000)
                # Move to next level (adjust as needed)
                level_3()  # For level 1, or level_3() for level 2
                return
            else:
                # Optional: Display a message if coins are still left
                font = pygame.font.SysFont(None, 40)
                message = font.render("Collect all coins first!", True, (255, 0, 0))
                screen.blit(message, (player.x - 50, player.y - 30))

        # Draw
        pygame.draw.rect(screen, (50, 200, 50), ground)
        for plat in platforms:
            pygame.draw.rect(screen, (150, 100, 50), plat)
        for plat in moving_platforms:
            pygame.draw.rect(screen, (0, 150, 255), plat)
        for coin in coins:
            pygame.draw.circle(screen, YELLOW, coin.center, 10)
        for blooper in bloopers:
            screen.blit(blooper_img, blooper)
        for fish in fish_enemies:
            screen.blit(fish_img, fish)
        screen.blit(flag_img2, goal)
        screen.blit(mario_img, player)

        font = pygame.font.SysFont(None, 36)
        hud = font.render(f"Lives: {lives}    Coins: {coin_collected}", True, YELLOW)
        screen.blit(hud, (20, 20))

        pygame.display.flip()
        clock.tick(60)
def level_2():
    # Setup
    bg2 = pygame.image.load(r"mario-web\lvl2\bgd2.jpg")
    bg2 = pygame.transform.scale(bg2, (WIDTH, HEIGHT))

    pygame.mixer.music.load(r"mario-web\lvl2\underwater_theme.mp3")
    pygame.mixer.music.play(-1)

    blooper_img = pygame.image.load(r"mario-web\lvl2\blooper.jpg")
    blooper_img = pygame.transform.scale(blooper_img, (40, 40))

    fish_img = pygame.image.load(r"mario-web\lvl2\fish.jpg")
    fish_img = pygame.transform.scale(fish_img, (40, 40))

    flag_img2 = pygame.image.load(r"mario-web\lvl1\flag.jpeg")
    flag_img2 = pygame.transform.scale(flag_img2, (20, 60))

    player = pygame.Rect(50, 400, 40, 60)
    player_x_vel = 0
    player_y_vel = 0
    gravity = 0.2
    jump_power = -7  # 🔺 Higher jump
    speed = 2
    on_ground = False
    coin_collected = 0
    lives = 3

    ground = pygame.Rect(0, 660, WIDTH, 40)

    # 🔁 Easier platforms
    # Example: Creating multiple vertical spaced platforms
    platforms = [
        pygame.Rect(200, 500, 120, 20),
        pygame.Rect(400, 400, 120, 20),
        pygame.Rect(600, 300, 120, 20),
        pygame.Rect(800, 200, 120, 20),
        pygame.Rect(1000, 100, 120, 20)
    ]

    # 🔁 Moving platforms at start and end
    moving_platforms = [
        pygame.Rect(50, 520, 100, 20),     # start
        pygame.Rect(1100, 300, 100, 20),   # middle
        pygame.Rect(1250, 500, 100, 20),   # end
    ]
    moving_dirs = [1, -1, 1]

    coins = [
        pygame.Rect(245, 460, 20, 20),  # above platform 1
        pygame.Rect(445, 360, 20, 20),  # above platform 2
        pygame.Rect(645, 260, 20, 20),  # above platform 3
        pygame.Rect(845, 160, 20, 20),  # above platform 4
        pygame.Rect(1040, 60, 20, 20)
        # floating between moving platforms
    ]

    goal = pygame.Rect(1300, 600, 20, 60)

    bloopers = []
    blooper_dirs = []
    for i in range(4):
        blooper = pygame.Rect(500 + i * 300, 500, 40, 40)
        bloopers.append(blooper)
        blooper_dirs.append([random.choice([-1, 1]), random.choice([-1, 1])])

    fish_enemies = []
    fish_dirs = []
    for i in range(4):
        fish_enemy = pygame.Rect(600 + i * 300, 620, 40, 40)
        fish_enemies.append(fish_enemy)
        fish_dirs.append([random.choice([-1, 1]), random.choice([-1, 1])])

    while True:
        screen.blit(bg2, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x_vel = -speed
        elif keys[pygame.K_RIGHT]:
            player_x_vel = speed
        else:
            if player_x_vel > 0:
                player_x_vel -= 0.1
            elif player_x_vel < 0:
                player_x_vel += 0.1

        if keys[pygame.K_SPACE] and on_ground:
            player_y_vel = jump_power
            on_ground = False

        player.x += player_x_vel
        player_y_vel += gravity
        player.y += player_y_vel

        #Prevent Mario from going off-screen
        if player.x < 0:
            player.x = 0
        elif player.x + player.width > WIDTH:
            player.x = WIDTH - player.width

        on_ground = False
        for plat in platforms + moving_platforms + [ground]:
            if player.colliderect(plat) and player_y_vel >= 0:
                player.y = plat.y - player.height
                player_y_vel = 0
                on_ground = True

        # Move moving platforms
        for i, plat in enumerate(moving_platforms):
            plat.x += moving_dirs[i] * 2
            if plat.x < 20 or plat.x > WIDTH - 120:
                moving_dirs[i] *= -1

        # Move enemies
        for i, blooper in enumerate(bloopers):
            blooper.x += blooper_dirs[i][0] * 2
            blooper.y += blooper_dirs[i][1] * 2
            if blooper.x < 0 or blooper.x > WIDTH - 40:
                blooper_dirs[i][0] *= -1
            if blooper.y < 0 or blooper.y > HEIGHT - 40:
                blooper_dirs[i][1] *= -1

        for i, fish in enumerate(fish_enemies):
            fish.x += fish_dirs[i][0] * 2
            fish.y += fish_dirs[i][1] * 2
            if fish.x < 0 or fish.x > WIDTH - 40:
                fish_dirs[i][0] *= -1
            if fish.y < 0 or fish.y > HEIGHT - 40:
                fish_dirs[i][1] *= -1

        # Collision with enemies
        for enemy in fish_enemies + bloopers:
            if player.colliderect(enemy):
                pygame.mixer.music.stop()
                die_sound.play()
                lives -= 1
                pygame.time.delay(1500)
                if lives == 0:
                    game_over_sound.play()
                    screen.fill(BLACK)
                    font = pygame.font.SysFont(None, 80)
                    text = font.render("GAME OVER", True, YELLOW)

                    # Add restart prompt
                    font_small = pygame.font.SysFont(None, 36)
                    restart_text = font_small.render("Press R to restart", True, WHITE)

                    screen.blit(text, (WIDTH // 2 - 200, HEIGHT // 2 - 40))
                    screen.blit(restart_text, (WIDTH // 2 - 100, HEIGHT // 2 + 50))
                    pygame.display.flip()

                    waiting = True
                    while waiting:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_r:  # Checks both 'r' and 'R'
                                    waiting = False

                    # Restart the level
                    player.x, player.y = 50, 400  # Reset player position
                    player_y_vel = 0
                    coin_collected = 0
                    lives = 3
                    pygame.mixer.music.play(-1)
                    continue  # Skip rest of the loop and continue level

                else:
                    player.x, player.y = 50, 400
                    player_y_vel = 0
                    coin_collected = 0
                    pygame.mixer.music.play(-1)

        for coin in coins[:]:
            if player.colliderect(coin):
                coins.remove(coin)
                coin_collected += 1
                print(f"✨ Coins collected: {coin_collected}")

        if player.colliderect(goal):
            if len(coins) == 0:
                # Allow level completion only if all coins are collected
                pygame.mixer.music.stop()
                win_sound.play()
                print("🎉 Level Complete!")
                screen.fill((0, 0, 0))
                font = pygame.font.SysFont(None, 60)
                message = font.render("            Level 2 Complete!", True, YELLOW)
                screen.blit(message, (400, HEIGHT // 2 - 40))
                pygame.display.flip()
                pygame.time.delay(3000)
                # Move to next level (adjust as needed)
                level_3()  # For level 1, or level_3() for level 2
                return
            else:
                # Optional: Display a message if coins are still left
                font = pygame.font.SysFont(None, 40)
                message = font.render("Collect all coins first!", True, (255, 0, 0))
                screen.blit(message, (player.x - 50, player.y - 30))

        # Draw
        pygame.draw.rect(screen, (50, 200, 50), ground)
        for plat in platforms:
            pygame.draw.rect(screen, (150, 100, 50), plat)
        for plat in moving_platforms:
            pygame.draw.rect(screen, (0, 150, 255), plat)
        for coin in coins:
            pygame.draw.circle(screen, YELLOW, coin.center, 10)
        for blooper in bloopers:
            screen.blit(blooper_img, blooper)
        for fish in fish_enemies:
            screen.blit(fish_img, fish)
        screen.blit(flag_img2, goal)
        screen.blit(mario_img, player)

        font = pygame.font.SysFont(None, 36)
        hud = font.render(f"Lives: {lives}    Coins: {coin_collected}", True, YELLOW)
        screen.blit(hud, (20, 20))

        pygame.display.flip()
        clock.tick(60)


#Level 3
def level_3():
    print("Level 3 (Boss Battle) Starting...")

    bg3 = pygame.image.load(r"mario-web\lvl3\bgd3.jpg")
    bg3 = pygame.transform.scale(bg3, (WIDTH, HEIGHT))

    pygame.mixer.music.load(r"mario-web\lvl3\final_battle.mp3")
    pygame.mixer.music.play(-1)

    mario_img = pygame.image.load(r"mario-web\lvl1\classic_mario.jpeg")
    mario_img = pygame.transform.scale(mario_img, (40, 60))
    mario = pygame.Rect(50, 400, 40, 60)

    bowser_img = pygame.image.load(r"mario-web\lvl3\bowser.jpeg")
    bowser_img = pygame.transform.scale(bowser_img, (60, 80))
    bowser = pygame.Rect(1000, 395, 60, 80)

    princess_peach_img = pygame.image.load(r"mario-web\lvl3\princess_peach.jpg")
    princess_peach_img = pygame.transform.scale(princess_peach_img, (40, 40))

    toad_img = pygame.image.load(r"mario-web\lvl3\toad.jpg")
    toad_img = pygame.transform.scale(toad_img, (40, 40))

    star_img = pygame.image.load(r"mario-web\lvl3\star.jpg")
    star_img = pygame.transform.scale(star_img, (40, 40))

    red_mushroom_img = pygame.image.load(r"mario-web\lvl3\red_mushroom.jpg")
    red_mushroom_img = pygame.transform.scale(red_mushroom_img, (30, 30))

    blue_mushroom_img = pygame.image.load(r"mario-web\lvl3\blue_mushroom.jpg")
    blue_mushroom_img = pygame.transform.scale(blue_mushroom_img, (30, 30))

    green_mushroom_img = pygame.image.load(r"mario-web\lvl3\green_mushroom.jpg")
    green_mushroom_img = pygame.transform.scale(green_mushroom_img, (30, 30))

    flag_img3 = pygame.image.load(r"mario-web\lvl1\flag.jpeg")
    flag_img3 = pygame.transform.scale(flag_img3, (20, 60))

    win_sound = pygame.mixer.Sound(r"mario-web/lvl3/win.mp3")
    win_sound_played = False  # So it's played only once
    final_battle_music_playing = True  # Track if the battle music is still on
    game_won = False
    GROUND_Y = 400

    flag_rect = pygame.Rect(WIDTH - 100, GROUND_Y, 20, 60)
    flag_visible = False
    victory = False

    fired_powerup_keys = {"f": False, "w": False, "g": False, "s": False}

    mario_health = 500
    bowser_health = 600
    bowser_fire_timer = 0
    mario_coins = 0
    bowser_alive = True

    gravity = 0.5
    jump_power = -10
    mario_vel_y = 0
    speed = 3
    mario_speed = 5
    on_ground = False

    fireballs = []
    fireball_timer = 0
    fireball_delay = 90

    spike_img = pygame.Surface((20, 40))
    spike_img.fill((100, 100, 100))
    falling_spikes = []

    powerups = []  # now holds mushrooms and star
    mario_big = False
    mario_fire = False
    mario_water = False
    mario_star = False
    star_timer = 0

    fireballs_mario = []
    waterballs_mario = []

    mario_fireball_img = pygame.Surface((20, 10))
    mario_fireball_img.fill((255, 80, 0))

    mario_waterball_img = pygame.Surface((20, 10))
    mario_waterball_img.fill((0, 180, 255))

    congrats_font = pygame.font.SysFont('comicsans', 80)
    font_small = pygame.font.SysFont('comicsans', 24)
    instruction_font = pygame.font.SysFont('comicsans', 30)
    instructions = instruction_font.render("Press F (fire), W (water), G (heal), S (star) for power-ups!", True, (255, 255, 255))

    bowser_defeated = False
    victory_displayed = False

    bowser_dir = -2
    bowser_hit_back = False
    bowser_back_timer = 0

    screen.blit(bg3, (0, 0))
    screen.blit(instructions, (WIDTH // 2 - 300, 10))
    pygame.display.update()
    pygame.time.delay(2500)

    bowser_fireballs = []
    bowser_fireball_img = pygame.Surface((20, 10))
    bowser_fireball_img.fill((255, 100, 0))
    bowser_fireball_timer = 0

    bowser_invincible = False
    bowser_invincible_timer = 0
    bowser_invincible_cooldown = 500  # every ~8 seconds

    bowser_jump = False
    bowser_jump_timer = 0

    mario_shielded = False
    mario_shield_timer = 0

    DAMAGE_AMOUNT = 5 # both Mario and Bowser lose this amount per hit

    FIRE_DAMAGE = 3
    WATER_DAMAGE = 3

    flag_reached = False
    win_animation_started = False
    animation_timer = 0

    mario_fire_power = False
    fire_power_timer = 0

    mario_water_power = False
    water_power_timer = 0

    FIRE_WATER_DURATION = 50  # same duration as the shield (~5 seconds if 60 FPS)

    game_over = False

    mario_invincible = False
    mario_invincible_timer = 0

    while True:
        screen.blit(bg3, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            mario.x -= mario_speed
        elif keys[pygame.K_RIGHT]:
            mario.x += mario_speed
        if keys[pygame.K_UP] and on_ground:
            mario_vel_y = jump_power
            on_ground = False

        if keys[pygame.K_f] and not fired_powerup_keys["f"]:
            powerups.append({"type": "red", "rect": pygame.Rect(mario.x, 0, 30, 30)})
            fired_powerup_keys["f"] = True
        if not keys[pygame.K_f]:
            fired_powerup_keys["f"] = False

        if keys[pygame.K_w] and not fired_powerup_keys["w"]:
            powerups.append({"type": "blue", "rect": pygame.Rect(mario.x, 0, 30, 30)})
            fired_powerup_keys["w"] = True
        if not keys[pygame.K_w]:
            fired_powerup_keys["w"] = False

        if keys[pygame.K_g] and not fired_powerup_keys["g"]:
            powerups.append({"type": "green", "rect": pygame.Rect(mario.x, 0, 30, 30)})
            fired_powerup_keys["g"] = True
        if not keys[pygame.K_g]:
            fired_powerup_keys["g"] = False

        if keys[pygame.K_s] and not fired_powerup_keys["s"]:
            powerups.append({"type": "star", "rect": pygame.Rect(mario.x, 0, 30, 30)})
            fired_powerup_keys["s"] = True
        if not keys[pygame.K_s]:
            fired_powerup_keys["s"] = False

        mario_vel_y += gravity
        mario.y += mario_vel_y

        if mario.y >= GROUND_Y:
            mario.y = GROUND_Y
            mario_vel_y = 0
            on_ground = True

        if mario.x < 0:
            mario.x = 0
        elif mario.x + mario.width > WIDTH:
            mario.x = WIDTH - mario.width

        # Bowser moves toward Mario
        if not bowser_hit_back:
            if bowser.x > mario.x:
                bowser.x -= 2
            elif bowser.x < mario.x:
                bowser.x += 2

        # Bowser moves back temporarily after being hit
        if bowser_hit_back and bowser_alive:
            bowser.x += 6  # move back to the right
            bowser_back_timer += 1
            if bowser.x > 1200:
                bowser_hit_back = False
                bowser_back_timer = 0
        # Bowser attacks at intervals
        bowser_fireball_timer += 1
        if bowser_fireball_timer >= 120 and bowser_alive:
            bowser_fireball = pygame.Rect(bowser.left, bowser.centery, 20, 10)
            bowser_fireballs.append(bowser_fireball)
            bowser_fireball_timer = 0

        # Bowser becomes invincible occasionally
        if not bowser_invincible and bowser_alive:
            if random.randint(1, 500) == 1:
                bowser_invincible = True
                bowser_invincible_timer = 120  # 2 seconds of invincibility
        else:
            bowser_invincible_timer -= 1
            if bowser_invincible_timer <= 0:
                bowser_invincible = False

        # Bowser jump attack logic
        if not bowser_jump and random.randint(1, 400) == 1 and bowser_alive:
            bowser_jump = True
            bowser_jump_timer = 60  # 1 second in the air
            bowser.y -= 50  # simulate jump
        if bowser_jump and bowser_alive:
            bowser_jump_timer -= 1
            if bowser_jump_timer <= 0:
                bowser.y = GROUND_Y  # land back
                falling_spikes.append(pygame.Rect(bowser.centerx, 0, 20, 40))  # slam creates spike
                bowser_jump = False

        if random.randint(1, 70) == 1:
            spike_x = random.randint(100, 1200)
            falling_spikes.append(pygame.Rect(spike_x, 0, 20, 40))
        if bowser_alive:
            for spike in falling_spikes:
                spike.y += 7
                screen.blit(spike_img, (spike.x, spike.y))
            for spike in falling_spikes:
                if spike.colliderect(mario):
                    mario_health -= 7
                    falling_spikes.remove(spike)
            falling_spikes = [s for s in falling_spikes if s.top < HEIGHT]

        # Bowser shoots fireball if Mario is nearby
        bowser_fire_timer += 1
        if abs(bowser.x - mario.x) < 600 and bowser_fire_timer >= 120:
            bowser_fireball = pygame.Rect(bowser.x, bowser.y + 30, 25, 10)
            bowser_fireballs.append(bowser_fireball)
            bowser_fire_timer = 0

        new_powerups = []
        for p in powerups:
            p["rect"].y += 3
            screen.blit(
                {"red": red_mushroom_img, "blue": blue_mushroom_img,
                 "green": green_mushroom_img, "star": star_img}[p["type"]], p["rect"])

            if p["rect"].colliderect(mario):
                if p["type"] == "green":
                    mario_health = max(100, mario_health + 20)
                    mario_shielded = True
                    mario_shield_timer = 50  # Shield lasts 3 seconds (180 frames)
                    mario_invincible = True  # ✅ Set invincible ON
                    mario_invincible_timer = 60  # ✅ 1 second invincibility
                    mario_big = True
                    mario.width = 70
                    mario.height = 70
                    mario_img = pygame.transform.scale(pygame.image.load(r"mario-web\lvl1\classic_mario.jpeg"), (70, 70))
                elif p["type"] == "red":
                    mario_fire = True
                    mario_water = False
                    fire_power_timer = 0  # ⬅️ Reset fire timer
                elif p["type"] == "blue":
                    mario_water = True
                    mario_fire = False
                    water_power_timer = 0  # ⬅️ Reset water timer
                elif p["type"] == "star":
                    mario_star = True
                    star_timer = 50
                    mario.width = 90
                    mario.height = 100
                    mario_speed = 10
                    mario_img = pygame.transform.scale(pygame.image.load(r"mario-web\lvl1\classic_mario.jpeg"), (90, 100))
                # Do NOT add to new_powerups, since it collided
            else:
                new_powerups.append(p)

        powerups = new_powerups

        for p in powerups:
            if p["rect"].colliderect(mario):
                if p["type"] == "green":
                    mario_health = min(100, mario_health + 20)
                    mario_big = True
                    mario.width = 70
                    mario.height = 70
                    mario_img = pygame.transform.scale(mario_img, (70, 70))
                    if mario_invincible:
                        mario_invincible_timer -= 1
                        if mario_invincible_timer <= 0:
                            mario_invincible = False
                elif p["type"] == "red":
                    mario_fire = True
                    mario_water = False
                    fire_power_timer += 1
                    if fire_power_timer > FIRE_WATER_DURATION:
                        mario_fire_power = False
                elif p["type"] == "blue":
                    mario_water = True
                    mario_fire = False
                    water_power_timer += 1
                    if water_power_timer > FIRE_WATER_DURATION:
                        mario_water_power = False
                elif p["type"] == "star":
                    mario_star = True
                    star_timer = 50
                    mario.width = 90
                    mario.height = 100
                    mario_speed = 10
                    mario_img = pygame.transform.scale(mario_img, (90, 100))
                powerups.remove(p)

        if mario_star:
            star_timer -= 1
            if star_timer <= 0:
                mario_star = False
                mario_speed = 3
                mario_img = pygame.transform.scale(pygame.image.load(r"mario-web\lvl1\classic_mario.jpeg"), (40, 60))
                mario.width = 40
                mario.height = 60

        if mario_shielded:
            mario_shield_timer -= 1
            if mario_shield_timer <= 0:
                mario_shielded = False

        if mario_fire:
            fire_power_timer += 1
            if fire_power_timer > FIRE_WATER_DURATION:
                mario_fire = False

        if mario_water:
            water_power_timer += 1
            if water_power_timer > FIRE_WATER_DURATION:
                mario_water = False

        if mario_invincible:
            mario_invincible_timer -= 1
            if mario_invincible_timer <= 0:
                mario_invincible = False
                mario_big = False
                mario.width = 40
                mario.height = 60
                mario_img = pygame.transform.scale(pygame.image.load(r"mario-web\lvl1\classic_mario.jpeg"), (40, 60))

                #mario_img = pygame.transform.scale(mario_img, (50, 60))

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            mario.x -= mario_speed
        elif keys[pygame.K_RIGHT]:
            mario.x += mario_speed
        if keys[pygame.K_UP] and on_ground:
            mario_vel_y = jump_power
            on_ground = False

        # ✅ Fire/Water shooting based on power-up
        if keys[pygame.K_SPACE]:
            if not mario_star:  # Only allow shooting if not in star mode
                if mario_fire and fire_power_timer <= FIRE_WATER_DURATION:
                    fireballs_mario.append(pygame.Rect(mario.right, mario.centery, 20, 10))
                elif mario_water and water_power_timer <= FIRE_WATER_DURATION:
                    waterballs_mario.append(pygame.Rect(mario.right, mario.centery, 20, 10))

        for fb in fireballs_mario:
            fb.x += 10
            screen.blit(mario_fireball_img, fb)
        fireballs_mario = [fb for fb in fireballs_mario if fb.left < WIDTH]

        for wb in waterballs_mario:
            wb.x += 12
            screen.blit(mario_waterball_img, wb)
        waterballs_mario = [wb for wb in waterballs_mario if wb.left < WIDTH]

        for fb in fireballs_mario[:]:
            fb.x += 10
            screen.blit(mario_fireball_img, fb)
            if fb.colliderect(bowser) and not bowser_invincible:
                #bowser_health -= 5
                bowser_hit_back = True
                bowser_back_timer = 0
                fireballs_mario.remove(fb)
                bowser_health -= FIRE_DAMAGE

        for wb in waterballs_mario[:]:
            wb.x += 12
            screen.blit(mario_waterball_img, wb)
            if wb.colliderect(bowser) and not bowser_invincible:
                #bowser_health -= 5
                bowser_hit_back = True
                bowser_back_timer = 0
                waterballs_mario.remove(wb)
                bowser_health -= WATER_DAMAGE

        for bfb in bowser_fireballs[:]:
            bfb.x -= 8  # Bowser fireball moves left
            pygame.draw.rect(screen, (255, 100, 0), bfb)  # Orange fireball rectangle

            if bfb.colliderect(mario):
                if not mario_star:
                    if mario_shielded:
                        mario_health -= 2  # Small damage if shielded
                    else:
                        mario_health -= 5  # Normal damage
                bowser_fireballs.remove(bfb)

            elif bfb.right < 0:
                bowser_fireballs.remove(bfb)

        screen.blit(mario_img, mario)
        if bowser_alive:
            screen.blit(bowser_img, (bowser.x, bowser.y))

        if flag_visible:
            screen.blit(flag_img3, flag_rect)
            if mario.colliderect(flag_rect) and not victory:
                victory = True
                screen.fill((0, 0, 0))  # Black screen
                win_text = congrats_font.render(" Congratulations! Mario Wins! ", True, (255, 255, 0))
                screen.blit(win_text, (WIDTH // 2 - 350, HEIGHT // 2 - 50))
                pygame.display.update()
                pygame.time.delay(4000)
                return

        # Mario's health bar out of 500
        pygame.draw.rect(screen, (0, 0, 0), (50, 30, 500, 20))  # background border
        pygame.draw.rect(screen, (255, 0, 0), (50, 30, mario_health, 20))  # red fill based on current health
        screen.blit(font_small.render(f"Mario: {mario_health}/500", True, (255, 255, 255)), (50, 5))

        # Bowser's health bar out of 500
        pygame.draw.rect(screen, (0, 0, 0), (850, 30, 500, 20))  # background border
        pygame.draw.rect(screen, (255, 0, 0), (800, 30, bowser_health, 20))  # red fill
        screen.blit(font_small.render(f"Bowser: {bowser_health}/600", True, (255, 255, 255)), (850, 5))

        if game_over:
            screen.fill((0, 0, 0))  # Black background
            game_over_font = pygame.font.SysFont(None, 100)
            game_over_text = game_over_font.render("Game Over", True, (255, 0, 0))
            screen.blit(game_over_text, (WIDTH // 2 - 200, HEIGHT // 2 - 50))
            bowser_defeated = True
            pygame.display.update()
            continue  # Skip the rest of the game loop

        if mario_shielded:
            pygame.draw.rect(screen, (0, 255, 0), mario, 3)  # green outline

        # ✅ Bowser hits Mario — Mario loses a little energy
        if mario.colliderect(bowser):
            if not mario_star and not mario_shielded and not mario_invincible:
                mario_health -= 2  # Small amount of damage
                if mario_health < 0:
                    mario_health = 0

        if bowser_health <= 0 and not win_animation_started:
            bowser_health = 0
            bowser_alive = False  # Flag to indicate Bowser is gone
            falling_spikes.clear()  # Remove all spikes
            spike_active = False  # Stop new spikes
            mario_has_power = False  # Remove any power effect
            fireballs.clear()
            #bowser_attacks.clear()
            show_energy_bars = False  # New flag to hide energy bars
            win_animation_started = True
            animation_timer = 0
            mario_moving_to_flag = True  # Let Mario move to flag
            game_won = True
            game_over = False  # make sure it's not game over

            pygame.mixer.music.stop()
            pygame.mixer.music.load(r"mario-web\lvl3\win.mp3")
            pygame.mixer.music.play()

            screen.fill(BLACK)
            font = pygame.font.SysFont(None, 80)
            text = font.render("Level 3 Complete!", True, (255, 255, 0))
            screen.blit(text, (
                WIDTH // 2 - text.get_width() // 2,
                HEIGHT // 2 - text.get_height() // 2
            ))

            pygame.display.update()
            pygame.time.wait(3000)  # Wait for 3 seconds before anything else
            # Do not call pygame.quit() or sys.exit() here

        if bowser_alive and mario.colliderect(bowser):
            if not bowser_invincible:
                if mario_star:
                    # Mario is invincible – normal damage to Bowser
                    bowser_health -= 5
                elif mario_shielded:
                    # Mario is shielded – Bowser loses only minimal energy
                    bowser_health -= 3
                else:
                    # Normal collision – Bowser loses small energy
                    bowser_health -= 1
                bowser_hit_back = True
                bowser_back_timer = 0

        if bowser_defeated:
            screen.blit(star_img, (650, 200))
            screen.blit(princess_peach_img, (mario.x + 80, mario.y - 20))
            screen.blit(toad_img, (mario.x + 140, mario.y - 20))
            congrats_text = congrats_font.render(" Level 3 Complete!", True, (255, 215, 0))
            screen.blit(congrats_text, (WIDTH // 2 - 300, HEIGHT // 2 - 100))
            bowser_dir = 0
            mario_speed = 0
            mario_fire = False
            mario_water = False
            mario_star = False
            game_won = True
            game_over = False  # make sure it's not game over

            if not victory_displayed:
                pygame.mixer.music.stop()
                pygame.mixer.Sound(r"mario-web\sounds\game_over.mp3").play()
                victory_displayed = True

        if bowser_health <= 0 and not win_animation_started:
            win_animation_started = True
            game_won = True  # ✅ Add this line
            animation_timer = 0

        if not flag_reached:
            screen.blit(flag_img3, (1300, GROUND_Y - 60))  # Place flag at far end
            flag_rect = pygame.Rect(1300, GROUND_Y - 60, 20, 60)
            if mario.colliderect(flag_rect):
                flag_reached = True
                win_animation_started = True
                animation_timer = 0

        if not bowser_defeated:
            # Bowser movement, spike attacks, power-ups etc.
            if bowser.x > mario.x:
                bowser.x -= 2
            elif bowser.x < mario.x:
                bowser.x += 2

            # Bowser's attack logic here
            # Spikes, fireballs, health regeneration, etc.

        '''if mario_health <= 0:
            mario_health = 0
            screen.fill((0, 0, 0))
            game_over_text = congrats_font.render("Game Over - Bowser Wins!", True, (255, 0, 0))
            screen.blit(game_over_text, (WIDTH // 2 - 300, HEIGHT // 2 - 50))
            pygame.display.update()
            pygame.time.delay(3000)
            return'''

        if mario_health <= 0 and not bowser_defeated and not game_won:
            game_over_text = congrats_font.render("Game Over: Bowser Wins", True, (255, 0, 0))
            screen.blit(game_over_text, (WIDTH // 2 - 300, HEIGHT // 2 - 100))
            mario_speed = 0
            bowser_dir = 0
            if not victory_displayed:
                pygame.mixer.music.stop()
                pygame.mixer.Sound(r"mario-web\sounds\mario_loses_life.mp3").play()
                victory_displayed = True
            game_over = True  # ✅ Set only here

            # Add restart prompt
            font_small = pygame.font.SysFont(None, 36)
            restart_text = font_small.render("Press R to restart", True, (255, 255, 255))
            screen.blit(restart_text, (WIDTH // 2 - 100, HEIGHT // 2 + 50))
            pygame.display.flip()

            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:  # Checks both 'r' and 'R'
                            level_3()  # Restart the level
                            return

        # Bowser randomly regenerates a bit of health (e.g., once every 8 seconds)
        if random.randint(1, 480) == 1 and bowser_health < 150:
            bowser_health = min(150, bowser_health + 30)

        if win_animation_started:
            animation_timer += 1
            screen.fill((0, 0, 0))  # Black background

            # Step 1: Move Peach and Toad to center (frames 0–90)
            if animation_timer < 90:
                peach_x = WIDTH // 2 - 60 + (90 - animation_timer)
                toad_x = WIDTH // 2 + 20 - (90 - animation_timer)
                screen.blit(princess_peach_img, (peach_x, HEIGHT // 2 - 40))
                screen.blit(toad_img, (toad_x, HEIGHT // 2 - 40))

            # Step 2: Then bring Mario to center (frames 90–180)
            elif animation_timer < 180:
                mario_x = WIDTH // 2 - 20
                screen.blit(princess_peach_img, (WIDTH // 2 - 60, HEIGHT // 2 - 40))
                screen.blit(toad_img, (WIDTH // 2 + 20, HEIGHT // 2 - 40))
                screen.blit(mario_img, (mario_x, HEIGHT // 2 + 10))

            # Step 3: Hold characters for a few seconds, then remove them (frames 180–360)
            elif animation_timer < 360:
                congrats_text = congrats_font.render("Congratulations!", True, (255, 215, 0))
                screen.blit(congrats_text, (WIDTH // 2 - 300, HEIGHT // 2 - 50))
                screen.blit(princess_peach_img, (WIDTH // 2 - 60, HEIGHT // 2 - 40))
                screen.blit(toad_img, (WIDTH // 2 + 20, HEIGHT // 2 - 40))
                screen.blit(mario_img, (WIDTH // 2 - 20, HEIGHT // 2 + 5))

            # Step 4: Only show “Congratulations!” permanently after frame 360
            # Step 3: Show “Congratulations!”
            # Step 4: Only show “Congratulations!” permanently after frame 90
            else:
                if game_won:
                    # ✅ Stop final battle music once
                    if final_battle_music_playing:
                        pygame.mixer.music.stop()
                        final_battle_music_playing = False

                    # ✅ Play win sound only once
                    if not win_sound_played:
                        win_sound.play()
                        win_sound_played = True

                    # ✅ Show final congratulations text only
                    congrats_text = congrats_font.render("Congratulations!", True, (255, 215, 0))
                    screen.blit(congrats_text, (WIDTH // 2 - 300, HEIGHT // 2 - 50))

        pygame.display.update()
        clock.tick(60)

level_1()
