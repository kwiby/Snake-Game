from random import randint
import time
import pygame

pygame.init()


# | ----------------- |
# | -+- Variables -+- | ----------------------------------------------------------------------------------------------------<>
# | ----------------- |

# -+- Display Stuff -+-
WIDTH = 800
HEIGHT = 800
gameWindow = pygame.display.set_mode((WIDTH, HEIGHT))

TOP = 0
BOTTOM = HEIGHT
WIDTH_MIDDLE = WIDTH / 2
HEIGHT_MIDDLE = HEIGHT / 2

defaultDelay = 80 #speed of snake (Defaults: Easy - 100, Medium - 80, Hard - 50)
delay = defaultDelay

# -+- Colours -+-
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)
X_RED = (210, 70, 70)

BORDER_GREEN = (70, 130, 70)
SCOREBOARD_GREEN = (80, 150, 80)
TITLE_COLOUR = (180, 150, 70)
TITLE_SHADOW_COLOUR = (100, 90, 80)
GRID_GREEN_1 = (130, 180, 120)
GRID_GREEN_2 = (125, 175, 115)
BLUE1 = (80, 120, 190)
BLUE2 = (70, 100, 170)

snakeHeadColours = [(80, 120, 190), (80, 175, 75), (190, 80, 80), (190, 130, 80), (190, 180, 80), (135, 80, 190), (60, 60, 60), (180, 180, 180)] #Blue, Green, Red, Orange, Yellow, Purple, Dark Gray, Light Gray
snakeBodyColours = [(70, 100, 170), (70, 160, 60), (170, 70, 70), (180, 110, 60), (170, 160, 70), (110, 70, 170), (40, 40, 40), (160, 160, 160)]

# -+- Design Variables -+-
BORDER_WIDTH = 10
SCOREBOARD_HEIGHT = 160

# -+- Snake's Properties -+-
SNAKE_R = 10
SNAKE_D = SNAKE_R * 2
HORIZONTAL_STEP = 20
VERTICAL_STEP = 20
stepX = 0
stepY = -VERTICAL_STEP #initially the snake moves upwards
snakeX = []
snakeY = []
for i in range(3): #add coordinates for the head and 3 segments
    snakeX.append(WIDTH_MIDDLE)
    snakeY.append(HEIGHT_MIDDLE + 300)

# -+- Time Variables -+-
timeCheck = True #used to check if you are looping through the while statement for the first time or not
timerBoost = 0 #the value added to the timer when you eat two apples quickly or after you pause
BOOST_PERIOD = 1.5 #how long you have in seconds to eat two apples to get a boost
TIME_CONVERSION = 60
elapsedTime = 0
maxTime = 180 #time remaining in seconds (Defaults: Easy - 300 seconds or 5 minutes, Medium - 180 seconds or 3 minutes, Hard - 60 seconds or 1 minute)
lastAppleEatenTime = maxTime
seconds = 0
minutes = 0
pausedTime = 0

# -+- Volume Variables -+-
volumeValue = 0.5
volumeText = 50
volumeSliderStart = WIDTH / 16 + 5
volumeSliderEnd = WIDTH / 3 - 5
volumeSliderWidth = (volumeSliderEnd - volumeSliderStart) / 2 + volumeSliderStart

# -+- Difficulty Variables -+-
difficultyText = 2
difficultySliderStart = WIDTH - WIDTH / 2.9 + 5
difficultySliderEnd = WIDTH / 1.06 - 5
DIFFICULTY_SLIDER_WIDTH_DEFAULT = difficultySliderEnd - difficultySliderStart
difficultySliderWidth = DIFFICULTY_SLIDER_WIDTH_DEFAULT / 2 + difficultySliderStart

# -+- Border Death Variables -+-
borderDeath = True
borderDeathButtonMoveValue = 20
borderDeathOnText = WHITE
borderDeathOffText = BLACK

# -+- Obstacles Variables -+-
obstacles = False
obstaclesButtonMoveValue = 60
obstaclesOnText = BLACK
obstaclesOffText = WHITE
obstacleAmount = 10 #amount of obstacles (Defaults: Easy - 5, Medium - 10, Hard - 15)###
obstacleX = [None] * obstacleAmount
obstacleY = [None] * obstacleAmount
spawnObstacles = True
obstacleLocations = []

# -+- Score Variables -+-
score = 0
highScore = 0

# -+- Images -+-
appleImageFile = pygame.image.load("Images\Apple.PNG")
appleImage = pygame.transform.scale(appleImageFile, (SNAKE_D, SNAKE_D))

# -+- Audio -+-
pygame.mixer.music.load("Audio\Music.ogg")
buttonClick = pygame.mixer.Sound("Audio\Button Click.ogg")
appleEaten = pygame.mixer.Sound("Audio\Apple Eaten.ogg")
lost = pygame.mixer.Sound("Audio\Lost.ogg")

pygame.mixer.music.set_volume(0.5)
buttonClick.set_volume(0.5)
appleEaten.set_volume(0.5)
lost.set_volume(0.5)

pygame.mixer.music.play(-1)

# -+- Keybinds -+-
upKeybind = pygame.K_UP
downKeybind = pygame.K_DOWN
rightKeybind = pygame.K_RIGHT
leftKeybind = pygame.K_LEFT

upKeybindChange = False
downKeybindChange = False
rightKeybindChange = False
leftKeybindChange = False

upKeybindText = pygame.key.name(upKeybind)
downKeybindText = pygame.key.name(downKeybind)
rightKeybindText = pygame.key.name(rightKeybind)
leftKeybindText = pygame.key.name(leftKeybind)


# | ----------------- |
# | -+- Functions -+- | ----------------------------------------------------------------------------------------------------<>
# | ----------------- |

