from math import floor
sudoku = [
        [0,0,0,0,0,0,9,0,0],
        [5,0,0,0,0,0,0,1,8],
        [0,2,8,0,0,7,0,4,0],
        [0,0,0,1,0,5,0,0,9],
        [0,9,0,0,3,0,0,6,0],
        [4,0,0,9,0,2,0,0,0],
        [0,3,0,5,0,0,6,2,0],
        [2,8,0,0,0,0,0,0,1],
        [0,0,6,0,0,0,0,0,0]
        ]
def row(sudoku,guess,x,y):
    for i in range(len(sudoku)):
        if sudoku[i][y] == guess and i != x:
            break                
    else:
        return True
    return False

def column(sudoku,guess,x,y):
    for i in range(len(sudoku[0])):
        if sudoku[x][i] == guess and i != y:
            break   
    else:
        return True
    return False

def box(sudoku,guess,x,y):
    boxes = {(0,0):((0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)),
            (0,1):((0,3),(0,4),(0,5),(1,3),(1,4),(1,5),(2,3),(2,4),(2,5)),
            (0,2):((0,6),(0,7),(0,8),(1,6),(1,7),(1,8),(2,6),(2,7),(2,8)),
            (1,0):((3,0),(3,1),(3,2),(4,0),(4,1),(4,2),(5,0),(5,1),(5,2)),
            (1,1):((3,3),(3,4),(3,5),(4,3),(4,4),(4,5),(5,3),(5,4),(5,5)),
            (1,2):((3,6),(3,7),(3,8),(4,6),(4,7),(4,8),(5,6),(5,7),(5,8)),
            (2,0):((6,0),(6,1),(6,2),(7,0),(7,1),(7,2),(7,0),(7,1),(7,2)),
            (2,1):((6,3),(6,4),(6,5),(7,3),(7,4),(7,5),(8,3),(8,4),(8,5)),
            (2,2):((6,6),(6,7),(6,8),(7,6),(7,7),(7,6),(8,6),(8,7),(8,8)),
            }
    for i in boxes[(floor(x/3),floor(y/3))]:
        if sudoku[i[0]][i[1]] == guess and (i[0],i[1]) != (x,y):
            break
    else:
        return True
    return False
def solve(sudoku):
    def find(sudoku,x,y,current=0):
        guess = 0
        while current <= 8:
            current += 1
            if row(sudoku,current,x,y):
                if column(sudoku,current,x,y):
                    if box(sudoku,current,x,y):
                        guess = current
                        break
        return guess


    current_x,current_y = 0,0
    stack = []
    spots = []
    while current_x <= 8:
        done = False
        x = sudoku[current_x][current_y]
        if x == 0 or ((current_x,current_y) in spots):
            a = find(sudoku,current_x,current_y,x)
            if a == 0:
                sudoku[current_x][current_y] = 0
                current_x,current_y = stack[-1]
                stack.pop()
                done = True
            else:
                sudoku[current_x][current_y] = a
                stack.append((current_x,current_y))
                spots.append((current_x,current_y))
        if not done:      
            current_y += 1
            if current_y > len(sudoku[0])-1:
                current_y = 0
                current_x += 1

    return sudoku

if __name__ == '__main__':
    board = solve(sudoku)
    for i in range(len(board)):
        if i % 3 == 0 and i != 0:
            print('-'*22)
        for j in range(len(board[i])):
            if j % 3 == 0 and j != 0:
                print('|',end=' ')
            print(board[i][j],end=" ")
        print()