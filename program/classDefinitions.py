import pygame
from constants import *
pygame.mixer.init()

class Text:
    def __init__ (self, text, fontsize, bold, textcolor, xpos, ypos):
        self.text = text.replace('_',',')
        self.fontsize = fontsize
        self.textcolor = textcolor
        self.backcolor = BGCOLOR
        self.bold = bold
        self.xpos = xpos
        self.ypos = ypos
        
    def draw(self, display):
        Font = pygame.font.SysFont('calibri', self.fontsize, self.bold)
        textsurf = Font.render(self.text, True, self.textcolor, self.backcolor) if self.backcolor else Font.render(self.text, True, self.textcolor) 
        textrect = textsurf.get_rect()
        textrect.topleft = (self.xpos - textsurf.get_width()/2, self.ypos - textsurf.get_height()/2)
        display.blit(textsurf, textrect)

class Image:
    def __init__(self, image, positions):
        self.image = image
        self.positions = positions

    def draw(self, display):
        display.blit(self.image, self.positions)

class Rectangle:
    def __init__(self, color, positions):
        self.color = color
        self.positions = positions

    def draw(self, display):
        pygame.draw.rect(display, self.color, (self.positions[0], self.positions[1], logoWidth, logoHeight), 0)
        
class Dialogue:

    def __init__ (self, bgcolor, bordercolor, borderwidth, xTL, yTL, width, height):
        self.bgcolor = bgcolor
        self.bordercolor = bordercolor
        self.borderwidth = borderwidth
        self.xtopleft = xTL
        self.ytopleft = yTL
        self.width = width
        self.height = height
        
    def draw(self, display):
        pygame.draw.rect(display, self.bordercolor, (self.xtopleft - self.borderwidth, self.ytopleft - self.borderwidth, self.width + (2*self.borderwidth), self.height + (2*self.borderwidth)), 0)
        pygame.draw.rect(display, self.bgcolor, (self.xtopleft, self.ytopleft, self.width, self.height), 0)
        

class Amitabh:

    amitabhPointer = 0
    def __init__ (self, dialogue, fontsize, fontcolor):
        self.dialogue = dialogue
        self.fontsize = fontsize
        self.fontcolor = fontcolor
        self.pointer = Amitabh.amitabhPointer
        self.yincr = 0
        self.last_slice = ""
        self.i = 0
        self.j = 0
        self.history = []
        self.cache_string_list = []

        step = 45
        i = 0

        while i <= len(self.dialogue):

            subtext = self.dialogue[i:i+step][::-1]
            if len(subtext) >= step:
                spaceindex = subtext.find(' ')
                revsubtext = subtext[::-1]
                finaltext = revsubtext[:len(revsubtext)-spaceindex]
                i -= spaceindex
                self.cache_string_list.append(finaltext)
                i += step
            else:
                self.cache_string_list.append(subtext[::-1])
                i += step
        else:
            if len(self.dialogue) - i <= step:
                self.cache_string_list.append(self.dialogue[i:])

        
    def draw(self, display):
        Font = pygame.font.Font("fonts//DTM-Mono.ttf", self.fontsize)
        for i in self.history:
            textsurf = Font.render(i[0], True, self.fontcolor)
            textrect = textsurf.get_rect()
            textrect.topleft = (abPosition[0] + 200, i[1])
            display.blit(textsurf, textrect)
        
        line = self.cache_string_list[self.i]
        letter = line[:self.j]
        textsurf = Font.render(letter, True, self.fontcolor)
        textrect = textsurf.get_rect()
        textrect.topleft = (abPosition[0] + 200, abPosition[1] + self.yincr)
        display.blit(textsurf, textrect)
        
        if self.last_slice != letter:
            amitabhSound.play()
            self.last_slice = letter
            
        self.j += 1
        
        if (self.j > len(line)) and (len(self.cache_string_list) > (self.i + 1)):
            self.history.append((line, abPosition[1] + self.yincr))
            self.i += 1
            self.j = self.j % len(line)
            self.yincr += 40


class QuestionBox:
    QuestionNumber = 1
    def __init__(self, bgcolor, borderwidth, bordercolor, questiontext = ""):
        self.bgcolor = bgcolor
        self.borderwidth = borderwidth
        self.bordercolor = bordercolor
        self.questiontext = "Q{}: ".format(QuestionBox.QuestionNumber) + questiontext
        QuestionBox.QuestionNumber += 1

        self.fontsize = 30
        self.fontcolor = WHITE
        self.yincr = 0
        self.last_slice = ""
        self.i = 0
        self.j = 0
        self.history = []
        self.cache_string_list = []
        
        step = 55
        i = 0

        while i <= len(self.questiontext):

            subtext = self.questiontext[i:i+step][::-1]
            if len(subtext) >= step:
                spaceindex = subtext.find(' ')
                revsubtext = subtext[::-1]
                finaltext = revsubtext[:len(revsubtext)-spaceindex]
                i -= spaceindex
                self.cache_string_list.append(finaltext)
                i += step
            else:
                self.cache_string_list.append(subtext[::-1])
                i += step
        else:
            if len(self.questiontext) - i <= step:
                self.cache_string_list.append(self.questiontext[i:])
        
        self.xpos, self.ypos, self.width, self.height = QuestionCoordinates


    def draw(self, display):
        pygame.draw.rect(display, self.bordercolor, (self.xpos - self.borderwidth, self.ypos- self.borderwidth, self.width + (2*self.borderwidth), self.height + (2*self.borderwidth)), 0)
        pygame.draw.rect(display, self.bgcolor, (self.xpos, self.ypos, self.width, self.height), 0)

        Font = pygame.font.Font("fonts//DTM-Mono.ttf", self.fontsize)
        for i in self.history:
            textsurf = Font.render(i[0], True, self.fontcolor)
            textrect = textsurf.get_rect()
            textrect.topleft = (self.xpos + 40, i[1])
            display.blit(textsurf, textrect)
        
        line = self.cache_string_list[self.i]
        letter = line[:self.j]
        textsurf = Font.render(letter, True, self.fontcolor)
        textrect = textsurf.get_rect()
        textrect.topleft = (self.xpos + 40 , self.ypos + self.yincr)
        display.blit(textsurf, textrect)
        
        if self.last_slice != letter:  
            self.last_slice = letter
            
        self.j += 1
        
        if (self.j > len(line)) and (len(self.cache_string_list) > (self.i + 1)):
            self.history.append((line, self.ypos + self.yincr))
            self.i += 1
            self.j = self.j % len(line)
            self.yincr += 40

