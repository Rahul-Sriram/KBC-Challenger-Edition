from classDefinitions import *
from constants import *

def make_TextObject(title, font, fontsize, fontcolor, backcolor, xpos, ypos, AnimationQueue):
    TextObject = Text(title, font, fontsize, fontcolor, backcolor, xpos, ypos)
    add_to_AnimationQueue(TextObject, AnimationQueue)

def make_ImageObject(image, positions, AnimationQueue):
    ImageObject = Image(image, positions)
    add_to_AnimationQueue(ImageObject, AnimationQueue)
    
def make_dialogueObject(bgcolor, bordercolor, borderwidth, xTL, yTL, width, height, AnimationQueue):
    DialogueObject = Dialogue(bgcolor, bordercolor, borderwidth, xTL, yTL, width, height)
    add_to_AnimationQueue(DialogueObject, AnimationQueue)

def make_AmitabhObject(dialogue, fontsize, fontcolor, AnimationQueue):
    AmitabhObject = Amitabh(dialogue, fontsize, fontcolor)
    add_to_AnimationQueue(AmitabhObject, AnimationQueue)

def make_QuestionObject(bgcolor, borderwidth, bordercolor, questiontext, AnimationQueue):
    QuestionObject = QuestionBox(bgcolor, borderwidth, bordercolor, questiontext)
    add_to_AnimationQueue(QuestionObject, AnimationQueue)

def make_4OptionsObject(listofoptions, color, borderwidth, bordercolor, textcolor, AnimationQueue):
    height = 40
    for option in range(len(listofoptions)):
        x, y = optionBoxPositions[option]
        text = listofoptions[option]
        optionIndex = option
        OptionObject = OptionButton(x, y, height, color, borderwidth, bordercolor, text, optionIndex, textcolor)
        add_to_AnimationQueue(OptionObject, AnimationQueue)

def make_AmitabhSpeak(dialogue, fontsize, fontcolor, AnimationQueue, bgcolor = BLACK, bordercolor = WHITE, borderwidth = 10, xTL = DIALOGUEx, yTL = DIALOGUEy, width = DIALOGUEwidth, height = DIALOGUEheight):
    make_dialogueObject(bgcolor, bordercolor, borderwidth, xTL, yTL, width, height, AnimationQueue)
    make_ImageObject(abImage, abPosition, AnimationQueue)
    make_AmitabhObject(dialogue, fontsize, fontcolor, AnimationQueue)

def make_Logo(AnimationQueue):
    logoObject = Image(logoImage, logoPositions)
    add_to_AnimationQueue(logoObject, AnimationQueue)

def make_Lifeline(lifelinerIndex, AnimationQueue):
    lifelineObject = Lifeline(lifelinerIndex)
    add_to_AnimationQueue(lifelineObject, AnimationQueue)

def make_LockObject(AnimationQueue):
    lockObject = LockButton(False)
    add_to_AnimationQueue(lockObject, AnimationQueue)

def make_Money(text, AnimationQueue, color = MONEYGREEN, fontsize = 40, MoneyYcord = 50):
    moneyText = Text(text, fontsize, 10, color, WINDOWWIDTH/2, MoneyYcord)
    add_to_AnimationQueue(moneyText, AnimationQueue)

def make_creditSubclass(headingText, listoftext, headingSize, textSize, headingY, AnimationQueue, headingColor = GOLDBORDER, textColor = YELLOW):
    moneyText = Text(headingText, headingSize, 5, headingColor, WINDOWWIDTH/2 , headingY)
    add_to_AnimationQueue(moneyText, AnimationQueue)
    for i in range(len(listoftext)):
        
        textText = Text(listoftext[i], textSize, 1, textColor, WINDOWWIDTH/2, moneyText.ypos + headingSize + 30 + (i*textSize + 5))
        add_to_AnimationQueue(textText, AnimationQueue)

def make_QA(questiontext, listofoptions, AnswerIndex, AnimationQueue, textcolor = WHITE, bgcolor = QUESCOLOR, bordercolor = GOLDBORDER):
    make_QuestionObject(bgcolor, 5, bordercolor, questiontext, AnimationQueue)
    make_4OptionsObject(listofoptions, bgcolor, 3, bordercolor, textcolor, AnimationQueue)
    make_LockObject(AnimationQueue)
    prefix_AnimationQueue(AnswerIndex, AnimationQueue)

def prefix_AnimationQueue(Index, AnimationQueue):
    AnimationQueue.insert(0, (Index,))

def add_to_AnimationQueue(Object, AnimationQueue):
    AnimationQueue.append(Object)