def drawText(font, text, size, colour, coords):
    font = pygame.font.SysFont(font, size)
    graphics = font.render(text, 1, colour)
    gameWindow.blit(graphics, coords)

def randomApple(whichApple):
    noRespawnAppleCoords = []
    for index in range(1, len(appleX)):
        noRespawnAppleCoords.append((appleX[index], appleY[index]))
        
    snakeCoords = []
    for index in range(len(snakeX)):
        snakeCoords.append((snakeX[index], snakeY[index]))
    
    if (whichApple == -1 or len(appleX) == 0):
        appleX.append(randint(1, WIDTH / 20 - 1) * SNAKE_D - SNAKE_R)
        appleY.append(randint((SCOREBOARD_HEIGHT + BORDER_WIDTH * 2) / 20 + 1, HEIGHT / 20 - 1) * SNAKE_D - SNAKE_R)
    
    while (((appleX[whichApple], appleY[whichApple]) in noRespawnAppleCoords) or ((appleX[whichApple] + SNAKE_R, appleY[whichApple] + SNAKE_R) in snakeCoords) or \
           ((appleX[whichApple], appleY[whichApple]) in obstacleLocations) or (appleX[whichApple] == WIDTH_MIDDLE - SNAKE_R)):
        appleX[whichApple] = randint(1, WIDTH / 20 - 1) * SNAKE_D - SNAKE_R
        appleY[whichApple] = randint((SCOREBOARD_HEIGHT + BORDER_WIDTH * 2) / 20 + 1, HEIGHT / 20 - 1) * SNAKE_D - SNAKE_R

def setObstacleCoords():
    global obstacleLocations
    
    snakeCoords = []
    for index in range(len(snakeX)):
        snakeCoords.append((snakeX[index], snakeY[index]))
    appleCoords = []
    for index in range(len(appleX)):
        appleCoords.append((appleX[index], appleY[index]))

    obstacleLocations = []
    for count in range(obstacleAmount):
        obstacleX[count] = randint(1, WIDTH / 20 - 1) * SNAKE_D - SNAKE_R
        obstacleY[count] = randint((SCOREBOARD_HEIGHT + BORDER_WIDTH * 2) / 20, HEIGHT / 20 - 1) * SNAKE_D - SNAKE_R
        while (((obstacleX[count], obstacleY[count]) in appleCoords) or ((obstacleX[count], obstacleY[count]) in snakeCoords) or \
               ((obstacleX[count], obstacleY[count]) in obstacleLocations) or (obstacleX[count] == WIDTH_MIDDLE - SNAKE_R)):
            obstacleX[count] = randint(1, WIDTH / 20 - 1) * SNAKE_D - SNAKE_R
            obstacleY[count] = randint((SCOREBOARD_HEIGHT + BORDER_WIDTH * 2) / 20 + 1, HEIGHT / 20 - 1) * SNAKE_D - SNAKE_R
        obstacleLocations.append((obstacleX[count], obstacleY[count]))

def drawSnakeEyes(x1, x2, y1, y2, radius):
    pygame.draw.circle(gameWindow, WHITE, (snakeX[0] + x1, snakeY[0] + y1), radius)
    pygame.draw.circle(gameWindow, WHITE, (snakeX[0] + x2, snakeY[0] + y2), radius)
    pygame.draw.circle(gameWindow, BLACK, (snakeX[0] + x1, snakeY[0] + y1), radius / 2)
    pygame.draw.circle(gameWindow, BLACK, (snakeX[0] + x2, snakeY[0] + y2), radius / 2)

def drawBackground():
        gameWindow.fill(GRID_GREEN_1)
        for row in range(0, 39):
            if (row % 2 == 0):
                gridSwitch = 20
            else:
                gridSwitch = 0
            for column in range(0, 39):
                if (column % 2 == 0):
                    pygame.draw.rect(gameWindow, GRID_GREEN_2, (10 + column * SNAKE_D - gridSwitch, 10 + row * SNAKE_D, SNAKE_D, SNAKE_D))
                    
        pygame.draw.rect(gameWindow, BORDER_GREEN, (0, 0, WIDTH, HEIGHT), 10)

def resetGame():
    global score, timeCheck, delay, defaultDelay, lastAppleEatenTime, maxTime, stepX, stepY, VERTICAL_STEP, snakeX, WIDTH_MIDDLE, snakeY, HEIGHT_MIDDLE, appleX, appleY, timerBoost, inWhatPage
    score = 0
    timeCheck = True
    delay = defaultDelay
    lastAppleEatenTime = maxTime
    stepX = 0
    stepY = -VERTICAL_STEP #initially the snake moves upwards
    snakeX = []
    snakeY = []
    for i in range(3): #add coordinates for the head and 3 segments
        snakeX.append(WIDTH_MIDDLE)
        snakeY.append(HEIGHT_MIDDLE + 300)
    appleX = []
    appleY = []
    timerBoost = 0
    randomApple(0)
    inWhatPage = "game"


# ----------------------------------------------------------------------------------------------------<>

# -+- Apple Properties -+-
spawnInterval = 5 #how long it takes for 1-2 apple(s) to spawn in seconds
appleCoords = []
appleX = [] #x coordinate of each apple
appleY = [] #y coordinate of each apple
randomApple(0) #0 or -1 is which index to add the apple to (0 is changing the first index [which is the only apple which respawns] and -1 is adding an apple at the end of the list)


# | ------------ |
# | -+- Main -+- | ----------------------------------------------------------------------------------------------------<>
# | ------------ |

inWhatPage = "title" #title, settings, game, pause, end, exit

