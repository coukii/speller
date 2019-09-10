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
        self.image = pygame.Surface((70,70))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y
        self.letterfont = pygame.font.SysFont('Times New Roman', 36)
        self.scorefont = pygame.font.SysFont('Times New Roman', 16)
        self.letter = letter
        self.score = score
        self.letterrender = self.letterfont.render(self.letter, True, BLACK)
        self.scorerender = self.scorefont.render(self.score, True, BLACK)
        #pygame.display.update

    def update(self):
        screen.blit(self.letterrender, (self.rect.centerx - (self.letterfont.size(self.letter)[0] / 2.), self.rect.centery - (self.letterfont.size(self.letter)[1] / 2.)))
        screen.blit(self.scorerender, (self.rect.right - (self.scorefont.size(self.score)[0]) - 2, self.rect.bottom - (self.scorefont.size(self.score)[1])))

class Selection(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((70, 70))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y

all_sprites = pygame.sprite.Group()

board=[[0,0,0,0],
       [0,0,0,0],
       [0,0,0,0],
       [0,0,0,0]]

for column in range(0,4):
    for row in range(0,4):
        tileInfo = random.choice(list(LETTERSCORES.items()))
        tile = Tile(tileInfo[0], str(tileInfo[1]), (WIDTH / 2) + (column * 70) + (column * 10) - 155, (HEIGHT * 0.75) + (row * 70) + (row * 10) - 155)
        all_sprites.add(tile)
        print("adding row", row, "column", column)
        board[row][column] = tile

selectedTile = board[0][0]

selection = Selection(selectedTile.rect.left, selectedTile.rect.top)
all_sprites.add(selection)

# ADD GREEN TILES TO EVERY TILE OBJECT (BLACK AS DEFAULT)
# ENABLE WHEN SELECTED

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
