#!/usr/bin/env python3

import pygame
from pygame.locals import *

from Reversi_perso import MyBoard

class Display():
    """ Display the game """
    _READY = False

    _WIDTH = 640
    _HEIGHT = 720

    _PIECE_SIZE_RATIO = 0.9

    # take on https://coolors.co/, from dark to light
    _COLORS_UGLY = [
        pygame.Color("#4e5340"),
        pygame.Color("#697268"),
        pygame.Color("#95a3a4"),
        pygame.Color("#b7d1da"),
        pygame.Color("#e2e8dd")
    ]

    _COLORS = [
        pygame.Color("#582c4d"),
        pygame.Color("#a26769"),
        pygame.Color("#d5b9b2"),
        pygame.Color("#ece2d0"),
        pygame.Color("#bfb5af")
    ]

    def newGame(self, board_size):
        self.initPygame()
        self.setBoard(board_size)
        self.create_window()
        self.font = pygame.font.Font('freesansbold.ttf', 24)

        pygame.display.set_caption('Reversi AI')
        self._READY = True

    def create_window(self):
        self.window = pygame.display.set_mode((self._WIDTH, self._HEIGHT))
        

    def initPygame(self):
        pygame.init()
        pygame.font.init()

    
    def setBoard(self, board_size):
        self.board = MyBoard(board_size)
        self._BOARD_OFFSET = board_size
        self._BOARD_WIDTH = self._WIDTH - 2 * self._BOARD_OFFSET
        self.caseSize = self._BOARD_WIDTH // self._BOARD_OFFSET


    def drawBackground(self):
        pygame.draw.rect(self.window, self._COLORS[3], Rect((0, 0), (self._WIDTH, self._HEIGHT)))
    

    def drawBoardGrid(self):
        boardSize = self.board.get_board_size()

        for i in range(1, boardSize):
            pygame.draw.line(
                self.window,
                self._COLORS[0],
                (self._BOARD_OFFSET, self._BOARD_OFFSET + i * self.caseSize),
                (self._BOARD_WIDTH + self._BOARD_OFFSET , self._BOARD_OFFSET + i * self.caseSize),
                1
            )

            pygame.draw.line(
                self.window,
                self._COLORS[0],
                (self._BOARD_OFFSET + i * self.caseSize, self._BOARD_OFFSET),
                (self._BOARD_OFFSET + i * self.caseSize, self._BOARD_WIDTH + self._BOARD_OFFSET),
                1
            )


    def drawPiece(self, x, y, size, type, ghost = False):
        pygame.draw.circle(
            self.window, 
            self._COLORS[0 if ghost else (3 if type == self.board._WHITE else 1)],
            (x + size//2, y + size//2),
            int(size//2*self._PIECE_SIZE_RATIO),
            1 if ghost else 0
        )

    def drawPossibleMoves(self):
        legalMoves = self.board.legal_moves()
        for move in legalMoves:
            self.drawPiece(
                move[1] * self.caseSize + self._BOARD_OFFSET, 
                move[2] * self.caseSize + self._BOARD_OFFSET,
                self.caseSize,
                0,
                True
            )
            
    def drawScores(self, curr_playername, curr_playercolor):

        playernametext = self.font.render(curr_playername + " as " + ("White" if curr_playercolor == 2 else "Black"), False, (0,0,0))
        textPos = playernametext.get_rect()
        textPos.center = ( self._WIDTH // 2, int(self._HEIGHT * 0.93))

        (nbwhites, nbblacks) = self.board.get_nb_pieces()

        score = self.font.render(str(nbblacks)+" black - "+str(nbwhites)+" white", False, (0,0,0))
        scorePos = score.get_rect()
        scorePos.center = ( self._WIDTH // 2, int(self._HEIGHT * 0.96))

        self.window.blit(playernametext,textPos)
        self.window.blit(score,scorePos)
        

    def drawBoard(self, curr_playername, curr_playercolor):
        if not self._READY:
            return

        self.drawBackground()

        boardSize = self.board.get_board_size()
        boardArray = self.board.get_board()

        pygame.draw.rect(
            self.window,
            self._COLORS[4],
            Rect(
                (self._BOARD_OFFSET, self._BOARD_OFFSET),
                (self._BOARD_WIDTH, self._BOARD_WIDTH)
            )
        )

        self.drawBoardGrid()

        for x in range(boardSize):
            for y in range(boardSize):
                if boardArray[x][y] == self.board._EMPTY:
                    continue

                self.drawPiece(
                    x * self.caseSize + self._BOARD_OFFSET, 
                    y * self.caseSize + self._BOARD_OFFSET,
                    self.caseSize,
                    boardArray[x][y]
                )
        
        self.drawPossibleMoves()

        self.drawScores(curr_playername, curr_playercolor)

        self.refreshWindow()


    def refreshWindow(self):
        pygame.display.flip()

    
    def isLegalMove(self, playerColor, x, y):
        legalMoves = self.board.legal_moves()
        
        for move in legalMoves:
            if move[0] == playerColor or playerColor == 0:
                if move[1] == x and move[2] == y:
                    return True
        
        return False


    def inputHandler(self):
        ev = pygame.event.get()
        
        for event in ev:

            # handle MOUSEBUTTONUP
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                x = (pos[0] - self._BOARD_OFFSET) // self.caseSize
                y = (pos[1] - self._BOARD_OFFSET) // self.caseSize

                if self.isLegalMove(0, x, y):
                    return (x, y)

        return ()

    def performMove(self,player,x,y):
        if(self.isLegalMove(player,x,y)):
            self.board.push((player,x,y))