while (inWhatPage != "exit"):
    # -+- Title Screen -+-
    if (inWhatPage == "title"):

        upKeybindChange = False
        downKeybindChange = False
        rightKeybindChange = False
        leftKeybindChange = False
        
        # - Drawing Title Stuff -
        
        # Drawing the background grid
        drawBackground()

        # Title
        drawText("Bold", "Snake Game", 150, TITLE_SHADOW_COLOUR, (WIDTH_MIDDLE - 320, HEIGHT_MIDDLE - 295))
        drawText("Bold", "Snake Game", 150, TITLE_COLOUR, (WIDTH_MIDDLE - 325, HEIGHT_MIDDLE - 300))

        # Start Button
        startRect = pygame.draw.rect(gameWindow, BLUE2, (WIDTH_MIDDLE - 140, HEIGHT_MIDDLE - 95, 285, 125), 10, 30)
        drawText("Bold", "Start", 150, BLUE1, (WIDTH_MIDDLE - 120, HEIGHT_MIDDLE - 80))
    
        # Settings Button
        settingsRect = pygame.draw.rect(gameWindow, BLUE2, (WIDTH_MIDDLE - 102, HEIGHT_MIDDLE + 40, 205, 70), 6, 15)
        drawText("Bold", "Settings", 60, BLUE1, (WIDTH_MIDDLE - 87, HEIGHT_MIDDLE + 55))

        # Exit Button
        exitRect = pygame.draw.rect(gameWindow, BLUE2, (WIDTH_MIDDLE - 60, HEIGHT_MIDDLE + 120, 113, 70), 6, 15)
        drawText("Bold", "Exit", 60, BLUE1, (WIDTH_MIDDLE - 45, HEIGHT_MIDDLE + 135))

        # Start Button Actions
        if (startRect.collidepoint(pygame.mouse.get_pos())):
            pygame.draw.rect(gameWindow, BLUE1, (WIDTH_MIDDLE - 230, HEIGHT_MIDDLE - 45, 75, 25), 0, 100)
            pygame.draw.rect(gameWindow, BLUE1, (WIDTH_MIDDLE + 160, HEIGHT_MIDDLE - 45, 75, 25), 0, 100)
            if (pygame.mouse.get_pressed()[0]): #[0] is the left click button
                spawnObstacles = True
                buttonClick.play()
                resetGame()

        # Settings Button Actions
        if (settingsRect.collidepoint(pygame.mouse.get_pos())):
            pygame.draw.rect(gameWindow, BLUE1, (WIDTH_MIDDLE - 158, HEIGHT_MIDDLE + 66, 45, 15), 0, 100)
            pygame.draw.rect(gameWindow, BLUE1, (WIDTH_MIDDLE + 115, HEIGHT_MIDDLE + 66, 45, 15), 0, 100)
            if (pygame.mouse.get_pressed()[0]): #[0] is the left click button
                buttonClick.play()
                inWhatPage = "settings"

        # Exit Button Actions
        if (exitRect.collidepoint(pygame.mouse.get_pos())):
            pygame.draw.rect(gameWindow, BLUE1, (WIDTH_MIDDLE - 118, HEIGHT_MIDDLE + 144, 45, 18), 0, 100)
            pygame.draw.rect(gameWindow, BLUE1, (WIDTH_MIDDLE + 65, HEIGHT_MIDDLE + 144, 45, 18), 0, 100)
            if (pygame.mouse.get_pressed()[0]): #[0] is the left click button
                inWhatPage = "exit"
    
        pygame.display.update()
        pygame.event.clear()


