from numpy import copy
from Controllers.GameState import GameState
from ImportedScripts.CMDTextColorizer.ColorizeText import colored

def getNumberFromASCII(asciiChar):
    num = ord(asciiChar) - 65
    return num if num >= 0 else -1

def getValidIntInput(min:int, max:int, inputContext:str):
    inp = -1
    while(inp <= min or inp > max):   #da li je od 0 do dimenzije table
        try:
            inp = int(input(colored(f"Enter {inputContext} position: ", 'yellow')))
        except:
            print(colored("Invalid input", 'red', attrs=['bold']))
    return inp - 1

def getValidCharToIntInput(min:int, max:int, inputContext:str):  
    inp = -1
    while(inp < min or inp > max):
        try:
            asciiVal = input(colored(f"Enter {inputContext} position: ", 'yellow')).upper()
            inp = getNumberFromASCII(asciiVal)
        except:
            print(colored("Invalid input", 'red', attrs=['bold']))
    return inp


def getValidMoveInput():
    possible_moves = ["GL", "GD", "DL", "DD"]
    move = input(colored("Enter the move (GL, GD, DL, DD): ",'yellow')).upper()

    while move not in possible_moves:
        print(colored("Invalid move! Please enter a valid move.",'red'))
        move = input(colored("Enter the move (GL, GD, DL, DD): ",'yellow')).upper()

    return move


def playTurnWithInputs(state:GameState):
    rowInput = -1
    colInput = chr(0)

    print(colored(f'\nPotez {state.currentTurn}:', 'magenta', attrs=['bold']))
    
    #nova istanca stanja
    newState = GameState()
    newState = copy.deepcopy(state)

    if newState.currentTurn == "X":
        while(True):
            # Send rowDim instead of rowDim-1 because row at the table that user sees starts from 1
            rowInput = getValidIntInput(0, newState.dimension, "row (1,2,3...)")
            colInput = getValidCharToIntInput(0, newState.dimension, "column (A,B,C...)")
            stackInput=getValidIntInput(-1,8,"stack")   #0 do 7
            moveInput=getValidMoveInput()

        #    if not isMoveValid(newState.stateMatrix, newState.dimension, (rowInput, colInput)):
        #        print(colored("You can't place stack here, try again!", 'red', attrs=['bold']))
        #    else:
        #        break

        newState.stateMatrix[rowInput][colInput] = "X"
        newState.stateMatrix[rowInput+1][colInput] = "X"
        newState.lastPlayedX = [rowInput, colInput]

    elif state.currentTurn == "O":
        while(True):
            # Send rowDim instead of rowDim-1 because row at the table that user sees starts from 1
            rowInput = getValidIntInput(0, newState.dimension, "ROW (1,2,3)")
            colInput = getValidCharToIntInput(0, newState.dimension, "COLUMN (A,B,C)")

           # if not isHorizontalMoveValid(newState.stateMatrix, newState.colDim, (rowInput, colInput)):
           #     print(colored("You can't place a domino here, try again!", 'red', attrs=['bold']))
           # else:
           #     break

        newState.stateMatrix[rowInput][colInput] = "O"
        newState.stateMatrix[rowInput][colInput+1] = "O"
        newState.lastPlayedO = [rowInput, colInput]

    newState.currentTurn = "O" if newState.currentTurn == "X" else "X"
    newState.lastPlayedMove = [rowInput, colInput]

    return newState



# Only valid turns are passed as row and col arguments
def playValidTurnInstantly(state:GameState, row, col):
    newState = GameState()
    newState = copy.deepcopy(state)

    if newState.currentTurn == "X":
        newState.stateMatrix[row][col] = "X"
        newState.stateMatrix[row + 1][col] = "X"
        newState.lastPlayedX = [row, col]

    elif state.currentTurn == "O":
        newState.stateMatrix[row][col] = "O"
        newState.stateMatrix[row][col + 1] = "O"
        newState.lastPlayedO = [row, col]

    newState.currentTurn = "O" if newState.currentTurn == "X" else "X"
    newState.lastPlayedMove = [row, col]

    return newState