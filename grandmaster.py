#!/usr/bin/env python3
import pyautogui
import time
import random
import sys
import tensorflow as tf
import numpy as np

#TODO
#   Find where current piece is roughly
#INFO
#   10/24 board size (0 no block,1 if block, 3 if current block shadow)
#   1443,230 center of scoreboard area
#   -465,-64 board 1
#   -465,-87 board 2
#   0,0,367,884 board size
#   978,166,1345,1050 board pos
#   0,0 is top left



#pyautogui.PAUSE = .1
pyautogui.FAILSAFE = True
pausex = -1
pausey = -1

def FindBoard ():
    location = pyautogui.locateOnScreen('board2.png')

    if location == None:
        print("No board found!")
        exit(-1)

    locationx, locationy = pyautogui.center(location)

    global pausex, pausey

    pausex = locationx
    pausey = locationy -20

    pyautogui.moveTo(locationx,locationy)

    return (locationx - 465,locationy - 87)

def ClickPause():#could use keyboard 'p'since it pauses
    if (pausex == -1 or pausey == -1):
        exit()

    pyautogui.moveTo(pausex,pausey)
    pyautogui.click()
    return True

def BoardFocus():
    if (pausex == -1 or pausey == -1):
        return False
    pyautogui.moveTo(pausex - 125,pausey)
    pyautogui.click()
    return True

def GrabBoard(topx,topy,move):
    MOVETODO = False


    if(move == 0):
        #MOVETODO = DontMove()
        pass
    elif(move == 1):
        MOVETODO = MoveLeft
    elif(move == 2):
        MOVETODO = MoveRight
    elif(move == 3):
        MOVETODO = RotateLeft
    elif(move == 4):
        MOVETODO = RotateRight

    ClickPause()
    if MOVETODO != False:
        print("MOVE ",MOVETODO())
    else:
        pass
    im = pyautogui.screenshot(region=(topx,topy, 367, 884))
    ClickPause()
    w,h = 10,24
    board = [[0 for x in range(w)] for y in range(h)]

    piece1 = (0,0)
    piece2 = (0,0)
    piece3 = (0,0)
    piece4 = (0,0)

    for j in range(24):
        curry = (j * 37) + 5#18 How far from the top of the box
        for i in range(10):
            currx = (i * 37) + 18
            #pyautogui.moveTo(currx + topx,curry + topy,duration=.15)
            #time.sleep(.5)
            pix = im.getpixel((currx,curry))
            #if(pix != (153,153,153) and pix != (119,119,119) and pix != (0,0,0) and pix != (255,255,255) and pix != (111,111,111)):
            if(pix == (255,0,255) or pix == (0,255,0) or pix == (255,255,0) or pix == (255,119,0) or pix == (0,238,238) or pix == (34,34,255) or pix == (255,0,0)):
                board[j][i] =  1
            elif(pix == (119,119,119)):
                board[j][i] = 3
                piece1 = piece2
                piece2 = piece3
                piece3 = piece4
                piece4 = (i,j)

    print(piece1,piece2,piece3,piece4)
    if(piece4 == (0,0)):
        return board

    for i in range(piece1[1]-1,-1,-1):
        if(board[i][piece1[0]] == 1):
            board[i][piece1[0]]= 0
            break

    for i in range(piece2[1]-1,-1,-1):
        if(board[i][piece2[0]] == 1):
            board[i][piece2[0]] = 0
            break

    for i in range(piece3[1]-1,-1,-1):
        if(board[i][piece3[0]] == 1):
            board[i][piece3[0]] = 0
            break

    for i in range(piece4[1]-1,-1,-1):
        if(board[i][piece4[0]] == 1):
            board[i][piece4[0]] = 0
            break
        
    return board


def MoveLeft():
    #if (BoardFocus() == False):
    #    return False

    return pyautogui.typewrite(['left'])
    return True

def MoveRight():
    #if (BoardFocus() == False):
    #    return False

    return pyautogui.typewrite(['right'])
    return True

def RotateLeft():
    #if (BoardFocus() == False):
    #    return False

    return pyautogui.typewrite(['up','up','up'])
    return True

def RotateRight():
    #if (BoardFocus() == False):
    #    return False

    return pyautogui.typewrite(['up'])
    return True

def RestartGame():
    if (BoardFocus() == False):
        return False
    pyautogui.typewrite(['f5'])
    return True

