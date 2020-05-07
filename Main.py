import pygame, sys, time, datetime, os, pickle, bisect, random
from Constants import Button, colours, Image, UserInput, Message
from GameItems import *

pygame.init()

monitorSize = [pygame.display.Info().current_w, pygame.display.Info().current_h] #Get's the monitor size of the user's computer
#For mine, Macbook Air 2015, it's 13.3-inch, 1440 x 900 pixel display (128 ppi) so it'll be [1440, 900]

windowSize = (800, 600) #TODO: Make the default size relative to the screen size
screen = pygame.display.set_mode(windowSize, pygame.RESIZABLE)
pygame.display.set_caption("Pirate Game")
clock = pygame.time.Clock()
username = ""

def log(listLines, filename, cash):
    with open(filename, "a") as file:
        now = datetime.datetime.now()
        dateAndTime = now.strftime("%d/%m/%y %H:%M")
        
        #for each string in the list of strings given, log the current time, cash and the message 
        for line in listLines:
            file.write(dateAndTime + "\t" + str(cash) + "\t" + line + "\n")

def fade(width, height, alpha=95, colour="white"):
    fade = pygame.Surface((width, height))
    fade.fill(colours[colour])
    fade.set_alpha(alpha)
    screen.blit(fade, (0, 0))

def pause(seconds = None):
    paused = True
    startTime = time.time()
    currentScreen = screen.copy()
    
    if seconds == None: #display "Paused" message indefinitely until the user presses c.
        fade(windowSize[0], windowSize[1]) #make the screen look whitish
        pauseMessage = Message("Paused", 48)
        pauseMessage.blit(screen, ("horizontalCentre", "verticalCentre"), windowSize=windowSize)

    while paused:
        clock.tick(2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c: #if c pressed, continue playing
                    screen.blit(currentScreen, (0, 0))
                    paused = False
                    
        if seconds != None and time.time() - startTime > seconds:
            paused = False
            
        pygame.display.update()

def checkFileExists(filename):
    try:
        with open(filename):
            return True
    except FileNotFoundError:
        return False

def loadGame(): #Transition from continue game -> main screen    
    with open("savedGame.pickle", "rb") as f:
        grid = pickle.load(f)
        enteredCoordinates = pickle.load(f)
        cash = pickle.load(f)
        bankAmount = pickle.load(f)
        shield = pickle.load(f)
        mirror = pickle.load(f)
        global username
        username = pickle.load(f)
    mainScreen(grid, enteredCoordinates, cash, bankAmount, shield, mirror, False)

def titleScreen():
    screen.fill(colours["sea"])
    
    waitingForUser = True #TODO: Define the logic for this.
    
    newGameButton = Button(colours["red"], windowSize[0]//2 - 100, 300, text="New Game")
    continueGameButton = Button(colours["red"], windowSize[0]//2 - 150, 400, text="Continue Game")
    howToPlayButton = Button(colours["red"], 100, 0, text="How To Play", fontSize=24)
    backToTitleScreen = Button(colours["red"], 100, windowSize[1]-100, text="Back")
    
    newGameButton.draw(screen)
    continueGameButton.draw(screen)
    howToPlayButton.draw(screen)
    
    title = Message("The Pirate Game", 64)
    title.blit(screen, (windowSize[0]//2 - title.width//2, 200))
    
    titleScreen = screen.copy()
    
    while waitingForUser:
        clock.tick(20)
        for event in pygame.event.get():
            mousePosition = pygame.mouse.get_pos()
            
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            #TODO: Make the screen resizable.
            #if event.type == pygame.VIDEORESIZE:
            #   screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
    
            if event.type == pygame.MOUSEBUTTONDOWN: #if mouse is clicked
                if newGameButton.isMouseHover(mousePosition):
                    newGameButton.color = colours["blue"]
                    mode = chooseMode()
                    setupScreen(mode)
                    
                if continueGameButton.isMouseHover(mousePosition):                    
                    if checkFileExists("savedGame.pickle"):
                        loadingMessage = Message("Loading...", 48)
                        loadingMessage.blit(screen, ("horizontalCentre", "verticalCentre"), windowSize=windowSize)
                        pause(seconds=3) #show the message for 3 seconds
                        waitingForUser = False
                        loadGame() #load the game
                    else:
                        loadingMessage = Message("Could not find a game!", 48)
                        loadingMessage.blit(screen, ("horizontalCentre", "verticalCentre"), windowSize=windowSize)
                        pause(seconds=3) #show the message for 3 seconds
                        screen.blit(titleScreen, (0, 0)) #hide the message

                if howToPlayButton.isMouseHover(mousePosition):
                    #display how to play rules
                    screen.fill(colours["blue"])
                    backToTitleScreen.draw(screen, 24)
                    
                    ruleBackground = pygame.image.load("Images/rules.png")
                    screen.blit(ruleBackground, (0, 0))
                
                if backToTitleScreen.isMouseHover(mousePosition):
                    screen.blit(titleScreen, (0, 0)) #go back to the title screen
                    
            #TODO: Change button colour upon hover is not working
            if event.type == pygame.MOUSEMOTION: #if mouse is moving
                if newGameButton.isMouseHover(mousePosition):
                    newGameButton.color = colours["green"]
                else:
                    newGameButton.color = colours["red"]
        pygame.display.update()

def chooseMode():
    screen.fill(colours["white"])
    
    chooseModeMessage = Message("Choose your setup mode", 24)
    chooseModeMessage.blit(screen, ("horizontalCentre", 100), windowSize=windowSize)
    
    customButton = Button(colours["green"], "horizontalCentre", 300, text="Custom Setup", fontSize=24, windowSize=windowSize)
    customButton.draw(screen)
    
    semiCustomButton = Button(colours["green"], "horizontalCentre", 400, text="Semi-custom Setup", fontSize=24, windowSize=windowSize)
    semiCustomButton.draw(screen)
    
    randomButton = Button(colours["green"], "horizontalCentre", 500, text="Random Setup", fontSize=24, windowSize=windowSize)
    randomButton.draw(screen)
    
    waitingForMode = True
    while waitingForMode:
        clock.tick(10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePosition = pygame.mouse.get_pos()
                if customButton.isMouseHover(mousePosition):
                    waitingForMode = False
                    mode = "C"
                if semiCustomButton.isMouseHover(mousePosition):
                    waitingForMode = False
                    mode = "S"
                if randomButton.isMouseHover(mousePosition):
                    waitingForMode = False
                    mode = "R"
        pygame.display.update()
    return mode

def customItems(grid, itemDict, xLeft, xRight, yTop, yBottom, squareSize, fill, inset):
    for key in itemDict.keys(): #for each item,
        currentItem = itemDict[key] #set currentItem to the item OBJECT
        filename = "Images/GameItems/" + currentItem.itemName + ".png" #find its filename,
        currentItemImage = Image(filename, size=(int(squareSize * fill), int(squareSize * fill)))
        currentItemImage.blit(screen, pos=(100, 100))
        waitingForItemSetup = True

        while waitingForItemSetup:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mousePosition = pygame.mouse.get_pos()
                    
                    if mousePosition[0] > xLeft and mousePosition[0] < xRight and mousePosition[1] > yTop and mousePosition[1] < yBottom:
                        row = int( (mousePosition[0] - xLeft) // ((xRight - xLeft)/7) ) #calculate the row number from 0 - 6
                        col = int( (mousePosition[1] - yTop) // ((yBottom - yTop)/7) ) #calculate the col number from 0 - 6
                        
                        if grid[row][col] == "":                                
                            currentItemImage.blit(screen, pos=(row * squareSize + (inset * xLeft), col * squareSize + (inset * yTop)))
                            grid[row][col] = itemDict[key]
                            
                            itemArea = pygame.Rect((100, 100), (currentItemImage.width, currentItemImage.height))
                            screen.fill(colours["sea"], rect=itemArea)
                            waitingForItemSetup = False
                            
                        else: #This square was already set.
                            #Remind the user to click on an empty square
                            currentScreen = screen.copy()
                            warningMessage = Message("This square is already set up", 24, textColour=colours["black"], backgroundColour=colours["red"])
                            warningMessage.blit(screen, ("horizontalCentre", "verticalCentre"), windowSize=windowSize)
                            pause(seconds=1)
                            screen.blit(currentScreen, (0, 0))
                    else:
                        #Remind the user to click inside the grid only
                        currentScreen = screen.copy()
                        warningMessage = Message("Please click inside the grid", 24, textColour=colours["black"], backgroundColour=colours["red"])
                        warningMessage.blit(screen, ("horizontalCentre", "verticalCentre"), windowSize=windowSize)
                        pause(seconds=1)
                        screen.blit(currentScreen, (0, 0))
            pygame.display.update()
    return grid

def customCash(grid, cashDict, xLeft, xRight, yTop, yBottom, squareSize, fill, inset):
    for key in cashDict.keys(): #for each type of cash,
        for _ in range(cashDict[key].numCash): #we need 24 $200, 10 $1000, etc
            
            currentItem = cashDict[key] #set currentItem to the item OBJECT
            filename = "Images/GameItems/" + currentItem.itemName + ".png" #find its filename,
            currentItemImage = Image(filename, size=(int(squareSize * fill), int(squareSize * fill)))
            itemArea = pygame.Rect((100, 100), (currentItemImage.width, currentItemImage.height))
            screen.fill(colours["sea"], rect=itemArea)
            currentItemImage.blit(screen, pos=(100, 100))
            waitingForCashSetup = True
            while waitingForCashSetup:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mousePosition = pygame.mouse.get_pos()
                        
                        if mousePosition[0] > xLeft and mousePosition[0] < xRight and mousePosition[1] > yTop and mousePosition[1] < yBottom:
                            row = int( (mousePosition[0] - xLeft) // ((xRight - xLeft)/7) ) #calculate the row number from 0 - 6
                            col = int( (mousePosition[1] - yTop) // ((yBottom - yTop)/7) ) #calculate the col number from 0 - 6
                            
                            if grid[row][col] == "":    
                                currentItemImage.blit(screen, pos=(row * squareSize + (inset * xLeft), col * squareSize + (inset * yTop)))
                                grid[row][col] = cashDict[key]
                                
                                itemArea = pygame.Rect((100, 100), (currentItemImage.width, currentItemImage.height))
                                screen.fill(colours["sea"], rect=itemArea)
                                waitingForCashSetup = False
                                
                            else: #This square was already set.
                                #Remind the user to click on an empty square
                                currentScreen = screen.copy()
                                warningMessage = Message("This square is already set up", 24, textColour=colours["black"], backgroundColour=colours["red"])
                                warningMessage.blit(screen, ("horizontalCentre", "verticalCentre"), windowSize=windowSize)
                                pause(seconds=1)
                                screen.blit(currentScreen, (0, 0))
                        else:
                            #Remind the user to click inside the grid only
                            currentScreen = screen.copy()
                            warningMessage = Message("Please click inside the grid", 24, textColour=colours["black"], backgroundColour=colours["red"])
                            warningMessage.blit(screen, ("horizontalCentre", "verticalCentre"), windowSize=windowSize)
                            pause(seconds=1)
                            screen.blit(currentScreen, (0, 0))
                pygame.display.update()
    return grid

def randomItems(grid, itemDict, xLeft, yTop, squareSize, fill, inset):
    for key in itemDict.keys(): #for each item,
        currentItem = itemDict[key] #set currentItem to the item OBJECT
        filename = "Images/GameItems/" + currentItem.itemName + ".png" #find its filename,
        currentItemImage = Image(filename, size=(int(squareSize * fill), int(squareSize * fill)))

        validCoordinateFound = False
        while not validCoordinateFound:
            row = random.randint(0, 6)
            col = random.randint(0, 6)
                        
            if grid[row][col] == "":                                
                currentItemImage.blit(screen, pos=(row * squareSize + (inset * xLeft), col * squareSize + (inset * yTop)))
                grid[row][col] = itemDict[key]
                
                validCoordinateFound = True
    return grid

def randomCash(grid, cashDict, xLeft, yTop, squareSize, fill, inset):
    del cashDict["$200"]
    for key in cashDict.keys(): #for each item,
        for _ in range(cashDict[key].numCash):
            currentItem = cashDict[key] #set currentItem to the item OBJECT
            filename = "Images/GameItems/" + currentItem.itemName + ".png" #find its filename,
            currentItemImage = Image(filename, size=(int(squareSize * fill), int(squareSize * fill)))
    
            validCoordinateFound = False
            while not validCoordinateFound:
                row = random.randint(0, 6)
                col = random.randint(0, 6)

                if grid[row][col] == "":
                    currentItemImage.blit(screen, pos=((row * squareSize + (inset * xLeft)), (col * squareSize + (inset * yTop))))
                    grid[row][col] = cashDict[key]
                    
                    validCoordinateFound = True
    
    for rowNum, row in enumerate(grid):
        for colNum, element in enumerate(row):
            if element == "":
                currentItem = Cash(200)
                filename = "Images/GameItems/" + currentItem.itemName + ".png" #find its filename,
                currentItemImage = Image(filename, size=(int(squareSize * fill), int(squareSize * fill)))

                currentItemImage.blit(screen, pos=(rowNum * squareSize + (inset * xLeft), colNum * squareSize + (inset * yTop)))
                grid[rowNum][colNum] = currentItem
    return grid

def setupScreen(mode):
    screen.fill(colours["sea"])
    requestMessage = Message("Enter your game name", 24)
    requestMessage.blit(screen, ("horizontalCentre", 200), windowSize=windowSize)
    newField = UserInput(300, 400) #x, y
    global username
    username = newField.takeUserInput(screen)
    
    screen.fill(colours["sea"])
    gridImage = Image("Images/grid.png", size=(460, 460))
    gridImage.blit(screen, pos = (windowSize[0]//2 - gridImage.width//2, windowSize[1]//2 - gridImage.height//2))
    
    xLeft, xRight = 228, 628
    yTop, yBottom = 129, 529
    squareSize = gridImage.width / 8 #the grid has 8 squares, so / 8 will produce the size of each grid.    
    fill = 0.85 #the image will fill 85% of the square
    inset = 1 + ((squareSize * (1-fill)/2))/2/100 #for a square size of 57 and fill of 85%, is 2.15625%%.
    
    grid = [
        ["", "", "", "", "", "", ""], 
        ["", "", "", "", "", "", ""],
        ["", "", "", "", "", "", ""],
        ["", "", "", "", "", "", ""],
        ["", "", "", "", "", "", ""],
        ["", "", "", "", "", "", ""],
        ["", "", "", "", "", "", ""],
    ]
    
    itemDict = {
         "Present": Present(), "ChooseNextSquare": ChooseNextSquare(), "LostAtSea": LostAtSea(),
         "SwapScore": SwapScore(), "Rob": Rob(), "Mirror": Mirror(), "DoubleScore": DoubleScore(),
         "Shield": Shield(), "SinkShip": SinkShip(), "Backstab": Backstab(), "SneakPeek": SneakPeak(),
         "Bank": Bank()
    }
    
    cashDict = {
        "$200": Cash(200), "$1000": Cash(1000), "$3000": Cash(3000), "$5000": Cash(5000)
    }
    
    if mode == "C":
        grid = customItems(grid, itemDict, xLeft, xRight, yTop, yBottom, squareSize, fill, inset)
        grid = customCash(grid, cashDict, xLeft, xRight, yTop, yBottom, squareSize, fill, inset)
    elif mode == "S":
        grid = customItems(grid, itemDict, xLeft, xRight, yTop, yBottom, squareSize, fill, inset)
        grid = randomCash(grid, cashDict, xLeft, yTop, squareSize, fill, inset)
    else: #mode == "R"
        grid = randomItems(grid, itemDict, xLeft, yTop, squareSize, fill, inset)
        grid = randomCash(grid, cashDict, xLeft, yTop, squareSize, fill, inset)
    
    mainScreen(grid, [], 0, 0, False, False, True, gridImage=gridImage)

def saveGame(grid, enteredCoordinates, cash, bankAmount, shield, mirror):
    with open("savedGame.pickle", "wb") as f:
        pickle.dump(grid, f)
        pickle.dump(enteredCoordinates, f)
        pickle.dump(cash, f)
        pickle.dump(bankAmount, f)
        pickle.dump(shield, f)
        pickle.dump(mirror, f)
        pickle.dump(username, f)

#Converts from something like 4, 2 to D3
def intCoordinateToStrCoordinate(rowCoordinate, colCoordinate):
    rows = "ABCDEFG"
    return rows[rowCoordinate] + str(colCoordinate+1)

#item is a GameItem class
def makeChanges(item, cash, bankAmount, shield, mirror):
    itemName = item.itemName
    
    currentScreen = screen.copy()
    itemMessage = Message(item.itemDescription, 24)
    itemMessage.blit(screen, ("horizontalCentre", "verticalCentre"), windowSize=windowSize)
    pause(seconds=1)
    screen.blit(currentScreen, (0, 0))
    
    log([item.itemDescription], "currentGame.txt", cash)
    
    if itemName[0] == "$": #this means the item is either $5000, $3000, $1000 or $200
        value = int(itemName[1:]) #the part after the $, so 5000, 3000, 1000 or 200
        return cash+value, bankAmount, shield, mirror
    elif itemName == "Rob":
        screenBeforeUserInput = screen.copy()
        requestMessage = Message("Please type how much you robbed", 24)
        requestMessage.blit(screen, ("horizontalCentre", 200), windowSize=windowSize)
        newField = UserInput(300, 400, numeric=True) #x, y
        amountRobbed = int(newField.takeUserInput(screen))
        screen.blit(screenBeforeUserInput, (0, 0))
        return cash+amountRobbed, bankAmount, shield, mirror
    
    elif itemName == "SwapScore":
        screenBeforeUserInput = screen.copy()
        requestMessage = Message("Please type your opponent's cash", 24)
        requestMessage.blit(screen, ("horizontalCentre", 200), windowSize=windowSize)
        newField = UserInput(300, 400, numeric=True) #x, y
        opponentCash = int(newField.takeUserInput(screen))
        screen.blit(screenBeforeUserInput, (0, 0))
        return opponentCash, bankAmount, shield, mirror

    elif itemName == "Bank":
        return 0, cash, shield, mirror
    elif itemName == "Mirror":
        return cash, bankAmount, shield, True
    elif itemName == "Shield":
        return cash, bankAmount, True, mirror
    elif itemName == "LostAtSea":
        #TODO: if user has shield == True or mirror == True, ask user if they would like to use it, 
        return 0, bankAmount, shield, mirror
    elif itemName == "DoubleScore":
        return 2*cash, bankAmount, shield, mirror
    
    elif itemName == "ChooseNextSquare":
        screenBeforeUserInput = screen.copy()
        requestMessage = Message("Please type which square you want", 24)
        requestMessage.blit(screen, ("horizontalCentre", 200), windowSize=windowSize)
        newField = UserInput(300, 400) #x, y
        square = newField.takeUserInput(screen)
        #TODO: Send {username:square} to server
        screen.blit(screenBeforeUserInput, (0, 0))
    
    #default case - present (which does nothing), sneak peek (again, nothing), choose next square, sink ship, back stab (?)
    return cash, bankAmount, shield, mirror

def updateUI(cash, bankAmount, shield, mirror):
    region = pygame.Rect((500, 20), (300, 30)) #the square to cover with blue
    screen.fill(colours["sea"], rect=region)
    
    cashButton = Button(colours["green"], 650, 20, text="Cash: %d" % cash, fontSize=24)
    cashButton.draw(screen)
    
    #if bank is not 0, then this game is being continued and not a new game
    if bankAmount != 0: 
        bankButton = Button(colours["green"], 650, 60, text="Bank: %d" % bankAmount, fontSize=24)
        bankButton.draw(screen)

    #Add the shield and mirror icons if they are initialised as True
    shieldButton = Button(colours["green"], 650, 100, image="Images/GameItems/Shield.png", width=80, height=80)
    if shield:
        shieldButton.draw(screen)
    else:
        buttonRegion = pygame.Rect((650, 100), (int(80), int(80))) #TODO: remove hardcoding
        screen.fill(colours["sea"], rect=buttonRegion)
        
    mirrorButton = Button(colours["green"], 650, 190, image="Images/GameItems/Mirror.png", width=80, height=80)
    if mirror:
        mirrorButton.draw(screen)
    else:
        buttonRegion = pygame.Rect((650, 190), (int(80), int(80))) #TODO: remove hardcoding
        screen.fill(colours["sea"], rect=buttonRegion)
    return shieldButton, mirrorButton

def confirm(message):
    currentScreen = screen.copy()
    
    screen.fill(colours["white"])
    confirmMessage = Message(message, 24)
    confirmMessage.blit(screen, (windowSize[0]//2 - confirmMessage.width//2, 200))
    
    yesButton = Button(colours["green"], 'horizontalCentre', 300, text="Yes", widthScale=2, windowSize=windowSize)
    yesButton.draw(screen)
    
    noButton = Button(colours["red"], 'horizontalCentre', 400, text="No", widthScale=2, windowSize=windowSize)
    noButton.draw(screen)
    
    waitingForReply = True
    while waitingForReply:
        clock.tick(5)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePosition = pygame.mouse.get_pos()
                if yesButton.isMouseHover(mousePosition):
                    waitingForReply = False
                    screen.blit(currentScreen, (0, 0))
                    return True
                if noButton.isMouseHover(mousePosition):
                    waitingForReply = False
                    screen.blit(currentScreen, (0, 0))
                    return False
        pygame.display.update()
    

#Triggered either by titleScreen -> loadGame or setUpScreen()
def mainScreen(grid, enteredCoordinates, cash, bankAmount, shield, mirror, newGame, gridImage=None):   
    print(username)  
    if newGame:
        xLeft, xRight = 228, 628
        yTop, yBottom = 129, 529
        squareSize = gridImage.width / 8 #the grid has 8 squares, so / 8 will produce the size of each grid.   
    else: #if continuing game, we need to setup
        screen.fill(colours["sea"]) #background blue colour
        
        welcomeBackMessage = Message(f"Welcome back, {username}!", 24)
        welcomeBackMessage.blit(screen, ("horizontalCentre", 200), windowSize=windowSize)
        pause(seconds=2)
        
        screen.fill(colours["sea"])
        gridImage = Image("Images/grid.png", size=(460, 460))
        gridImage.blit(screen, pos = (windowSize[0]//2 - gridImage.width//2, windowSize[1]//2 - gridImage.height//2))
        
        xLeft, xRight = 228, 628
        yTop, yBottom = 129, 529
        squareSize = gridImage.width / 8 #the grid has 8 squares, so / 8 will produce the size of each grid.
        
        #Add the game item images to the grid ONLY NECESSARY IF playing via CONTINUE GAME and not setup
        fill = 0.85 #the image will fill 85% of the square
        inset = 1 + ((squareSize * (1-fill)/2))/2/100 #for a square size of 57 and fill of 85%, is 2.15625%%.
        for rowCoordinate, row in enumerate(grid):
            for colCoordinate, element in enumerate(row):
                if intCoordinateToStrCoordinate(rowCoordinate, colCoordinate) not in enteredCoordinates:
                    filename = "Images/GameItems/" + element.itemName + ".png"
                    image = Image(filename, size=(int(squareSize * fill), int(squareSize * fill)))
                    image.blit(screen, pos=(rowCoordinate * squareSize + (inset * xLeft), colCoordinate * squareSize + (inset * yTop)))
        
    # ---------------- Clickable Buttons With Text ---------------
    whatHappenedButton = Button(colours["green"], windowSize[0]//2 - 150, 550, text="What Happened?", fontSize=24)
    whatHappenedButton.draw(screen)
    
    saveGameButton = Button(colours["green"], 20, 20, text="Save Game", fontSize=24)
    saveGameButton.draw(screen)
    
    undoButton = Button(colours["green"], 20, 60, text="Undo Square", fontSize=24)
    undoButton.draw(screen)
    
    #TODO: Display log button
    #If clicked, showLog()
    # ------------------------------------------------------------

    shieldButton, mirrorButton = updateUI(cash, bankAmount, shield, mirror)
    oldCash, oldBankAmount, oldShield, oldMirror = cash, bankAmount, shield, mirror
    oldMainScreen = screen.copy()
    saved = False #initially, the game is unsaved
    clickable = False #initially, the user may not enter a square
    undoAllowed = False
    while len(enteredCoordinates) < 49:
        clock.tick(30)

        for event in pygame.event.get():
            mousePosition = pygame.mouse.get_pos()
            
            if event.type == pygame.QUIT:
                if not saved and confirm("Would you like to save your game?"):
                    saveGame(grid, enteredCoordinates, cash, bankAmount, shield, mirror)
                    confirmationMessage = Message("Your game was saved!", 24)
                    confirmationMessage.blit(screen, ("horizontalCentre", 200), windowSize=windowSize)
                    pause(seconds=2)
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:
                    currentScreen = screen.copy()
                    clickable = True #the user may now click on the grid to remove a square
                     
                    clickMessage = Message("Click on the coordinate that the teacher called out", 24) #TODO: Very annoying? Fix.
                    clickMessage.blit(screen, ("horizontalCentre", 200), windowSize=windowSize)
                    pause(seconds=1)
                    screen.blit(currentScreen, (0, 0))
                    
                if event.key == pygame.K_p:
                    pause()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(mousePosition)
                if shieldButton.isMouseHover(mousePosition) and shield == True:
                    if confirm("Use shield?"):
                        shield = False
                        shieldButton, mirrorButton = updateUI(cash, bankAmount, shield, mirror)
                        saved = False
                if mirrorButton.isMouseHover(mousePosition) and mirror == True:
                    if confirm("Use mirror?"):
                        mirror = False
                        shieldButton, mirrorButton = updateUI(cash, bankAmount, shield, mirror)
                        saved = False
                
                if saveGameButton.isMouseHover(mousePosition):
                    saveGame(grid, enteredCoordinates, cash, bankAmount, shield, mirror)
                    screenBeforeSaving = screen.copy()
                    confirmationMessage = Message("Your game was saved!", 24)
                    confirmationMessage.blit(screen, ("horizontalCentre", 200), windowSize=windowSize)
                    pause(seconds=2)
                    screen.blit(screenBeforeSaving, (0, 0))
                    saved = True
                
                if len(enteredCoordinates) != 0 and undoAllowed and undoButton.isMouseHover(mousePosition):
                    screen.blit(oldMainScreen, (0, 0))
                    shieldButton, mirrorButton = updateUI(oldCash, oldBankAmount, oldShield, oldMirror)
                    cash, bankAmount, shield, mirror = oldCash, oldBankAmount, oldShield, oldMirror
                    previousSquare = enteredCoordinates.pop()
                    
                    screenBeforeUndoMessage = screen.copy()
                    undoMessage = Message("{} was reverted!".format(previousSquare), 24)
                    undoMessage.blit(screen, ("horizontalCentre", 200), windowSize=windowSize)   
                    pause(seconds=2)
                    screen.blit(screenBeforeUndoMessage, (0, 0))     
                    undoAllowed = False
                
                #this entire if block is for entering coordinates onto the grid
                if clickable:
                    #TODO: Game logic - don't hard code
                    #244, 126 - - - - - 610, 126
                    #    -    - - - - -     -
                    #    -    - - - - -     -
                    #    -    - - - - -     -
                    #    -    - - - - -     -
                    #    -    - - - - -     -
                    #244, 534 - - - - - 610, 534
                    
                    #if the user presses within the boundaries of the grid
                    if mousePosition[0] > xLeft and mousePosition[0] < xRight and mousePosition[1] > yTop and mousePosition[1] < yBottom:
                        row = int( (mousePosition[0] - xLeft) // ((xRight - xLeft)/7) ) #calculate the row number from 0 - 6
                        col = int( (mousePosition[1] - yTop) // ((yBottom - yTop)/7) ) #calculate the col number from 0 - 6
                        
                        if intCoordinateToStrCoordinate(row, col) not in enteredCoordinates:    
                            undoAllowed = True  
                            oldMainScreen = screen.copy()
                            oldCash, oldBankAmount, oldShield, oldMirror = cash, bankAmount, shield, mirror
                                                  
                            #topLeft corner of the square has the least x and y value
                            top = int(yTop + (col * squareSize))
                            left = int(xLeft + (row * squareSize))
                            region = pygame.Rect((left, top), (int(squareSize), int(squareSize))) #the square to cover with blue
                            screen.fill(colours["sea"], rect=region)
                            
                            cash, bankAmount, shield, mirror = makeChanges(grid[row][col], cash, bankAmount, shield, mirror) #if user lands on cash, increase cash, if user lands on double, double score, etc.
                            shieldButton, mirrorButton = updateUI(cash, bankAmount, shield, mirror)
                            
                            enteredCoordinates.append(intCoordinateToStrCoordinate(row, col))
                            saved = False
                        else: #This square was already played.
                            #Remind the user to click on an empty square
                            currentScreen = screen.copy()
                            
                            warningMessage = Message("Please enter available square", 24, textColour=colours["black"], backgroundColour=colours["red"])
                            warningMessage.blit(screen, ("horizontalCentre", "verticalCentre"), windowSize=windowSize)
                            pause(seconds=1)
                            screen.blit(currentScreen, (0, 0))
                    else:
                        #Remind the user to click inside the grid only
                        currentScreen = screen.copy()
                        
                        warningMessage = Message("Please click inside the grid", 24, textColour=colours["black"], backgroundColour=colours["red"])
                        warningMessage.blit(screen, ("horizontalCentre", "verticalCentre"), windowSize=windowSize)
                        pause(seconds=1)
                        screen.blit(currentScreen, (0, 0))
                    
                    clickable = False #The user entered a square now, so they are now not allowed to enter again.
        pygame.display.update()
    
    gameOverScreen(cash+bankAmount)
    
def gameOverScreen(todaysScore):
    screen.fill(colours["white"])
    
    today = datetime.date.today()
    formattedDate = today.strftime("%d-%m-%y")

    message = "Great Effort!"
    if os.path.exists("highScores.pickle"):
        with open("highScores.pickle", "rb") as f:
            highScoresDict = pickle.load(f)
            oldHighScores = sorted(highScoresDict.keys()) #before adding today's entry, take note of the previous high scores
            
            highScoresDict[todaysScore] = formattedDate #add today's score to the high scores dictionary
    
            newHighScores = oldHighScores
            bisect.insort(newHighScores, todaysScore) #add today's score in the list of new high scores
            newHighScores = sorted(oldHighScores, reverse=True) #with today's score included, sort the list again.
            
            if len(newHighScores) <= 5: #if there are less than 5 high scores total, display all scores
                newHighScoresDict = {score:highScoresDict[score] for score in newHighScores}
            else: #otherwise, only display the top 5.
                newHighScoresDict = {score:highScoresDict[score] for score in newHighScores[:5]}
                
                if oldHighScores[len(oldHighScores)-1] > todaysScore:
                    message = "Your score does not belong in your high scores list :("

            if newHighScores[0] == todaysScore:
                message = "You have a new high score!"
    else:
        message = "This is your first recorded high score!"
        newHighScoresDict = {todaysScore:formattedDate}
    
    gameOverMessage = Message(message, 24)
    gameOverMessage.blit(screen, ("horizontalCentre", 100), windowSize=windowSize)
    index = 1
    for score, date in newHighScoresDict.items():
        entry = date + " " + str(score)
        entryMessage = Message(entry, 24)
        entryMessage.blit(screen, ("horizontalCentre", 200+50*index), windowSize=windowSize)
        index += 1
    
    #update the high scores dictionary
    with open("highScores.pickle", "wb") as f:
        pickle.dump(newHighScoresDict, f)

    if os.path.exists("savedGame.pickle"): #will not exist if first time playing
        os.remove("savedGame.pickle")
    if os.path.exists("currentGame.txt"): #this one should definitely exist, but just in case the user deleted it manually
        os.rename("currentGame.txt", "archive_" + formattedDate + ".txt")
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                goodbyeMessage = Message("Thank you for playing!", 24)
                goodbyeMessage.blit(screen, ("horizontalCentre", 200), windowSize=windowSize)
                pause(seconds=2)
                pygame.quit()
                sys.exit()
        pygame.display.update()

if __name__ == "__main__":
    titleScreen()
    #gameOverScreen(4000) 