# ----------------------------------------------------------------------------------------------------<>

    # -+- Settings Screen -+-
    if (inWhatPage == "settings"):
        
        # - Drawing Settings Stuff -
        
        drawBackground()

        drawText("Bold", "Settings", 100, WHITE, (WIDTH_MIDDLE - 150, 50))

        # Drawing back button
        backRect = pygame.draw.rect(gameWindow, BORDER_GREEN, (0, 0, 100, 55), border_bottom_right_radius = 15)
        pygame.draw.polygon(gameWindow, WHITE, ((20, 29), (40, 15), (40, 25), (80, 25), (80, 35), (40, 35), (40, 45)))

        # Drawing volume stuff
        drawText("Bold", "Volume", 30, WHITE, (WIDTH / 16, HEIGHT / 4))
        drawText("Bold", str(volumeText) + "%", 30, WHITE, (WIDTH / 3 - 50, HEIGHT / 4))

        pygame.draw.line(gameWindow, BLUE2, (WIDTH / 16 - 3, HEIGHT / 4 + 50), (WIDTH / 3 + 3, HEIGHT / 4 + 50), 21)
        volumeSlider = pygame.draw.line(gameWindow, WHITE, (WIDTH / 16, HEIGHT / 4 + 50), (WIDTH / 3, HEIGHT / 4 + 50), 15)
        pygame.draw.line(gameWindow, BLUE1, (volumeSliderStart, HEIGHT / 4 + 50), (volumeSliderWidth, HEIGHT / 4 + 50), 8)

        #Drawing difficulty stuff
        drawText("Bold", "Difficulty", 30, WHITE, (WIDTH - WIDTH / 2.9, HEIGHT / 4))
        drawText("Bold", str(difficultyText), 30, WHITE, (WIDTH / 1.06 - 15, HEIGHT / 4))

        pygame.draw.line(gameWindow, BLUE2, (WIDTH - WIDTH / 2.9 - 3, HEIGHT / 4 + 50), (WIDTH / 1.06 + 3, HEIGHT / 4 + 50), 21)
        difficultySlider = pygame.draw.line(gameWindow, WHITE, (WIDTH - WIDTH / 2.9, HEIGHT / 4 + 50), (WIDTH / 1.06, HEIGHT / 4 + 50), 15)
        pygame.draw.line(gameWindow, BLUE1, (difficultySliderStart, HEIGHT / 4 + 50), (difficultySliderWidth, HEIGHT / 4 + 50), 8)

        # Drawing border death stuff
        drawText("Bold", "Border Death", 30, WHITE, (WIDTH / 16, HEIGHT / 4 + 100))
        pygame.draw.rect(gameWindow, BLUE2, (WIDTH / 16 - 3, HEIGHT / 4 + 138, 86, 46), 0, 100)
        pygame.draw.rect(gameWindow, WHITE, (WIDTH / 16, HEIGHT / 4 + 141, 80, 40), 0, 100)
        borderDeathButton = pygame.draw.circle(gameWindow, BLUE1, (WIDTH / 16 + borderDeathButtonMoveValue, HEIGHT / 4 + 161), 16)
        if (borderDeath == True):
            borderDeathOnText = WHITE
            borderDeathOffText = BLACK
        else:
            borderDeathOnText = BLACK
            borderDeathOffText = WHITE
        drawText("Bold", "ON", 15, borderDeathOnText, (WIDTH / 16 + 12, HEIGHT / 4 + 156))
        drawText("Bold", "OFF", 15, borderDeathOffText, (WIDTH / 16 + 50, HEIGHT / 4 + 156))

        # Drawing obstacles stuff
        drawText("Bold", "Obstacles", 30, WHITE, (WIDTH - WIDTH / 2.9, HEIGHT / 4 + 100))
        pygame.draw.rect(gameWindow, BLUE2, (WIDTH - WIDTH / 2.9 - 3, HEIGHT / 4 + 138, 86, 46), 0, 100)
        pygame.draw.rect(gameWindow, WHITE, (WIDTH - WIDTH / 2.9, HEIGHT / 4 + 141, 80, 40), 0, 100)
        obstaclesButton = pygame.draw.circle(gameWindow, BLUE1, (WIDTH - WIDTH / 2.9 + obstaclesButtonMoveValue, HEIGHT / 4 + 161), 16)
        if (obstacles == True):
            obstaclesOnText = WHITE
            obstaclesOffText = BLACK
        else:
            obstaclesOnText = BLACK
            obstaclesOffText = WHITE
        drawText("Bold", "ON", 15, obstaclesOnText, (WIDTH - WIDTH / 2.9 + 12, HEIGHT / 4 + 156))
        drawText("Bold", "OFF", 15, obstaclesOffText, (WIDTH - WIDTH / 2.9 + 50, HEIGHT / 4 + 156))

        # Drawing keybinds stuff
        drawText("Bold", "Keybinds", 30, WHITE, (WIDTH / 16, HEIGHT / 4 + 220))

        # Up Keybind
        drawText("Bold", "--- Up Key", 20, WHITE, (WIDTH / 16 + 60, HEIGHT / 4 + 265, 56, 36))
        pygame.draw.rect(gameWindow, BLUE2, (WIDTH / 16 - 3, HEIGHT / 4 + 255, 56, 36), 0, 10)
        upKeybindRect = pygame.draw.rect(gameWindow, WHITE, (WIDTH / 16, HEIGHT / 4 + 258, 50, 30), 0, 10)
        drawText("Bold", upKeybindText, 20, BLACK, (WIDTH / 16 + 3, HEIGHT / 4 + 266))

        # Left Keybind    
        drawText("Bold", "--- Left Key", 20, WHITE, (WIDTH / 16 + 60, HEIGHT / 4 + 315, 56, 36))
        pygame.draw.rect(gameWindow, BLUE2, (WIDTH / 16 - 3, HEIGHT / 4 + 305, 56, 36), 0, 10)
        leftKeybindRect = pygame.draw.rect(gameWindow, WHITE, (WIDTH / 16, HEIGHT / 4 + 308, 50, 30), 0, 10)
        drawText("Bold", leftKeybindText, 20, BLACK, (WIDTH / 16 + 3, HEIGHT / 4 + 316, 50, 30))
            
        # Down Keybind    
        drawText("Bold", "--- Down Key", 20, WHITE, (WIDTH / 16 + 60, HEIGHT / 4 + 365, 56, 36))
        pygame.draw.rect(gameWindow, BLUE2, (WIDTH / 16 - 3, HEIGHT / 4 + 355, 56, 36), 0, 10)
        downKeybindRect = pygame.draw.rect(gameWindow, WHITE, (WIDTH / 16, HEIGHT / 4 + 358, 50, 30), 0, 10)
        drawText("Bold", downKeybindText, 20, BLACK, (WIDTH / 16 + 3, HEIGHT / 4 + 366, 50, 30))

        # Right Keybind    
        drawText("Bold", "--- Right Key", 20, WHITE, (WIDTH / 16 + 60, HEIGHT / 4 + 415, 56, 36))
        pygame.draw.rect(gameWindow, BLUE2, (WIDTH / 16 - 3, HEIGHT / 4 + 405, 56, 36), 0, 10)
        rightKeybindRect = pygame.draw.rect(gameWindow, WHITE, (WIDTH / 16, HEIGHT / 4 + 408, 50, 30), 0, 10)
        drawText("Bold", rightKeybindText, 20, BLACK, (WIDTH / 16 + 3, HEIGHT / 4 + 416, 50, 30))

        # Drawing snake colour stuff
        drawText("Bold", "Snake Colour", 30, WHITE, (WIDTH - WIDTH / 2.9, HEIGHT / 4 + 220))
        pygame.draw.rect(gameWindow, snakeHeadColours[0], (WIDTH - WIDTH / 2.9 + 30, HEIGHT / 4 + 255, 40, 40), 0, 10)
        pygame.draw.rect(gameWindow, snakeBodyColours[0], (WIDTH - WIDTH / 2.9 + 70, HEIGHT / 4 + 255, 40, 40), 0, 10)
        pygame.draw.rect(gameWindow, snakeBodyColours[0], (WIDTH - WIDTH / 2.9 + 110, HEIGHT / 4 + 255, 40, 40), 0, 10)
        
        pygame.draw.circle(gameWindow, WHITE, (WIDTH - WIDTH / 2.9 + 40, HEIGHT / 4 + 285), 8)
        pygame.draw.circle(gameWindow, WHITE, (WIDTH - WIDTH / 2.9 + 40, HEIGHT / 4 + 265), 8)
        pygame.draw.circle(gameWindow, BLACK, (WIDTH - WIDTH / 2.9 + 40, HEIGHT / 4 + 285), 4)
        pygame.draw.circle(gameWindow, BLACK, (WIDTH - WIDTH / 2.9 + 40, HEIGHT / 4 + 265), 4)

        leftArrowRect = pygame.Rect(WIDTH - WIDTH / 2.9, HEIGHT / 4 + 263, 20, 20)
        rightArrowRect = pygame.Rect(WIDTH - WIDTH / 2.9 + 160, HEIGHT / 4 + 263, 20, 20)
        drawText("Bold", "<", 50, WHITE, (WIDTH - WIDTH / 2.9, HEIGHT / 4 + 253))
        drawText("Bold", ">", 50, WHITE, (WIDTH - WIDTH / 2.9 + 160, HEIGHT / 4 + 253))

        # Drawing apple spawn interval
        drawText("Bold", "Apple Spawn Interval", 30, WHITE, (WIDTH - WIDTH / 2.9, HEIGHT / 4 + 330))
        pygame.draw.rect(gameWindow, BLUE2, (WIDTH - WIDTH / 2.9 + 27, HEIGHT / 4 + 372, 46, 36), 0, 10)
        intervalRect = pygame.draw.rect(gameWindow, WHITE, (WIDTH - WIDTH / 2.9 + 30, HEIGHT / 4 + 375, 40, 30), 0, 10)

        minusRect = pygame.Rect(WIDTH - WIDTH / 2.9 - 4, HEIGHT / 4 + 378, 20, 20)
        plusRect = pygame.Rect(WIDTH - WIDTH / 2.9 + 86, HEIGHT / 4 + 380, 20, 20)
        drawText("Bold", "-", 50, WHITE, (WIDTH - WIDTH / 2.9, HEIGHT / 4 + 370))
        drawText("Bold", "+", 50, WHITE, (WIDTH - WIDTH / 2.9 + 86, HEIGHT / 4 + 370))

        drawText("Bold", str(spawnInterval), 25, BLACK, (WIDTH - WIDTH / 2.9 + 40, HEIGHT / 4 + 383))
        
        # Back button actions
        if (backRect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]):
            buttonClick.play()
            inWhatPage = "title"
                
        # Volume slider actions
        if (volumeSlider.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]):
            if (pygame.mouse.get_pos()[0] <= volumeSliderStart + 3.5):
                volumeSliderWidth = volumeSliderStart + 1
                volumeValue = 0
                volumeText = 0
            if (pygame.mouse.get_pos()[0] >= WIDTH / 3 - 6):
                volumeSliderWidth = volumeSliderEnd + 1
                volumeValue = 100
                volumeText = 100
            if ((pygame.mouse.get_pos()[0] > volumeSliderStart) and (pygame.mouse.get_pos()[0] < volumeSliderEnd)):
                volumeSliderWidth = pygame.mouse.get_pos()[0]
                volumeValue = round((pygame.mouse.get_pos()[0] - volumeSliderStart) / (volumeSliderEnd - volumeSliderStart), 2)
                volumeText = round(volumeValue * 100)
            pygame.mixer.music.set_volume(volumeValue)
            buttonClick.set_volume(volumeValue)
            appleEaten.set_volume(volumeValue)
            lost.set_volume(volumeValue)

        # Difficulty slider actions
        if (difficultySlider.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]):
            difficultySliderWidth = pygame.mouse.get_pos()[0]
            if (difficultySliderWidth <= DIFFICULTY_SLIDER_WIDTH_DEFAULT / 16 + difficultySliderStart - 10):
                difficultySliderWidth = difficultySliderStart + 1
            if (difficultySliderWidth >= DIFFICULTY_SLIDER_WIDTH_DEFAULT + difficultySliderStart):
                difficultySliderWidth = difficultySliderEnd
        if (not pygame.mouse.get_pressed()[0]):
            if (difficultySliderWidth <= DIFFICULTY_SLIDER_WIDTH_DEFAULT / 4 + difficultySliderStart):
                difficultySliderWidth = difficultySliderStart + 1
                obstacleAmount = 5
                maxTime = 300
                defaultDelay = 100
                difficultyText = 1
                obstacleX = [None] * obstacleAmount
                obstacleY = [None] * obstacleAmount
            if (difficultySliderWidth >= DIFFICULTY_SLIDER_WIDTH_DEFAULT / 4 + difficultySliderStart and difficultySliderWidth <= difficultySliderEnd - DIFFICULTY_SLIDER_WIDTH_DEFAULT / 4):
                difficultySliderWidth = DIFFICULTY_SLIDER_WIDTH_DEFAULT / 2 + difficultySliderStart
                obstacleAmount = 10
                maxTime = 180
                defaultDelay = 80
                difficultyText = 2
                obstacleX = [None] * obstacleAmount
                obstacleY = [None] * obstacleAmount
            if (difficultySliderWidth >= difficultySliderEnd - DIFFICULTY_SLIDER_WIDTH_DEFAULT / 4):
                difficultySliderWidth = difficultySliderEnd
                obstacleAmount = 15
                maxTime = 60
                defaultDelay = 50
                difficultyText = 3
                obstacleX = [None] * obstacleAmount
                obstacleY = [None] * obstacleAmount

        # Border death button actions
        if (borderDeathButton.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]):
            if (borderDeath == True):
                borderDeath = False
                borderDeathButtonMoveValue = 60
            else:
                borderDeath = True
                borderDeathButtonMoveValue = 20

        # Obstacles button actions
        if (obstaclesButton.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]):
            if (obstacles == True):
                obstacles = False
                obstaclesButtonMoveValue = 60
            else:
                obstacles = True
                obstaclesButtonMoveValue = 20

        # Keybind stuff actions
        keys = pygame.key.get_pressed()
        if (pygame.mouse.get_pressed()[0] and upKeybindRect.collidepoint(pygame.mouse.get_pos())):
            upKeybindChange = True
            downKeybindChange = False
            rightKeybindChange = False
            leftKeybindChange = False
            upKeybindText = "[_____]"
        if (pygame.mouse.get_pressed()[0] and downKeybindRect.collidepoint(pygame.mouse.get_pos())):
            downKeybindChange = True
            upKeybindChange = False
            rightKeybindChange = False
            leftKeybindChange = False
            downKeybindText = "[_____]"
        if (pygame.mouse.get_pressed()[0] and rightKeybindRect.collidepoint(pygame.mouse.get_pos())):
            rightKeybindChange = True
            upKeybindChange = False
            downKeybindChange = False
            leftKeybindChange = False
            rightKeybindText = "[_____]"
        if (pygame.mouse.get_pressed()[0] and leftKeybindRect.collidepoint(pygame.mouse.get_pos())):
            leftKeybindChange = True
            upKeybindChange = False
            downKeybindChange = False
            rightKeybindChange = False
            leftKeybindText = "[_____]"

        if ((upKeybindChange == True) or (downKeybindChange == True) or (rightKeybindChange == True) or (leftKeybindChange == True)):
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if (upKeybindChange == True):
                        upKeybind = event.key
                        upKeybindText = pygame.key.name(upKeybind)
                        upKeybindChange = False

                    if (downKeybindChange == True):
                        downKeybind = event.key
                        downKeybindText = pygame.key.name(downKeybind)
                        downKeybindChange = False

                    if (rightKeybindChange == True):
                        rightKeybind = event.key
                        rightKeybindText = pygame.key.name(rightKeybind)
                        rightKeybindChange = False

                    if (leftKeybindChange == True):
                        leftKeybind = event.key
                        leftKeybindText = pygame.key.name(leftKeybind)
                        leftKeybindChange = False

        # Arrow buttons actions
        if (pygame.mouse.get_pressed()[0] and leftArrowRect.collidepoint(pygame.mouse.get_pos())):
            tempValueHold1 = snakeHeadColours[0]
            tempValueHold2 = snakeBodyColours[0]
            for index in range(len(snakeHeadColours)):
                if (index == len(snakeHeadColours) - 1):
                    snakeHeadColours[index] = tempValueHold1
                    snakeBodyColours[index] = tempValueHold2
                else:
                    snakeHeadColours[index] = snakeHeadColours[index + 1]
                    snakeBodyColours[index] = snakeBodyColours[index + 1]
            time.sleep(0.1)
                        
        if (pygame.mouse.get_pressed()[0] and rightArrowRect.collidepoint(pygame.mouse.get_pos())):
            tempValueHold1 = snakeHeadColours[-1]
            tempValueHold2 = snakeBodyColours[-1]
            for index in range(len(snakeBodyColours) - 1, -1, -1):
                if (index == 0):
                    snakeHeadColours[index] = tempValueHold1
                    snakeBodyColours[index] = tempValueHold2
                else:
                    snakeHeadColours[index] = snakeHeadColours[index - 1]
                    snakeBodyColours[index] = snakeBodyColours[index - 1]
            time.sleep(0.1)

        # Interval buttons actions
        if (pygame.mouse.get_pressed()[0] and minusRect.collidepoint(pygame.mouse.get_pos())):
            if (spawnInterval > 1):
                spawnInterval -= 1
            time.sleep(0.1)
        if (pygame.mouse.get_pressed()[0] and plusRect.collidepoint(pygame.mouse.get_pos())):
            if (spawnInterval < 30):
                spawnInterval += 1
            time.sleep(0.1)
            

        # Updates
        pygame.display.update()
        pygame.event.clear()


