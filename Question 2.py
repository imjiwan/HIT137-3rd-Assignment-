import pygame
import random

# Define colors as RGB values
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GOLD = (255, 215, 0)

# Define the screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Initialize Pygame
pygame.init()

# Set up the font for text
font = pygame.font.Font(None, 36)

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Collectibles Game")

# Define classes for objects in the game
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT-100))
        self.speed = 5

    def update(self):
        # Move the player left or right
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        # Keep player inside the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH


class Collectible(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(GOLD)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speed = random.randrange(1, 8)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT + 10:
            self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speed = random.randrange(1, 8)


# Create the game objects
all_sprites_group = pygame.sprite.Group()
player = Player()
all_sprites_group.add(player)
collectibles_group = pygame.sprite.Group()
for i in range(5):
    collectible = Collectible()
    collectibles_group.add(collectible)
    all_sprites_group.add(collectible)

# Create the clock to control the game's frame rate
clock = pygame.time.Clock()

# Set up the score and timer
score = 0
start_time = pygame.time.get_ticks()

# Create the game loop
game_running = True
while game_running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False

    # Update game objects
    player.update()
    collectibles_group.update()

    # Handle collisions between player and collectibles
    for collectible in pygame.sprite.spritecollide(player, collectibles_group, True):
        score += 10

    # Draw game objects
    screen.fill(WHITE)
    all_sprites_group.draw(screen)

    # Draw the score and timer
    score_text = font.render("Score: {}".format(score), True, BLACK)
    screen.blit(score_text, (10, 10))
    elapsed_time = pygame.time.get_ticks() - start_time
    seconds = int(elapsed_time / 1000)
    remaining_seconds = 30 - seconds
    timer_text = font.render("Time: {}".format(remaining_seconds), True, BLACK)
    screen.blit(timer_text, (SCREEN_WIDTH - 150, 10))

    # Update the display
    pygame.display.flip()

    # Check if time has run out
    if remaining_seconds <= 0:
        game_running = False

    # Wait to ensure the game runs at a proper frame rate
    clock.tick(60)

# Display the final score
gameover_text = font.render("Game Over! Final Score: {}".format(score), True, RED)
gameover_rect = gameover_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
screen.fill(WHITE)
screen.blit(gameover_text, gameover_rect)
pygame.display.flip()

# Wait for two seconds before quitting Pygame and closing the game window
pygame.time.wait(2000)
pygame.quit()