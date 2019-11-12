import pygame
import random
from constants import *
from os import path



class Tile(pygame.sprite.Sprite):
    def __init__(self, game, letter, score, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((70,70))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y
        self.game = game
        self.letterFont = pygame.font.SysFont('Times New Roman', 36)
        self.scoreFont = pygame.font.SysFont('Times New Roman', 16)
        self.letter = letter
        self.score = score
        self.letterRender = self.letterFont.render(self.letter, True, BLACK)
        self.scoreRender = self.scoreFont.render(self.score, True, BLACK)
        self.selected = False

    def select(self):
        self.game.all_sprites.remove(self)
        self.selected = True
        spelltile = Tile(self.game, self.letter, self.score, WIDTH / 2, HEIGHT / 3)
        self.game.letterlist.append(spelltile)
        # self.game.all_sprites.add(spelltile)
        self.game.tiles.add(spelltile)

    def randomise(self):
        tileInfo = random.choice(list(LETTERSCORES.items()))
        self.letter = tileInfo[0]
        self.score = str(tileInfo[1])
        self.vowels = 0
        for row in self.game.board:
            for column in row:
                if column.letter in "aeiouAEIOU":
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
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
#
#     def renderText(self, text, color, x, y):
#         self.font = pygame.font.Font('FSEX302.ttf', 60)
#         self.textSurface = self.font.render(text, False, color)
#         self.textRect = self.textSurface.get_rect()
#         self.textRect.center = (x, y)
#         return self.textSurface, self.textRect
#
#     def displayWordScore(self, text):
#         self.font = pygame.font.Font('FSEX302.ttf', 60)
#         self.wordSurface, self.wordRect = self.renderText(str(text), WHITE, WIDTH / 2, (HEIGHT / 2) - 5)
#         self.game.screen.blit(self.wordSurface, self.wordRect)
#
#     def displayTotalScore(self, score):
#         self.font = pygame.font.Font('FSEX302.ttf', 60)
#         self.scoreSurface, self.scoreRect = self.renderText(str(score), WHITE, WIDTH / 2, 40)
#         self.game.screen.blit(self.scoreSurface, self.scoreRect)


class HealthBar():
    def __init__(self, game, x, y, health, onRight=False):
        self.game = game
        self.heart = pygame.image.load(path.join(self.game.spriteDir, 'heart.png')).convert_alpha()
        self.rect = pygame.Rect(x, y, 1, 1)
        self.health = health
        self.onRight = onRight

    def update(self, health):
        self.health = health
        if self.health > 0:
            if self.onRight == False:
                for i in range(self.health):
                    self.game.screen.blit(self.heart, [self.rect.x + i*50, self.rect.y - 20])
            else:
                for i in range(self.health):
                    self.game.screen.blit(self.heart, [self.rect.x - i*50 - 40, self.rect.y - 20])


class Projectile(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, 20))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.xvel = random.choice([-4, -3, -2, -1, 1, 2, 3, 4])
        self.yvel = random.choice([-4, -3, -2, -1, 1, 2, 3, 4])
        self.rect.centerx = (WIDTH / 2) - (self.xvel*50)
        self.game = game
        self.timer = pygame.time.get_ticks()
        if self.xvel == -4 or self.xvel == 4:  # talk about adding the second self.xvel
            self.rect.centery = (HEIGHT * 0.75) - (self.yvel*50)

        else:
            self.rect.centery = (HEIGHT / 2)
            self.yvel = random.choice([1, 2, 3, 4])

    def update(self):
        if not self.game.screen.get_rect().contains(self.rect):
            self.kill()
            print("killing projectile")
        now = pygame.time.get_ticks()
        if now - self.timer > 1000:
            self.rect.centerx += self.xvel
            self.rect.centery += self.yvel


class Enemy(pygame.sprite.Sprite):
    def __init__(self, health, damage, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        size = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(size[0]/1.5), int(size[1]/1.5)))
        self.rect = self.image.get_rect()
        self.rect.bottom = 300
        self.rect.right = WIDTH - 100
        self.health = health
        self.damage = damage
        self.cooldown = 400

    def attack(self):
        projectile = Projectile()
        all_sprites.add(projectile)

    def die(self):
        self.kill()


