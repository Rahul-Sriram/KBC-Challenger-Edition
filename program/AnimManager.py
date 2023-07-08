from animationManager import *

# RULES FOR MAKING AnimationProcesses:
# 1) An AnimationProcesses list will add Animations to a corresponding AnimationQueue
# 2) An AnimationQueue can have atmost 1 AmitabhObject. Having more than one will cause the program to malfunction.
# 3) Order Matters! Make sure to add the Objects in the correct order to avoid overlapping during GameLoop
# 4) You have to import the needed AnimationQueue to execute the corresponding AnimationProcesses block

'''SPECIAL NOTE: HAVING A A.Q WITH ONLY ONE AMITABH OBJECT WILL NOT LOOK GOOD. THERE WONT BE ANY DIALOGUE BOX, SO MAKE SURE TO INCLUDE IT AS WELL'''

"""ULTRA SPECIAL NOTE: To enhance performance of Q&A Objects, make the corresponding AnimationQueue as simple as possible..."""


def lambda_type_Amitabh(correctIndex, buttonObject, AnimationPool, text = 'That was incorrect! The correct option was'):
    if type(buttonObject) != int:
        if buttonObject.optionIndex == correctIndex:
            lambda_Amitabh = []
            make_AmitabhSpeak("{} {}: {}".format(text, OptionButton.indextoAlpha[correctIndex], buttonObject.text), 25, WHITE, lambda_Amitabh)
            for i in lambda_Amitabh:
                AnimationPool.append(i)
    
    else:
        lambda_Amitabh = []
        make_AmitabhSpeak("{}".format(text), 25, WHITE, lambda_Amitabh)
    
        for i in lambda_Amitabh:
            AnimationPool.append(i)

def lambda_lifelines(phone, gp, fifty, gf, poll, gpll, AnimationPool):
    if phone and (gp == 0):
        lambda_phone = []
        make_Lifeline(0, lambda_phone)
        for i in lambda_phone:
            AnimationPool.append(i)

    if fifty and (gf == 0):
        lambda_fifty = []
        make_Lifeline(1, lambda_fifty)
        for i in lambda_fifty:
            AnimationPool.append(i)

    if poll and (gpll == 0):
        lambda_poll = []
        make_Lifeline(2, lambda_poll)
        for i in lambda_poll:
            AnimationPool.append(i)

def lambda_money(moneyIndex, AnimationPool, fontsize = 40, ycoord = 50, credit = False):
    import moneyTree
    money = moneyTree.MoneyValueHashmap[moneyIndex]
    lambdaMoney = []
    if not credit:
        make_Money("This Question: ₹" + money, lambdaMoney, fontsize = fontsize, MoneyYcord= ycoord)
    else:
        make_Money("₹" + money, lambdaMoney, fontsize = fontsize, MoneyYcord= ycoord)
    for i in lambdaMoney:
        AnimationPool.append(i)


### ANIMATION QUEUE SETUP ###

InitAnims = []

Dialogue1 = []
Dialogue2 = []
Dialogue3 = []
Dialogue4 = []
Dialogue5 = []

Question1 = []
Question2 = []
Question3 = []
Question4 = []
Question5 = []

Question6 = []
Question7 = []
Question8 = []
Question9 = []
Question10 = []

Question11 = []
Question12 = []
Question13 = []
Question14 = []
Question15 = []

### ANIMATION PROCESSES SETUP ###
""" These AnimationProcessesX in the end will not be used. However we implement this way to make the code more readable and group together similar commands"""
# Example

make_Logo(InitAnims)

Process0 = [make_AmitabhSpeak('Hello! This is Amitabh Bachchan! The founder of this beautiful game Kaun Banega Krorepati', 25, WHITE, Dialogue1)]
Process1 = [make_AmitabhSpeak('Are you ready to play this AMAZING game?', 25, WHITE, Dialogue2)]
Process2 = [make_AmitabhSpeak('Congratulations so far. You have Rs.10,000 right now. Good Luck in answering the next questions, and becoming a CROREPATI!', 25, WHITE, Dialogue3)]
Process3 = [make_AmitabhSpeak('You are amazing! You have come so far, and you have Rs.3,20,000 with you. Just 5 more questions and you are a CROREPATI!', 25, MONEYGREEN, Dialogue4)]
Process4 = [make_AmitabhSpeak('This is the last question... You are THIS close to becoming a CROREPATI... But beware... It won\'t be that easy... ALL THE BEST!', 25, WHITE, Dialogue5, bordercolor= GOLDBORDER)]