# ----------------------------------------------------------------------------------------------------<>

    # -+- Game Screen -+-
    if (inWhatPage == "game"):
        # - Drawing Game Stuff -

        # Drawing the background grid
        gameWindow.fill(GRID_GREEN_1)
        for row in range(0, 39):
            if (row % 2 == 0):
                gridSwitch = 20
            else:
                gridSwitch = 0
            for column in range(0, 39):
                if (column % 2 == 0):
                    pygame.draw.rect(gameWindow, GRID_GREEN_2, (10 + column * SNAKE_D - gridSwitch, 10 + row * SNAKE_D, SNAKE_D, SNAKE_D))

        # Drawing borders/other bckgrounds
        pygame.draw.rect(gameWindow, SCOREBOARD_GREEN, (BORDER_WIDTH, BORDER_WIDTH, WIDTH - 20, SCOREBOARD_HEIGHT)) #drawing the scoreboard
        pygame.draw.rect(gameWindow, BORDER_GREEN, (0, 0, WIDTH, HEIGHT), BORDER_WIDTH) #drawing the border
        pygame.draw.line(gameWindow, BORDER_GREEN, (0, SCOREBOARD_HEIGHT + 4), (WIDTH, SCOREBOARD_HEIGHT + 4), BORDER_WIDTH) #drawing the border

        # Drawing the scoreboard
        drawText("Bold", "Best: " + str(highScore), 60, WHITE, (605, 64))
        drawText("Bold", "Score: " + str(score), 60, WHITE, (330, 64)) #drawing the score counter
        if (seconds > 9): #drawing the timer
            drawText("Bold", "Time: " + str(minutes) + ":" + str(seconds), 60, WHITE, (55, 64))
        else:
            drawText("Bold", "Time: " + str(minutes) + ":0" + str(seconds), 60, WHITE, (55, 64)) #if the seconds is one digit, it needs a 0 in front of it so the the formatting is proper in the scoreboard

        # Drawing the apples
        for index in range(len(appleX)):
            gameWindow.blit(appleImage, (appleX[index], appleY[index]))

        # Drawing the obstacles
        if (obstacles == True):
            if (spawnObstacles == True):
                setObstacleCoords()
                spawnObstacles = False
            for index in range(obstacleAmount):
                pygame.draw.rect(gameWindow, TITLE_COLOUR, (obstacleX[index], obstacleY[index], SNAKE_D, SNAKE_D))
                pygame.draw.rect(gameWindow, TITLE_SHADOW_COLOUR, (obstacleX[index], obstacleY[index], SNAKE_D, SNAKE_D), 1)
                pygame.draw.rect(gameWindow, TITLE_SHADOW_COLOUR, (obstacleX[index], obstacleY[index], SNAKE_D, SNAKE_D), 1, 30)
                pygame.draw.rect(gameWindow, TITLE_SHADOW_COLOUR, (obstacleX[index] + 5, obstacleY[index] + 5, SNAKE_R, SNAKE_R), 1)
                pygame.draw.rect(gameWindow, TITLE_SHADOW_COLOUR, (obstacleX[index] + 5, obstacleY[index] + 5, SNAKE_R, SNAKE_R), 1, 30)
                
        # Time Stuff
        if (timeCheck == True):
            startTime = time.time()
            elapsedTime -= elapsedTime
            timeCheck = False
        elapsedTime = time.time() - startTime
        timer = round(maxTime - elapsedTime) + timerBoost
        seconds = timer % TIME_CONVERSION
        minutes = timer // TIME_CONVERSION
        if (minutes <= 0 and seconds <= 0):
            lost.play()
            inWhatPage = "end"

        lastIndex = len(snakeX) - 1
            
        # Drawing the snake
        for i in range(len(snakeX)):
            if (i == 0):
                segmentColour = snakeHeadColours[0]
            else:
                segmentColour = snakeBodyColours[0]
            
            pygame.draw.rect(gameWindow, segmentColour, (snakeX[i] - SNAKE_R, snakeY[i] - SNAKE_R, SNAKE_D, SNAKE_D), 0, 5)
        
            if (stepY < 0):
                drawSnakeEyes(-5, 5, -5, -5,4 ) #eye coords for when the snake is going up
            elif (stepY > 0):
                drawSnakeEyes(-5, 5, 5, 5, 4) #eye coords for when the snake is going down
            elif (stepX < 0):
                drawSnakeEyes(-5, -5, 5, -5, 4) #eye coords for when the snake is going left
            else:
                drawSnakeEyes(5, 5, 5, -5, 4) #eye coords for when the snake is going right

        # Updates
        pygame.time.delay(delay)
        pygame.display.update()
        pygame.event.clear()

        # Keybinds and Movement Conditions
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_ESCAPE]):
            pausedStartTime = time.time()
            inWhatPage = "pause"
        if (keys[leftKeybind] and (snakeX[1] + SNAKE_D != snakeX[0]) and (snakeX[1] != snakeX[0] + 760)):
            stepX = -HORIZONTAL_STEP
            stepY = 0
        if (keys[rightKeybind] and (snakeX[1] - SNAKE_D != snakeX[0]) and (snakeX[1] != snakeX[0] - 760)):
            stepX = HORIZONTAL_STEP
            stepY = 0
        if (keys[upKeybind] and (snakeY[1] + SNAKE_D != snakeY[0]) and (snakeY[1] != snakeY[0] + 600)):
            stepX = 0
            stepY = -VERTICAL_STEP
        if (keys[downKeybind] and (snakeY[1] - SNAKE_D != snakeY[0]) and (snakeY[1] != snakeY[0] - 600)):
            stepX = 0
            stepY = VERTICAL_STEP
            
        # Move the segments
        for i in range(lastIndex, 0, -1): #starting from the tail, and going backwards:
            snakeX[i] = snakeX[i - 1] #every segment takes the coordinates
            snakeY[i] = snakeY[i - 1] #of the previous one
            
        # Move the head
        snakeX[0] += stepX
        snakeY[0] += stepY


        # Checking if the snake hits the border
        for index in range(len(snakeX)):
            if (snakeX[index] < SNAKE_R + BORDER_WIDTH or snakeX[index] > WIDTH - SNAKE_R - BORDER_WIDTH \
                or snakeY[index] < SNAKE_R + SCOREBOARD_HEIGHT + BORDER_WIDTH or snakeY[index] > HEIGHT - SNAKE_R - BORDER_WIDTH):
                if (borderDeath == True):
                    lost.play()
                    inWhatPage = "end"
                else:
                    if (stepY < 0):
                        snakeY[index] += 620
                    elif (stepY > 0):
                        snakeY[index] -= 620
                    elif (stepX < 0):
                        snakeX[index] += 780
                    else:
                        snakeX[index] -= 780        

        # Detecting when the snake cuts into itself
        snakeBodyCoords = []
        for index in range(1, len(snakeX)):
            snakeBodyCoords.append((snakeX[index], snakeY[index]))
        if ((snakeX[0], snakeY[0]) in snakeBodyCoords):
            lost.play()
            inWhatPage = "end"
                    

        # Detecting when the snake hits an obstacle
        if (((snakeX[0] - SNAKE_R, snakeY[0] - SNAKE_R) in obstacleLocations) and (obstacles == True)):
            lost.play()
            inWhatPage = "end"

        # Detecting when the snake eats an apple
        appleCoords = []
        for index in range(len(appleX)):
            appleCoords.append((appleX[index], appleY[index]))
            
        if ((snakeX[0] - SNAKE_R, snakeY[0] - SNAKE_R) in appleCoords):
            if ((lastAppleEatenTime - timer < BOOST_PERIOD) and (lastAppleEatenTime - timer >= 0)): #boosting timer if you eat two apples within a certain time period
                timerBoost += 5
            lastAppleEatenTime = timer
            
            score += 1
            if (score > highScore):
                highScore = score
                
            snakeX.append(snakeX[lastIndex])
            snakeY.append(snakeY[lastIndex])
            
            if (appleX.index(snakeX[0] - SNAKE_R) == 0): #checking if the index of the eaten apple is the first apple (so the one that respawns)
                randomApple(0)
            else:
                appleIndex = appleCoords.index((snakeX[0] - SNAKE_R, snakeY[0] - SNAKE_R))
                appleX.pop(appleIndex)
                appleY.pop(appleIndex)
                
            delay = defaultDelay - score // 5 * 3 #increases speed (delay - 3) every 5 apples eaten

            appleEaten.play()

        if ((round(time.time() - startTime, 1) % spawnInterval in [0, 0.1]) and (timer != maxTime)): #0 and 0.1 because the timer can sometimes be both depending on the rounding, and it also
                                                                                                      #adds an extra cool feature of sometimes having two apples spawn at once
            randomApple(-1)


