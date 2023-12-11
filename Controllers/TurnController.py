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
    while(inp < min or inp > max):   #da li je od 0 do dimenzije table
        try:
            inp = int(input(colored(f"Enter {inputContext} position: ", 'yellow')))
        except:
            print(colored("Invalid input", 'red', attrs=['bold']))
    return inp - 1

def getValidStackInput(min:int, max:int, inputContext:str):
    inp = -1
    while(inp < min or inp > max):   #da li je od 0 do dimenzije table
        try:
            inp = int(input(colored(f"Enter {inputContext} position: ", 'yellow')))
        except:
            print(colored("Invalid input", 'red', attrs=['bold']))
    return inp


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



#da li ima stacka na tom polju
def isPositionValidSrc(dim:int,position:tuple,stekovi:list):
    row = position[0] #slovo
    col = position[1] #broj

    x = int(dim/2)
    y = col + 2
    

    if row < 0 or row > dim - 1:

        return False
    elif(row+col)%2!=0:    #ako nema stackova na tom polju

        return False
    elif stekovi[((row)*x)+y//2 - 1].is_empty(): #ako nema sta da se skine sa stacka
        return False
    return True

def isPositionValidDst(dim:int,position:tuple,stekovi:list):
    row = position[0] #slovo
    col = position[1] #broj

    x = int(dim/2)
    y = col + 2
    


    if row < 0 or row > dim - 1:
        return False
    elif(row+col)%2!=0:    #ako nema stackova na tom polju
        return False
    #elif stekovi[((row)*x)+y//2 - 1].is_empty(): #ako nema sta da se skine sa stacka
    #    print(f"NASTANAK3 {((row)*x)+y//2 - 1}")
    #    return False
    return True

#da li ima figurice na zadatom mestu u stacku
def isStackPosValid(stackInput:int,dim:int,position:tuple,stekovi:list):
    row = position[0] #slovo
    col = position[1] #broj
    x = int(dim/2)
    y = col + 2
    

    if row < 0 or row > dim - 1:

        return False
    elif stekovi[((row)*x)+y//2 - 1].stackLen()==0: #ako nema sta da se skine sa stacka

        return False
    elif stekovi[((row)*x)+y//2 - 1].stackLen()<= stackInput:

        return False
    return True

#da li moze da se izvrsi pokret
def isMoveValid(stekovi:list, rowDim:int, position:tuple,moveInput,stackInput, dim : int):
    row = position[0] #slovo
    col = position[1] #broj

    if moveInput=="GL":
        if not isPositionValidDst(rowDim,(row-1,col-1), stekovi):
            return False
        #kolko se prenosi iz stacka(row,col) na stack u GL
        elif not StackCapacity(HowMuchFromStack(stackInput,(row,col), stekovi, dim),(row-1,col-1), stekovi, rowDim):
            return False
        else:
            return True
    elif moveInput=="DL":
        if not isPositionValidDst(rowDim,(row+1,col-1), stekovi):
            return False
        #kolko se prenosi iz stacka(row,col) na stack u GD
        elif not StackCapacity(HowMuchFromStack(stackInput,(row,col), stekovi, dim),(row+1,col-1), stekovi, rowDim):
            return False
        else:
            return True
    elif moveInput=="GD":
        if not isPositionValidDst(rowDim,(row-1,col+1), stekovi):
            return False
    #kolko se prenosi iz stacka(row,col) na stack u DL
        elif not StackCapacity(HowMuchFromStack(stackInput,(row,col), stekovi, dim),(row-1,col+1), stekovi, rowDim):
            return False
        else:
            return True
    elif moveInput=="DD":
        if not isPositionValidDst(rowDim,(row+1,col+1), stekovi):
            return False
    #kolko se prenosi iz stacka(row,col) na stack u GD
        elif not StackCapacity(HowMuchFromStack(stackInput,(row,col), stekovi, dim),(row+1,col+1), stekovi, rowDim):
            return False
        else:
            return True


#da li stack moze da primi n broj figura
def StackCapacity(adding:int,position:tuple, stekovi:list, dim:int):
    row = position[0] #slovo
    col = position[1] #broj
    x = int(dim/2)
    y = col + 2


    if stekovi[((row)*x)+y//2 - 1].stackLen()+adding >8:
        return False
    return True



#kolko figura se prenosi
def HowMuchFromStack(stackInput:int,position:tuple, stekovi:list, dim:int):
    row = position[0] #slovo
    col = position[1] #broj
    x = int(dim/2)
    y = col + 2


    pom =stekovi[((row)*x)+y//2 - 1].stackLen()
    return pom-stackInput

def transferFromStack(position:tuple, stekovi:list, stackInput:int,moveInput, dim:int):
     row = position[0] #slovo
     col = position[1] #broj
     positionNew=newPostionCalc(position, moveInput)
     rowNew=positionNew[0]
     colNew=positionNew[1]
     transfer=[]
     x = int(dim/2)
     y = col + 2
     yNew=colNew+2
    


     for i in range (HowMuchFromStack(stackInput, position, stekovi, dim)):
           transfer.append(stekovi[((row)*x)+y//2 - 1].pop())
     for i in range (1, len(transfer)+1):

        stekovi[((rowNew)*x)+yNew//2 - 1].push(transfer[-i])
   
    

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
      

def pointsUpdate(state):
    for stek in state.stekovi:
        if len(stek.array)==8:
            if stek.array[7]==state.playerSign:
               state.playerScore+=1
            else:
               state.cpuScore+=1
            stek.emptyFullStack()
           
               

#provera za potez  - player sign mora da se poklapa sa stekom koji treba da se poreri(da je X ako igra X)
#provera za potez - da li postiji neprazno polje GD,  GL, DL,DD 
#provera ako ne postoji neprazno polje - računa se najmanja udaljenost do nezauzetog polja(???) - onda su valjani potezi oni sa najmanjom udaljenoscu
#proverava visine stekova hsrc<hdest
#fja koja će da vrati sve valjane poteze za sve figurice 
#ako ima valjani bar jedan - mora da odigra

      

    


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

                if not isPositionValidSrc(newState.dimension,(rowInput, colInput),newState.stekovi):
                    print(colored("There is no stack here or it is empty, try again!", 'red', attrs=['bold']))
                    continue
                
                stackInput=getValidStackInput(0,8,"stack (0,1,2..)")   #0 do 7

                if not isStackPosValid(stackInput, newState.dimension,(rowInput, colInput),newState.stekovi):
                    print(colored("There are not enough figures on a stack, try again!", 'red', attrs=['bold']))
                    continue
                
                moveInput=getValidMoveInput()

                if not isMoveValid(newState.stekovi, newState.dimension, (rowInput, colInput),moveInput,stackInput, newState.dimension):
                    print(colored("You can't place stack here, try again!", 'red', attrs=['bold']))
                    continue
                
                else: break

            #push i pop 
            transferFromStack((rowInput, colInput), newState.stekovi, stackInput,moveInput, newState.dimension)
            pointsUpdate(newState)
            state.stekovi=newState.stekovi
            state.playerScore=newState.playerScore
            state.cpuScore=newState.cpuScore
            state.currentTurn = "O"
            gameIsOver()
            printWholeTable(newState)


        elif state.currentTurn == "O":
            print(colored(f'\nPotez {state.currentTurn}:', 'magenta', attrs=['bold']))
            while(True):
            
                # Send rowDim instead of rowDim-1 because row at the table that user sees starts from 1
                rowInput = getValidCharToIntInput(0, newState.dimension, "row (A,B,C...)")
                colInput = getValidIntInput(0, newState.dimension, "column (1,2,3...)")

                if not isPositionValidSrc(newState.dimension,(rowInput, colInput),newState.stekovi):
                    print(colored("There is no stack here or it is empty, try again!", 'red', attrs=['bold']))
                    continue
                
                stackInput=getValidStackInput(0,8,"stack (0,1,2..)")   #0 do 7
                
                if not isStackPosValid(stackInput, newState.dimension,(rowInput, colInput),newState.stekovi):
                    print(colored("There are not enough figures on a stack, try again!", 'red', attrs=['bold']))
                    continue
                
                moveInput=getValidMoveInput()

                if not isMoveValid(newState.stekovi, newState.dimension, (rowInput, colInput),moveInput,stackInput, newState.dimension):
                    print(colored("You can't place stack here, try again!", 'red', attrs=['bold']))
                    continue
                
                else: break

            #push i pop 
            transferFromStack((rowInput, colInput), newState.stekovi, stackInput,moveInput, newState.dimension)
            pointsUpdate(newState)
            state.stekovi=newState.stekovi
            state.playerScore=newState.playerScore
            state.cpuScore=newState.cpuScore
            state.currentTurn = "X"
            gameIsOver()
            printWholeTable(state)

   



