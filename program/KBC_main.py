import pygame, sys
from pygame.locals import * 
from classDefinitions import *
from constants import *
import AnimManager

from time import sleep

### INITIALIZATIONS ###

pygame.init()
pygame.mixer.init()

### ANIMATION POOL INITIALIZATION ###

AnimationPool = AnimManager.AnimationPool
Credits = False
AnimationPoolPointer = 0
AnimationManager = AnimationPool[AnimationPoolPointer]

### FPS CLOCK ###

FPSCLOCK = pygame.time.Clock()

### DISPLAY SETUP ###

DISPLAY = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption('KAUN BANEGA CROREPATI')
DISPLAY.fill(BGCOLOR)

MONITOR_SIZE = [pygame.display.Info().current_w, pygame.display.Info().current_h]
FULLSCREEN = True

### FUNCTIONS ####

def checkForKeyPress(choiceTakenArg = None):
    global GlobalLocked, initCHANNELFlag, DialogueFlag, confirmationProceedToCredits

    if choiceTakenArg:
        return 123456789
 
    if len(pygame.event.get(QUIT)) > 0:
        pygame.quit()
        sys.exit()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0: return None

    if keyUpEvents[0].key == K_ESCAPE:
        pygame.quit(); sys.exit()

    if keyUpEvents[0].key == K_RETURN and (GlobalLocked or initCHANNELFlag or DialogueFlag):
        global AnimationPool, AnimationPoolPointer, Credits, AnimationManager

        if not confirmationProceedToCredits:
            restoreGlobalValues()
            initCHANNELFlag = False

            if bug1Flag:
                quit()

            if AnimationPoolPointer < len(AnimationPool)-1:
                AnimationPoolPointer += 1

            else:
                global MoneyIndexValue
                AnimationPool = AnimManager.CreditPool
                AnimationPoolPointer = 0
                MoneyIndexValue += 1
                AnimationManager = AnimationPool[AnimationPoolPointer]
                Credits = True
                showCredits()

        else:
            AnimationPool = AnimManager.CreditPool
            AnimationPoolPointer = 0
            AnimationManager = AnimationPool[AnimationPoolPointer]
            Credits = True
            
            showCredits()

    if keyUpEvents[0].key == K_F11:
        global FULLSCREEN
        FULLSCREEN = not FULLSCREEN
        if FULLSCREEN: DISPLAY = pygame.display.set_mode(MONITOR_SIZE, pygame.FULLSCREEN)
        else: DISPLAY = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), pygame.RESIZABLE)
    
    return keyUpEvents[0].key


def showCredits():

    global CHANNEL_backtrackbusy, CHANNEL_backtrack, AnimationPoolPointer
    
    stopCHANNELS('backtrack')
    CHANNEL_backtrack.play(bgmSound)
    AnimManager.lambda_money(MoneyIndexValue-1, AnimationPool[0], fontsize = 70, ycoord = WINDOWHEIGHT//2.5, credit = True)
    
    def checkForKeyPressWithinCredits():
        
        if len(pygame.event.get(QUIT)) > 0:
            pygame.quit()
            sys.exit()

        keyUpEvents = pygame.event.get(KEYUP)
        if len(keyUpEvents) == 0: return None

        if keyUpEvents[0].key == K_ESCAPE:
            pygame.quit(); sys.exit()
        
        if keyUpEvents[0].key == K_RETURN:
            global AnimationPoolPointer
            if AnimationPoolPointer < len(AnimationPool)-1:
                AnimationPoolPointer += 1
            else: pygame.quit(); sys.exit()
        
        if keyUpEvents[0].key == K_F11:
            global FULLSCREEN
            FULLSCREEN = not FULLSCREEN
            if FULLSCREEN: DISPLAY = pygame.display.set_mode(MONITOR_SIZE, pygame.FULLSCREEN)
            else: DISPLAY = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), pygame.RESIZABLE)
        
        return keyUpEvents[0].key

    while True:
        
        if not CHANNEL_backtrack.get_busy():
            CHANNEL_backtrack.play(bgmSound)

        DISPLAY.fill(BGCOLOR)
        
        AnimationManager = AnimationPool[AnimationPoolPointer]

        for animation in AnimationManager:
            animation.draw(DISPLAY)
            checkForKeyPressWithinCredits()

        pygame.display.update()
        FPSCLOCK.tick(FPS)

        for animation in AnimationManager:
            if checkForKeyPressWithinCredits():  
                pygame.event.get() # clear event queue

            

