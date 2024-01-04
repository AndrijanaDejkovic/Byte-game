import copy
from Controllers.GameState import GameState
import random
import time
from Controllers.MinMaxAlg.Heuristics import *
from Controllers.TurnController import *


def minMax(state:GameState, maxDepth:int = 1, alpha:tuple = -50000000, beta:tuple = 50000000):
    #print("uso sam u min maks")
    # random.seed(int(time.time())*1000)
    copyState:GameState = copy.deepcopy(state)
    copyState.minMaxGeneratedTurns = []

    nextState:GameState = None
    depth = 0

    if copyState.currentTurn == "X":
        nextState = maxState(copyState, depth, maxDepth, alpha, beta)[0]
    else:
        nextState = minState(copyState, depth, maxDepth, alpha, beta)[0]  

    return nextState 


def maxState(state, depth, maxDepth, alpha, beta):
    newStates = returnAllPossibleNextStates(state)

    if depth == maxDepth or len(newStates) == 0:
        return (None, evaluateState(state, "X", "O"))
        # return evaluateState(state, "X", "O")
    
    # maxValue = -1000000000
    maxState = None
    for newState in newStates:
        newStateMinValue = minState(newState, depth+1, maxDepth, alpha, beta)
        if newStateMinValue[1] > alpha:
            alpha = newStateMinValue[1]
            if depth == 0:
                maxState = newState
        # alpha = max(alpha, newStateMinValue)
        if alpha >= beta:
            break


        # alpha = max(alpha, minState(newState, depth+1, maxDepth, alpha, beta))
        # if alpha[1] >= beta[1]:
        #     break
        # minValue = minState(newState, depth + 1, maxDepth, alpha, beta)
        # if minValue[1] > maxValue:
        #     maxValue = minValue[1]
        #     if depth == 0:
        #         maxState = newState

    # return alpha
    return (maxState, alpha)

def minState(state, depth, maxDepth, alpha, beta):
    newStates = returnAllPossibleNextStates(state)

    if depth == maxDepth or len(newStates) == 0:
        return (None, evaluateState(state, "O", "X"))
    
    # minValue = 1000000000
    minState = None
    for newState in newStates:
        # maxValue = maxState(newState, depth + 1, maxDepth, alpha, beta)
        # if maxValue[1] < minValue:
        #     minValue = maxValue[1]
        #     if depth == 0:
        #         minState = newState
        newStateMaxValue = maxState(newState, depth+1, maxDepth, alpha, beta)
        if newStateMaxValue[1] < beta:
            beta = newStateMaxValue[1]
            if depth == 0:
                minState = newState
            if alpha >= beta:
                break
    # return (minState, minValue)
    return (minState, beta)
