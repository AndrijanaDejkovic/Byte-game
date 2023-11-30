from numpy import copy
from Controllers.GameState import GameState
from ImportedScripts.CMDTextColorizer.ColorizeText import colored
from Interface.Stack import is_empty
state:GameState = GameState()
#??
def getNumberFromASCII(asciiChar):
    num = ord(asciiChar) - 65
    return num if num >= 0 else -1

#??
def getValidIntInput(min:int, max:int, inputContext:str):
    inp = -1
    while(inp <= min or inp > max):   #da li je od 0 do dimenzije table
        try:
            inp = int(input(colored(f"Enter {inputContext} position: ", 'yellow')))
        except:
            print(colored("Invalid input", 'red', attrs=['bold']))
    return inp - 1

#??
def getValidCharToIntInput(min:int, max:int, inputContext:str):  
    inp = -1
    while(inp < min or inp > max):
        try:
            asciiVal = input(colored(f"Enter {inputContext} position: ", 'yellow')).upper()
            inp = getNumberFromASCII(asciiVal)
        except:
            print(colored("Invalid input", 'red', attrs=['bold']))
    return inp

#smer provera sintaksno
def getValidMoveInput():
    possible_moves = ["GL", "GD", "DL", "DD"]
    move = input(colored("Enter the move (GL, GD, DL, DD): ",'yellow')).upper()

    while move not in possible_moves:
        print(colored("Invalid move! Please enter a valid move.",'red'))
        move = input(colored("Enter the move (GL, GD, DL, DD): ",'yellow')).upper()

    return move
#proverava da li je moguc pomeraj (ivica)

#provera indeksa reda (slovo)
def getValidFieldRow():
   
    move = input(colored(f"Enter the row index (1-{state.dimension}): ",'yellow')).upper()

    while 1<move<state.dimension:
        print(colored("Invalid index! Please enter a valid index.",'red'))
        move = input(colored(f"Enter the index (1-{state.dimension}): ",'yellow')).upper()

    return move

#provera indeksa kolone (broj)
def getValidFieldColumn():
    start_char = ord('A')  # ASCII code for 'A'
    possible_letters = [chr(start_char + i) for i in range(state.dimension)]
    move = input(colored(f"Enter the column index ({possible_letters[0]}-{possible_letters[-1]}): ",'yellow')).upper()

    while move not in possible_letters:
        print(colored("Invalid index! Please enter a valid index.",'red'))
        move = input(colored(f"Enter the index ({possible_letters[0]}-{possible_letters[-1]}): ",'yellow')).upper()

    return move

#provera da li je stek na tom polju prazan, ako jeste zahteva ponovno unošenje indeksa
def getValidPosition(col:int, row:int):
    
    while is_empty(state.stekovi[row, col]):
        print(colored("Invalid stack! Please enter a not-empty stack index.",'red'))
        getValidFieldRow()
        getValidFieldColumn()

#proverava da li postoji nesto na zadatom indeksu u zadatom steku

#da li ima stacka na tom polju
def isPositionValid(dim:int,position:tuple):
    row = position[0] #broj
    col = position[1] #slovo

    if row < 0 or row >= dim - 1:
        return False
    elif(row+col)%2!=0:    #ako nema stackova na tom polju
        return False
    elif state.stekovi[(col*4)+row/2].is_empty: #ako nema sta da se skine sa stacka
        return False
    return True

#da li ima figurice na zadatom mestu u stacku
def isStackPosValid(stackInput:int,dim:int,position:tuple):
    row = position[0] #broj
    col = position[1] #slovo

    if row < 0 or row >= dim - 1:
        return False
    elif state.stekovi[(col*4)+row/2].is_empty: #ako nema sta da se skine sa stacka
        return False
    elif len(state.stekovi[(col*4)+row/2])<=stackInput:
        return False
    return True