### RANDOMIZING THE QUESTIONS ###

with open('.\\files\\questions.dat.dat', 'rb') as questions_file:
    from pickle import load
    questions_list = load(questions_file)

import random

i = 1
while i <= 15:
    random_question = questions_list.pop(random.randint(0, len(questions_list)-1))
    Process_Random = [make_QA(random_question[0], random_question[1], int(random_question[2]), eval('Question{}'.format(i)))]
    i += 1

### TESTING ###

AnimationPool = [InitAnims, Dialogue1, Dialogue2] + [eval('Question{}'.format(i)) for i in range(1, 6)]\
            + [Dialogue3] + [eval('Question{}'.format(i)) for i in range(6, 11)]\
            + [Dialogue4] + [eval('Question{}'.format(i)) for i in range(11, 15)]\
            + [Dialogue5] + [eval('Question{}'.format(i)) for i in range(15, 16)]


#=NOTE=#=NOTE=#=NOTE=#=NOTE=#=NOTE=#=NOTE=#=NOTE=#=NOTE=#=NOTE=#=NOTE=#=NOTE=#=NOTE=#=NOTE=#=NOTE=#=NOTE=#=NOTE=#=NOTE=#=NOTE=#

### Credits POOL ###

# Headings will be make_Money(text, AnimQ), while text will be make_TextObject(title, font, fontsize, fontcolor, backcolor, xpos, ypos, AnimationQueue)

paddedWDH = WINDOWHEIGHT - (WINDOWHEIGHT//15)
FourTierCreditsYCORDS = [WINDOWHEIGHT//15, WINDOWHEIGHT//15 + 0.25*paddedWDH, WINDOWHEIGHT//15 + 0.50*paddedWDH, WINDOWHEIGHT//15 + 0.75*paddedWDH]

GOSurf = []
Text1 = []
Text2 = []

Process0 = [make_Money("GAME OVER", GOSurf, GOLDBORDER, 60),
            make_creditSubclass('', ['YOU EARNED'], 20, 50, FourTierCreditsYCORDS[1] - 100, GOSurf),
            make_creditSubclass('', ['----------------------------','','Press Enter to continue to credits','','Press Esc to quit game'], 20, 30, FourTierCreditsYCORDS[2], GOSurf, textColor= WHITE)]

Process1 = [make_creditSubclass('CREATED BY', ['Rahul Sriram', 'Joel Alphonso'], 40, 30, FourTierCreditsYCORDS[0], Text1),
            make_creditSubclass('DEVELOPERS', ['Joel Alphonso', 'Rahul Sriram'], 40, 30, FourTierCreditsYCORDS[1], Text1),
            make_creditSubclass('FRONT-END', ['Rahul Sriram'], 40, 30, FourTierCreditsYCORDS[2], Text1),
            make_creditSubclass('BACK-END', ['Joel Alphonso'], 40, 30, FourTierCreditsYCORDS[3], Text1)]

Process2 = [make_creditSubclass('IMAGES & EDITING', ['Naresh Ramesh'], 40, 30, FourTierCreditsYCORDS[0], Text2),
            make_creditSubclass('MUSIC & SFX', ['Rahul Sriram'], 40, 30, FourTierCreditsYCORDS[1], Text2),
            make_creditSubclass('CONTRIBUTORS', ['Naresh Ramesh', 'Aryan Bhoraskar'], 40, 30, FourTierCreditsYCORDS[2], Text2),
            make_creditSubclass('INSPIRED BY', ['Undertale - Toby Fox', 'KBC 2020 - Rima Patira'], 40, 30, FourTierCreditsYCORDS[3], Text2)]


CreditPool = [GOSurf, Text1, Text2]