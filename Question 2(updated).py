import pygame, random

# Define some colors as RGB values
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GOLD = (255, 215, 0)

# Set up the Pygame environment
pygame.init()
screen_size = (800, 600)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Collect the gold!")

# Define a class for the player sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([50, 50])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = screen_size[0] // 2 - self.rect.width // 2
        self.rect.y = screen_size[1] - self.rect.height - 10
        self.speed = 5

    def update(self):
        # Move the player sprite based on user input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        # Keep the player sprite inside the screen boundaries
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.right > screen_size[0]:
            self.rect.right = screen_size[0]

# Define a class for the collectible sprite
class Collectible(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([20, 20])
        self.image.fill(GOLD)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_size[0] - self.rect.width)
        self.rect.y = random.randint(-500, -50)
        self.speed = random.randint(2, 10)

    def update(self):
        # Move the collectible sprite down the screen
        self.rect.y += self.speed

        # Re-position the collectible sprite at the top of the screen when it goes off the bottom
        if self.rect.top > screen_size[1]:
            self.rect.x = random.randint(0, screen_size[0] - self.rect.width)
            self.rect.y = random.randint(-500, -50)
            self.speed = random.randint(2, 10)

# Define a function that handles the game loop
def play_game():
    # Set up the game objects
   player = Player()
   all_sprites_list = pygame.sprite.Group()
   all_sprites_list.add(player)
   collectibles_list = pygame.sprite.Group()
   for i in range(10):
        collectible = Collectible()
        collectibles_list.add(collectible)
        all_sprites_list.add(collectible)

    # Set up the font for text
   font = pygame.font.Font(None, 36)

    # Set up the game variables
   score = 0
   game_over = False
   clock = pygame.time.Clock()
   start_ticks = pygame.time.get_ticks()

    # The game loop
   while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                break

        # Update game objects
        all_sprites_list.update()

        # Get the current time and calculate elapsed time
        seconds = (pygame.time.get_ticks() - start_ticks) // 1000

        # Handle collisions between player and collectibles
        for collectible in pygame.sprite.spritecollide(player, collectibles_list, True):
            score += 1

        # Draw everything
        screen.fill(WHITE)
        all_sprites_list.draw(screen)
        score_text = font.render("Score: " + str(score), 1, BLACK)
        screen.blit(score_text, (10, 10))
        time_text = font.render("Time: " + str(30 - seconds), 1, BLACK)
        screen.blit(time_text, (screen_size[0] - 100, 10))
        pygame.display.flip()

        # Check for game over
        if seconds >= 30:
            game_over = True

        # Wait to ensure the game runs at a consistent frame rate
        clock.tick(60)

    # Game over screen
   game_over_text = font.render("Game Over! Final Score: {}".format(score), True, BLUE)
   game_over_rect = game_over_text.get_rect(center=screen.get_rect().center)
   exit_button_rect = pygame.Rect(325, 400, 150, 50)
   restart_button_rect = pygame.Rect(325, 475, 150, 50)

   while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = False
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if exit_button_rect.collidepoint(mouse_pos):
                    game_over = False
                elif restart_button_rect.collidepoint(mouse_pos):
                    play_game()

        screen.fill(WHITE)
        screen.blit(game_over_text, game_over_rect)
        pygame.draw.rect(screen, BLACK, exit_button_rect, 2)
        pygame.draw.rect(screen, BLACK, restart_button_rect, 2)
        exit_text = font.render("Exit", True, BLACK)
        screen.blit(exit_text, (exit_button_rect.centerx - exit_text.get_width() // 2, exit_button_rect.centery - exit_text.get_height() // 2))
        restart_text = font.render("Restart", True, BLACK)
        screen.blit(restart_text, (restart_button_rect.centerx - restart_text.get_width() // 2, restart_button_rect.centery - restart_text.get_height() // 2))
        pygame.display.flip()

    # Quit Pygame
   pygame.quit()

# Start the game
play_game()