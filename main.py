from Interface.GameInitializer import intializeGame
from Controllers.GameState import GameState
from Interface.StatePrinter import printWholeTable
#from Controllers.TurnController import getValidPosition
state:GameState = intializeGame(16)

printWholeTable(state)
