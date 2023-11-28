from Interface.GameInitializer import intializeGame
from Controllers.GameState import GameState
state:GameState = intializeGame(16,16)

printWholeTable(state)
