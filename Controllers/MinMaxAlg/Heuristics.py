import copy
from Controllers.GameState import GameState
from Controllers.TurnController import returnAllValidMovesForSign
def evaluateState(state:GameState, whoPlayed=None, whoIsOpponent = None):
    score = 0
    multiplier = -1 if state.currentTurn == "X" else 1
    opponentSign = "O" if state.currentTurn == "X" else "X"
    score+=state.playerScore * 1000 - state.cpuScore * 1000
    score+= len(returnAllValidMovesForSign(state, state.currentTurn)) - len(returnAllValidMovesForSign(state, opponentSign))
    
    return score * multiplier