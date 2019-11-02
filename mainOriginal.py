import pygame
import random
import json
import time
from constants import *

currentX = 0
currentY = 0

gameScore = 0

blit = False

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
        self.letterFont = pygame.font.SysFont('Times New Roman', 36)
        self.scoreFont = pygame.font.SysFont('Times New Roman', 16)
        self.letter = letter
        self.score = score
        self.letterRender = self.letterFont.render(self.letter, True, BLACK)
        self.scoreRender = self.scoreFont.render(self.score, True, BLACK)
        self.selected = False
    def update(self):
        screen.blit(self.letterRender, (self.rect.centerx - (self.letterFont.size(self.letter)[0] / 2.), self.rect.centery - (self.letterFont.size(self.letter)[1] / 2.)))
        screen.blit(self.scoreRender, (self.rect.right - (self.scoreFont.size(self.score)[0]) - 2, self.rect.bottom - (self.scoreFont.size(self.score)[1])))
    def select(self):
        all_sprites.remove(self)
        self.selected = True
        if len(letterlist) == 0:
            spelltile = Tile(self.letter, self.score, 5, HEIGHT / 3)
        elif len(letterlist) > 0:
            spelltile = Tile(self.letter, self.score, letterlist[len(letterlist)-1].rect.right + 10, HEIGHT / 3)
        letterlist.append(spelltile)
        all_sprites.add(spelltile)
    def randomise(self):
        tileInfo = random.choice(list(LETTERSCORES.items()))
        self.letter = tileInfo[0]
        self.score = str(tileInfo[1])
        self.vowels = 0
        for row in board:
            for column in row:
                if column.letter in "aeiouAEIOU":
                    print("found vowel", column.letter)
                    self.vowels += 1
        if self.vowels > 2:
            tileInfo = random.choice(list(LETTERSCORES.items()))
        else:
            tileInfo = random.choice(list(VOWELSCORES.items()))
        self.letter = tileInfo[0]
        self.score = str(tileInfo[1])
        self.letterRender = self.letterFont.render(self.letter, True, BLACK)
        self.scoreRender = self.scoreFont.render(self.score, True, BLACK)

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

class HUD(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font('FSEX302.ttf', 50)
    def renderText(self, text, color, x, y):
        self.textSurface = self.font.render(text, False, color)
        self.textRect = self.textSurface.get_rect()
        self.textRect.center = (x, y)
        return self.textSurface, self.textRect
    def displayWordScore(self, text):
        self.wordSurface, self.wordRect = self.renderText(str(text), WHITE, WIDTH / 2, HEIGHT / 2)
        screen.blit(self.wordSurface, self.wordRect)
    def displayTotalScore(self, score):
        self.scoreSurface, self.scoreRect = self.renderText(str(score), WHITE, 40, 40)
        screen.blit(self.scoreSurface, self.scoreRect)

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
                        column.randomise()
                        all_sprites.add(column)
                        column.selected = False
            return word, totalScore
        else:
            return "WORD DOES NOT EXIST!", 0
    else:
        return "WORD TOO SHORT!", 0

hud = HUD()

# Game loop

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
                    displayWord, displayScore = wordScore(letterlist)
                    gameScore += displayScore
                    blit=True
                    start_time = time.time()

    # Draw / render
    screen.fill(BLACK)
    bg_sprites.draw(screen)
    all_sprites.draw(screen)
    # Update sprites
    all_sprites.update()

    if blit:
        hud.displayWordScore(displayWord + " : " + str(displayScore) + " POINTS")
        if time.time() - start_time > 2:
            blit=False

    hud.displayTotalScore(gameScore)

    # Flip the display
    pygame.display.flip()

pygame.quit()
