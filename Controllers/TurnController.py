import copy
from Controllers.GameState import GameState
from ImportedScripts.CMDTextColorizer.ColorizeText import colored
from Interface.Stack import Stack
from Interface.StatePrinter import printWholeTable
from Interface.GameInitializer import gameIsOver
from collections import deque


#state:GameState = GameState()

# ===== REKURZIJA - KONCEPT ======= 
# u ovom slucaju, deosteka nek bude samo brojka kolko figurice(zetona) prenosimo
# 
def rekurzija(trenutnoPoljeMatrice:list, deosteka:int, putanja:list, duzinaPuta = 0):
    # Ispitati da li je polje u matrici - tj ako nije u matrici, nevalidno je
        # if uMatrici(trenutnoPoljeMatrice) == false: return [None, None, None]
    # Ispitati da li je trenutno polje stek ili je prazno
        # if prazno(trenutnoPoljeMatrice) == false:
            #if mozemoDaStavimoDeoSteka(deosteka, stekNaTrenutnomPoljuMatrice) == true: ---> NALAZIMO SE NA NEKOM STEKU, I MOZEMO DA STAVIMO TOLKO FIGURICA KOLKO PRENOSIMO
                #return [trenutnoPoljeMatrice, putanja[prvoNarednoPolje], duzinaPuta] ---- ubaciti i duzinu puta u kalkulaciju
            #else:
                #return [None, None, None] -> dosli smo do polja koje je stek, ALI taj stek je recimo skoro pun i ne mozemo da stavimo "deosteka", izlazimo iz ove putanje jer ne mozemo dalje
        # else:
            #duzinaPuta++;
            #putanja.append(trenutnoPoljeMatrice) --- ovo nece bas da radi najbolje, ako npr dodjemo na jedno prazno polje, a sledece polje nam ne daje validan potez,
            #samo razmisliti kako se dodaju i/ili uklanjaju stvari iz putanje, da bi radilo dobro
            
    # Svejedno je kojim smerom, ali probamo prvo GORE LEVO
    #rekurzija([trenutnoPoljeMatrice[0]-1, trenutnoPoljeMatrice[1]-1], 3, putanja.append([trenutnoPoljeMatrice[0]-1, trenutnoPoljeMatrice[1]-1]))
    # DOLE LEVO 
    #rekurzija([trenutnoPoljeMatrice[0]+1, trenutnoPoljeMatrice[1]-1], 3, putanja.append([trenutnoPoljeMatrice[0]+1, trenutnoPoljeMatrice[1]-1]))
    # GORE DESNO
    #rekurzija([trenutnoPoljeMatrice[0]-1, trenutnoPoljeMatrice[1]+1], 3, putanja.append([trenutnoPoljeMatrice[0]-1, trenutnoPoljeMatrice[1]+1]))
    # DOLE DESNO
    #rekurzija([trenutnoPoljeMatrice[0]+1, trenutnoPoljeMatrice[1]+1], 3, putanja.append([trenutnoPoljeMatrice[0]+1, trenutnoPoljeMatrice[1]+1]))

    return [None, None, None]

#mozemoDaStavimoDeoSteka(deosteka, stekNaTrenutnomPoljuMatrice):
    #return deosteka + stekNaTrenutnomPoljuMatrice <= 8
def isPositionInMatrix(position :(int,int), dimension : int) :
    return position[0] >=0 and position[0] < dimension and position[1] >=0 and position[1] < dimension

