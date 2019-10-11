import pygame
import random
import json
from scores import *

WIDTH = 1280
HEIGHT = 720
FPS = 30

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

currentX = 0
currentY = 0

WORDDICT = json.load(open("words_dictionary.json", "r"))

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
        #self.selection = pygame.Surface((70,70))
        #self.selection.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y
        self.letterfont = pygame.font.SysFont('Times New Roman', 36)
        self.scorefont = pygame.font.SysFont('Times New Roman', 16)
        self.letter = letter
        self.score = score
        self.letterrender = self.letterfont.render(self.letter, True, BLACK)
        self.scorerender = self.scorefont.render(self.score, True, BLACK)
        self.selected = False
        #pygame.display.update
    def update(self):
        screen.blit(self.letterrender, (self.rect.centerx - (self.letterfont.size(self.letter)[0] / 2.), self.rect.centery - (self.letterfont.size(self.letter)[1] / 2.)))
        screen.blit(self.scorerender, (self.rect.right - (self.scorefont.size(self.score)[0]) - 2, self.rect.bottom - (self.scorefont.size(self.score)[1])))
    def select(self):
        all_sprites.remove(self)
        self.selected = True
        if len(letterlist) == 0:
            spelltile = Tile(self.letter, self.score, 5, HEIGHT / 3)
        elif len(letterlist) > 0:
            spelltile = Tile(self.letter, self.score, letterlist[len(letterlist)-1].rect.right + 10, HEIGHT / 3)
        letterlist.append(spelltile)
        # print(letterlist[len(letterlist)-1].letter)
        all_sprites.add(spelltile)
        print()
        for i in letterlist:
            print(i.letter, ":", str(i.score), end=' ')
    def randomise(self):
        tileInfo = random.choice(list(LETTERSCORES.items()))
        self.letter = tileInfo[0]
        self.score = str(tileInfo[1])
        self.letterrender = self.letterfont.render(self.letter, True, BLACK)
        self.scorerender = self.scorefont.render(self.score, True, BLACK)

class Selection(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((70, 70))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y
    def move(self, object):
        self.rect.left = object.rect.left - 5
        self.rect.top = object.rect.top + 5

class HUD():
    def __init__(self):
        self.font = pygame.font.Font('FSEX302.ttf', 50)
    def update(self):
        pass
    def display(self, text):
        self.textSurface = self.font.render(text, False, WHITE)
        self.textRect = self.textSurface.get_rect()
        self.textRect.center = (WIDTH / 2, HEIGHT / 2)
        screen.blit(self.textSurface, self.textRect)
        # self.last = pygame.time.get_ticks()
        # now = pygame.time.get_ticks()


all_sprites = pygame.sprite.Group()
bg_sprites = pygame.sprite.Group()

letterlist = []

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

selectedTile = board[currentY][currentX]

selection = Selection(selectedTile.rect.left - 5, selectedTile.rect.top + 5)
bg_sprites.add(selection)

# Game loop

def cancel():
    print(letterlist)
    for letter in letterlist[:]:
        print(letter.letter, "removed")
        letter.kill()
        letterlist.remove(letter)
    for row in board:
        for column in row:
            all_sprites.add(column)
            column.selected = False

def wordScore(inputList):
    totalScore = 0
    wordList = []
    for tile in inputList:
        totalScore += int(tile.score)
        wordList.append(tile.letter)
    word = ''.join(wordList)
    if len(word) > 2:
        if word.lower() in WORDDICT:
            for tile in inputList[:]:
                print(tile.letter, "removed")
                tile.kill()
                inputList.remove(tile)
            for row in board:
                for column in row:
                    if column.selected == True:
                        print(column.letter)
                        column.randomise()
                        all_sprites.add(column)
                        column.selected = False
            return word + ": " + str(totalScore) + " POINTS"
        else:
            return "WORD DOES NOT EXIST!"
    else:
        return "WORD TOO SHORT!"

hud = HUD()

running = True
while running:
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # Check for closing window
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if currentY < 3:
                if event.key == pygame.K_DOWN:
                    currentY += 1
                    if board[currentY][currentX] != 0:
                        selectedTile = board[currentY][currentX]
                        selection.move(selectedTile)
            if currentY > 0:
                if event.key == pygame.K_UP:
                    currentY -= 1
                    if board[currentY][currentX] != 0:
                        selectedTile = board[currentY][currentX]
                        selection.move(selectedTile)
            if currentX < 3:
                if event.key == pygame.K_RIGHT:
                    currentX += 1
                    if board[currentY][currentX] != 0:
                        selectedTile = board[currentY][currentX]
                        selection.move(selectedTile)
            if currentX > 0:
                if event.key == pygame.K_LEFT:
                    currentX -= 1
                    if board[currentY][currentX] != 0:
                        selectedTile = board[currentY][currentX]
                        selection.move(selectedTile)
            if event.key == pygame.K_z and selectedTile.selected == False:
                selectedTile.select()
            if event.key == pygame.K_x:
                cancel()
            if event.key == pygame.K_c:
                if len(letterlist) > 0:
                    print(wordScore(letterlist))
                    counter = 0
                    while counter < 30:
                        hud.display(wordScore(letterlist))
                        counter += 1

    # Draw / render
    screen.fill(BLACK)
    bg_sprites.draw(screen)
    all_sprites.draw(screen)

    # Update sprites
    all_sprites.update()
    hud.update()
    # Flip the display
    pygame.display.flip()

pygame.quit()
