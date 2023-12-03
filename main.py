# Example file showing a circle moving on screen
import pygame
import sys
import random
# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Obstacle class
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def set_position(self, new_x, new_y):
        self.rect.topleft = (new_x, new_y)

# Game over function
def game_over():
    font = pygame.font.Font(None, 74)
    game_over_text = font.render("Game Over", True, (255, 255, 255))
    game_over_text_x = screen.get_width() // 2 - game_over_text.get_width()
    game_over_text_y = screen.get_height() // 2 - game_over_text.get_height()
    screen.blit(game_over_text, game_over_text_x, game_over_text_y)
    pygame.display.flip()
    pygame.time.delay(2000)  # Display the game over message for 2 seconds
    pygame.quit()
    sys.exit()

player = Player('assets/images/bird1.png', screen.get_width() / 2, screen.get_height() / 2)

#obstacle = Obstacle('assets/images/pipe.png', screen.get_width(), 200)
showing_speed = 60*5
space_between_obstacles = 200

# Create sprite groups and add sprites to them
all_sprites = pygame.sprite.Group(player)
obstacles_group = pygame.sprite.Group()

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    # Change the x position of the obst])
    #print(obstacle.rect.topleft[0])
    #print(obstacle)
    move_obstacle_speed = 7
    for obstacle in obstacles_group:
        obstacle.set_position(obstacle.rect.topleft[0] - move_obstacle_speed, obstacle.rect.y)
        if obstacle.rect.x < 0-obstacle.rect.width:
            # Remove obstacle from sprite groups
            obstacles_group.remove(obstacle)
            all_sprites.remove(obstacle)

    # Update and draw all sprites
    all_sprites.update()

    # Check if the obstacle is off the left side of the screen
    showing_speed -= 1
    if showing_speed < 0:
        showing_speed = 120
        random_height = random.randint(0, screen.get_height())
        obstacle = Obstacle('assets/images/pipe.png', screen.get_width(), random_height+50)
        print(obstacle.rect.height)
        obstacle2 = Obstacle('assets/images/pipe.png', screen.get_width(), random_height - space_between_obstacles - obstacle.rect.height)
        obstacle2.image = pygame.transform.rotate(obstacle2.image, 180)
        obstacles_group.add(obstacle)
        all_sprites.add(obstacle)
        obstacles_group.add(obstacle2)
        all_sprites.add(obstacle2)
        print(obstacles_group)

    # Check for collisions between player and obstacles
    if pygame.sprite.spritecollide(player, obstacles_group, False):
        game_over()

    all_sprites.draw(screen)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        if player.rect.y > 0:
            player.rect.y -= 300 * dt
    if keys[pygame.K_s]:
        if player.rect.y < screen.get_height() - player.rect.height:
            player.rect.y += 300 * dt
    if keys[pygame.K_a]:
        if player.rect.x > 0:
            player.rect.x -= 300 * dt
    if keys[pygame.K_d]:
        if player.rect.x < screen.get_width() - player.rect.width:
            player.rect.x += 300 * dt

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()