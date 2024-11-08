import pygame
import math
import time

# initialize Pygame
pygame.init()

# set up the display
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Simple Platform Game")

# colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# player settings
player_width, player_height = 40, 60
player_x, player_y = 200, screen_height - 40 - player_height
player_dx, player_dy = 0, 0
jumping = False

# floor settings
floor = pygame.Rect(0, screen_height - 20, screen_width, 20)

# platform settings
platforms = [
    pygame.Rect(100, screen_height - 80, 200, 20),
    pygame.Rect(350, screen_height - 150, 150, 20),
    pygame.Rect(550, screen_height - 220, 180, 20),
    pygame.Rect(200, screen_height - 300, 130, 20),
    pygame.Rect(400, screen_height - 380, 200, 20),
    pygame.Rect(100, screen_height - 450, 150, 20)
]

# coin settings
coin_radius = 10
coins = [
    pygame.Rect(120, screen_height - 110, coin_radius * 2, coin_radius * 2),
    pygame.Rect(370, screen_height - 180, coin_radius * 2, coin_radius * 2),
    pygame.Rect(580, screen_height - 250, coin_radius * 2, coin_radius * 2),
    pygame.Rect(230, screen_height - 330, coin_radius * 2, coin_radius * 2),
    pygame.Rect(420, screen_height - 410, coin_radius * 2, coin_radius * 2),
    pygame.Rect(150, screen_height - 480, coin_radius * 2, coin_radius * 2)
]
collected_coins = 0
collected_coins_times = [0] * len(coins)
respawn_delay = 4  # in seconds

# enemy settings
enemy_radius = 20
enemy_x, enemy_y = screen_width // 2, screen_height // 2
enemy_speed = 2

# game state
game_over = False

# score
score = 0

# game loop
running = True
clock = pygame.time.Clock()

while running:
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_dx = -5
                elif event.key == pygame.K_RIGHT:
                    player_dx = 5
                elif event.key == pygame.K_UP and not jumping:
                    jumping = True
                    player_dy = -10

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player_dx < 0:
                    player_dx = 0
                elif event.key == pygame.K_RIGHT and player_dx > 0:
                    player_dx = 0

    if not game_over:
        # update player position
        player_x += player_dx
        player_y += player_dy
        
        # apply gravity
        if player_y < screen_height - player_height - 10:
            player_dy += 0.5
        else:
            player_dy = 0
            jumping = False

        # collision detection with floor
        player = pygame.Rect(player_x, player_y, player_width, player_height)
        if player.colliderect(floor):
            game_over = True

        # collision detection with platforms
        for platform in platforms:
            if player.colliderect(platform):
                if player_dy > 0:
                    player_y = platform.y - player_height
                    player_dy = 0
                    jumping = False
                elif player_dy < 0:
                    player_y = platform.y + platform.height
                    player_dy = 0

        # update enemy position (follow player)
        dx = player_x - enemy_x
        dy = player_y - enemy_y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance != 0:
            enemy_dx = (dx / distance) * enemy_speed
            enemy_dy = (dy / distance) * enemy_speed
            enemy_x += enemy_dx
            enemy_y += enemy_dy

        # ensure the player stays within the screen boundaries
        if player_x < 0:
            player_x = 0
        elif player_x > screen_width - player_width:
            player_x = screen_width - player_width

        if player_y < 0:
            player_y = 0
        elif player_y > screen_height - player_height:
            player_y = screen_height - player_height

        # check for collision with enemy
        enemy = pygame.Rect(enemy_x - enemy_radius, enemy_y - enemy_radius, 2 * enemy_radius, 2 * enemy_radius)
        if player.colliderect(enemy):
            game_over = True

        # check for collision with coins
        for i, coin in enumerate(coins):
            if player.colliderect(coin) and time.time() - collected_coins_times[i] > respawn_delay:
                collected_coins += 1
                collected_coins_times[i] = time.time()
                score += 1

        # draw the background
        screen.fill(WHITE)

        # draw the floor
        pygame.draw.rect(screen, RED, floor)

        # draw the platforms
        for platform in platforms:
            pygame.draw.rect(screen, BLUE, platform)

        # draw the player
        pygame.draw.rect(screen, GREEN, (player_x, player_y, player_width, player_height))

        # draw the coins
        for i, coin in enumerate(coins):
            if time.time() - collected_coins_times[i] > respawn_delay:
                pygame.draw.circle(screen, YELLOW, coin.center, coin_radius)

        # draw the enemy
        pygame.draw.circle(screen, RED, (int(enemy_x), int(enemy_y)), enemy_radius)

        # draw the score
        font = pygame.font.Font(None, 36)
        score_text = font.render("Score: " + str(score), True, BLUE)
        screen.blit(score_text, (10, 10))

        if game_over:
            # draw game over text
            font = pygame.font.Font(None, 36)
            text = font.render("Game Over", True, RED)
            text_rect = text.get_rect(center=(screen_width / 2, screen_height / 2))
            screen.blit(text, text_rect)

        # update the display
        pygame.display.flip()

        # limit the frame rate
        clock.tick(60)

# quit the game
pygame.quit()