class Player(pygame.sprite.Sprite):
    def __init__(self, game, health):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pygame.image.load(path.join(self.game.spriteDir, "player.png")).convert_alpha()
        size = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(size[0]/1.5), int(size[1]/1.5)))
        self.rect = self.image.get_rect()
        self.rect.bottom = 300
        self.rect.x = 100
        self.health = health
        self.xp = 0

    def drawXP(self, x, y):
        self.bgrect = pygame.Rect(x, y, 205, 27)
        width = int(max(min(self.xp / 100 * (self.bgrect.width - 5), self.bgrect.width - 5), 0))
        xprect = pygame.Rect(x + 4, y + 4, width, 20)
        pygame.draw.rect(self.game.screen, WHITE, self.bgrect, 2)
        pygame.draw.rect(self.game.screen, BLUE, xprect)


class Game:
    def __init__(self):
        # init pygame, create window
        pygame.init()
        pygame.mixer.pre_init(44100, -16, 2, 64)
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Programming Project 1")
        self.clock = pygame.time.Clock()
        self.running = True
        # create font
        self.mainFont = self.getFont('FSEX302.ttf', 60)
        self.smallFont  = self.getFont('FSEX302.ttf', 25)
        self.tileLetterFont = pygame.font.SysFont('Times New Roman', 36)
        self.tileScoreFont = pygame.font.SysFont('Times New Roman', 16)
        # create HUD (talk about how this had to be moved from startBattle)
        self.hud = HUD(self)
        # self.currentX = 0
        # self.currentY = 0
        # load directories
        self.dir = path.dirname(__file__)
        self.sndDir = path.join(self.dir, 'sounds')
        self.spriteDir = path.join(self.dir, 'sprites')
        # load sounds
        self.dmgSound = pygame.mixer.Sound(path.join(self.sndDir, 'shoot.wav'))
        self.hurtSound = pygame.mixer.Sound(path.join(self.sndDir, 'hurt.wav'))
        pygame.mixer.music.load(path.join(self.sndDir, 'music.ogg'))
        # load enemy sprites
        self.enemySprites = []
        for i in range(1,4):
            self.enemySprites.append(pygame.image.load(path.join(self.spriteDir, 'enemy{}.png'.format(i))))
        self.damageCounter = False
        self.gameOver = False

    def startBattle(self):
        # start battle
        self.gameScore = 0
        self.all_sprites = pygame.sprite.Group()
        self.bg_sprites = pygame.sprite.Group()
        self.tiles = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.letterlist = []

        pygame.mixer.music.play(loops=-1)
        self.board = [[0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0]]

        # generate tiles on board
        vowels = 0
        for row in range(0, len(self.board)):
            for column in range(0, len(self.board[row])):
                tileInfo = random.choice(list(LETTERSCORES.items()))
                if tileInfo[0] in "aeiouAEIOU":
                    vowels += 0
                tile = Tile(self, tileInfo[0], str(tileInfo[1]), (WIDTH / 2) + (column * 70) + (column * 10) - 155, (HEIGHT * 0.75) + (row * 70) + (row * 10) - 155)
                self.all_sprites.add(tile)
                self.tiles.add(tile)
                self.board[row][column] = tile

        if vowels < 2:
            for tile in self.tiles:
                tile.randomise()

        self.selectedTile = self.board[0][0]
        self.currentX = 0
        self.currentY = 0

        # create health bars
        self.enemyHealth = HealthBar(self, WIDTH -25, 40, 0, onRight=True)
        self.playerHealth = HealthBar(self, 25, 40, 0)

        # create player and enemy
        self.enemy = self.spawnEnemy(random.randint(1, 10), 10)
        self.player = Player(self, 10)
        self.all_sprites.add(self.player)

        # create selection (this may be moved to yourTurn later)
        self.selection = Selection(self.selectedTile.rect.left - 5, self.selectedTile.rect.top + 5)
        self.bg_sprites.add(self.selection)

    def getFont(self, name, size):
        font = pygame.font.Font(name, size)
        return font

    def draw(self):
        # fill bg color
        self.screen.fill(BLACK)

        # draw sprites (probably should change to LayeredUpdates)
        self.bg_sprites.draw(self.screen)
        self.all_sprites.draw(self.screen)

        # draw health bars and total score
        self.enemyHealth.update(self.enemy.health)
        self.playerHealth.update(self.player.health)
        self.drawText(self.mainFont, str(self.gameScore), WHITE, WIDTH / 2, 40)

        self.player.drawXP(self.playerHealth.rect.x , self.playerHealth.rect.y + 40)
        self.drawText(self.smallFont, "XP: "+str(self.player.xp)+" / 100", WHITE, self.player.bgrect.centerx, self.player.bgrect.centery)


        if self.playerAttacking:
            self.drawText(self.mainFont, self.displayWord + " : " + str(self.displayScore) + " POINTS", WHITE, WIDTH / 2, (HEIGHT / 2) - 5)

        now = pygame.time.get_ticks()
        if self.damageCounter:
            if now - self.damageTimer < 1000:
                self.drawText(self.mainFont, "-"+str(self.damageAmount)+"!", RED, self.damageRecipient.rect.x, self.damageRecipient.rect.y + 200)
            else:
                self.damageCounter = False

        for tile in self.tiles:
            # self.screen.blit(tile.letterRender, (tile.rect.centerx - (self.letterFont.size(self.letter)[0] / 2.), self.rect.centery - (self.letterFont.size(self.letter)[1] / 2.)))
            # self.screen.blit(tile.scoreRender, (tile.rect.right - (self.scoreFont.size(self.score)[0]) - 2, self.rect.bottom - (self.scoreFont.size(self.score)[1])))
            if tile.selected == False:
                self.drawText(self.tileLetterFont, tile.letter, BLACK, tile.rect.centerx, tile.rect.centery)
                self.drawText(self.tileScoreFont, tile.score, BLACK, (tile.rect.right - (self.tileScoreFont.size(tile.score)[0] / 2.) - 2), (tile.rect.bottom - (self.tileScoreFont.size(tile.score)[1] / 2.)))

        for i in range (0, len(self.letterlist)):
            tile = self.letterlist[i]
            tile.rect.x = (WIDTH / 2 + i*80 - (len(self.letterlist)*40) + 5)
            if tile not in self.all_sprites:
                self.all_sprites.add(tile)

        self.projectiles.draw(self.screen)


        # flip display
        pygame.display.flip()

    def yourTurn(self):
        currentX = self.currentX
        currentY = self.currentY
        self.selectedTile = self.board[currentY][currentX]
        self.selection.move(self.selectedTile)
        self.playerAttacking = False
        self.enemyDamage = 0
        looping = True
        shot_timer = pygame.time.get_ticks()
        while looping:
            self.clock.tick(FPS)
            # Process input (events)
            for event in pygame.event.get():
                # Check for closing window
                if event.type == pygame.QUIT:
                    self.running = False
                    looping = False
                if event.type == pygame.KEYDOWN:
                    if currentY < 3:
                        if event.key == pygame.K_DOWN:
                            currentY += 1
                            if self.board[currentY][currentX] != 0:
                                self.selectedTile = self.board[currentY][currentX]
                                self.selection.move(self.selectedTile)
                    if currentY > 0:
                        if event.key == pygame.K_UP:
                            currentY -= 1
                            if self.board[currentY][currentX] != 0:
                                self.selectedTile = self.board[currentY][currentX]
                                self.selection.move(self.selectedTile)
                    if currentX < 3:
                        if event.key == pygame.K_RIGHT:
                            currentX += 1
                            if self.board[currentY][currentX] != 0:
                                self.selectedTile = self.board[currentY][currentX]
                                self.selection.move(self.selectedTile)
                    if currentX > 0:
                        if event.key == pygame.K_LEFT:
                            currentX -= 1
                            if self.board[currentY][currentX] != 0:
                                self.selectedTile = self.board[currentY][currentX]
                                self.selection.move(self.selectedTile)
                    if event.key == pygame.K_z and self.selectedTile.selected == False:
                        self.selectedTile.select()
                    if event.key == pygame.K_x:
                        self.cancel()
                    if event.key == pygame.K_c:
                        if len(self.letterlist) > 0:
                            # set current word and score
                            self.displayWord, self.displayScore = self.wordScore(self.letterlist)
                            # increment game score
                            self.gameScore += self.displayScore
                            self.playerAttacking = True
                            # self.damage(self.displayScore // 3, self.enemy)
                            if self.displayScore > 0:
                                self.currentX = currentX
                                self.currentY = currentY
                                looping = False
                            start_time = pygame.time.get_ticks()

                        # shots = 0

            # Update sprites
            self.bg_sprites.update()
            self.all_sprites.update()
            self.projectiles.update()

            if self.playerAttacking:
                if pygame.time.get_ticks() - start_time > 2000:
                    self.playerAttacking = False
                    # if self.displayScore > 0:
                    #     looping = False

            hits = pygame.sprite.spritecollide(self.selection, self.projectiles, True)
            for hit in hits:
                self.enemyDamage += 1
                self.hurtSound.play()

            now = pygame.time.get_ticks()
            if now - shot_timer > 1000:
                shot_timer = now
                projectile = Projectile(self)
                self.projectiles.add(projectile)

            if self.player.health <= 0:
                self.running = False
                looping = False
                self.gameOverScreen()

            if self.enemy.health <= 0:
                self.enemy.die()
                self.player.xp += 20
                self.enemy = self.spawnEnemy(random.randint(1, 10), 10)


            self.draw()

    def theirTurn(self):
        self.projectiles.empty()
        self.damage(self.displayScore // 3, self.enemy)
        self.playerAttacking = True

        timer = pygame.time.get_ticks()
        enemyAttacked = False
        looping = True

        while looping:
            self.clock.tick(FPS)
            # Process input (events)
            for event in pygame.event.get():
                # Check for closing window
                if event.type == pygame.QUIT:
                    self.running = False
                    looping = False

            self.bg_sprites.update()
            self.all_sprites.update()

            now = pygame.time.get_ticks()

            if now - timer > 2000:
                if enemyAttacked is False:
                    self.playerAttacking = False
                    self.damage(self.enemyDamage, self.player)
                    enemyAttacked = True

            if now - timer > 4000:
                looping = False

            self.draw()

    def cancel(self):
        for letter in self.letterlist[:]:
            print(letter.letter, "removed")
            letter.kill()
            self.letterlist.remove(letter)
        for row in self.board:
            for column in row:
                self.all_sprites.add(column)
                column.selected = False

    def wordScore(self, inputList):
        totalScore = 0
        wordList = []
        for tile in inputList:
            totalScore += int(tile.score)
            wordList.append(tile.letter.upper())
        word = ''.join(wordList)
        if len(word) > 2:
            if word.lower() in WORDDICT:
                for tile in inputList[:]:
                    print(tile.letter, "removed")
                    tile.kill()
                    inputList.remove(tile)
                for row in self.board:
                    for column in row:
                        if column.selected is True:
                            column.randomise()
                            self.all_sprites.add(column)
                            self.tiles.add(column)
                            column.selected = False
                return word, totalScore
            else:
                return "WORD DOES NOT EXIST!", 0
        else:
            return "WORD TOO SHORT!", 0

    def damage(self, damage, recipient):
        recipient.health -= damage
        if damage > 0:
            self.drawText(self.mainFont, "-"+str(damage)+"!", RED, recipient.rect.x, recipient.rect.y)
            self.dmgSound.play()
            self.damageCounter = True
            self.damageRecipient = recipient
            self.damageAmount = damage
            self.damageTimer = pygame.time.get_ticks()

    def spawnEnemy(self, hp, atk):
        image = random.choice(self.enemySprites)
        enemy = Enemy(hp, atk, image)
        self.all_sprites.add(enemy)
        return enemy

    def startMenu(self):
        running = True
        titleFont = self.getFont('FSEX302.ttf', 130)
        while running:
            self.clock.tick(FPS)
            # Process input (events)
            for event in pygame.event.get():
                # Check for closing window
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYUP:
                    running = False
            self.screen.fill(BLACK)
            self.drawText(titleFont, "SPELLER", WHITE, WIDTH / 2, HEIGHT * 0.25)
            self.drawText(self.mainFont, "PRESS ANY KEY TO CONTINUE", WHITE, WIDTH / 2, HEIGHT * 0.75)
            pygame.display.flip()

    def gameOverScreen(self):
        running = True
        while running:
            self.clock.tick(FPS)
            # Process input (events)
            for event in pygame.event.get():
                # Check for closing window
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYUP:
                    running = False
            self.screen.fill(BLACK)
            self.drawText(self.mainFont, "GAME OVER!", RED, WIDTH / 2, HEIGHT / 2)
            pygame.display.flip()

    def drawText(self, typeface, text, color, x, y):
        font = typeface
        fontSurface = font.render(text, True, color)
        fontRect = fontSurface.get_rect()
        fontRect.center = (x, y)
        self.screen.blit(fontSurface, fontRect)


# all_sprites = pygame.sprite.Group()
# bg_sprites = pygame.sprite.Group()
#
# letterlist = []
#
# board=[[0,0,0,0],
#        [0,0,0,0],
#        [0,0,0,0],
#        [0,0,0,0]]
#
# for row in range(0,len(board)):
#     for column in range(0,len(board[row])):
#         tileInfo = random.choice(list(LETTERSCORES.items()))
#         tile = Tile(tileInfo[0], str(tileInfo[1]), (WIDTH / 2) + (column * 70) + (column * 10) - 155, (HEIGHT * 0.75) + (row * 70) + (row * 10) - 155)
#         all_sprites.add(tile)
#         board[row][column] = tile
#
# selectedTile = board[currentY][currentX]
#
# enemyHealth = HealthBar(WIDTH * 0.75, 40, 0)
# playerHealth = HealthBar(WIDTH * 0.25, 40, 5)
#
# enemy = spawnEnemy(10, 10)
#
# player = Player(10)
# all_sprites.add(player)
#
# selection = Selection(selectedTile.rect.left - 5, selectedTile.rect.top + 5)
# bg_sprites.add(selection)
#
# hud = HUD()

# def spawnEnemy(hp, atk):
#     enemy = Enemy(hp, atk)
#     all_sprites.add(enemy)
#     return enemy

# def cancel():
#     print(letterlist)
#     for letter in letterlist[:]:
#         print(letter.letter, "removed")
#         letter.kill()
#         letterlist.remove(letter)
#     for row in board:
#         for column in row:
#             all_sprites.add(column)
#             column.selected = False

# def wordScore(inputList):
#     totalScore = 0
#     wordList = []
#     for tile in inputList:
#         totalScore += int(tile.score)
#         wordList.append(tile.letter.upper())
#     word = ''.join(wordList)
#     if len(word) > 2:
#         if word.lower() in WORDDICT:
#             for tile in inputList[:]:
#                 print(tile.letter, "removed")
#                 tile.kill()
#                 inputList.remove(tile)
#             for row in board:
#                 for column in row:
#                     if column.selected == True:
#                         column.randomise()
#                         all_sprites.add(column)
#                         column.selected = False
#             return word, totalScore
#         else:
#             return "WORD DOES NOT EXIST!", 0
#     else:
#         return "WORD TOO SHORT!", 0

# def damage(damage, recipient):
#     recipient.health -= damage

# def menu():
#     currentX = 0
#     currentY = 0
#     all_sprites = pygame.sprite.Group()
#     bg_sprites = pygame.sprite.Group()
#
#     running = True
#     while running:
#         clock.tick(FPS)
#         # Process input (events)
#         for event in pygame.event.get():
#             # Check for closing window
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#             if event.type == pygame.KEYUP:
#                 running = False
#         screen.fill(BLACK)
#
#         hud.displayWordScore("PRESS ANY KEY TO CONTINUE")
#         pygame.display.flip()


g = Game()
g.startMenu()
g.startBattle()
while g.running:
    if g.running:
        g.yourTurn()
    if g.running:
        g.theirTurn()
pygame.quit()