# ----------------------------------------------------------------------------------------------------<>

    # -+- Pause Screen -+-
    if (inWhatPage == "pause"):
        pausedTime = round(time.time() - pausedStartTime)
        
        pauseCover = pygame.Surface((WIDTH, HEIGHT))
        pauseCover.fill((100, 200, 100))
        pauseCover.set_alpha(3)  
        gameWindow.blit(pauseCover, (0, 0))

        # - Drawing the pause menu -

        pygame.draw.rect(gameWindow, SCOREBOARD_GREEN, (WIDTH_MIDDLE - 250, HEIGHT_MIDDLE - 150, 500, 300), 0, 15)
        pygame.draw.rect(gameWindow, BORDER_GREEN, (WIDTH_MIDDLE - 250, HEIGHT_MIDDLE - 150, 500, 300), 10, 15)
        drawText("Courier", "Paused", 80, WHITE, (WIDTH_MIDDLE - 220, HEIGHT_MIDDLE - 130))

        # Drawing the X button
        xRect = pygame.draw.rect(gameWindow, SCOREBOARD_GREEN, (WIDTH_MIDDLE + 217, HEIGHT_MIDDLE - 137, 20, 20), 0, 5)
        drawText("Bold", "X", 30, X_RED, (WIDTH_MIDDLE + 220, HEIGHT_MIDDLE - 135))

        # Drawing the menu button
        menuRect = pygame.draw.rect(gameWindow, BLUE2, (WIDTH_MIDDLE - 180, HEIGHT_MIDDLE, 150, 75), 0, 13)
        drawText("Bold", "Menu", 60, WHITE, (WIDTH_MIDDLE - 161, HEIGHT_MIDDLE + 19))

        # Drawing the restart button
        restartRect = pygame.draw.rect(gameWindow, BLUE2, (WIDTH_MIDDLE + 10, HEIGHT_MIDDLE, 170, 75), 0, 13)
        drawText("Bold", "Restart", 60, WHITE, (WIDTH_MIDDLE + 21, HEIGHT_MIDDLE + 19))
        
        # X button actions
        if (xRect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]):
            timerBoost += pausedTime
            time.sleep(0.3)
            inWhatPage = "game"

        # Menu button actions
        if (menuRect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]):
            buttonClick.play()
            time.sleep(0.2)
            inWhatPage = "title"

        # Restart button actions
        if (restartRect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]):
            spawnObstacles = True
            buttonClick.play()
            resetGame()

        # Updates
        pygame.display.update()
        pygame.event.clear()


