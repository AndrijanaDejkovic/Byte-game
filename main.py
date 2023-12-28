from Interface.GameInitializer import intializeGame, gameIsOver
from Controllers.GameState import GameState
from Interface.StatePrinter import printWholeTable

from Controllers.TurnController import playTurnWithInputs, allValidStacks
from Controllers.MinMaxAlg.MinMax import *
from ImportedScripts.TextColorizer.ColorizeText import *

state:GameState = intializeGame(16)

gameIsOver()
printWholeTable(state)
isGameFinished = False



while not isGameFinished:
    isGameFinished = gameIsOver()
    turn = state.currentTurn
    if state.currentTurn == "X":
        if state.playerSign == "X":
            state = playTurnWithInputs(state)
        else:
            state = playTurnWithInputs(state)
            #state = minMax(state, 3)
            #state = playValidTurnInstantly(state, minMaxState[0].minMaxGeneratedTurns[0][0], minMaxState[0].minMaxGeneratedTurns[0][1])
    else:
        if state.playerSign == "O":
            state = playTurnWithInputs(state)
        else:
            state = playTurnWithInputs(state)
            #state = minMax(state, 3)
            #state = playValidTurnInstantly(state, minMaxState[0].minMaxGeneratedTurns[0][0], minMaxState[0].minMaxGeneratedTurns[0][1])
    printWholeTable(state)
    state.currentTurn = "X" if turn == "O" else "O"


#while not isGameFinished:
#    isGameFinished = gameIsOver()
#    turn = state.currentTurn
#    if state.currentTurn == "X":
#        if state.playerSign == "X":
#            state = playTurnWithInputs(state)
#        else:
#            state = minMax(state, 3)
#            #state = playValidTurnInstantly(state, minMaxState[0].minMaxGeneratedTurns[0][0], minMaxState[0].minMaxGeneratedTurns[0][1])
#    else:
#        if state.playerSign == "O":
#            state = playTurnWithInputs(state)
#        else:
#            state = minMax(state, 3)
#            #state = playValidTurnInstantly(state, minMaxState[0].minMaxGeneratedTurns[0][0], minMaxState[0].minMaxGeneratedTurns[0][1])
#    printWholeTable(state)
#    state.currentTurn = "X" if turn == "O" else "O"
#
#
#print(colored(f"GAME OVER! The winner is {gameIsOver()}", "green" if gameIsOver()=="X" else "red", attrs=["bold"]))