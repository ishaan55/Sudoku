import Sudoku
import pygame
from pygame.locals import *
from math import floor
import requests
pygame.init()


response = requests.get('https://sugoku.herokuapp.com/board?difficulty=easy')  # difficulty = easy,medium,hard,random
board = response.json()["board"]

WIDTH, HEIGHT = 540, 540
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku")
FPS = 60

BLACK = (1,2,3)
BLUE = (50,50,255)
GRAY = (100,100,100)

FONT = pygame.font.Font(None,64)
NUMS_B = {1:FONT.render('1',True,BLACK),\
        2:FONT.render('2',True,BLACK),\
        3:FONT.render('3',True,BLACK),\
        4:FONT.render('4',True,BLACK),\
        5:FONT.render('5',True,BLACK),\
        6:FONT.render('6',True,BLACK),\
        7:FONT.render('7',True,BLACK),\
        8:FONT.render('8',True,BLACK),\
        9:FONT.render('9',True,BLACK)}
NUMS_BL = {1:FONT.render('1',True,BLUE),\
        2:FONT.render('2',True,BLUE),\
        3:FONT.render('3',True,BLUE),\
        4:FONT.render('4',True,BLUE),\
        5:FONT.render('5',True,BLUE),\
        6:FONT.render('6',True,BLUE),\
        7:FONT.render('7',True,BLUE),\
        8:FONT.render('8',True,BLUE),\
        9:FONT.render('9',True,BLUE)}
TEXT_COLORS = [NUMS_B, NUMS_BL]

NFONT = pygame.font.Font(None,28)
NUMS_Gray = {1:NFONT.render('1',True,GRAY),\
        2:NFONT.render('2',True,GRAY),\
        3:NFONT.render('3',True,GRAY),\
        4:NFONT.render('4',True,GRAY),\
        5:NFONT.render('5',True,GRAY),\
        6:NFONT.render('6',True,GRAY),\
        7:NFONT.render('7',True,GRAY),\
        8:NFONT.render('8',True,GRAY),\
        9:NFONT.render('9',True,GRAY)}




cell_length = WIDTH / 9

class cell:
    def __init__(self, x, y,value):
        self.x = x
        self.y = y
        self.value = value
        if self.value != 0:
            self.color = 0
            self.fixed = True
        else:
            self.color = 1
            self.fixed = False

        if not self.fixed:
            self.notes = [0] + [False]*9 
        
    def show(self, selected=False):
        color,width = (0,0,0),1
        if selected:
            color = (30,200,30)
            width = 5

        pygame.draw.rect(WIN,color,(self.x * cell_length,\
            self.y*cell_length,cell_length,cell_length),width)

        if self.value != 0:
            WIN.blit(TEXT_COLORS[self.color][self.value],(self.x*cell_length+17,\
                self.y*cell_length+10))
        
        if not self.fixed and self.value == 0:
            if self.notes[1]:
                WIN.blit(NUMS_Gray[1],(self.x*cell_length+3,\
                    self.y*cell_length))
            if self.notes[2]:
                WIN.blit(NUMS_Gray[2],(self.x*cell_length+22,\
                    self.y*cell_length))
            if self.notes[3]:
                WIN.blit(NUMS_Gray[3],(self.x*cell_length+42,\
                    self.y*cell_length))
            if self.notes[4]:
                WIN.blit(NUMS_Gray[4],(self.x*cell_length+3,\
                    self.y*cell_length+20))
            if self.notes[5]:
                WIN.blit(NUMS_Gray[5],(self.x*cell_length+22,\
                    self.y*cell_length+20))
            if self.notes[6]:
                WIN.blit(NUMS_Gray[6],(self.x*cell_length+42,\
                    self.y*cell_length+20))
            if self.notes[7]:
                WIN.blit(NUMS_Gray[7],(self.x*cell_length+3,\
                    self.y*cell_length+40))
            if self.notes[8]:
                WIN.blit(NUMS_Gray[8],(self.x*cell_length+22,\
                    self.y*cell_length+40))
            if self.notes[9]:
                WIN.blit(NUMS_Gray[9],(self.x*cell_length+42,\
                    self.y*cell_length+40))
            




