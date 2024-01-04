from Interface.GameInitializer import intializeGame, gameIsOver
from Controllers.GameState import GameState
from Interface.StatePrinter import printWholeTable

from Controllers.TurnController import playTurnWithInputs
from Controllers.MinMaxAlg.MinMax import *
from ImportedScripts.TextColorizer.ColorizeText import *

state:GameState = intializeGame(16)

#gameIsOver(state)
printWholeTable(state)
isGameFinished = False


#print(state.playerSign, "player sign\n" )
#print(state.cpuSign, "cpu sign\n")
while not isGameFinished:

    
    turn = state.currentTurn
    print(colored(f'\nPotez {state.currentTurn}:', 'magenta', attrs=['bold']))

    if state.currentTurn == state.playerSign:
        #print("\ncurrent turn: ", state.currentTurn)
        stateNew = playTurnWithInputs(state)
        
    else:
            #state = playTurnWithInputs(state)
        #print("\ncurrent turn: ", state.currentTurn)
        stateNew = minMax(state, 1)
        
            #state = playValidTurnInstantly(state, minMaxState[0].minMaxGeneratedTurns[0][0], minMaxState[0].minMaxGeneratedTurns[0][1])
    if(stateNew==None):
         print(colored(f'\nPotez {turn}: Nema valjanih poteza, prepušta se potez protivniku', 'magenta', attrs=['bold']))
    else:
         state=stateNew
         printWholeTable(state)
    if turn == "O" :
        state.currentTurn = "X" 
    else: 
        state.currentTurn="O"
    isGameFinished = gameIsOver(state)


#while not isGameFinished:
#    isGameFinished = gameIsOver(state)
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
#print(colored(f"GAME OVER! The winner is {gameIsOver(state)}", "green" if gameIsOver(state)=="X" else "red", attrs=["bold"]))
    #printuje su unutar game is over