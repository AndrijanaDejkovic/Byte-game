from Interface.GameInitializer import intializeGame, gameIsOver
from Controllers.GameState import GameState
from Interface.StatePrinter import printWholeTable

from Controllers.TurnController import playTurnWithInputs, closestNonEmptyStack

state:GameState = intializeGame(16)

gameIsOver()
printWholeTable(state)
playTurnWithInputs(state)
#print(closestNonEmptyStack(1,1,state.dimension, state.stekovi, state))