def shortestPathBetweenPositions(state : GameState, startPosition : (int, int), endPosition : (int, int)) :
    rows =  state.dimension
    cols = state.dimension
    visited = [[False] * cols for _ in range(rows)]
    moves = [(-1, 1), (-1, -1), (1, -1), (1, 1)]
    queue = deque([(startPosition[0], startPosition[1], 0)])
    while queue:
        current_x, current_y, distance = queue.popleft()

        # Check if we reached the destination
        if (current_x, current_y) == endPosition:
            return distance

        # Mark the current position as visited
        visited[current_x][current_y] = True

        # Explore possible moves
        for move_x, move_y in moves:
            new_x, new_y = current_x + move_x, current_y + move_y
            #print(current_x, current_y, distance)
            # Check if the new position is valid

            if isPositionInMatrix((new_x, new_y), state.dimension) == True : 
                if ((new_x, new_y) == startPosition):
                    continue
                if (state.matrix[new_x][new_y] == None or (isinstance(state.matrix[new_x][new_y], Stack) and (new_x, new_y) == endPosition)) :
                    queue.append((new_x, new_y, distance + 1))
            else:
                continue

    # If no path is found
    return -1

def validMovesToNonEmtyStacks(arrayOfClosestNonEmptyIndexes : list, startPosition : (int, int), state : GameState) :
    minumumDistancePositions = [(startPosition, 10000)]
    distances = []
    print(arrayOfClosestNonEmptyIndexes)
    for currentStackIndex in arrayOfClosestNonEmptyIndexes :
        relative_positions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dx, dy in relative_positions:
            new_position = (startPosition[0] + dx, startPosition[1] + dy)

            if isPositionInMatrix(new_position, state.dimension):
                print(shortestPathBetweenPositions(state, new_position, currentStackIndex))
                x = shortestPathBetweenPositions(state, new_position, currentStackIndex)
                if (x > -1):
                    distance = x + 1
                    distances.append((new_position, distance))
                    print("ovo ja sad proveravam")
                    print((currentStackIndex[0], currentStackIndex[1]))
                    print((new_position, distance))

        sortedDistances = sorted(distances, key=lambda x: x[1])
        if sortedDistances[0][1] <= minumumDistancePositions[0][1]:
            minumumDistancePositions.clear()
            for e in sortedDistances :
                if (e[1] == sortedDistances[0][1]) :
                    minumumDistancePositions.append(e)
    print(minumumDistancePositions)

    return [item[0] for item in minumumDistancePositions]

def returnValidMovesForFigure(row, col, rowDim, stekovi, stackInput, state):
    
    #za svako neprazno mod isMoveValid
    moveIndexes=[(row-1, col-1), (row+1, col-1), (row-1, col+1), (row+1, col+1)]
    validMovesArray=[]
    moveEmptyIndexes=[]
    arrayOfClosestNonEmptyIndexes=[]
    for move in moveIndexes:
        if coorToStack(move[0], move[1], rowDim, stekovi).is_empty():
            moveEmptyIndexes.append(move)
            continue 
        elif not isPositionValidDst(rowDim,(move[0], move[1]), stekovi):
            continue
        #kolko se prenosi iz stacka(row,col) na stack u DL
        elif not StackCapacity(HowMuchFromStack(stackInput,(move[0], move[1]), stekovi, rowDim),(move[0], move[1]), stekovi, rowDim):
            continue
        elif not isHeightValid(move[0], move[1], stackInput, rowDim, stekovi):
            continue
        validMovesArray.append(move)
    if len(moveEmptyIndexes)==4:#ako su sva polja susedna prazna
        arrayOfClosestNonEmptyIndexes=allValidStacks(rowDim, state, row, col, stackInput)
        validMovesArray = validMovesToNonEmtyStacks(arrayOfClosestNonEmptyIndexes, (row, col), state)
        #andrijana nadje indekse na koje moze da ide i to stavlja u validMovesArray
    return validMovesArray



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

