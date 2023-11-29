from Interface.GameInitializer import intializeGame, gameIsOver
from Controllers.GameState import GameState
from Interface.StatePrinter import printWholeTable
#from Controllers.TurnController import getValidIntInput
state:GameState = intializeGame(16)

gameIsOver()
printWholeTable(state)

