import copy
from Controllers.GameState import GameState
import random
import time
from Heuristics import *
from TurnController import *


def minimax(state:GameState, depth:int = 0, alpha:tuple = None, beta:tuple = None):
    random.seed(int(time.time())*1000)
    copyState:GameState = copy.deepcopy(state)
    copyState.minMaxGeneratedTurns = []

    if alpha == None: alpha = (copyState, -50000)
    if  beta == None:  beta = (copyState,  50000)

    nextState:GameState = None

    if copyState.currentTurn == "X":
        nextState = maxState(copyState, depth, alpha, beta)
    else:
        nextState = minState(copyState, depth, alpha, beta)  

    return nextState 


def maxState(state, depth, alpha, beta):
    newStates = returnAllPossibleNextStates(state)

    if depth == 0 or len(newStates) == 0:
        return (state, evaluateState(state, "X", "O"))
    else:
        for newState in newStates:
            alpha = max(alpha, minState(newState, depth-1, alpha, beta), key = lambda x:x[1])
            if alpha[1] >= beta[1]:
                return beta
    return alpha

def minState(state, depth, alpha, beta):
    newStates = returnAllPossibleNextStates(state)

    if depth == 0 or len(newStates) == 0:
        return (state, evaluateState(state, "O", "X"))
    else:
        for newState in newStates:
            beta = min(beta, maxState(newState, depth-1, alpha, beta), key = lambda x:x[1])
            if beta[1] <= alpha[1]:
                return alpha
    return beta