def coorToStack(row, col, dim, stekovi):

    x = int(dim/2)
    y = int(col + 2)
    return stekovi[(int)(((row)*x)+y//2 - 1)]

def stackToCoor(stack, state):#nije provereno da l radi
    row=state.stekovi.index(stack)//(state.dimension/2)
    if(row%2==0):
        col=((state.stekovi.index(stack))%(state.dimension/2))*2 
    else:
        col=((state.stekovi.index(stack))%(state.dimension/2))*2 +1
    #x = int(state.dimension / 2)
    #y = state.stekovi.index(stack) + 1
    #row = (y - 1) // x
    #col = ((y - 1) % x) * 2 - 2
    return (row, col)


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
#za hsrc i hdst
def isHeightValid(rowDest, colDest, stackInput, dim, stekovi):
    stek=coorToStack(rowDest, colDest, dim, stekovi)
    if((stackInput)<(stek.stackLen())):
        return True
    else:
        return False

#za player sign i figurica da se poklope
def isSignCorrect(row, col, stackInput, dim, stekovi, newState):
    stek=coorToStack(row, col, dim, stekovi)
    if(stek.array[stackInput]==newState.currentTurn):
        return True
    return False

#za player sign i figurica da se poklope

#da li moze da se izvrsi pokret
def isMoveValid(stekovi:list, rowDim:int, position:tuple,moveInput,stackInput, dim : int, newState:GameState):
    row = position[0] #slovo
    col = position[1] #broj

    if moveInput=="GL":
         #za player sign i figurica da se poklope
        if not isSignCorrect(row, col, stackInput, dim, stekovi, newState):
            return False
        #i ako je dest stack prazan pozovi fju isThisFieldInValidMoves(za row i col npr)
        elif (coorToStack(row-1,col-1, dim, stekovi)).is_empty():
            if (row-1, col-1) in returnValidMovesForFigure(row, col, dim, stekovi, stackInput, newState):
                print("prazno polje je validno")
                return True
        elif not isPositionValidDst(rowDim,(row-1,col-1), stekovi):
            return False
        #kolko se prenosi iz stacka(row,col) na stack u GL
        elif not StackCapacity(HowMuchFromStack(stackInput,(row,col), stekovi, dim),(row-1,col-1), stekovi, rowDim):
            return False
        #za hsrc i hdst
        elif not isHeightValid(row-1,col-1, stackInput, dim, stekovi):
            return False    
       

        else:
            return True
    elif moveInput=="DL":
        #za player sign i figurica da se poklope
        if not isSignCorrect(row, col, stackInput, dim,stekovi, newState):
            return False
        elif (coorToStack(row+1,col-1, dim, stekovi)).is_empty():
            if (row+1, col-1) in returnValidMovesForFigure(row, col, dim, stekovi,stackInput, newState):
                print("prazno polje je validno")
                
                return True
        elif not isPositionValidDst(rowDim,(row+1,col-1), stekovi):
            return False
        #kolko se prenosi iz stacka(row,col) na stack u GD
        elif not StackCapacity(HowMuchFromStack(stackInput,(row,col), stekovi, dim),(row+1,col-1), stekovi, rowDim):
            return False
        elif not isHeightValid(row+1,col-1, stackInput, dim, stekovi):
            return False
       
        else:
            return True
    elif moveInput=="GD":
        #za player sign i figurica da se poklope
        if not isSignCorrect(row, col, stackInput, dim,stekovi, newState):
            return False
        elif (coorToStack(row-1,col+1, dim, stekovi)).is_empty():
            if (row-1, col+1) in returnValidMovesForFigure(row, col, dim, stekovi, stackInput, newState):
                print("prazno polje je validno")

                return True
        elif not isPositionValidDst(rowDim,(row-1,col+1), stekovi):
            return False
    #kolko se prenosi iz stacka(row,col) na stack u DL
        elif not StackCapacity(HowMuchFromStack(stackInput,(row,col), stekovi, dim),(row-1,col+1), stekovi, rowDim):
            return False
        elif not isHeightValid(row-1,col+1, stackInput, dim, stekovi):
            return False
       
        else:
            return True
    elif moveInput=="DD":
         #za player sign i figurica da se poklope
        if not isSignCorrect(row, col, stackInput, dim, stekovi, newState):
            print("sign not correct")
            return False
        elif (coorToStack(row+1,col+1, dim, stekovi)).is_empty():
            if (row-1, col-1) in returnValidMovesForFigure(row, col, dim, stekovi, stackInput, newState):
                print("prazno polje je validno")

                return True
        elif not isPositionValidDst(rowDim,(row+1,col+1), stekovi):
            print("position not correct")
            return False
    #kolko se prenosi iz stacka(row,col) na stack u GD
        elif not StackCapacity(HowMuchFromStack(stackInput,(row,col), stekovi, dim),(row+1,col+1), stekovi, rowDim):
            print("stack not correct")
            return False
        elif not isHeightValid(row+1,col+1, stackInput, dim, stekovi):
            print("height not correct")
            return False
       
        else:
            return True



             
#provera za potez  - player sign mora da se poklapa sa stekom koji treba da se poreri(da je X ako igra X)
#provera za potez - da li postiji neprazno polje GD,  GL, DL,DD 
#provera ako ne postoji neprazno polje - računa se najmanja udaljenost do nezauzetog polja(???) - onda su valjani potezi oni sa najmanjom udaljenoscu
#proverava visine stekova hsrc<hdest
#fja koja će da vrati sve valjane poteze za sve figurice 
#ako ima valjani bar jedan - mora da odigra

#OVO JE ZA SVE MOGUĆE VALJANE POTEZE     
#for za sve figurice tog igrača i za svaki proveri gde može da se pomeri gg.. ovo proverava visine stekova hsrc<hdest i onda 
    #ako su svi prazni ili neprazni ne ispunjavaju ove gore uslove gleda najmanje udaljenosti do nepraznog polja koja vode do najblizem nepraznom polju
        #fja koja traži najblizi - promenjiva min i vraća niz indeksa koji imaju udaljenost jednaku min ({i,j},.. ) 
        #pozivamo dfs za te indekse i vraća početne kordinate puta i svešta u niz valjanih puteva ali proverava da se već ne nalaze tu
    #ako ima valjani bar jedan - mora da odigra
        #ako nema printamo ne postoji valjani potez i igra drugi igrač


#ZA UNETE PARAMETRE VALJANI POTEZ
#ako su svi prazni ili neprazni ne ispunjavaju ove gore uslove gleda najmanje udaljenosti do nepraznog polja koja vode do najblizem nepraznom polju
        #fja koja traži najblizi - promenjiva min i vraća niz indeksa koji imaju udaljenost jednaku min ({i,j},.. ) 
        #pozivamo dfs za te indekse i vraća početne kordinate puta i svešta u niz valjanih puteva ali proverava da se već ne nalaze tu
        #provera za potez  - player sign mora da se poklapa sa stekom koji treba da se poreri(da je X ako igra X)
        #proverava visine stekova hsrc<hdest


#returnAllValidMoves --- dodace se fja koja ce da poz returnValidMovesForFigure u for petlji za svaku figuru tog znaka!
#predaja potez

def returnValidMovesForFigure(row, col, rowDim, stekovi, stackInput, state):
    
    #za svako neprazno mod isMoveValid
    moveIndexes=[(row-1, col-1), (row+1, col-1), (row-1, col+1), (row+1, col+1)]
    validMovesArray=[]
    moveEmptyIndexes=[]
    arrayOfClosestNonEmptyIndexes=[]
    for move in moveIndexes:
        if coorToStack(move[0], move[1], rowDim, stekovi).is_empty():
            moveEmptyIndexes.append(move)
            continue 
        elif not isPositionValidDst(rowDim,(move[0], move[1]), stekovi):
            continue
        #kolko se prenosi iz stacka(row,col) na stack u DL
        elif not StackCapacity(HowMuchFromStack(stackInput,(move[0], move[1]), stekovi, rowDim),(move[0], move[1]), stekovi, rowDim):
            continue
        elif not isHeightValid(move[0], move[1], stackInput, rowDim, stekovi):
            continue
        validMovesArray.append(move)
    if len(moveEmptyIndexes)==4:#ako su sva polja susedna prazna
        print("sva su polja okolna prazna")
        arrayOfClosestNonEmptyIndexes=allValidStacks(rowDim, state, row, col, stackInput)
        validMovesArray = validMovesToNonEmtyStacks(arrayOfClosestNonEmptyIndexes, (row, col), state)
        #andrijana nadje indekse na koje moze da ide i to stavlja u validMovesArray
    return validMovesArray


def allValidStacks( dim, state, row, col, stackInput):#nije proradilo jos veceras ce 
    min=float('inf')
    result=[]
    #print("usao je u all-Valid-stacks")
    result=[]
    for stek in state.stekovi:
        rowDest=stackToCoor(stek, state)[0]
        colDest=stackToCoor(stek, state)[1]
        print([rowDest, colDest])
        if not coorToStack(rowDest, colDest, dim, state.stekovi).is_empty() and not (rowDest==row and colDest==col) :#razlicit od posmatranog i nije prazan,
            #provera validnosti
            if not StackCapacity(HowMuchFromStack(stackInput,(row,col), state.stekovi, dim),(rowDest,colDest), state.stekovi, dim):
                continue
            #za hsrc i hdst
            elif not isHeightValid(rowDest,colDest, stackInput, dim, state.stekovi):
                continue
            print("ispunjava sve uslove")
            result.append((rowDest,colDest))

            #da li moze da se prebaci toliko figurica
            #pom=max(abs(rowSrc-rowDest), abs(colSrc-colDest))
            #if(pom<min):
            #    min=pom
            #    result=[]
            #    result.append((rowDest,colDest))
            #elif(pom==min):
            #    result.append((rowDest,colDest))
    print(result)
    return result



#da li stack moze da primi n broj figura
def StackCapacity(adding:int,position:tuple, stekovi:list, dim:int):
    row = position[0] #slovo
    col = position[1] #broj
    x = int(dim/2)
    y = col + 2


    if stekovi[(int)(((row)*x)+y//2 - 1)].stackLen()+adding >8:
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
    newState.matrix = state.matrix
    # Kopiranje stekova - moguće je napraviti kopiju stekova jedan po jedan ili prilagoditi njihovo kopiranje
    newState.stekovi = [elem for elem in state.stekovi]

    while(gameIsOver()==False):
        if state.currentTurn == "X":
            print(colored(f'\nPotez {state.currentTurn}:', 'magenta', attrs=['bold']))
            while(True):
            
                # Send rowDim instead of rowDim-1 because row at the table that user sees starts from 1
                rowInput = getValidCharToIntInput(0, state.dimension, "row (A,B,C...)")
                colInput = getValidIntInput(0, state.dimension, "column (1,2,3...)")

                if not isPositionValidSrc(state.dimension,(rowInput, colInput),state.stekovi):
                    print(colored("There is no stack here or it is empty, try again!", 'red', attrs=['bold']))
                    continue
                
                stackInput=getValidStackInput(0,8,"stack (0,1,2..)")   #0 do 7

                if not isStackPosValid(stackInput, newState.dimension,(rowInput, colInput),newState.stekovi):
                    print(colored("There are not enough figures on a stack, try again!", 'red', attrs=['bold']))
                    continue
                
                moveInput=getValidMoveInput()

                if not isMoveValid(newState.stekovi, newState.dimension, (rowInput, colInput),moveInput,stackInput, newState.dimension, newState):
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
            state.matrix = newState.matrix
            newState.currentTurn="O"

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

                if not isMoveValid(newState.stekovi, newState.dimension, (rowInput, colInput),moveInput,stackInput, newState.dimension, newState):
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
            newState.currentTurn="X"
            gameIsOver()
            printWholeTable(state)

   



