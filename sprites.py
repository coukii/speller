import pygame
from constants import *

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
        self.letterFont = pygame.font.SysFont('Times New Roman', 36)
        self.scoreFont = pygame.font.SysFont('Times New Roman', 16)
        self.letter = letter
        self.score = score
        self.letterRender = self.letterFont.render(self.letter, True, BLACK)
        self.scoreRender = self.scoreFont.render(self.score, True, BLACK)
        self.selected = False
        #pygame.display.update
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
        # print(letterlist[len(letterlist)-1].letter)
        all_sprites.add(spelltile)
        print()
        for i in letterlist:
            print(i.letter, ":", str(i.score), end=' ')
    def randomise(self):
        tileInfo = random.choice(list(LETTERSCORES.items()))
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

class HUD:
    def __init__(self):
        self.font = pygame.font.Font('FSEX302.ttf', 50)
        self.lastUpdate = 0
    def displayWordScore(self, text):
        self.now = pygame.time.get_ticks()
        self.textSurface = self.font.render(text, False, WHITE)
        self.textRect = self.textSurface.get_rect()
        self.textRect.center = (WIDTH / 2, HEIGHT / 2)
        if self.now - self.lastUpdate > 300:
            self.lastUpdate = self.now
            screen.blit(self.textSurface, self.textRect)

        # self.last = pygame.time.get_ticks()
        # now = pygame.time.get_ticks()
    def update(self):
        pass
