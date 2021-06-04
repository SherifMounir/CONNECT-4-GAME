import numpy as np
import sys
import math
import random
import pygame

GAME_ROW_NUMBER = 6
GAME_COLUMN_NUMBER = 7
SQUARE_SIZE = 100
PLAYER = 0
AI = 1
RADIUS = int(SQUARE_SIZE/2 - 7)
GREY = (128 , 128 , 128)
WHITE = (224 , 224 , 224)
BLACK = (0 , 0 , 0)
RED = (255 , 0 , 0)
BLUE = (0 , 0 , 255)

def createGameCells(): #42 Cell , 6 rows and 7 columns
    gameCells = np.zeros((GAME_ROW_NUMBER , GAME_COLUMN_NUMBER))
    return gameCells

def validCellLocation(gameBoard , selection):
    if gameBoard[GAME_ROW_NUMBER - 1][selection] == 0:
        return True
    else:
        return False

def nextOpenCell(gameBoard , selection):
    for row in range(GAME_ROW_NUMBER):
        if gameBoard[row][selection] == 0:
            return row

def dropPieceInCell(gameBoard , row , col , piece):
    gameBoard[row][col] = piece
    
def flipOverBoard(gameBoard):
    print(np.flip(gameBoard , 0))

def winningGameMove(gameBoard , piece):
    # Check horizontal location for Win
    for col in range(GAME_COLUMN_NUMBER - 3):
        for row in range(GAME_ROW_NUMBER):
            if gameBoard[row][col] == piece and gameBoard[row][col + 1] == piece and gameBoard[row][col + 2] == piece and gameBoard[row][col + 3] == piece:
                return True
    # Check Vertical Location for win        
    for col in range(GAME_COLUMN_NUMBER):
        for row in range(GAME_ROW_NUMBER - 3):
            if gameBoard[row][col] == piece and gameBoard[row + 1][col] == piece and gameBoard[row + 2][col] == piece and gameBoard[row + 3][col] == piece:
                return True    
    # Check Positively sloped diagonals
    for col in range(GAME_COLUMN_NUMBER - 3):
        for row in range(GAME_ROW_NUMBER - 3):
            if gameBoard[row][col] == piece and gameBoard[row + 1][col + 1] == piece and gameBoard[row + 2][col + 2] == piece and gameBoard[row + 3][col + 3] == piece:
                return True      
    # Check Negatively sloped diagonals
    for col in range(GAME_COLUMN_NUMBER - 3):
        for row in range(3 ,GAME_ROW_NUMBER):
            if gameBoard[row][col] == piece and gameBoard[row - 1][col + 1] == piece and gameBoard[row - 2][col + 2] == piece and gameBoard[row - 3][col + 3] == piece:
                return True 
    for col in range(GAME_COLUMN_NUMBER - 1 , 2):
        for row in range(3 ,GAME_ROW_NUMBER):
            if gameBoard[row][col] == piece and gameBoard[row - 1][col - 1] == piece and gameBoard[row - 2][col - 2] == piece and gameBoard[row - 3][col - 3] == piece:
                return True 

def drawGameGraphics(gameBoard):
    for col in range(GAME_COLUMN_NUMBER):
        for row in range(GAME_ROW_NUMBER): 
            pygame.draw.rect(gameScreen , GREY , (col*SQUARE_SIZE , row*SQUARE_SIZE+SQUARE_SIZE , SQUARE_SIZE , SQUARE_SIZE))
            pygame.draw.circle(gameScreen , WHITE , (int(col*SQUARE_SIZE+SQUARE_SIZE/2) , int(row*SQUARE_SIZE+SQUARE_SIZE+SQUARE_SIZE/2)) , RADIUS)
    for col in range(GAME_COLUMN_NUMBER):
        for row in range(GAME_ROW_NUMBER): 
            if gameBoard[row][col] == 1:
                pygame.draw.circle(gameScreen , RED , (int(col*SQUARE_SIZE+SQUARE_SIZE/2) , windowHeight - int(row*SQUARE_SIZE+SQUARE_SIZE/2)) , RADIUS)
            elif gameBoard[row][col] == 2:
                pygame.draw.circle(gameScreen , BLUE , (int(col*SQUARE_SIZE+SQUARE_SIZE/2) , windowHeight - int(row*SQUARE_SIZE+SQUARE_SIZE/2)) , RADIUS)
    pygame.display.update()