# ----------------------------------------------------------------------------------------------------<>

    # -+- End Screen -+-
    if (inWhatPage == "end"):
        pauseCover = pygame.Surface((WIDTH, HEIGHT))
        pauseCover.fill((100, 200, 100))
        pauseCover.set_alpha(3)  
        gameWindow.blit(pauseCover, (0, 0))

        # - Drawing the end menu -

        pygame.draw.rect(gameWindow, SCOREBOARD_GREEN, (WIDTH_MIDDLE - 250, HEIGHT_MIDDLE - 150, 500, 300), 0, 15)
        pygame.draw.rect(gameWindow, BORDER_GREEN, (WIDTH_MIDDLE - 250, HEIGHT_MIDDLE - 150, 500, 300), 10, 15)
        drawText("Courier", "Game Over", 80, WHITE, (WIDTH_MIDDLE - 215, HEIGHT_MIDDLE - 130))

        # Drawing the menu button
        menuRect = pygame.draw.rect(gameWindow, BLUE2, (WIDTH_MIDDLE - 180, HEIGHT_MIDDLE, 150, 75), 0, 13)
        drawText("Bold", "Menu", 60, WHITE, (WIDTH_MIDDLE - 161, HEIGHT_MIDDLE + 19))

        # Drawing the restart button
        restartRect = pygame.draw.rect(gameWindow, BLUE2, (WIDTH_MIDDLE + 10, HEIGHT_MIDDLE, 170, 75), 0, 13)
        drawText("Bold", "Restart", 60, WHITE, (WIDTH_MIDDLE + 21, HEIGHT_MIDDLE + 19))

        # Menu button actions
        if (menuRect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]):
            buttonClick.play()
            time.sleep(0.2)
            inWhatPage = "title"

        # Restart button actions
        if (restartRect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]):
            spawnObstacles = True
            buttonClick.play()
            resetGame()

        # Updates
        pygame.display.update()
        pygame.event.clear()

("Exited.")

pygame.quit()
