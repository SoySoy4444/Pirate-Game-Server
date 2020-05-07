import pygame, sys

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
SEA = (59, 111, 226)

colours = {"white":WHITE, "black":BLACK, "blue":BLUE, "red":RED, "green":GREEN, "sea": SEA}

class Button():
    #width and height will only be passed in for buttons with no text (images and plain buttons)
    #windowSize will only be passed in if width="horizontalCentre" or height="verticalCentre"
    def __init__(self, color, x, y, text='', textColour = BLACK, image = None, fontSize=48, width=None, height=None, widthScale=1, windowSize=None):
        self.color = color
        self.text = text
        self.textColour = textColour
        self.image = image
        self.fontSize = fontSize
        
        self.widthScale = widthScale
        if self.text != '': #We want text displayed on our button
            arialFont = pygame.font.SysFont("arialunicodettf", fontSize)
            text = arialFont.render(self.text, 1, self.textColour)
            self.width, self.height = arialFont.size(self.text)
            self.width *= self.widthScale
        else:
            self.width, self.height = width, height
        
        #the location depends on the width and height and so must be set after the width/height
        self.x = windowSize[0]//2 - self.width//2 if x == "horizontalCentre" else x
        self.y = windowSize[1]//2 - self.height//2 if y == "verticalCentre" else y


    def draw(self, screen, outline = None):
        #Call this method to draw the button on the screen
        
        if outline:
            pygame.draw.rect(screen, outline, (self.x-2, self.y-2, self.width+4, self.height+4), 0)
        
        if self.image != None: #We want an image button
            img = pygame.image.load(self.image)
            img = pygame.transform.scale(img, (self.width, self.height))
            screen.blit(img, (self.x, self.y))
        else:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0)
        
        if self.text != '': #We want text displayed on our button
            arialFont = pygame.font.SysFont("arialunicodettf", self.fontSize)
            text = arialFont.render(self.text, 1, self.textColour)
            screen.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isMouseHover(self, mousePos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if mousePos[0] > self.x and mousePos[0] < self.x + self.width:
            if mousePos[1] > self.y and mousePos[1] < self.y + self.height:
                return True
        return False


class Image():
    def __init__(self, filename, size = None):
        #We cannot initialise position yet because it may depend on the size of the image
        self.image = pygame.image.load(filename)
        
        #User has ordered manual scaling
        if size == None: #if the size was not specified, then use the default values for size
            self.width, self.height = self.image.get_rect().size
        else: #the file size was specified, so scale the image to the correct size
            self.width = size[0]
            self.height = size[1]
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
        
    def blit(self, screen, pos):
        self.x = pos[0]
        self.y = pos[1]
        screen.blit(self.image, (self.x, self.y))


class Message():
    def __init__(self, text, fontSize, fontStyle = "arialunicodettf", textColour = colours["black"], backgroundColour = colours["white"]):        
        font = pygame.font.SysFont(fontStyle, fontSize)
        self.myText = font.render(text, 1, textColour, backgroundColour)
        self.width, self.height = self.myText.get_size()[0], self.myText.get_size()[1]
        
    def blit(self, screen, pos, windowSize=None):
        self.x = windowSize[0]//2 - self.width//2 if pos[0] == "horizontalCentre" else pos[0]
        self.y = windowSize[1]//2 - self.height//2 if pos[1] == "verticalCentre" else pos[1]
        screen.blit(self.myText, (self.x, self.y))
    
class UserInput():
    def __init__(self, x, y, fontSize = 24, numeric = False, textColour = colours["black"], backgroundColour = colours["white"]):
        self.x = x
        self.y = y
        self.fontSize = fontSize
        self.numeric = numeric
        self.textColour = textColour
        self.backgroundColour = backgroundColour
    
    def updateSearchBox(self, searchBoxWidth, searchBoxHeight, screen, textObj, screenBeforeUserInput):
        screen.blit(screenBeforeUserInput, (0, 0))
        pygame.draw.rect(screen, self.backgroundColour, [self.x, self.y, searchBoxWidth, searchBoxHeight])
        screen.blit(textObj, (self.x, self.y))
    
    def takeUserInput(self, screen):
        screenBeforeUserInput = screen.copy()
        
        text = ""
        arialFont = pygame.font.SysFont("arialunicodettf", self.fontSize)
        textObj = arialFont.render(text, 1, self.textColour)

        #initial empty text field area        
        searchBoxWidth, searchBoxHeight = arialFont.size(" ")
        self.updateSearchBox(searchBoxWidth, searchBoxHeight, screen, textObj, screenBeforeUserInput)
        
        typing = True
        while typing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    
                    if ( (event.unicode.isalpha() or event.key == pygame.K_SPACE) and not self.numeric) or event.unicode.isnumeric():
                        text += event.unicode #add the character
                        textObj = arialFont.render(text, 1, self.textColour)
                        
                        searchBoxWidth, searchBoxHeight = arialFont.size(text)               
                        self.updateSearchBox(searchBoxWidth, searchBoxHeight, screen, textObj, screenBeforeUserInput)

                    elif event.key == pygame.K_BACKSPACE and len(text) != 0: #you can only delete if there is text to delete
                        text = text[:-1] #delete the last character
                        textObj = arialFont.render(text, 1, self.textColour)
                        
                        searchBoxWidth, searchBoxHeight = arialFont.size(text)
                        self.updateSearchBox(searchBoxWidth, searchBoxHeight, screen, textObj, screenBeforeUserInput)
                    elif event.key == pygame.K_RETURN:
                        typing = False
            pygame.display.update()
        return text