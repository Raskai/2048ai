from random import randint
import math
gameboard = [[0 for x in range(4)] for y in range(4)]
stop = 0
topscore = 0
topboard = [[0 for x in range(4)] for y in range(4)]
def place(board):
    if any(0 in sublist for sublist in board):
        a = randint(0,15)
        if board[int(a/4)][a-int(a/4)*4] == 0:
            if randint(0,9) == 0:
                board[int(a/4)][a-int(a/4)*4] = 2
            else:
                board[int(a/4)][a-int(a/4)*4] = 1
        else:
            place(board)
        return(board)
    else:
        return(board)

sekvence1 = [[(1/32),(1/64),(1/128),(1/256)],
            [(1/16),(1/8),(1/4),(1/2)],
            [8,4,2,1],
            [16,32,64,512]]
sekvence2 = [[(1/32),(1/16),8,16],
            [(1/64),(1/8),4,32],
            [(1/128),(1/4),2,64],
            [(1/256),(1/2),1,512]]
sekvence3 = [[0 for x in range(4)] for y in range(4)]
for i in range(4):
    for j in range(4):
        sekvence3[i][j] = sekvence1[i][(3-j)]
sekvence4 = [[0 for x in range(4)] for y in range(4)]
for i in range(4):
    for j in range(4):
        sekvence4[i][j] = sekvence1[(3-i)][j]
sekvence5 = [[0 for x in range(4)] for y in range(4)]
for i in range(4):
    for j in range(4):
        sekvence5[i][j] = sekvence2[i][(3-j)]
sekvence6 = [[0 for x in range(4)] for y in range(4)]
for i in range(4):
    for j in range(4):
        sekvence6[i][j] = sekvence2[(3-i)][j]
sekvence7 = [[0 for x in range(4)] for y in range(4)]
for i in range(4):
    for j in range(4):
        sekvence7[i][j] = sekvence1[(3-i)][(3-j)]
sekvence8 = [[0 for x in range(4)] for y in range(4)]
for i in range(4):
    for j in range(4):
        sekvence8[i][j] = sekvence2[(3-i)][(3-j)]
listRight = []
listRightScores = []
listLeft = []
listLeftScores = []

def read_lists():
    global listRight
    global listLeft
    global listRightScores
    global listLeftScores
    f = open('right.txt', 'r')
    for line in f:
        for word in line.split():
            listRight.append(int(word))
    f.close()
    f = open('left.txt', 'r')
    for line in f:
        for word in line.split():
            listLeft.append(int(word))
    f.close()
    f = open('rightScores.txt', 'r')
    for line in f:
        for word in line.split():
            listRightScores.append(int(word))
    f.close()
    f = open('leftScores.txt', 'r')
    for line in f:
        for word in line.split():
            listLeftScores.append(int(word))
    f.close()

def right(board):
    for i in range(4):
        line = 0
        for j in range(4):
            line += board[i][j] << (4*(3-j))
        newLine = listRight[line]
        for j in range (4):
            board[i][j] = (newLine & (0xF << (4*(3-j)))) >> (4*(3-j))
    return(board)

def left(board):
    for i in range(4):
        line = 0
        for j in range(4):
            line += board[i][j] << (4*(3-j))
        newLine = listLeft[line]
        for j in range (4):
            board[i][j] = (newLine & (0xF << (4*(3-j)))) >> (4*(3-j))
    return(board)

def up(board):
    transposedBoard = [[0 for x in range(4)] for y in range(4)]
    for i in range(4):
        for j in range(4):
            transposedBoard[i][j] = board[j][i]
    for i in range(4):
        line = 0
        for j in range(4):
            line += transposedBoard[i][j] << (4*(3-j))
        newLine = listLeft[line]
        for j in range (4):
            transposedBoard[i][j] = (newLine & (0xF << (4*(3-j)))) >> (4*(3-j))
    for i in range(4):
        for j in range(4):
            board[i][j] = transposedBoard[j][i]
    return(board)

def down(board):
    transposedBoard = [[0 for x in range(4)] for y in range(4)]
    for i in range(4):
        for j in range(4):
            transposedBoard[i][j] = board[j][i]
    for i in range(4):
        line = 0
        for j in range(4):
            line += transposedBoard[i][j] << (4*(3-j))
        newLine = listRight[line]
        for j in range (4):
            transposedBoard[i][j] = (newLine & (0xF << (4*(3-j)))) >> (4*(3-j))
    for i in range(4):
        for j in range(4):
            board[i][j] = transposedBoard[j][i]
    return(board)

moveOptions = {0 : up,
           1 : right,
           2 : down,
           3 : left,
           }

