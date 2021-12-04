#!/usr/bin/python3
board = [
        [0,0,0,0,6,0,5,1,0],
        [0,7,0,2,5,8,0,0,0],
        [0,0,4,0,0,3,0,2,0],
        [6,0,0,8,3,0,0,5,0],
        [0,0,8,0,0,0,6,0,0],
        [0,3,0,0,4,7,0,0,2],
        [0,5,0,4,0,0,3,0,0],
        [0,0,0,7,8,6,0,9,0],
        [0,9,6,0,1,0,0,0,0]
]

def printBoard(board):
    for i in range(len(board)):
        if i % 3 == 0 and i != 0:
            print("-- -- -- -- -- -- -- --")

        for j in range(len(board[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")

            if j == 8:
                print(board[i][j])

            else:
                print(str(board[i][j]) + " ", end="")


def findEmpty():
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i, j) # row, col
    return None


def checkRow(row, num):
    for j in range(len(board[row])):
        if num == board[row][j]:
            return False
    return True

def checkCol(col, num):
    for j in range(len(board)):
        if num == board[j][col]:
            return False
    return True

def change(num):
    num += 1
    if num % 3 == 0:
        return num
    num = num + (3 - (num % 3))
    return num

def checkBox(row, col, num):
    rowTill = change(row)
    colTill = change(col)
    for i in range(rowTill - 3, rowTill):
        for j in range(colTill - 3, colTill):
            if num == board[i][j]:
                return False
    return True

def fillBoard():
    find = findEmpty()
    if not find:
        return True
    else:
        row, col = find
    for i in range(1, 10):
        if (checkRow(row, i) and checkCol(col, i) and checkBox(row, col, i)):
            board[row][col] = i
            if fillBoard():
                return True
            board[row][col] = 0
    return False


printBoard(board)
fillBoard()
print("------Solution------")
printBoard(board)
