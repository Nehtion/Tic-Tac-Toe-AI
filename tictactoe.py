import copy
import random
import sys
import pygame
import numpy as np
import math

from constants import *

# PYGAME

#Spiel Setup
pygame.init()
screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
pygame.display.set_caption('Tic Tac Toes Stockfish Evaluation')
screen.fill(COLOR_BG)

class Board:
    
    def __init__(self) :
        self.squares = np.zeros((ROWS, COLS))
        self.empty_sqrs = self.squares # [List of empty squares]
        self.marked_sqrs = 0
        
    def final_state(self,  show=False):
        '''
            @return 0 if there is no win (Doesnt mean Draw)
            @return 1 if player 1 wins (Cross)
            @return 2 if player 2 wins (Circle)
        '''
        
        #vertical wins
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                if show:
                    color = COLOR_CIRCLE if self.squares[0][col] == 2 else COLOR_CROSS
                    clock = pygame.time.Clock()
                    fps = 1000
                    for i in range(1,281):
                        iPos = (col * SQSIZE+SQSIZE//2,300)
                        pygame.draw.line(screen, color, iPos, (col * SQSIZE+SQSIZE//2, 300-i), LINE_WINNING)
                        pygame.draw.line(screen, color, iPos, (col * SQSIZE+SQSIZE//2, 300+i), LINE_WINNING)
                        pygame.display.flip()
                        clock.tick(fps)
                return self.squares[0][col]
            
        #horizontal wins 
        for row in range(ROWS):
           if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    color = COLOR_CIRCLE if self.squares[row][0] == 2 else COLOR_CROSS
                    clock = pygame.time.Clock()
                    fps = 1000
                    for i in range(1,281):
                        iPos = (300, row * SQSIZE + SQSIZE // 2)
                        pygame.draw.line(screen, color, iPos, (300-i, row * SQSIZE + SQSIZE // 2), LINE_WINNING)
                        pygame.draw.line(screen, color, iPos, (300+i, row * SQSIZE + SQSIZE // 2), LINE_WINNING)
                        pygame.display.flip()
                        clock.tick(fps)
                return self.squares[row][0]
            
            
        #diagonal Wins (desc)
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show:
                color = COLOR_CIRCLE if self.squares[1][1] == 2 else COLOR_CROSS
                clock = pygame.time.Clock()
                fps = 1410
                for i in range(1,281):
                    iPos = (300,300)
                    pygame.draw.line(screen, color, iPos, (300-i,300-i), CROSS_WIDTH)
                    pygame.draw.line(screen, color, iPos, (300+i,300+i), CROSS_WIDTH)
                    pygame.draw.line(screen, COLOR_BG, (10,30), (30,10), CROSS_WIDTH)
                    pygame.draw.line(screen, COLOR_BG, (570,590), (590,570), CROSS_WIDTH)
                    
                    pygame.display.flip()
                    clock.tick(fps)
            return self.squares[1][1]
        
        #diagonal Wins (asc)
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            if show:
                color = COLOR_CIRCLE if self.squares[1][1] == 2 else COLOR_CROSS
                clock = pygame.time.Clock()
                fps = 1410
                for i in range(1,281):
                    iPos = (300,300)
                    pygame.draw.line(screen, color, iPos, (300+i,300-i), CROSS_WIDTH)
                    pygame.draw.line(screen, color, iPos, (300-i,300+i), CROSS_WIDTH)
                    pygame.draw.line(screen, COLOR_BG, (570,10), (590,30), CROSS_WIDTH)
                    pygame.draw.line(screen, COLOR_BG, (10,570), (30,590), CROSS_WIDTH)
                
                    pygame.display.flip()
                    clock.tick(fps)
            return self.squares[1][1]
        
        return 0 # No winning winner that has won yet
    
    def mark_sqr(self, row, col, player):
        self.squares[row][col] = player
        self.marked_sqrs += 1
        
    def empty_sqr(self, row,col):
        return self.squares[row][col] == 0
    
    def get_empty_sqrs(self):
        empty_sqrs = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.empty_sqr(row, col):
                    empty_sqrs.append((row,col))
        return empty_sqrs
    
    def isfull(self):
        return self.marked_sqrs == 9
    
    def isempty(self):
        return self.marked_sqrs == 0

class AI:
    
    def __init__(self, level=1, player=2):
        self.level = level
        self.player = player
        
    def rnd(self, board):
        empty_sqrs = board.get_empty_sqrs()
        idx = random.randrange(0, len(empty_sqrs))
        
        return empty_sqrs[idx] # row, col
    
    def minimax(self, board, maximizing): #maximizing = who is the ai playing? = circle (response) minimizing = cross (beginning)
        
        # terminal case
        case = board.final_state()

        # player 1 wins
        if case == 1:
            return 1, None # eval, move

        # player 2 wins
        if case == 2:
            return -1, None

        # draw
        elif board.isfull():
            return 0, None
        
        if maximizing:
            max_eval = -100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, 1)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)

            return max_eval, best_move

        elif not maximizing:
            min_eval = 100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, self.player)
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)

            return min_eval, best_move
            
    def eval(self, main_board):
        if self.level == 0:
            # random choice
            eval = 'random'
            move = self.rnd(main_board)
        else:
            # minimax algo choice
            eval, move = self.minimax(main_board, False)

        print(f'AI has chosen to mark the square in pos {move} with an eval of: {eval}')

        return move # row, col

class Game:
    
    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 1 #1 = Kreuz 2 = Kreis
        self.gamemode = 'ai' # pvp or ai
        self.running = True
        self.show_lines()
        
    def make_move(self, row, col):
        self.board.mark_sqr(row, col, self.player)
        self.draw_fig(row,col)
        self.next_turn()
        
    def show_lines(self):
        # BG Coloring
        screen.fill( COLOR_BG )
        clock = pygame.time.Clock()
        fps = 1000
        for i in range(1,301):
            pygame.draw.line(screen, COLOR_LINE, (200,300),(200, 300 - i), LINE_WIDTH)
            pygame.draw.line(screen, COLOR_LINE, (200,300),(200, 300 + i), LINE_WIDTH)
            
            pygame.draw.line(screen, COLOR_LINE, (400,300),(400, 300 - i),LINE_WIDTH)
            pygame.draw.line(screen, COLOR_LINE, (400,300),(400, 300 + i),LINE_WIDTH)
            
            pygame.draw.line(screen, COLOR_LINE, (300,200),(300 - i, 200),LINE_WIDTH)
            pygame.draw.line(screen, COLOR_LINE, (300,200),(300 + i, 200),LINE_WIDTH)
            
            pygame.draw.line(screen, COLOR_LINE, (300,400),(300 - i, 400),LINE_WIDTH)
            pygame.draw.line(screen, COLOR_LINE, (300,400),(300 + i, 400),LINE_WIDTH)
            pygame.display.flip()
            clock.tick(fps)
    
    def draw_fig(self, row, col):
        if self.player == 1:
            #Kreuz zeichnen
            
            #Descending
            start_desc = (col * SQSIZE + OFFSET, row * SQSIZE+ OFFSET)
            start_fix_desc_start = (col * SQSIZE + OFFSET - OFFSET * 0.55, row * SQSIZE+ OFFSET + OFFSET * 0.55)
            end_fix_desc_start = (col * SQSIZE + OFFSET + OFFSET * 0.55 , row * SQSIZE+ OFFSET - OFFSET * 0.55)
            
            start_fix_desc_end = (col * SQSIZE + SQSIZE - OFFSET / 2, row * SQSIZE + SQSIZE - OFFSET * 1.5)
            end_fix_desc_end = (col * SQSIZE + SQSIZE - OFFSET * 1.5, row * SQSIZE + SQSIZE - OFFSET / 2)
            
            #Ascending
            start_asc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + OFFSET)
            start_fix_asc_start = (col * SQSIZE + OFFSET * 0.55, row * SQSIZE+ SQSIZE - OFFSET * 1.5)
            end_fix_asc_start = (col * SQSIZE + OFFSET * 1.5, row * SQSIZE+ SQSIZE - OFFSET * 0.55)
            
            start_fix_asc_end = (col * SQSIZE + SQSIZE - OFFSET * 1.5, row * SQSIZE + OFFSET / 2)
            end_fix_asc_end = (col * SQSIZE + SQSIZE - OFFSET / 2, row * SQSIZE + OFFSET * 1.5)
            
            clock = pygame.time.Clock()
            fps = 1000
            for i in range(1,101):
                #Descending
                pygame.draw.line(screen, COLOR_CROSS, start_desc, (col * SQSIZE + OFFSET + i , row * SQSIZE +  OFFSET + i), CROSS_WIDTH)
                pygame.draw.line(screen, COLOR_BG, start_fix_desc_start, end_fix_desc_start, CROSS_WIDTH)
                pygame.draw.line(screen, COLOR_BG, start_fix_desc_end, end_fix_desc_end, CROSS_WIDTH)
                #Ascending
                pygame.draw.line(screen, COLOR_CROSS, start_asc, (col * SQSIZE + SQSIZE - OFFSET - i, row * SQSIZE+ OFFSET + i), CROSS_WIDTH)
                pygame.draw.line(screen, COLOR_BG,start_fix_asc_start,end_fix_asc_start ,CROSS_WIDTH)
                pygame.draw.line(screen, COLOR_BG,start_fix_asc_end,end_fix_asc_end,CROSS_WIDTH)
                pygame.display.flip()
                clock.tick(fps)
                
        elif(self.player == 2):
            
            # Circle Drawing Progressivly
            clock = pygame.time.Clock()
            fps = 2000
            duration = 0.5
            num_frames = fps * duration
            angle_increment = 360 / num_frames
            running_circle = True
            angle = 90
            frames_elapsed = 0
            while running_circle and frames_elapsed <= num_frames:
                    center = (col * SQSIZE + SQSIZE / 2, row * SQSIZE + SQSIZE/2)
                    x = col * SQSIZE + SQSIZE / 2
                    y = row * SQSIZE + SQSIZE/2
                    pygame.draw.arc(screen,COLOR_CIRCLE, (x - RADIUS, y - RADIUS, RADIUS * 2, RADIUS * 2), math.radians(90), math.radians(angle), CIRCLE_WIDTH)
                    angle += angle_increment
                    frames_elapsed += 1
                    pygame.display.flip()
                    clock.tick(fps)
        
    def next_turn(self):
        self.player = self.player % 2 + 1
        
    def change_gamemode(self):
        self.gamemode = 'ai' if self.gamemode == 'pvp' else 'pvp'
        
    def isover(self):
        return self.board.final_state(show=True) != 0 or self.board.isfull()
        
    def reset(self):
        self.__init__()
        
        
def main():
    
    game = Game()
    board = game.board
    ai = game.ai
    
    # Main Loop
    while True:

        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                running = False
                    
            if event.type == pygame.KEYDOWN:
                
                #g = Change Gamemode
                if event.key == pygame.K_g:
                    game.change_gamemode()
                    
                #r = restart
                if event.key == pygame.K_r:
                    game.reset()
                    board = game.board
                    ai = game.ai
                    
                    
                #0-Random AI
                if event.key == pygame.K_0:
                    ai.level = 0
                    
                #1-Best AI
                if event.key == pygame.K_1:
                    ai.level = 1
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // SQSIZE
                col = pos[0] // SQSIZE

                if board.empty_sqr(row, col) and game.running:
                    game.make_move(row, col)
                    
                    if game.isover():
                        game.running = False
                    
        if game.gamemode == 'ai' and game.player == ai.player and game.running:
            #Update screen for sencefullness
            pygame.display.update()
            
            #ai method
            row, col = ai.eval(board)
            game.make_move(row,col)
            
            if game.isover():
                        game.running = False
            
        pygame.display.update()

main()