### initialize Mixer Channels ###

initCHANNELFlag = True

CHANNEL_backtrack = pygame.mixer.Channel(1)
CHANNEL_backtrackbusy = pygame.mixer.Channel(1).get_busy()

CHANNEL_intro = pygame.mixer.Channel(2)
CHANNEL_introbusy = pygame.mixer.Channel(2).get_busy()

CHANNEL_locktrack = pygame.mixer.Channel(3)

CHANNEL_nextQtrack = pygame.mixer.Channel(4)

CHANNEL_wintrack = pygame.mixer.Channel(5)

CHANNEL_phoneAFriend = pygame.mixer.Channel(6)
CHANNEL_audiencePoll = pygame.mixer.Channel(7)

if initCHANNELFlag: CHANNEL_intro.play(introSound); CHANNEL_intro.set_volume(0.7)

#=======================================================#
### GAME LOOP ========================================###
#=======================================================#

def stopCHANNELS(exceptionChannel):
    CHANNELHashMap = {'intro' :CHANNEL_intro, "backtrack" :CHANNEL_backtrack, "nextq" :CHANNEL_nextQtrack, "wintrack" :CHANNEL_wintrack,
                      "paf" :CHANNEL_phoneAFriend, "lock": CHANNEL_locktrack, "poll": CHANNEL_audiencePoll}
    for i in CHANNELHashMap:
        if exceptionChannel != i:
            CHANNELHashMap[i].stop()

def restoreGlobalValues():
    global optionClickedIndex, questionAnswerIndex, GlobalOptionClicked, GlobalLocked, Locked_i
    global GlobalCorrect, Correct_i, alreadyChosen, WinOptionFlag, LifeLines_blitter
    global DialogueFlag, Money_blitter, avoidOverridingBackTrack

    CHANNEL_intro.stop()
    if not avoidOverridingBackTrack:
        CHANNEL_backtrack.stop()
    avoidOverridingBackTrack = not avoidOverridingBackTrack
    CHANNEL_locktrack.stop()
    CHANNEL_nextQtrack.stop()
    CHANNEL_wintrack.stop()
    CHANNEL_phoneAFriend.stop()
    CHANNEL_audiencePoll.stop()

    optionClickedIndex, questionAnswerIndex, GlobalOptionClicked, GlobalLocked, Locked_i, GlobalCorrect, Correct_i, alreadyChosen, WinOptionFlag, LifeLines_blitter = None, -1, False, False, 0, "not defined yet", 0, False, "not defined yet", 0
    DialogueFlag, Money_blitter = False, 0


def phoneAFriendFN(correctIndex):
    CHANNEL_phoneAFriend.play(pafSound)
    stopCHANNELS('paf')
    optionsList = [animation.optionIndex for animation in AnimationManager if type(animation) == OptionButton]

    friendOpted = friend_randomizer(correctIndex, optionsList)
    for animation in AnimationManager:
        if type(animation) == OptionButton:
            if animation.optionIndex == friendOpted:
                animation.friended = True
    sleep(pafSound.get_length())

def audiencePollFN(correctIndex):
    CHANNEL_audiencePoll.play(apSound)
    stopCHANNELS('poll')
    optionsList = [animation.optionIndex for animation in AnimationManager if type(animation) == OptionButton]

    audienceOpted = poll_randomizer(correctIndex, optionsList)
    for animation in AnimationManager:
        if type(animation) == OptionButton:
            if animation.optionIndex == audienceOpted:
                animation.polled = True
    sleep(apSound.get_length())
    