class OptionButton:

    indextoAlpha = {0:'A', 1:'B', 2:'C', 3:'D'}
    def __init__(self, x, y, height, color, borderwidth, bordercolor, text, optionIndex, textcolor):
        self.color = color
        self.x = x
        self.y = y
        self.isclicked = None
        self.polled = None
        self.friended = None
        self.chosen = None
        self.optionIndex = optionIndex
        self.width = (WINDOWWIDTH / 2) - 2*(60)
        self.height = height
        self.text = text
        self.borderwidth = borderwidth
        self.bordercolor = bordercolor
        self.textcolor = textcolor

    def draw(self, display):
        
        pygame.draw.rect(display, self.bordercolor, (self.x-self.borderwidth, self.y-self.borderwidth, self.width + 2*(self.borderwidth),self.height+2*(self.borderwidth)), 0)    
        pygame.draw.rect(display, self.color, (self.x,self.y,self.width,self.height), 0)
        
        font = pygame.font.Font("fonts//DTM-Mono.ttf", 27)
        text = font.render(self.text, True, self.textcolor)
        optionNumberText = font.render(OptionButton.indextoAlpha[self.optionIndex], True, GOLDBORDER)

        display.blit(optionNumberText, (self.x + 10, self.y + (self.height/2 - text.get_height()/2)))
        display.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False    
        

class LockButton:

    def __init__(self, locked):
        self.x = lockPositions[0][0]
        self.y = lockPositions[0][1]
        self.width = lockDimensions[0][0]
        self.height = lockDimensions[0][1]
        self.color = BGCOLOR
        self.textcolor = RED
        self.text = "LOCK"
        self.locked = locked

    def draw(self, display):
        pygame.draw.rect(display, GOLDBORDER, (self.x - 5, self.y - 5, self.width + 2*5, self.height + 2*5), 0)
        pygame.draw.rect(display, self.color, (self.x, self.y, self.width, self.height), 0)

        font = pygame.font.Font("fonts//DTM-Mono.ttf", 27)
        text = font.render(self.text, True, self.textcolor)
        display.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False  


class Lifeline:

    lifelinerIndex = {0: 'PHONE', 1: '50:50', 2:'POLL'}
    lifelinerPositions = {0: (WINDOWWIDTH/4 - 50, WINDOWHEIGHT/2 - 68), 1: (2* WINDOWWIDTH/4 - 50, WINDOWHEIGHT/2 - 68), 2: (3* WINDOWWIDTH/4 - 50, WINDOWHEIGHT/2 -68)}
    
    def __init__(self, lifeliner):
        self.width = 100
        self.height = 40
        self.lifeliner = lifeliner
        self.color = BGCOLOR
        self.textcolor = WHITE
        self.isclicked = False
        self.x, self.y = Lifeline.lifelinerPositions[self.lifeliner]
        self.text = Lifeline.lifelinerIndex[self.lifeliner]

    def draw(self, display):
        pygame.draw.rect(display, GOLDBORDER, (self.x - 3, self.y - 3, self.width + 2*3, self.height + 2*3), 0)
        pygame.draw.rect(display, self.color, (self.x, self.y, self.width, self.height), 0)

        font = pygame.font.Font("fonts//DTM-Sans.ttf", 27)
        text = font.render(self.text, True, self.textcolor)
        display.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))
    
    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False  

################################

import random

def poll_randomizer(correct_input, optionsList):
    '''This poll randomizer preferences the correct input with a probability of 73%'''
    universal_set = set().union(optionsList)
    complement_set = universal_set-{correct_input}
    sample_space = [correct_input for _ in range(73)] + [x for _ in range(9) for x in complement_set]
    return random.choice(sample_space)

def friend_randomizer(correct_input, optionsList):
    '''This friend randomizer preferences the correct input with a probability of 64%'''
    universal_set = set().union(optionsList)
    complement_set = universal_set-{correct_input}
    sample_space = [correct_input for _ in range(64)] + [x for _ in range(12) for x in complement_set]
    return random.choice(sample_space)


################################

def make_reward_for_finding_bug():
    htmlcode = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta http-equiv="refresh" content="3; url='https://www.youtube.com/watch?v=dQw4w9WgXcQ'" />
    </head>
    <body>
        <h1>REWARD LOADING . . . <a href="https://www.youtube.com/watch?v=dQw4w9WgXcQ"> </a>.</h1>
    </body>
    </html>
    """

    with open('This is Your Reward.html', 'w') as reward_File:
        reward_File.write(htmlcode)