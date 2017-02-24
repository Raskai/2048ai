from random import randint
import math

gameboard = [[0 for x in range(4)] for y in range(4)]

stop = 0

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
    score = 0
    for i in range(4):
        line = 0
        for j in range(4):
            line += board[i][j] << (4*(3-j))
        score += listRightScores[line]
        newLine = listRight[line]
        for j in range (4):
            board[i][j] = (newLine & (0xF << (4*(3-j)))) >> (4*(3-j))
    return(board, score)

def left(board):
    score = 0
    for i in range(4):
        line = 0
        for j in range(4):
            line += board[i][j] << (4*(3-j))
        score += listLeftScores[line]
        newLine = listLeft[line]
        for j in range (4):
            board[i][j] = (newLine & (0xF << (4*(3-j)))) >> (4*(3-j))
    return(board, score)

def up(board):
    score = 0
    transposedBoard = [[0 for x in range(4)] for y in range(4)]
    for i in range(4):
        for j in range(4):
            transposedBoard[i][j] = board[j][i]
    for i in range(4):
        line = 0
        for j in range(4):
            line += transposedBoard[i][j] << (4*(3-j))
        score += listLeftScores[line]
        newLine = listLeft[line]
        for j in range (4):
            transposedBoard[i][j] = (newLine & (0xF << (4*(3-j)))) >> (4*(3-j))
    for i in range(4):
        for j in range(4):
            board[i][j] = transposedBoard[j][i]
    return(board, score)

def down(board):
    score = 0
    transposedBoard = [[0 for x in range(4)] for y in range(4)]
    for i in range(4):
        for j in range(4):
            transposedBoard[i][j] = board[j][i]
    for i in range(4):
        line = 0
        for j in range(4):
            line += transposedBoard[i][j] << (4*(3-j))
        score += listRightScores[line]
        newLine = listRight[line]
        for j in range (4):
            transposedBoard[i][j] = (newLine & (0xF << (4*(3-j)))) >> (4*(3-j))
    for i in range(4):
        for j in range(4):
            board[i][j] = transposedBoard[j][i]
    return(board, score)

moveOptions = {0 : up,
           1 : right,
           2 : down,
           3 : left,
           }

def montecarlo(board, iter):
    trialBoard = [[0 for x in range(4)] for y in range(4)]
    iterBoard = [[0 for x in range(4)] for y in range(4)]
    stop = 0
    total = []
    for f in range(4):
        score = 0
        for j in range(4):
            for k in range(4):
                iterBoard[j][k] = board[j][k]
        result = moveOptions[f](iterBoard)
        iterBoard = place(iterBoard)
        score += result[1]
        for j in range(4):
            for k in range(4):
                iterBoard[j][k] = result[0][j][k]
        if iterBoard != board:
            for i in range(iter):
                b = 0
                stop = 0
                for j in range(4):
                    for k in range(4):
                        trialBoard[j][k] = iterBoard[j][k]
                while True:
                    backup = [[0 for x in range(4)] for y in range(4)]
                    for j in range(4):
                        for k in range(4):
                            backup[j][k] = trialBoard[j][k]
                    result = moveOptions[randint(0,3)](trialBoard)
                    for j in range(4):
                        for k in range(4):
                            trialBoard[j][k] = result[0][j][k]
                    score += result[1]
                    trialBoard = place(trialBoard)
                    if backup != trialBoard:
                        stop = 0
                    else:
                        stop += 1
                    if stop > 19:
                        break
                    b += 1
            total.append(score)
        else:
            total.append(-1)
    return(total.index(max(total)), max(total))

read_lists()
gameboard = place(gameboard)
gameboard = place(gameboard)
for number in gameboard:
    print(number)
print("")

while(stop == 0):
        pohyb = montecarlo(gameboard, 200)
        gameboard = moveOptions[pohyb[0]](gameboard)[0]
        gameboard = place(gameboard)
        for number in gameboard:
            print(number)
        print("")
        if pohyb[1] == -1:
            stop = 1