def GameOver(board):
    #check if top row is filled and fourth row down under it is filled
    if(board[0][3] != 0 or board[0][4] != 0 or board[0][5] != 0 or board[0][6] != 0):
        if(board[3][3] != 0 or board[3][4] != 0 or board[3][5] != 0 or board[3][6] != 0):
            return True
    return False

def error():
    pass

def bestmovetm(board): # TO DO
    AHC = -.510066      #AggregateHeight
    CL = 0.760666       #CompleteLines
    HOL = -35663        #Holes
    BUMP = -0.184483    #Bumpiness

    #[0][0] top left
    #
    #
    #
    #
    #               [10] [24] bottom right

    #calculate agragate height
    height[10]
    j = 0
    for i in range(10):
        while True:
            if board[i][j] == 1: 
                break
            j+= 1;
        AggregateHeight += (24-j)
        height[i] = 24-j
    AggregateHeight = AggregateHeight/10

    #calculate complete lines
    for i in range (24):
        if (board[0][i] == board[1][i] and board[0][i] == board[2][i] and board[0][i] == board[3][i] and board[0][i] == board[4][i] 
        and board[0][i] == board[5][i] and board[0][i] == board[6][i] and board[0][i] == board[7][i] and board[0][i] == board[8][i] 
        and board[0][i] == board[9][i] and board[0][i] == 1):
            CompleteLines += 1
    #find holes
    for i in range(10):
        for j in range(20):
            x = 0
    #calculate bumpiness
    Bumpiness = (math.abs(height[0]-height[1])+math.abs(height[1]-height[2])+math.abs(height[2]-height[3])
    +math.abs(height[3]-height[4])+math.abs(height[4]-height[5])+math.abs(height[5]-height[6])+math.abs(height[6]-height[7])
    +math.abs(height[7]-height[8])+math.abs(height[8]-height[9]))
    return [AHC*AggregateHeight, CL*CompleteLines, HOL*Holes, BUMP*Bumpiness]
def nextmovetm(scores):
    if scores[0]< scores[1] and scores[0] < scores[2] and scores[0] < scores[3]:
        return 0
    elif scores[1]< scores[0] and scores[1] < scores[2] and scores[1] < scores[3]:
        return 1
    elif scores[2]< scores[0] and scores[2] < scores[1] and scores[2] < scores[3]:
        return 2
    elif scores[3]< scores[0] and scores[3] < scores[2] and scores[3] < scores[1]:
        return 3
    return 0

def Run(boardx,boardy,FindBoardEveryupdate = False):
    cboard = tf.placeholder(tf.float32,[None, 240],name = "input")
    move = tf.placeholder(tf.float32,[None,5],name = "output")

    oWeight = tf.Variable(tf.zeros([240,5],name = "output_weight"),dtype=tf.float32)
    oBias = tf.Variable(tf.zeros([5],name = "output_bias"),dtype=tf.float32)
    output = tf.sigmoid(tf.matmul(cboard,oWeight)+oBias)

    loss = tf.reduce_sum(tf.square(output - move))

    optimizer = tf.train.GradientDescentOptimizer(0.01)
    train = optimizer.minimize(loss)

    init = tf.global_variables_initializer()
    sess = tf.Session()
    sess.run(init) #reset values to wrong
    
    nextmove = 0#random.randint(0,4)

    while True:       
        if(FindBoardEveryupdate):
            boardx, boardy = FindBoard()
        board = GrabBoard(boardx,boardy,nextmove)
        for i in range(24):
            print(board[i])
        if(GameOver(board) == True):
            print("Game loss")
            exit(0)
            RestartGame()
            continue
        traindict = {cboard:[inputdata],move:[[.1,.2,.3,.4,.5]]}#!!!!!!!! will be bestmovetm 
        #print("Traindict: "+str(traindict))
        scores, _ = sess.run([output,train],traindict)
        #print("Scores: \n"+str(scores))

        
        nextmove = bestmovetm(scores)
        print("Next move ", nextmove)

def main():
    boardx, boardy = FindBoard()

    if (RestartGame() == False):
        return False
    ClickPause()
    pyautogui.typewrite(['enter'])  #need to hit enter
    ClickPause()
    Run(boardx,boardy)
    #call to mike 
    #make move based on that left right rotate nothing


if(__name__ == "__main__"):
    main()

