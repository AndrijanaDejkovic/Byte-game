import copy
from Controllers.GameState import GameState
from Controllers.TurnController import returnAllValidMovesForSing
def evaluateState(state:GameState, whoPlayed=None, whoIsOpponent = None):
    score = 0
    multiplier = -1 if state.currentTurn == "X" else 1
    opponentSign = "O" if state.currentTurn == "X" else "X"
    #treba da dodam upit da li je u prethodnom stanju neko imao poen 0, a sad ima jedan, takvo stanje ima vecu vrednost jer je popunio i uzeo stek
    score = len(returnAllValidMovesForSing(state), state.currentTurn) - len(returnAllValidMovesForSing(state, opponentSign))
    return score * multiplier