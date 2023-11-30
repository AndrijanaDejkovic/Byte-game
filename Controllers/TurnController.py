import copy
from Controllers.GameState import GameState
from ImportedScripts.CMDTextColorizer.ColorizeText import colored
from Interface.Stack import Stack
from Interface.StatePrinter import printWholeTable
from Interface.GameInitializer import gameIsOver

state:GameState = GameState()

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
def isPositionValid(dim:int,position:tuple,stekovi:list):
    row = position[0] #slovo
    col = position[1] #broj

    if row < 0 or row >= dim - 1:
        return False
    elif(row+col)%2!=0:    #ako nema stackova na tom polju
        return False
    elif stekovi[(row*4)+col//2].is_empty(): #ako nema sta da se skine sa stacka
        return False
    return True

#da li ima figurice na zadatom mestu u stacku
def isStackPosValid(stackInput:int,dim:int,position:tuple,stekovi:list):
    row = position[0] #slovo
    col = position[1] #broj

    if row < 0 or row >= dim - 1:
        return False
    elif stekovi[(row*4)+col//2].stackLen()==0: #ako nema sta da se skine sa stacka
        return False
    elif stekovi[(row*4)+col//2].stackLen()<=stackInput:
        return False
    return True

#da li moze da se izvrsi pokret
def isMoveValid(stekovi:list, rowDim:int, position:tuple,moveInput,stackInput):
    row = position[0] #slovo
    col = position[1] #broj

    if moveInput=="GL":
        if not isPositionValid(rowDim,(row-1,col-1), stekovi):
            return False
        #kolko se prenosi iz stacka(row,col) na stack u GL
        elif not StackCapacity(HowMuchFromStack(stackInput,(row,col), stekovi),(row-1,col-1), stekovi):
            return False
        else:
            return True
    elif moveInput=="DL":
        if not isPositionValid(rowDim,(row+1,col-1), stekovi):
            return False
        #kolko se prenosi iz stacka(row,col) na stack u GD
        elif not StackCapacity(HowMuchFromStack(stackInput,(row,col), stekovi),(row+1,col-1), stekovi):
            return False
        else:
            return True
    elif moveInput=="GD":
        if not isPositionValid(rowDim,(row-1,col+1), stekovi):
            return False
    #kolko se prenosi iz stacka(row,col) na stack u DL
        elif not StackCapacity(HowMuchFromStack(stackInput,(row,col), stekovi),(row-1,col+1), stekovi):
            return False
        else:
            return True
    elif moveInput=="DD":
        if not isPositionValid(rowDim,(row+1,col+1), stekovi):
            return False
    #kolko se prenosi iz stacka(row,col) na stack u GD
        elif not StackCapacity(HowMuchFromStack(stackInput,(row,col), stekovi),(row+1,col+1), stekovi):
            return False
        else:
            return True


#da li stack moze da primi n broj figura
def StackCapacity(adding:int,position:tuple, stekovi:list):
    row = position[0] #slovo
    col = position[1] #broj

    if stekovi[(row*4)+col//2].stackLen()+adding >8:
        return False
    return True



#kolko figura se prenosi
def HowMuchFromStack(stackInput:int,position:tuple, stekovi:list):
    row = position[0] #slovo
    col = position[1] #broj
    pom =stekovi[(row*4)+col//2].stackLen()
    return pom-stackInput

def transferFromStack(position:tuple, stekovi:list, stackInput:int,moveInput):
     row = position[0] #slovo
     col = position[1] #broj
     positionNew=newPostionCalc(position, moveInput)
     rowNew=positionNew[0]
     colNew=positionNew[1]
     transfer=[]
     for i in range (HowMuchFromStack(stackInput, position, stekovi)):
           transfer.append(stekovi[(row*4)+col//2].pop())
     for i in range (1, len(transfer)+1):
         if(stekovi[(rowNew*4)+colNew//2].is_empty()):
             stekovi[(rowNew*4)+colNew//2].makeBegginingStack(transfer[-i])
         else:
             stekovi[(rowNew*4)+colNew//2].push(transfer[-i])
    
    
    
    

def newPostionCalc( position:tuple,moveInput):
    row = position[0] #slovo
    col = position[1] #broj

    if moveInput=="GL":
        return (row-1,col-1)
        
    elif moveInput=="DL":
       return(row+1,col-1)
       
    elif moveInput=="GD":
        return(row-1,col+1)
     
    elif moveInput=="DD":
       return(row+1,col+1)
      


     

    


def playTurnWithInputs(state:GameState):
    rowInput = -1
    colInput = chr(0)
    stackInput=-1
    moveInput= chr(0)

    
    
    #nova istanca stanja
    newState = GameState()
    newState.playerSign = state.playerSign
    newState.cpuSign = state.cpuSign
    newState.currentTurn = state.currentTurn
    newState.dimension = state.dimension
    newState.maxDimension = state.maxDimension
    newState.playerScore = state.playerScore
    newState.cpuScore = state.cpuScore
    # Kopiranje stekova - moguće je napraviti kopiju stekova jedan po jedan ili prilagoditi njihovo kopiranje
    newState.stekovi = [elem for elem in state.stekovi]

    while(gameIsOver()==False):
        if state.currentTurn == "X":
            print(colored(f'\nPotez {state.currentTurn}:', 'magenta', attrs=['bold']))
            while(True):
            
                # Send rowDim instead of rowDim-1 because row at the table that user sees starts from 1
                rowInput = getValidCharToIntInput(0, newState.dimension, "row (A,B,C...)")
                colInput = getValidIntInput(0, newState.dimension, "column (1,2,3...)")

                if not isPositionValid(newState.dimension,(rowInput, colInput),newState.stekovi):
                    print(colored("There is no stack here or it is empty, try again!", 'red', attrs=['bold']))
                    continue
                
                stackInput=getValidIntInput(0,8,"stack (1,2,3..)")   #0 do 7

                if not isStackPosValid(stackInput, newState.dimension,(rowInput, colInput),newState.stekovi):
                    print(colored("There are not enough figures on a stack, try again!", 'red', attrs=['bold']))
                    continue
                
                moveInput=getValidMoveInput()

                if not isMoveValid(newState.stekovi, newState.dimension, (rowInput, colInput),moveInput,stackInput):
                    print(colored("You can't place stack here, try again!", 'red', attrs=['bold']))
                    continue
                
                else: break

            #push i pop 
            transferFromStack((rowInput, colInput), newState.stekovi, stackInput,moveInput)
            state.stekovi=newState.stekovi
            state.currentTurn = "O"
            gameIsOver()
            printWholeTable(state)


        elif state.currentTurn == "O":
            print(colored(f'\nPotez {state.currentTurn}:', 'magenta', attrs=['bold']))
            while(True):
            
                # Send rowDim instead of rowDim-1 because row at the table that user sees starts from 1
                rowInput = getValidCharToIntInput(0, newState.dimension, "row (A,B,C...)")
                colInput = getValidIntInput(0, newState.dimension, "column (1,2,3...)")

                if not isPositionValid(newState.dimension,(rowInput, colInput),newState.stekovi):
                    print(colored("There is no stack here or it is empty, try again!", 'red', attrs=['bold']))
                    continue
                
                stackInput=getValidIntInput(0,8,"stack (1,2,3..)")   #0 do 7
                
                if not isStackPosValid(stackInput, newState.dimension,(rowInput, colInput),newState.stekovi):
                    print(colored("There are not enough figures on a stack, try again!", 'red', attrs=['bold']))
                    continue
                
                moveInput=getValidMoveInput()

                if not isMoveValid(newState.stekovi, newState.dimension, (rowInput, colInput),moveInput,stackInput):
                    print(colored("You can't place stack here, try again!", 'red', attrs=['bold']))
                    continue
                
                else: break

            #push i pop 
            transferFromStack((rowInput, colInput), newState.stekovi, stackInput,moveInput)
            state.stekovi=newState.stekovi
            state.currentTurn = "X"
            gameIsOver()
            printWholeTable(state)

   



