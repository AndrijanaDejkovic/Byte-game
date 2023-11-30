from Interface.GameInitializer import intializeGame, gameIsOver
from Controllers.GameState import GameState
from Interface.StatePrinter import printWholeTable
<<<<<<< HEAD
#from Controllers.TurnController import getValidIntInput
=======
from Controllers.TurnController import playTurnWithInputs
>>>>>>> 95cf8a27a4e2720c026a87e6756747d341a58f77
state:GameState = intializeGame(16)

gameIsOver()
printWholeTable(state)
#playTurnWithInputs(state)
