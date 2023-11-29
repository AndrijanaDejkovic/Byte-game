from Interface.GameInitializer import intializeGame
from Controllers.GameState import GameState
from Interface.StatePrinter import printWholeTable
state:GameState = intializeGame(16)

printWholeTable(state)