def draw_window(grid,current):
    WIN.fill((255,255,255))
    
    current_cell = grid[current[0]][current[1]]
    if current_cell.value != 0:
        for i in range(9):
            for j in range(9):
                if grid[i][j].value == current_cell.value:
                    pygame.draw.rect(WIN,pygame.Color(68,218,245),\
                        (grid[i][j].x * cell_length, grid[i][j].y * cell_length, cell_length, cell_length))

    pygame.draw.line(WIN,(0,0,0),(3*cell_length,0),(3*cell_length,HEIGHT),5)
    pygame.draw.line(WIN,(0,0,0),(6*cell_length,0),(6*cell_length,HEIGHT),5)
    pygame.draw.line(WIN,(0,0,0),(0,3*cell_length),(WIDTH,3*cell_length),5)
    pygame.draw.line(WIN,(0,0,0),(0,6*cell_length),(WIDTH,6*cell_length,),5)

    for i in range(9):
        for j in range(9):
            if (i,j) == current:
                grid[i][j].show(True)
            else:
                grid[i][j].show()

    pygame.display.update()


def main():

    grid = []
    for i in range(9):
        temp = []
        for j in range(9):
            temp.append(cell(i,j,board[j][i]))
        grid.append(temp)
    current = (0,0)
    pen_state = 1         # 0-notes   1-confirm

    clock = pygame.time.Clock()
    run = True
    while run:

        mx, my = pygame.mouse.get_pos()
        current_cell = grid[current[0]][current[1]]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == MOUSEBUTTONDOWN:
                current = (floor(mx/cell_length),floor(my/cell_length))
            
            if event.type == pygame.KEYDOWN:
                if not current_cell.fixed:
                    if event.key == pygame.K_0:
                        current_cell.value = 0
                    if event.key == pygame.K_1:
                        if pen_state == 1:
                            current_cell.value = 1
                        else:
                            current_cell.notes[1] = not current_cell.notes[1]
                    if event.key == pygame.K_2:
                        if pen_state == 1:
                            current_cell.value = 2
                        else:
                            current_cell.notes[2] = not current_cell.notes[2]
                    if event.key == pygame.K_3:
                        if pen_state == 1:
                            current_cell.value = 3
                        else:
                            current_cell.notes[3] = not current_cell.notes[3]
                    if event.key == pygame.K_4:
                        if pen_state == 1:
                            current_cell.value = 4
                        else:
                            current_cell.notes[4] = not current_cell.notes[4]
                    if event.key == pygame.K_5:
                        if pen_state == 1:
                            current_cell.value = 5
                        else:
                            current_cell.notes[5] = not current_cell.notes[5]
                    if event.key == pygame.K_6:
                        if pen_state == 1:
                            current_cell.value = 6
                        else:
                            current_cell.notes[6] = not current_cell.notes[6]
                    if event.key == pygame.K_7:
                        if pen_state == 1:
                            current_cell.value = 7
                        else:
                            current_cell.notes[7] = not current_cell.notes[7]
                    if event.key == pygame.K_8:
                        if pen_state == 1:
                            current_cell.value = 8
                        else:
                            current_cell.notes[8] = not current_cell.notes[8]
                    if event.key == pygame.K_9:
                        if pen_state == 1:
                            current_cell.value = 9
                        else:
                            current_cell.notes[9] = not current_cell.notes[9]
                if event.key == pygame.K_p:
                    pen_state = not pen_state
                if event.key == pygame.K_SPACE:
                    Sudoku.solve(board)
                    for i in range(9):
                        for j in range(9):
                            if not grid[i][j].fixed:
                                grid[i][j].value = board[j][i]
                if event.key == pygame.K_RETURN:
                    x = []
                    for i in range(9):
                        temp = []
                        for j in range(9):
                            temp.append(grid[i][j].value)
                        x.append(temp)
                    error = False
                    for i in range(9):
                        if error:
                            break
                        for j in range(9):
                            if Sudoku.row(x,x[i][j],i,j):
                                if Sudoku.column(x,x[i][j],i,j):
                                    if Sudoku.box(x,x[i][j],i,j):
                                        continue
                                    else:
                                        error = True
                                        break
                                else:
                                    error = True
                                    break
                            else:
                                error = True
                                break
                    else:
                        print("You did it!!")

                    if error:
                        print('Puzzle is not solved')

 
        draw_window(grid,current)
        clock.tick(FPS)

    pygame.quit()

if __name__ == '__main__':
    main()