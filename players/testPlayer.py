# -*- coding: utf-8 -*-

import time
from Reversi import Board
from graphicalPlayer import *

from threading import Thread
from queue import Queue
from random import randint,choice

import copy

class OneDirection(Thread):
    """ Simple thread for on specific move """

    def __init__(self, board, initialMove, queue, color, algo, heuristic, depth, alpha=-1000, beta=1000):
        Thread.__init__(self)

        self.heuristic = heuristic
        self.algo = algo
        self.depth = depth

        self.board = board
        self.initialMove = initialMove
        self.queue = queue
        self.color = color

        self.alpha = alpha
        self.beta = beta

    def run(self):
        # Assume that game is not over when this function is called.
        self.board.push(self.initialMove)
        value = self.algo(self.board, self.alpha, self.beta, self.depth, self.heuristic, self.color)
        self.board.pop()

        self.queue.put((self.initialMove, value))

def simple_heuristic(board, color):
    (nbwhites, nbblacks) = board.get_nb_pieces()
    
    return nbwhites - nbblacks if color == board._BLACK else nbblacks - nbwhites


cst = 150
def heuristic_angle(board, color):
    boardSize = board.get_board_size()
    boardArray = board.get_board()

    (nbwhites, nbblacks) = board.get_nb_pieces()
    score = (nbblacks/(nbwhites + nbblacks)) * 100 if color == board._BLACK else (nbwhites/(nbblacks + nbwhites)) * 100


    if (boardArray[0][0] == color):
        score += cst
    elif (boardArray[0][0] != board._EMPTY):
        score -= cst
    elif (boardArray[1][0] == color or boardArray[1][1] == color or boardArray[0][1] == color):
        score -= cst

    if boardArray[2][2] == color:
        score += cst/2

    if (boardArray[0][boardSize - 1] == color):
        score += cst
    elif (boardArray[0][0] != board._EMPTY):
        score -= cst
    elif (boardArray[0][boardSize - 2] == color or boardArray[1][boardSize - 1] == color or boardArray[1][boardSize - 2] == color):
        score -= cst

    if boardArray[2][boardSize - 3] == color:
        score += cst/2

    if (boardArray[boardSize - 1][boardSize - 1] == color):
        score += cst
    elif (boardArray[0][0] != board._EMPTY):
        score -= cst
    elif (boardArray[boardSize - 2][boardSize - 2] == color or boardArray[boardSize - 2][boardSize - 1] == color or boardArray[boardSize - 1][boardSize - 2] == color):
        score -= cst

    if boardArray[boardSize - 3][boardSize - 3] == color:
        score += cst/2

    if (boardArray[boardSize - 1][0] == color):
        score += cst
    elif (boardArray[0][0] != board._EMPTY):
        score -= cst
    elif (boardArray[boardSize - 2][0] == color or boardArray[boardSize - 1][1] == color or boardArray[boardSize - 2][1] == color):
        score -= cst

    if boardArray[boardSize - 3][2] == color:
        score += cst/2

    return score

    



def negAlphaBetaDepth(board, alpha, beta, depth, heuristic, color):
    if depth == 0 or board.is_game_over():
        return heuristic(board, color)

    for move in board.legal_moves():

        board.push(move)
        value = negAlphaBetaDepth(board, -beta, -alpha, depth - 1, heuristic_angle, (color + 1) % 2)
        #print(value)
        board.pop()

        if value > alpha:
            if value > beta:
                return value
            
            alpha = value
    
    return alpha



class TestPlayer(GraphicalPlayer):

    def getPlayerName(self):
        return "Rob's test player"

    
    def nextMove(self):
        b = self._board
        if b.is_game_over():
            return (-1,-1)
        
        moves = {}
        best = -1000

        resultQueue = Queue()

        possibleMoves = b.legal_moves()
        numberPossibleMoves = len(possibleMoves)
        threadList = list()

        for i in range(numberPossibleMoves):
            threadList.append(
                OneDirection(
                    copy.deepcopy(self._board),
                    possibleMoves[i],
                    resultQueue,
                    self._mycolor,
                    negAlphaBetaDepth,
                    simple_heuristic,
                    4
                )
            )
            threadList[i].start()

        # Ne pas attendre les autres si on a un résultat satisfesant ?
        for i in range(numberPossibleMoves):
            threadList[i].join()

        for i in range(numberPossibleMoves):
            (move, value) = resultQueue.get()

            if value > best:
                best = value
            
            if str(value) in moves:
                moves[str(value)].append(move)
            else:
                moves[str(value)] = [move]
                
        m = choice(moves[str(best)])
        b.push(m)
        (c,x,y) = m

        return (x,y)
        

    def endGame(self, color):
        pass