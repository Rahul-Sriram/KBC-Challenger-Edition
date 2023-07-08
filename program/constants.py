import pygame
'''On my computer I tried finding out the actual time it takes to make FPS amount of Frames, turns out Real.FPS = 1.42 times FPS defined below'''
'''So suppose you want 30 frames per second, then make this FPS below as 30 x 1.42'''

FPS = 45 * 1.42

# 30 CHARS FOR OPTIONS
#157 CHARS FOR QUESTION
#180 CHARS FOR DIALOGUE

pygame.mixer.init()

### CONSTANTS ###

WINDOWWIDTH = 1280
WINDOWHEIGHT = 800

PADDING = 160
DIALOGUEPADDING = 20

DIALOGUEwidth = WINDOWWIDTH - 2*(PADDING) 
DIALOGUEheight = 230

DIALOGUEx = (WINDOWWIDTH - DIALOGUEwidth) / 2 #180
DIALOGUEy = (WINDOWHEIGHT - DIALOGUEheight) - DIALOGUEPADDING #for bottom border

### COLORS ###

BGCOLOR   = [ 36,   7,  75 ] # 36, 7, 75 or 42, 26, 69
QUESCOLOR = [ 50,  10, 100 ]
GOLDBORDER =[233, 192,  61 ]

BLACK     = [  0,   0,   0 ]

RED       = [255,   0,   0 ]
YELLOW    = [255, 255,   0 ]
GREEN     = [  0, 255,   0 ]
CYAN      = [  0, 255, 255 ]
BLUE      = [  0,   0, 255 ]
VIOLET    = [255,   0, 255 ]

MONEYGREEN = [15, 176, 133 ]
WHITE     = [255, 255, 255 ]

QuestionCoordinates = (100, 100, (WINDOWWIDTH - 200), 200)

### AMITABH VALUES ###

abPosition = (200, WINDOWHEIGHT - DIALOGUEheight + DIALOGUEPADDING)
abImage = pygame.image.load("images//amitabh.png")
optionBoxPositions = [(100, 400), (WINDOWWIDTH/2 + DIALOGUEPADDING, 400),
                      (100, 460), (WINDOWWIDTH/2 + DIALOGUEPADDING, 460)]

lockPositions = [(WINDOWWIDTH/2 - 60, WINDOWHEIGHT/2 + 120)]
lockDimensions =[(120, 40)]

logoImage = pygame.image.load("images//kbcLogo.jpg")
logoRect = logoImage.get_rect()
logoHeight, logoWidth = logoImage.get_width(), logoImage.get_height()

logoPositions = (0,0)#(((WINDOWWIDTH//2) - (logoWidth//2)), ((WINDOWHEIGHT//2) - (logoHeight//2)))


### AUDIO OBJECTS SETUP ###

bgmSound = pygame.mixer.Sound("audio//bgmKBC.wav")
introSound = pygame.mixer.Sound("audio//introKBC.wav")
nextqSound = pygame.mixer.Sound("audio//nextQKBC.wav")

pafSound = pygame.mixer.Sound("audio//phoneAFriendKBC.wav")
apSound = pygame.mixer.Sound("audio//audiencePollKBC.wav")
fiftySound = pygame.mixer.Sound("audio//fiftyKBC.wav")
suspSound = pygame.mixer.Sound("audio//suspenseKBC.wav")

lockSound = pygame.mixer.Sound("audio//lockKBC.wav")
lostSound = pygame.mixer.Sound("audio//lostKBC.wav")
amitabhSound = pygame.mixer.Sound("audio//amitabhKBC.wav")


