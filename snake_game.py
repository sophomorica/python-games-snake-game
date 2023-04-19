import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Game settings
SNAKE_SIZE = 20
INITIAL_SPEED = 10
speed_multiplier = 1
direction = 'RIGHT'
APPLE_SIZE = 20
SNAKE_SPEED = 10

game_mode = ''
# Add this function after the APPLE_SIZE variable
def start_screen():
    global game_mode

    # Text settings
    font = pygame.font.Font(None, 36)
    normal_text = font.render('Normal', True, (0, 0, 0))
    hardcore_text = font.render('Hardcore', True, (0, 0, 0))

    normal_rect = normal_text.get_rect()
    hardcore_rect = hardcore_text.get_rect()

    normal_rect.center = (WIDTH // 3, HEIGHT // 2)
    hardcore_rect.center = (2 * WIDTH // 3, HEIGHT // 2)

    while game_mode.lower() not in ['normal', 'hardcore']:
        screen.fill(WHITE)

        screen.blit(normal_text, normal_rect)
        screen.blit(hardcore_text, hardcore_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                if normal_rect.collidepoint(mouse_pos):
                    game_mode = 'normal'
                elif hardcore_rect.collidepoint(mouse_pos):
                    game_mode = 'hardcore'

snake_pos = [[100, 100], [100 - SNAKE_SIZE, 100], [100 - (2 * SNAKE_SIZE), 100]]
snake_speed = [SNAKE_SPEED, 0]

apple_pos = [random.randrange(1, (WIDTH//APPLE_SIZE)) * APPLE_SIZE, random.randrange(1, (HEIGHT//APPLE_SIZE)) * APPLE_SIZE]

def draw_objects():
    screen.fill(WHITE)

    for pos in snake_pos:
        pygame.draw.rect(screen, GREEN, pygame.Rect(pos[0], pos[1], SNAKE_SIZE, SNAKE_SIZE))

    pygame.draw.rect(screen, RED, pygame.Rect(apple_pos[0], apple_pos[1], APPLE_SIZE, APPLE_SIZE))

def move_snake():
    global direction

    for i in range(len(snake_pos) - 1, 0, -1):
        snake_pos[i] = list(snake_pos[i-1])

    if direction == 'UP':
        snake_pos[0][1] -= int(INITIAL_SPEED * speed_multiplier)
    elif direction == 'DOWN':
        snake_pos[0][1] += int(INITIAL_SPEED * speed_multiplier)
    elif direction == 'LEFT':
        snake_pos[0][0] -= int(INITIAL_SPEED * speed_multiplier)
    elif direction == 'RIGHT':
        snake_pos[0][0] += int(INITIAL_SPEED * speed_multiplier)

def check_collision():
    # Check collision with the screen borders
    if snake_pos[0][0] < 0 or snake_pos[0][0] >= WIDTH or snake_pos[0][1] < 0 or snake_pos[0][1] >= HEIGHT:
        return True

    # Check collision with itself
    for pos in snake_pos[1:]:
        if snake_pos[0] == pos:
            return True

    return False

def check_apple_collision():
    global snake_speed, SNAKE_SPEED

    snake_head_x, snake_head_y = snake_pos[0]
    apple_x, apple_y = apple_pos

    if (abs(snake_head_x - apple_x) < SNAKE_SIZE) and (abs(snake_head_y - apple_y) < SNAKE_SIZE):
        apple_pos[0] = random.randrange(1, (WIDTH // APPLE_SIZE)) * APPLE_SIZE
        apple_pos[1] = random.randrange(1, (HEIGHT // APPLE_SIZE)) * APPLE_SIZE

        snake_pos.append(snake_pos[-1])

        # Increase the speed by a factor of 1.1
        SNAKE_SPEED = int(SNAKE_SPEED * 1.1)
        if direction in ['LEFT', 'RIGHT']:
            snake_speed[0] = SNAKE_SPEED
        else:
            snake_speed[1] = SNAKE_SPEED

        return True
    return False

def check_apple_collision():
    global speed_multiplier

    snake_head_x, snake_head_y = snake_pos[0]
    apple_x, apple_y = apple_pos

    if (abs(snake_head_x - apple_x) < SNAKE_SIZE) and (abs(snake_head_y - apple_y) < SNAKE_SIZE):
        apple_pos[0] = random.randrange(1, (WIDTH // APPLE_SIZE)) * APPLE_SIZE
        apple_pos[1] = random.randrange(1, (HEIGHT // APPLE_SIZE)) * APPLE_SIZE

        snake_pos.append(snake_pos[-1])

        if game_mode.lower() == 'hardcore':
            # Increase the speed by a factor of 1.1
            speed_multiplier *= 1.1

        return True

    return False

def reset_game():
    global snake_pos, snake_speed, apple_pos, SNAKE_SPEED, speed_multiplier

    snake_pos = [[100, 100], [100 - SNAKE_SIZE, 100], [100 - (2 * SNAKE_SIZE), 100]]
    snake_speed = [SNAKE_SPEED, 0]
    apple_pos = [random.randrange(1, (WIDTH//APPLE_SIZE)) * APPLE_SIZE, random.randrange(1, (HEIGHT//APPLE_SIZE)) * APPLE_SIZE]
    speed_multiplier = 1

start_screen()
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 'DOWN':
                direction = 'UP'
                snake_speed = [0, -int(INITIAL_SPEED * speed_multiplier)]
            if event.key == pygame.K_DOWN and direction != 'UP':
                direction = 'DOWN'
                snake_speed = [0, int(INITIAL_SPEED * speed_multiplier)]
            if event.key == pygame.K_LEFT and direction != 'RIGHT':
                direction = 'LEFT'
                snake_speed = [-int(INITIAL_SPEED * speed_multiplier), 0]
            if event.key == pygame.K_RIGHT and direction != 'LEFT':
                direction = 'RIGHT'
                snake_speed = [int(INITIAL_SPEED * speed_multiplier), 0]
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()



    move_snake()

    if check_collision():
        reset_game()

    if check_apple_collision():
        pass

    draw_objects()

    pygame.display.flip()
    clock.tick(30)
