from numpy import blackman
import pygame
import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

pygame.init()
pygame.mixer.init()
screen_size = (800, 600)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Collect the gold!")


background_image = pygame.image.load(r'C:\Users\Acer\Desktop\Master\Software Now (HIT137)\Assignment 3\Image\sky.png') 

player_image = pygame.image.load(r'C:\Users\Acer\Desktop\Master\Software Now (HIT137)\Assignment 3\Image\guy4.png')  

collectible_image = pygame.image.load(r'C:\Users\Acer\Desktop\Master\Software Now (HIT137)\Assignment 3\Image\coin.png')  


font = pygame.font.Font(None, 36)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(player_image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = screen_size[0] // 2 - self.rect.width // 2
        self.rect.y = screen_size[1] - self.rect.height - 10
        self.speed = 5

    def update(self):
    
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

     
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.right > screen_size[0]:
            self.rect.right = screen_size[0]


class Collectible(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(collectible_image, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_size[0] - self.rect.width)
        self.rect.y = random.randint(-500, -50)
        self.speed = random.randint(2, 10)

    def update(self):
       
        self.rect.y += self.speed

        if self.rect.top > screen_size[1]:
            self.rect.x = random.randint(0, screen_size[0] - self.rect.width)
            self.rect.y = random.randint(-500, -50)
            self.speed = random.randint(2, 10)


def play_game():

    player = Player()
    all_sprites_list = pygame.sprite.Group()
    all_sprites_list.add(player)
    collectibles_list = pygame.sprite.Group()
    for i in range(10):
        collectible = Collectible()
        collectibles_list.add(collectible)
        all_sprites_list.add(collectible)

    score = 0
    game_over = False
    clock = pygame.time.Clock()
    start_ticks = pygame.time.get_ticks()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                break

        all_sprites_list.update()

        seconds = (pygame.time.get_ticks() - start_ticks) // 1000

        for collectible in pygame.sprite.spritecollide(player, collectibles_list, True):
            score += 1

        screen.blit(background_image, (0, 0))
        all_sprites_list.draw(screen)
        score_text = font.render("Score: " + str(score), 1, BLACK)
        screen.blit(score_text, (10, 10))
        time_text = font.render("Time: " + str(30 - seconds), 1, BLACK)
        screen.blit(time_text, (screen_size[0] - 100, 10))
        pygame.display.flip()

        if seconds >= 30:
            game_over = True

        clock.tick(60)

    game_over_text = font.render("Game Over! Final Score: {}".format(score), True, BLACK)
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

        screen.blit(background_image, (0, 0))
        screen.blit(game_over_text, game_over_rect)
        pygame.draw.rect(screen, WHITE, exit_button_rect, 2)
        pygame.draw.rect(screen, WHITE, restart_button_rect, 2)
        exit_text = font.render("Exit", True, BLACK)
        screen.blit(exit_text, (exit_button_rect.centerx - exit_text.get_width() // 2, exit_button_rect.centery - exit_text.get_height() // 2))
        restart_text = font.render("Restart", True, BLACK)
        screen.blit(restart_text, (restart_button_rect.centerx - restart_text.get_width() // 2, restart_button_rect.centery - restart_text.get_height() // 2))
        pygame.display.flip()

    pygame.quit()

play_game()
