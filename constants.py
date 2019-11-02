import json

LETTERSCORES = {'A': 1,
'B': 3,
'C': 3,
'D': 2,
'E': 1,
'F': 4,
'G': 2,
'H': 4,
'I': 1,
'J': 8,
'K': 5,
'L': 1,
'M': 3,
'N': 1,
'O': 1,
'P': 3,
'Q': 10,
'R': 1,
'S': 1,
'T': 1,
'U': 1,
'V': 4,
'W': 4,
'X': 8,
'Y': 4,
'Z': 10
}

VOWELSCORES = { 'A': 1,
'E': 1,
'I': 1,
'O': 1,
'U': 1
}

WIDTH = 1280
HEIGHT = 720
FPS = 30

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

WORDDICT = json.load(open("words_dictionary.json", "r"))