#da li moze da se izvrsi pokret
def isMoveValid(stekovi:list, rowDim:int, position:tuple,moveInput,stackInput):
    row = position[0] #broj
    col = position[1] #slovo

    if moveInput=='GL':
        if not isPositionValid(rowDim,(row-1,col-1)):
            return False
        #kolko se prenosi iz stacka(row,col) na stack u GL
        elif not StackCapacity(HowMuchFromStack(stackInput,(row,col)),(row-1,col-1)):
            return False
        else:
            return True
    elif moveInput=='GD':
        if not isPositionValid(rowDim,(row+1,col-1)):
            return False
        #kolko se prenosi iz stacka(row,col) na stack u GD
        elif not StackCapacity(HowMuchFromStack(stackInput,(row,col)),(row+1,col-1)):
            return False
        else:
            return True
    elif moveInput=='DL':
        if not isPositionValid(rowDim,(row-1,col+1)):
            return False
    #kolko se prenosi iz stacka(row,col) na stack u DL
        elif not StackCapacity(HowMuchFromStack(stackInput,(row,col)),(row-1,col+1)):
            return False
        else:
            return True
    elif moveInput=='GD':
        if not isPositionValid(rowDim,(row+1,col+1)):
            return False
    #kolko se prenosi iz stacka(row,col) na stack u GD
        elif not StackCapacity(HowMuchFromStack(stackInput,(row,col)),(row+1,col+1)):
            return False
        else:
            return True


#da li stack moze da primi n broj figura
def StackCapacity(adding:int,position:tuple):
    row = position[0] #broj
    col = position[1] #slovo

    if len(state.stekovi[(col*4)+row/2])+adding >8:
        return False
    return True



#kolko figura se prenosi
def HowMuchFromStack(stackInput:int,position:tuple):
    row = position[0] #broj
    col = position[1] #slovo

    return len(state.stekovi[(col*4)+row/2])-stackInput


    


def playTurnWithInputs(state:GameState):
    rowInput = -1
    colInput = chr(0)
    stackInput=-1
    moveInput= chr(0)

    print(colored(f'\nPotez {state.currentTurn}:', 'magenta', attrs=['bold']))
    
    #nova istanca stanja
    newState = GameState()
    newState = copy.deepcopy(state)

    if newState.currentTurn == "X":
        while(True):
            # Send rowDim instead of rowDim-1 because row at the table that user sees starts from 1
            rowInput = getValidIntInput(0, newState.dimension, "row (1,2,3...)")
            colInput = getValidCharToIntInput(0, newState.dimension, "column (A,B,C...)")

            if not isPositionValid(newState.dimension,(rowInput, colInput)):
                print(colored("There is no stack here or it is empty, try again!", 'red', attrs=['bold']))
            else:
                break
            stackInput=getValidIntInput(-1,8,"stack")   #0 do 7
            
            if not isStackPosValid(stackInput, newState.dimension,(rowInput, colInput)):
                print(colored("There are not enough figures on a stack, try again!", 'red', attrs=['bold']))
            else:
                break

            moveInput=getValidMoveInput()

            if not isMoveValid(newState.stekovi, newState.dimension, (rowInput, colInput),moveInput):
                print(colored("You can't place stack here, try again!", 'red', attrs=['bold']))
            else:
                break

     #   newState.stateMatrix[rowInput][colInput] = "X"
     #   newState.stateMatrix[rowInput+1][colInput] = "X"
     #   newState.lastPlayedX = [rowInput, colInput]

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

 #   if newState.currentTurn == "X":
 #       newState.stateMatrix[row][col] = "X"
 #       newState.stateMatrix[row + 1][col] = "X"
 #       newState.lastPlayedX = [row, col]
#
 #   elif state.currentTurn == "O":
 #       newState.stateMatrix[row][col] = "O"
 #       newState.stateMatrix[row][col + 1] = "O"
 #       newState.lastPlayedO = [row, col]
#
 #   newState.currentTurn = "O" if newState.currentTurn == "X" else "X"
 #   newState.lastPlayedMove = [row, col]
#
 #   return newState