def evaluateSubWindowScore(subWindow , piece):
    subWindowScore = 0
    inversePiece = 1
    if piece == 1:
        inversePiece = 2
        if subWindow.count(piece) == 4:
            subWindowScore+= 100
        elif subWindow.count(piece) == 3 and subWindow.count(0) == 1:
            subWindowScore+= 10    
        elif subWindow.count(piece) == 2 and subWindow.count(0) == 2:
            subWindowScore+= 5
        if subWindow.count(inversePiece) == 3 and subWindow.count(0) == 1:  
            subWindowScore-= 7
    return subWindowScore        

def scoreHeuristic(gameBoard , piece):
    gameScore = 0
    # Score Center
    centerList = [int(cell) for cell in list(gameBoard[:,GAME_COLUMN_NUMBER//2])]
    centerCount = centerList.count(piece)
    gameScore+= centerCount * 6
    
    # Score Horizontal
    for row in range(GAME_ROW_NUMBER):
        rowList = [int(cell) for cell in list(gameBoard[row,:])]
        for col in range(GAME_COLUMN_NUMBER - 3):
            subWindow = rowList[col:col+4]
            gameScore+= evaluateSubWindowScore(subWindow , piece)
            
    # Score Vertical
    for col in range(GAME_COLUMN_NUMBER):
        colList = [int(cell) for cell in list(gameBoard[:,col])]  # get all rows in this column
        for row in range(GAME_ROW_NUMBER - 3):
            subWindow = colList[row:row+4]
            gameScore+= evaluateSubWindowScore(subWindow , piece)
           
    # Score positivly sloped diagonal
    for row in range(GAME_ROW_NUMBER - 3):
        for col in range(GAME_COLUMN_NUMBER - 3):
            sunWindow = [gameBoard[row + i][col + i] for i in range(4)]
            gameScore+= evaluateSubWindowScore(subWindow , piece)
 
    # Score negatively sloped diagonael
    for row in range(GAME_ROW_NUMBER - 3):
        for col in range(GAME_COLUMN_NUMBER - 3):
            sunWindow = [gameBoard[row + 3 - i][col + i] for i in range(4)]
            gameScore+= evaluateSubWindowScore(subWindow , piece)
          
    return gameScore            


def allValidCells(gameBoard):
    validCells = []
    for col in range(GAME_COLUMN_NUMBER):
        if validCellLocation(gameBoard , col):
            validCells.append(col)
    return validCells        
        

def bestPieceMove(gameBoard , piece):
    validCells = allValidCells(gameBoard)
    bestScore = 0
    bestColumn = random.choice(validCells)
    for col in validCells:
        row = nextOpenCell(gameBoard , col)
        copiedBoard = gameBoard.copy()
        dropPieceInCell(copiedBoard , row , col , piece)
        score = scoreHeuristic(copiedBoard , piece)
        if score > bestScore:
            bestScore = score
            bestColumn = col
    return bestColumn        

def terminalNode(gameBoard):
    return winningGameMove(gameBoard , 1) or winningGameMove(gameBoard , 2) or len(allValidCells(gameBoard)) == 0
    
def minimaxAlgorithm(gameBoard , depth , maximizingplayer):
    validCells = allValidCells(gameBoard)
    terminal = terminalNode(gameBoard)
    if depth == 0 or terminal:
        if terminal:
            if winningGameMove(gameBoard , 2): # AI Wins
                return (None , 1000000)
            elif winningGameMove(gameBoard , 1): # Human Wins
                return (None , -1000000)
            else:
                return (None , 0) # No Win , gameBoard filfulled , no more valid moves
        else: # Depth = 0 , wselt le el leaf node , grbt kol el drops el mota7a
            return (None , scoreHeuristic(gameBoard , 2))
    if maximizingplayer:
        score = -math.inf
        col = random.choice(validCells)
        for cell in validCells:
            row = nextOpenCell(gameBoard , cell)
            copiedBoard = gameBoard.copy()
            dropPieceInCell(copiedBoard , row , cell , 2)
            _,maxScore = minimaxAlgorithm(copiedBoard , depth - 1 , False)
            if maxScore > score:
                score = maxScore
                col = cell
        return col , score
    else: # minimizing player
        score = math.inf
        col = random.choice(validCells)        
        for cell in validCells:
            row = nextOpenCell(gameBoard , cell)
            copiedBoard = gameBoard.copy()
            dropPieceInCell(copiedBoard , row , cell , 1)
            _,minScore = minimaxAlgorithm(copiedBoard , depth - 1 , True)
            if minScore < score:
                score = minScore
                col = cell
        return col , score
            
        
board = createGameCells()
flipOverBoard(board)
gameOver = False


pygame.init()
windowWidth = GAME_COLUMN_NUMBER * SQUARE_SIZE
windowHeight = (GAME_ROW_NUMBER + 1) * SQUARE_SIZE
windowSize = (windowWidth , windowHeight)
gameScreen = pygame.display.set_mode(windowSize)

drawGameGraphics(board)
pygame.display.update()
notificationFont = pygame.font.SysFont("monospace" , 80)
playerTurn = random.randint(PLAYER , AI)

while not gameOver:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOver = True
            pygame.display.quit()
            #sys.exit()
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(gameScreen , BLACK , (0,0, windowWidth , SQUARE_SIZE))
            xCoordinate = event.pos[0]
            if playerTurn == PLAYER:
                 pygame.draw.circle(gameScreen , RED , (xCoordinate ,int(SQUARE_SIZE/2)) , RADIUS)
                 
        pygame.display.update()    
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(gameScreen , BLACK , (0,0, windowWidth , SQUARE_SIZE))
            #print(event.pos)
            if playerTurn == PLAYER :
                xCoordinate = event.pos[0]
                #playerSelection = int(input("Player 1 Play, Select(0:6) :"))
                playerSelection = int(math.floor(xCoordinate/SQUARE_SIZE))                
                if validCellLocation(board , playerSelection):
                    row = nextOpenCell(board , playerSelection)
                    dropPieceInCell(board , row , playerSelection , 1)
                    if winningGameMove(board , 1):
                        notify = notificationFont.render("PLAYER 1 Wins!! Congrats" , 1 , RED)
                        gameScreen.blit(notify , (40,10))
                        print("PLAYER 1 Wins !! Congrats")
                        gameOver = True
                        #pygame.display.quit()
                playerTurn+= 1    
                playerTurn = playerTurn % 2
                flipOverBoard(board)  
                drawGameGraphics(board)                
    if playerTurn == AI and not gameOver:
        #playerSelection = bestPieceMove(board , 2)   
        playerSelection,_ = minimaxAlgorithm(board , 4 , True)             
        if validCellLocation(board , playerSelection):
            pygame.time.wait(500)
            row = nextOpenCell(board , playerSelection)
            dropPieceInCell(board , row , playerSelection , 2)
            if winningGameMove(board , 2):
                notify = notificationFont.render("AI beats You !" , 1 , BLUE)
                gameScreen.blit(notify , (40,10))                        
                print("AI beats You !")
                gameOver = True 
                #pygame.display.quit()
            flipOverBoard(board)  
            drawGameGraphics(board)
            playerTurn+= 1    
            playerTurn = playerTurn % 2
    if gameOver:
        pygame.time.wait(3000)
        pygame.display.quit()
            
            
            
            
    
    