def fiftyfiftyFN(correctIndex):
    global AnimationManager
    delCount = 0
    for animation in AnimationManager:
        if type(animation) == OptionButton and delCount < 2:
            if animation.optionIndex != correctIndex:
                del AnimationManager[AnimationManager.index(animation)]
                delCount += 1
    sleep(1)
    CHANNEL_intro.play(fiftySound)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


bug1Flag = False

DialogueFlag = False
optionClickedIndex = None
questionAnswerIndex = -1
MoneyIndexValue = 0

confirmationProceedToCredits = False
avoidOverridingBackTrack = False

Money_blitter = 0
LifeLines_blitter = 0

PHONE = True
FIFTY = True
POLL = True
GlobalPHONE = 0
GlobalFIFTY = 0
GlobalPOLL = 0

GlobalOptionClicked = False
GlobalLocked = False
GlobalCorrect = "not defined yet"

OptionClickable = True

Correct_i = 0
Locked_i = 0
alreadyChosen = False
WinOptionFlag = "not defined yet"

while True:

    CHANNEL_backtrackbusy = pygame.mixer.Channel(1).get_busy()
    
    if not CHANNEL_backtrackbusy and not alreadyChosen:
        if type(AnimationManager[0])== Dialogue:
            if type(AnimationPool[AnimationPoolPointer+1][0])!=Dialogue:
                avoidOverridingBackTrack = False
            else:
                avoidOverridingBackTrack = True
                CHANNEL_backtrack.play(bgmSound)
                CHANNEL_backtrack.set_volume(0.3)
        elif GlobalLocked:
            CHANNEL_backtrack.set_volume(0.7)
            CHANNEL_backtrack.play(suspSound)
        elif not initCHANNELFlag:
            CHANNEL_backtrack.set_volume(0.3)
            CHANNEL_backtrack.play(suspSound)

    if GlobalLocked and Locked_i == 0:
        CHANNEL_locktrack.play(lockSound)
        Locked_i += 1

        alreadyChosen = True
        CHANNEL_backtrack.stop()
        
        sleep(3)
        
        if GlobalCorrect == True and Correct_i == 0:
            WinOptionFlag = True
            CHANNEL_wintrack.play(introSound)
            Correct_i += 1
            for animation in AnimationManager:
                if type(animation) == Text:
                    AnimManager.lambda_type_Amitabh(1, 1, AnimationPool[AnimationPoolPointer], "Congratulations! That was the right answer! Here is {}".format(animation.text.replace("This Question: ₹", "Rs.")))
                    import moneyTree
                    animation.textcolor = GOLDBORDER
                    animation.text = "YOU HAVE: ₹{}".format(moneyTree.MoneyValueHashmap[MoneyIndexValue].replace('_',','))

        elif GlobalCorrect == False and Correct_i == 0:
            WinOptionFlag = False
            CHANNEL_wintrack.play(lostSound)
            Correct_i += 1
            for animation in AnimationManager:
                if type(animation) == OptionButton:
                    AnimManager.lambda_type_Amitabh(questionAnswerIndex, animation, AnimationPool[AnimationPoolPointer])
            confirmationProceedToCredits = True

        else:
            AnimManager.lambda_type_Amitabh(1, 1, AnimationPool[AnimationPoolPointer], "Nice! You found a bug in the game. Well, it was intentional (cuz I was lazy to code it) but to reward you, look into your game folder =)")
            make_reward_for_finding_bug()
            bug1Flag = True

    DISPLAY.fill(BGCOLOR)

    for animation in AnimationManager:
        if type(animation) != tuple:
            animation.draw(DISPLAY)
            checkForKeyPress()

        else:
            MoneyIndexValue += 1
            if LifeLines_blitter == 0:
                AnimManager.lambda_lifelines(PHONE, GlobalPHONE, FIFTY, GlobalFIFTY, POLL, GlobalPOLL, AnimationPool[AnimationPoolPointer])
                LifeLines_blitter += 1
            
            if Money_blitter == 0:
                AnimManager.lambda_money(MoneyIndexValue, AnimationPool[AnimationPoolPointer])
                Money_blitter += 1

            CHANNEL_nextQtrack.play(nextqSound)
            questionAnswerIndex = animation[0]
            del AnimationManager[AnimationManager.index(animation)]

    AnimationManager = AnimationPool[AnimationPoolPointer]
    
    # POST UPDATE CASES #

    pygame.display.update()
    FPSCLOCK.tick(FPS)

    for event in pygame.event.get():
    
        pos = pygame.mouse.get_pos()
        checkForKeyPress()
        
        for animation in AnimationManager:

            if checkForKeyPress():  
                pygame.event.get() # clear event queue 
            
            if type(animation) == OptionButton and OptionClickable:

                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if animation.isOver(pos) and not GlobalLocked:
                        animation.color = YELLOW
                        animation.textcolor = BLACK
                        animation.isclicked = True
                        GlobalOptionClicked = True
                        optionClickedIndex = animation.optionIndex

                if (event.type == pygame.MOUSEMOTION and not animation.isclicked and not GlobalLocked) or (animation.optionIndex != optionClickedIndex):
                    if animation.isOver(pos):
                        animation.color = BLUE
                        animation.textcolor = WHITE
                    elif animation.polled:
                        animation.color = VIOLET
                        animation.textcolor = WHITE
                    elif animation.friended:
                        animation.color = CYAN
                        animation.textcolor = BLACK
                    else:
                        animation.color = QUESCOLOR
                        animation.textcolor = WHITE
                     
            elif type(animation) == LockButton:
                GlobalLocked = animation.locked
                
                if event.type == pygame.MOUSEBUTTONDOWN and not alreadyChosen:
                    if animation.isOver(pos):
                        animation.color = RED if not animation.locked else BGCOLOR
                        animation.textcolor = WHITE if not animation.locked else RED
                        animation.locked = not animation.locked
                        animation.text = "LOCK" if not animation.locked else "LOCKED"


                if event.type == pygame.MOUSEMOTION and not animation.locked:
                    if animation.isOver(pos):
                        animation.color = BLUE
                    else:
                        animation.color = BGCOLOR

            
            elif type(animation) == QuestionBox:
                if WinOptionFlag == True:
                    animation.bgcolor = GREEN
                    animation.fontcolor = BLACK
                elif WinOptionFlag == False:
                    animation.bgcolor = RED
                    animation.fontcolor = WHITE    

            elif type(animation) == Lifeline:
                if animation.lifeliner == 0 and animation.isclicked and GlobalPHONE == 0:
                    phoneAFriendFN(questionAnswerIndex)
                    PHONE = False
                    GlobalPHONE += 1

                elif animation.lifeliner == 1 and animation.isclicked and GlobalFIFTY == 0:
                    fiftyfiftyFN(questionAnswerIndex)
                    FIFTY = False
                    GlobalFIFTY += 1

                elif animation.lifeliner == 2 and animation.isclicked and GlobalPOLL == 0:
                    audiencePollFN(questionAnswerIndex)
                    POLL = False
                    GlobalPOLL += 1
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if animation.isOver(pos) and not GlobalLocked:
                        animation.color = YELLOW
                        animation.textcolor = BLACK
                        animation.isclicked = True

                if (event.type == pygame.MOUSEMOTION) and not animation.isclicked:
                    if animation.isOver(pos):
                        animation.color = GOLDBORDER
                        animation.textcolor = WHITE
                    else:
                        animation.color = BGCOLOR
                        animation.textcolor = WHITE

            elif type(animation) == Dialogue:
                DialogueFlag = True

    if GlobalLocked:
        if optionClickedIndex == questionAnswerIndex:
            GlobalCorrect = True
        elif optionClickedIndex in {0,1,2,3}:
            GlobalCorrect = False
    
