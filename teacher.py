import pygame, sys, time, os.path, pickle
from Constants import Button, colours, Image, UserInput, Message
from GameItems import ChooseNextSquare

pygame.init()

windowSize = (800, 600) #TODO: Make the default size relative to the screen size
screen = pygame.display.set_mode(windowSize)
pygame.display.set_caption("Pirate Game Host")
clock = pygame.time.Clock()
screen.fill(colours["sea"])

def pause(seconds = None):
    def fade(width, height, alpha=95, colour="white"):
        fade = pygame.Surface((width, height))
        fade.fill(colours[colour])
        fade.set_alpha(alpha)
        screen.blit(fade, (0, 0))
    
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

def titleScreen():    
    waitingForTeacher = True
    
    newGameButton = Button(colours["red"], windowSize[0]//2 - 100, 300, text="New Game")
    continueGameButton = Button(colours["red"], windowSize[0]//2 - 150, 400, text="Continue Game")
    
    newGameButton.draw(screen)
    continueGameButton.draw(screen)
    
    title = Message("The Pirate Game Host", 64)
    title.blit(screen, (windowSize[0]//2 - title.width//2, 200))
    
    titleScreen = screen.copy()
    
    while waitingForTeacher:
        clock.tick(20)
        for event in pygame.event.get():
            mousePosition = pygame.mouse.get_pos()
            
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    
            if event.type == pygame.MOUSEBUTTONDOWN: #if mouse is clicked
                if newGameButton.isMouseHover(mousePosition):
                    main(set(), [], {})

                if continueGameButton.isMouseHover(mousePosition):                    
                    if os.path.exists("savedGameTeacher.pickle"):
                        loadingMessage = Message("Loading...", 48)
                        loadingMessage.blit(screen, ("horizontalCentre", "verticalCentre"), windowSize=windowSize)
                        pause(seconds=3) #show the message for 3 seconds
                        waitingForTeacher = False
                        
                        with open("savedGameTeacher.pickle", "rb") as f:
                            enteredCoordinates = pickle.load(f)
                            namesOrder = pickle.load(f)
                            chooseNextSquare = pickle.load(f)
                            main(enteredCoordinates, namesOrder, chooseNextSquare)
                    else:
                        loadingMessage = Message("Could not find a game!", 48)
                        loadingMessage.blit(screen, ("horizontalCentre", "verticalCentre"), windowSize=windowSize)
                        pause(seconds=3) #show the message for 3 seconds
                        screen.blit(titleScreen, (0, 0)) #hide the message
        pygame.display.update()


def main(enteredCoordinates, namesOrder, chooseNextSquare):
    def updateMainScreen():
        screen.fill(colours["sea"])
    
        global nextSquareButton
        nextSquareButton = Button(colours["red"], 100, 100, text="Next Square")
        nextSquareButton.draw(screen)
    rows = "ABCDEFG"

    availableCoordinates = {rows[row] + str(col+1) for col in range(7) for row in range(7)} #set comprehension. Sets are inherently unordered.
    availableCoordinates -= enteredCoordinates
    
    #namesOrder = ["Bob", "Dave", "ABC"]
    #chooseNextSquare = {"Bob":"A6", "ABC":"C4", "Dave":"D3"}
    
    updateMainScreen()
    while len(availableCoordinates) != 0:
        clock.tick(20)
        
        for event in pygame.event.get():
            mousePosition = pygame.mouse.get_pos()
            
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if nextSquareButton.isMouseHover(mousePosition):
                    updateMainScreen()
                    if chooseNextSquare: #if there are requests by students
                        nextStudent = namesOrder.pop(0) #get the name of the next student and remove it
                        nextCoordinate = chooseNextSquare.pop(nextStudent) #get the square that the student chose and remove it
                        availableCoordinates.remove(nextCoordinate) #remove the square from the set of all available squares
                        
                        nextSquareMessage = Message(f"{nextStudent} chose {nextCoordinate}!", 24)
                    else: #otherwise, the teacher will press the generate button
                        nextCoordinate = availableCoordinates.pop() #get the next random square and remove it
                        nextSquareMessage = Message(f"The next random coordinate is {nextCoordinate}!", 24)
                    
                    nextSquareMessage.blit(screen, (windowSize[0]//2 - nextSquareMessage.width//2, 200))
                    
                    squaresRemainingMesssage = Message(f"{len(availableCoordinates)} squares remaining.", 12)
                    squaresRemainingMesssage.blit(screen, (windowSize[0]//2 - squaresRemainingMesssage.width//2, 550))

        pygame.display.update()
    
    print("End of game!")

if __name__ == "__main__":
    titleScreen()