def hodnoceni(board):
    score1 = 0
    score2 = 0
    score3 = 0
    score4 = 0
    score5 = 0
    score6 = 0
    score7 = 0
    score8 = 0
    for i in range(4):
        for j in range(4):
            score1 += pow(2,board[i][j])*sekvence1[i][j]
            score2 += pow(2,board[i][j])*sekvence2[i][j]
            score3 += pow(2,board[i][j])*sekvence3[i][j]
            score4 += pow(2,board[i][j])*sekvence4[i][j]
            score5 += pow(2,board[i][j])*sekvence5[i][j]
            score6 += pow(2,board[i][j])*sekvence6[i][j]
            score7 += pow(2,board[i][j])*sekvence7[i][j]
            score8 += pow(2,board[i][j])*sekvence8[i][j]
    return(score1)

def minmax(board, turn, depth, alfa, beta):
    global topboard
    global topscore
    testBoard = [[0 for x in range(4)] for y in range(4)]
    for k in range(4):
                    for l in range(4):
                        testBoard[k][l] = board[k][l]
    heur = []
    moveOptions = {0 : up,
           1 : right,
           2 : down,
           3 : left,
           }
    if depth != 0:
        if turn == 0:
            heur = -float("inf")
            for i in range(4):
                for k in range(4):
                    for l in range(4):
                        testBoard[k][l] = board[k][l]
                testBoard = moveOptions[i](testBoard)
                if testBoard != board:
                    heur = max(heur,(minmax(testBoard, 1, depth-1, alfa, beta)))
                    alfa = max(alfa, heur)
                    if beta <= alfa:
                        break
            return(heur)
        else:
            heur = float("inf")
            for i in range(4):
                for j in range(4):
                    for k in range(4):
                        for l in range(4):
                            testBoard[k][l] = board[k][l]
                    if board[i][j] == 0:
                        testBoard[i][j] = 1
                        heur = min(heur, minmax(testBoard, 0, depth-1, alfa, beta))
                        beta = min(beta, heur)
                        if beta <= alfa:
                            break
                        testBoard[i][j] = 2
                        heur = min(heur, minmax(testBoard, 0, depth-1, alfa, beta))
                        beta = min(beta, heur)
                        if beta <= alfa:
                            break
            return(heur)
    else:
        for k in range(4):
            for l in range(4):
                testBoard[k][l] = board[k][l]
        heur = (hodnoceni(testBoard))
        return(heur)

def firstCall(board):
    global stop
    top = -float("inf")
    move = 0
    moznost = 0
    current = -float("inf")
    trialBoard = [[0 for x in range(4)] for y in range(4)]
    for i in range(4):
        for j in range(4):
            trialBoard[i][j] = board[i][j]
    trialBoard = up(trialBoard)
    if trialBoard != board:
        current = minmax(trialBoard, 1, 5, a, b)
    else:
        current = -float("inf")
    if current > top:
        top = current
        move = 0
    for i in range(4):
        for j in range(4):
            trialBoard[i][j] = board[i][j]
    trialBoard = right(trialBoard)
    if trialBoard != board:
        current = minmax(trialBoard, 1, 5, a, b)
    else:
        current = -float("inf")
    if current > top:
        top = current
        move = 1
    for i in range(4):
        for j in range(4):
            trialBoard[i][j] = board[i][j]
    trialBoard = down(trialBoard)
    if trialBoard != board:
        current = minmax(trialBoard, 1, 5, a, b)
    else:
        current = -float("inf")
    if current > top:
        top = current
        move = 2
    for i in range(4):
        for j in range(4):
            trialBoard[i][j] = board[i][j]
    trialBoard = left(trialBoard)
    if trialBoard != board:
        current = minmax(trialBoard, 1, 5, a, b)
    else:
        current = -float("inf")
    if current > top:
        top = current
        move = 3
    if top != -float("inf"):
        return(move)
    else:
        for n in range(4):
            for i in range(4):
                for j in range(4):
                    trialBoard[i][j] = board[i][j]
            trialBoard = moveOptions[n](trialBoard)
            if trialBoard != board:
                return(n)
        stop = 1    
        return(0)

a = -float("inf")
b = float("inf")
read_lists()
gameboard = place(gameboard)
gameboard = place(gameboard)
for number in gameboard:
    print(number)
print("")

while(stop == 0):
    topscore = 0
    topboard = [[0 for x in range(4)] for y in range(4)]
    gameboard = moveOptions[firstCall(gameboard)](gameboard)
    gameboard = place(gameboard)
    for number in gameboard:
        print(number)
    print("")

