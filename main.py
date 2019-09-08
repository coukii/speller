import pygame
import random
from scores import *

WIDTH = 1280
HEIGHT = 720
FPS = 30

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# init pygame, create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Programming Project 1")
clock = pygame.time.Clock()

class Tile(pygame.sprite.Sprite):
    def __init__(self, letter, score, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50,50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y
        self.letterfont = pygame.font.SysFont('Times New Roman', 30)
        self.scorefont = pygame.font.SysFont('Times New Roman', 12)
        self.letter = letter
        self.score = score
        self.letterrender = self.letterfont.render(self.letter, True, BLACK)
        self.scorerender = self.scorefont.render(self.score, True, BLACK)
        self.fontsize = self.letterfont.size(letter)
        #pygame.display.update

    def update(self):
        screen.blit(self.letterrender, (self.rect.centerx - (self.fontsize[0] / 2.), self.rect.centery - (self.fontsize[1] / 2.)))
        screen.blit(self.scorerender, (self.rect.right - 10, self.rect.bottom - 14))

all_sprites = pygame.sprite.Group()
for column in range(0,4):
    for row in range(0,4):
        tileInfo = random.choice(list(LETTERSCORES.items()))
        tile = Tile(tileInfo[0], str(tileInfo[1]), WIDTH / 2 + column * 50 + column * 10 - 115, HEIGHT / 2 + row * 50 + row * 10 - 115)
        all_sprites.add(tile)


# Game loop
running = True
while running:
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # Check for closing window
        if event.type == pygame.QUIT:
            running = False

    # Draw / render
    screen.fill(BLACK)
    all_sprites.draw(screen)
    # Update sprites
    all_sprites.update()
    # Flip the display
    pygame.display.flip()

pygame.quit()
