import pygame
import random
from constants import *
from sprites import *

class Game:
    def __init__(self):
        # init pygame, create window
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Programming Project 1")
        self.clock = pygame.time.Clock()
        self.running = True
        self.currentX = 0
        self.currentY = 0


    def startGame(self):
        self.all_sprites = pygame.sprite.Group()
        self.bg_sprites = pygame.sprite.Group()
        self.startBattle()
        self.run()

    def startBattle(self):
        self.board=[[0,0,0,0],
                    [0,0,0,0],
                    [0,0,0,0],
                    [0,0,0,0]]

        self.letterlist = []
        for column in range(0,4):
            for row in range(0,4):
                self.tileInfo = random.choice(list(LETTERSCORES.items()))
                self.tile = Tile(self.tileInfo[0], str(self.tileInfo[1]), (WIDTH / 2) + (column * 70) + (column * 10) - 155, (HEIGHT * 0.75) + (row * 70) + (row * 10) - 155)
                self.all_sprites.add(self.tile)
                self.board[row][column] = self.tile
        self.selectedTile = self.board[self.currentY][self.currentX]
        self.selection = Selection(self.selectedTile.rect.left - 5, self.selectedTile.rect.top + 5)
        self.bg_sprites.add(self.selection)
        self.hud = HUD()

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        self.all_sprites.update()

    def events(self):
        # Process input (events)
        for event in pygame.event.get():
            # Check for closing window
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if self.currentY < 3:
                    if event.key == pygame.K_DOWN:
                        self.currentY += 1
                        if self.board[self.currentY][self.currentX] != 0:
                            self.selectedTile = self.board[self.currentY][self.currentX]
                            selection.move(self.selectedTile)
                if self.currentY > 0:
                    if event.key == pygame.K_UP:
                        self.currentY -= 1
                        if self.board[self.currentY][self.currentX] != 0:
                            self.selectedTile = self.board[self.currentY][self.currentX]
                            selection.move(self.selectedTile)
                if self.currentX < 3:
                    if event.key == pygame.K_RIGHT:
                        self.currentX += 1
                        if self.board[self.currentY][self.currentX] != 0:
                            self.selectedTile = self.board[self.currentY][self.currentX]
                            selection.move(self.selectedTile)
                if currentX > 0:
                    if event.key == pygame.K_LEFT:
                        currentX -= 1
                        if self.board[self.currentY][self.currentX] != 0:
                            self.selectedTile = self.board[self.currentY][self.currentX]
                            selection.move(self.selectedTile)
                if event.key == pygame.K_z and selectedTile.selected == False:
                    selectedTile.select()
                if event.key == pygame.K_x:
                    cancel()
                if event.key == pygame.K_c:
                    if len(letterlist) > 0:
                        print(wordScore(letterlist))
                        counter = 0
                        while counter < 30:
                            hud.displayWordScore(wordScore(letterlist))
                            counter += 1

    def draw(self):
        self.screen.fill(BLACK)
        self.bg_sprites.draw(self.screen)
        self.all_sprites.draw(self.screen)
        # Flip the display
        pygame.display.flip()



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

game = Game()
while game.running:
    game.startGame()

pygame.quit()
