import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Super Mario Style Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
SKY_BLUE = (135, 206, 235)
BROWN = (139, 69, 19)
GOLD = (255, 215, 0)
DARK_GREEN = (0, 100, 0)
PURPLE = (128, 0, 128)

# Game variables
clock = pygame.time.Clock()
FPS = 60
score = 0
font = pygame.font.SysFont("Arial", 24)

# Player class
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 32
        self.height = 48
        self.vel_y = 0
        self.vel_x = 0
        self.speed = 5
        self.jump_power = -15
        self.gravity = 0.8
        self.on_ground = False
        self.direction = "right"
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
    def update(self, platforms):
        self.vel_y += self.gravity
        
        self.x += self.vel_x
        self.y += self.vel_y
        
        self.rect.x = self.x
        self.rect.y = self.y
        
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0 and self.rect.bottom - self.vel_y <= platform.rect.top:
                    self.rect.bottom = platform.rect.top
                    self.y = self.rect.y
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0 and self.rect.top - self.vel_y >= platform.rect.bottom:
                    self.rect.top = platform.rect.bottom
                    self.y = self.rect.y
                    self.vel_y = 0
                elif self.vel_x > 0 and self.rect.right - self.vel_x <= platform.rect.left:
                    self.rect.right = platform.rect.left
                    self.x = self.rect.x
                elif self.vel_x < 0 and self.rect.left - self.vel_x >= platform.rect.right:
                    self.rect.left = platform.rect.right
                    self.x = self.rect.x
        
        if self.x < 0:
            self.x = 0
        elif self.x > SCREEN_WIDTH - self.width:
            self.x = SCREEN_WIDTH - self.width
            
        self.rect.x = self.x
        self.rect.y = self.y
        
    def jump(self):
        if self.on_ground:
            self.vel_y = self.jump_power
            
    def move_left(self):
        self.vel_x = -self.speed
        self.direction = "left"
        
    def move_right(self):
        self.vel_x = self.speed
        self.direction = "right"
        
    def stop(self):
        self.vel_x = 0
        
    def draw(self, screen):
        pygame.draw.rect(screen, GREEN if self.direction == "right" else DARK_GREEN, self.rect)
        eye_size = 4
        if self.direction == "right":
            pygame.draw.rect(screen, WHITE, (self.rect.x + 20, self.rect.y + 10, eye_size, eye_size))
            pygame.draw.rect(screen, WHITE, (self.rect.x + 20, self.rect.y + 20, eye_size, eye_size))
        else:
            pygame.draw.rect(screen, WHITE, (self.rect.x + 8, self.rect.y + 10, eye_size, eye_size))
            pygame.draw.rect(screen, WHITE, (self.rect.x + 8, self.rect.y + 20, eye_size, eye_size))

# Platform class
class Platform:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
    def draw(self, screen):
        pygame.draw.rect(screen, BROWN, self.rect)
        for i in range(0, self.width, 20):
            pygame.draw.rect(screen, (160, 82, 45), (self.x + i, self.y, 10, self.height))

# Coin class
class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.collected = False
        self.bob_offset = 0
        self.bob_direction = 1
        
    def update(self):
        self.bob_offset += 0.1 * self.bob_direction
        if self.bob_offset > 5 or self.bob_offset < -5:
            self.bob_direction *= -1
        self.rect.y = self.y + int(self.bob_offset)
        
    def draw(self, screen):
        if not self.collected:
            pygame.draw.circle(screen, GOLD, self.rect.center, 10)
            pygame.draw.circle(screen, WHITE, (self.rect.centerx - 3, self.rect.centery - 3), 3)

# Enemy class
class Enemy:
    def __init__(self, x, y, min_x, max_x):
        self.x = x
        self.y = y
        self.width = 32
        self.height = 32
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.direction = 1
        self.speed = 2
        self.min_x = min_x
        self.max_x = max_x
        self.alive = True
        
    def update(self):
        if self.alive:
            self.x += self.speed * self.direction
            if self.x > self.max_x or self.x < self.min_x:
                self.direction *= -1
            self.rect.x = self.x
        
    def draw(self, screen):
        if self.alive:
            pygame.draw.rect(screen, PURPLE, self.rect)
            pygame.draw.rect(screen, WHITE, (self.rect.x + 5, self.rect.y + 8, 8, 8))
            pygame.draw.rect(screen, WHITE, (self.rect.x + 19, self.rect.y + 8, 8, 8))

def create_level():
    platforms = []
    platforms.append(Platform(0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40))
    platforms.append(Platform(200, SCREEN_HEIGHT - 150, 100, 20))
    platforms.append(Platform(400, SCREEN_HEIGHT - 250, 100, 20))
    platforms.append(Platform(600, SCREEN_HEIGHT - 180, 100, 20))
    platforms.append(Platform(100, SCREEN_HEIGHT - 300, 80, 20))
    platforms.append(Platform(500, SCREEN_HEIGHT - 350, 120, 20))
    return platforms

def create_coins():
    coins = []
    coins.append(Coin(230, SCREEN_HEIGHT - 180))
    coins.append(Coin(430, SCREEN_HEIGHT - 280))
    coins.append(Coin(630, SCREEN_HEIGHT - 210))
    coins.append(Coin(130, SCREEN_HEIGHT - 330))
    coins.append(Coin(550, SCREEN_HEIGHT - 380))
    coins.append(Coin(300, SCREEN_HEIGHT - 80))
    coins.append(Coin(500, SCREEN_HEIGHT - 80))
    return coins

def create_enemies():
    enemies = []
    enemies.append(Enemy(200, SCREEN_HEIGHT - 72, 100, 350))
    enemies.append(Enemy(500, SCREEN_HEIGHT - 72, 400, 700))
    enemies.append(Enemy(200, SCREEN_HEIGHT - 332, 100, 180))
    return enemies

def main():
    global score
    player = Player(50, SCREEN_HEIGHT - 100)
    platforms = create_level()
    coins = create_coins()
    enemies = create_enemies()
    
    running = True
    while running:
        keys = pygame.key.get_pressed()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    player.jump()
        
        if keys[pygame.K_LEFT]:
            player.move_left()
        elif keys[pygame.K_RIGHT]:
            player.move_right()
        else:
            player.stop()
        
        player.update(platforms)
        
        for coin in coins:
            coin.update()
            if player.rect.colliderect(coin.rect) and not coin.collected:
                coin.collected = True
                score += 100
        
        for enemy in enemies:
            enemy.update()
            if player.rect.colliderect(enemy.rect) and enemy.alive:
                if player.vel_y > 0 and player.rect.bottom < enemy.rect.centery + 10:
                    enemy.alive = False
                    player.vel_y = -10
                    score += 200
                else:
                    player.x = 50
                    player.y = SCREEN_HEIGHT - 100
                    player.vel_y = 0
                    score = max(0, score - 50)
        
        screen.fill(SKY_BLUE)
        
        for platform in platforms:
            platform.draw(screen)
            
        for coin in coins:
            coin.draw(screen)
            
        for enemy in enemies:
            enemy.draw(screen)
            
        player.draw(screen)
        
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()