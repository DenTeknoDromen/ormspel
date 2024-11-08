import pygame
from random import randint

# pygame setup
pygame.init()
pygame.display.set_caption('Ormspel')
screen_size = 630
screen = pygame.display.set_mode((screen_size, screen_size))
clock = pygame.time.Clock()
running = True

# Player snake variables
relative_speed = 90 # Number of frames to cross screen
speed = screen_size / relative_speed
size = 20
snake_len = 20 # Starting length of snake
pos_list = []

# Food variables
food_rect = 0
food_pos = 0

# Grid for locking movement
grid = []
for x in range(int(screen_size / (speed * 6))):
    grid.append(42 * x)

# Starting position based on grid
start_pos = pygame.Vector2(grid[7], grid[7])
player_pos = start_pos.copy()

# Variables handling directional movement
get_dir = {"w":(0, -speed),"s":(0, speed), "a":(-speed, 0), "d":(speed, 0)}
opposite_dir = {"w":"s", "s":"w", "a":"d", "d":"a"}
last_press = "w"
curr_dir = "w"

def create_food():
    global food_rect
    global food_pos
    x = randint(1, len(grid) - 2)
    y = randint(1, len(grid) - 2)
    size = 20
    grid_offset = size / 2
    food_rect = pygame.Rect(grid[x] - grid_offset, grid[y] - grid_offset, size, size)
    food_pos = pygame.Vector2(food_rect.centerx, food_rect.centery)
    if food_pos in pos_list:
        create_food()

create_food()

# Checks if player position is alligned to grid
def grid_alligned():
    if player_pos.x in grid and player_pos.y in grid:
        return True
    
    return False

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")

    if player_pos.x > screen_size:
        player_pos.x = 0
    if player_pos.x < 0:
        player_pos.x = screen_size
    if player_pos.y > screen_size:
        player_pos.y = 0
    if player_pos.y < 0:
        player_pos.y = screen_size
    
    # Handles player direction
    if grid_alligned():
        if curr_dir == opposite_dir[last_press]:
            last_press = curr_dir

        curr_dir = last_press

    player_pos.x += get_dir[curr_dir][0]
    player_pos.y += get_dir[curr_dir][1]
    
    # Draws snake
    for x in pos_list:
        pygame.draw.circle(screen, "white", x, size)

    # Handles snake length
    if len(pos_list) > snake_len:
        pos_list.pop(0)

    pos_list.append(player_pos.copy())

    # Food section
    pygame.draw.rect(screen, "white", food_rect)
    if player_pos == food_pos:
        snake_len += 5
        create_food()

    # Resets game if player collides with themselves
    if pos_list.count(player_pos) > 1:
        screen.fill("black")
        player_pos = start_pos.copy()
        snake_len = 20
        pos_list = []
        create_food()     

    # Input section
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        last_press = "w"
    if keys[pygame.K_s]:
        last_press = "s"
    if keys[pygame.K_a]:
        last_press = "a"
    if keys[pygame.K_d]:
        last_press = "d"
    
    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    clock.tick(60)

pygame.quit()