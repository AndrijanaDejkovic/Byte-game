import copy
from Controllers.GameState import GameState
from ImportedScripts.CMDTextColorizer.ColorizeText import colored
from Interface.Stack import Stack
from Interface.StatePrinter import printWholeTable
from Interface.GameInitializer import gameIsOver
from collections import deque



#SINTAKSNE PROVERE UNOSA


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


def getValidMoveInput():
    possible_moves = ["GL", "GD", "DL", "DD"]
    move = input(colored("Enter the move (GL, GD, DL, DD): ",'yellow')).upper()

    while move not in possible_moves:
        print(colored("Invalid move! Please enter a valid move.",'red'))
        move = input(colored("Enter the move (GL, GD, DL, DD): ",'yellow')).upper()
    return move


#POMOCNE FUNKCIJE


def coorToStack(row, col, state):

    x = int(state.dimension/2)
    y = int(col + 2)
    return state.stekovi[(int)(((row)*x)+y//2 - 1)]


def stackToCoor(stack, state):
    row=state.stekovi.index(stack)//(state.dimension//2)
    if(row%2==0):
        col=((state.stekovi.index(stack))%(state.dimension//2))*2 
    else:
        col=((state.stekovi.index(stack))%(state.dimension//2))*2 +1
    return (row, col)


def StackCapacity(adding:int,position:tuple, state):
    row = position[0] #slovo
    col = position[1] #broj
    x = int(state.dimension/2)
    y = col + 2
    if state.stekovi[(int)(((row)*x)+y//2 - 1)].stackLen()+adding >8:
        return False
    return True


#kolko figura se prenosi
def HowMuchFromStack(stackInput:int,position:tuple, state):
    row = position[0] #slovo
    col = position[1] #broj
    x = int(state.dimension/2)
    y = col + 2
    pom =state.stekovi[(int)(((row)*x)+y//2 - 1)].stackLen()
    return pom-stackInput


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
    

#PROVERE VALIDNOSTI UNOSA
    

#da li ima stacka na tom polju
def isPositionValidSrc(state, position):
    row = position[0] #slovo
    col = position[1] #broj
    x = int(state.dimension/2)
    y = col + 2
    
    if row < 0 or row > state.dimension - 1:
        return False
    elif(row+col)%2!=0:    #ako nema stackova na tom polju
        return False
    elif state.stekovi[((row)*x)+y//2 - 1].is_empty(): #ako nema sta da se skine sa stacka
        return False
    return True


def isPositionValidDst(state,position:tuple):
    row = position[0] #slovo
    col = position[1] #broj
    x = int(state.dimension/2)
    y = col + 2
    
    if row < 0 or row > state.dimension - 1:
        return False
    elif(row+col)%2!=0:    #ako nema stackova na tom polju
        return False
    return True


#da li ima figurice na zadatom mestu u stacku
def isStackPosValid(stackInput:int,position:tuple, state):
    dim=state.dimension
    stekovi=state.stekovi
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
def isHeightValid(rowDest, colDest, stackInput, state):
    dim=state.dimension
    stekovi=state.stekovi
    stek=coorToStack(rowDest, colDest, state)
    if((stackInput)<(stek.stackLen())):
        return True
    else:
        return False


#za player sign i figurica da se poklope
def isSignCorrect(row, col, stackInput, state):
    stek=coorToStack(row, col, state)
    if(stek.array[stackInput]==state.currentTurn):
        return True
    return False


#mozemoDaStavimoDeoSteka(deosteka, stekNaTrenutnomPoljuMatrice):
    #return deosteka + stekNaTrenutnomPoljuMatrice <= 8
def isPositionInMatrix(position :(int,int), dimension : int) :
    return position[0] >=0 and position[0] < dimension and position[1] >=0 and position[1] < dimension


def isMoveValid(position:tuple,moveInput,stackInput, state:GameState):
    stekovi=state.stekovi
    dim=state.dimension
    row = position[0] #slovo
    col = position[1] #broj


    if moveInput=="GL":
         #za player sign i figurica da se poklope
        if not isSignCorrect(row, col, stackInput, state):
            print(colored("You can't play with this figure, try again!", 'red', attrs=['bold']))
            return False
        elif not isPositionInMatrix((row-1,col-1),state.dimension):
            print(colored("Destination out of bounds, try again!", 'red', attrs=['bold']))
            return False
        #i ako je dest stack prazan pozovi fju isThisFieldInValidMoves(za row i col npr)
        elif (coorToStack(row-1,col-1, state)).is_empty():
            if (row-1, col-1) in returnValidMovesForFigure(row, col, stackInput, state):
                print("prazno polje je validno")
                return True
            else:
                print("prazno polje nije validno")
                return False
        elif not isPositionValidDst(state,(row-1,col-1)):
            return False
        #kolko se prenosi iz stacka(row,col) na stack u GL
        elif not StackCapacity(HowMuchFromStack(stackInput,(row,col), state),(row-1,col-1), state):
            return False
        #za hsrc i hdst
        elif not isHeightValid(row-1,col-1, stackInput, state):
            return False    
        else:
            return True
        
    elif moveInput=="DL":
        #za player sign i figurica da se poklope
        if not isSignCorrect(row, col, stackInput, state):
            print(colored("You can't play with this figure, try again!", 'red', attrs=['bold']))
            return False
        elif not isPositionInMatrix((row+1,col-1),state.dimension):
            print(colored("Destination out of bounds, try again!", 'red', attrs=['bold']))
            return False
        elif (coorToStack(row+1,col-1, state)).is_empty():
            if (row+1, col-1) in returnValidMovesForFigure(row, col, stackInput, state):
                print("prazno polje je validno")              
                return True
        elif not isPositionValidDst(state,(row+1,col-1)):
            return False
        #kolko se prenosi iz stacka(row,col) na stack u GD
        elif not StackCapacity(HowMuchFromStack(stackInput,(row,col), state),(row+1,col-1), state):
            return False
        elif not isHeightValid(row+1,col-1, stackInput, state):
            return False
        else:
            return True
        
    elif moveInput=="GD":
        #za player sign i figurica da se poklope
        if not isSignCorrect(row, col, stackInput, state):
            print(colored("You can't play with this figure, try again!", 'red', attrs=['bold']))
            return False
        elif not isPositionInMatrix((row-1,col+1),state.dimension):
            print(colored("Destination out of bounds, try again!", 'red', attrs=['bold']))
            return False
        elif (coorToStack(row-1,col+1, state)).is_empty():
            if (row-1, col+1) in returnValidMovesForFigure(row, col, stackInput, state):
                print("prazno polje je validno")
                return True
        elif not isPositionValidDst(state,(row-1,col+1)):
            return False
    #kolko se prenosi iz stacka(row,col) na stack u DL
        elif not StackCapacity(HowMuchFromStack(stackInput,(row,col), state),(row-1,col+1), state):
            return False
        elif not isHeightValid(row-1,col+1, stackInput, state):
            return False   
        else:
            return True
        
    elif moveInput=="DD":
         #za player sign i figurica da se poklope
        if not isSignCorrect(row, col, stackInput, state):
            print(colored("You can't play with this figure, try again!", 'red', attrs=['bold']))
            return False
        elif not isPositionInMatrix((row+1,col+1),state.dimension):
            print(colored("Destination out of bounds, try again!", 'red', attrs=['bold']))
            return False
        elif (coorToStack(row+1,col+1, state)).is_empty():
            if (row+1, col+1) in returnValidMovesForFigure(row, col, stackInput, state):
                print("prazno polje je validno")
                return True
        elif not isPositionValidDst(state,(row+1,col+1)):
            print("position not correct")
            return False
    #kolko se prenosi iz stacka(row,col) na stack u GD
        elif not StackCapacity(HowMuchFromStack(stackInput,(row,col), state),(row+1,col+1), state):
            print("stack not correct")
            return False
        elif not isHeightValid(row+1,col+1, stackInput, state):
            print("height not correct")
            return False
        else:
            return True


#DRUGA FAZA PROVERE VALJANOSTI

def makeStringForMove(position : tuple, prevPosition : tuple):
    difference : tuple = (position[0] - prevPosition[0], position[1] - prevPosition[1])
    if difference == (-1, -1) :
        return "GL"
    elif difference == (-1, 1) :
        return "GD"
    elif difference == (1, 1) :
        return "DD"
    elif difference == (1, -1) :
        return "DL"
#vraca sve moguce poteze za igraca sa tim znakom za trenutno stanje, plus koliko se sklanja sa steka i od koje pozicje se sklanja
#jer nam treba za funkciju play valid turn instantly    
def returnAllValidMovesForSing(state : GameState, sign : str) :
    allValidMoves = []
    for stack in state.stekovi:
        for positionInStack in range(stack.stackLen()):
            if(stack.array[positionInStack] == sign):
                positionFrom = stackToCoor(stack, state)
                coordinatesForMoves = returnValidMovesForFigure(positionFrom[0], positionFrom[1], positionInStack, state)
                if coordinatesForMoves == []:
                    continue
                #print(coordinatesForMoves)
                resultStrings = [makeStringForMove(coordinatesForMove, positionFrom) for coordinatesForMove in coordinatesForMoves]
                allValidMoves+=[(positionFrom, resultString, positionInStack) for resultString in resultStrings]
    return allValidMoves

#za minmax nam trebaju sva moguca narednja stanja
def returnAllPossibleNextStates(state : GameState) :
    # moves = []
    opponentSign = "O" if state.currentTurn == "X" else "X"
    moves = returnAllValidMovesForSing(state, state.currentTurn)

    possibleNextStates = []

    for i in range(0, len(moves)):
        nextState = playValidTurnInstantly(state, moves[i])
        possibleNextStates.append(nextState)
    
    return possibleNextStates

#na osnovu poteza se vrati novo stanje
def playValidTurnInstantly(state: GameState, move: tuple):

    #print(move)
    newState = copy.deepcopy(state)
    #move[0] je pozocija odakle se prenosi, [1] gde se prenosi, [2] od koje pozicje u steku, to se vidi u funkciji retunAllValidMovesForSign
    transferFromStack(move[0], move[2], move[1], newState)
    pointsUpdate(state)
    #newState.currentTurn = "O" if state.currentTurn == "X" else "X"

    return newState

        
#jos funkcija za sva moguca stanja igre

def numberOfNeighbours(position : (int, int), state : GameState):
    relative_positions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    neighbours = 0
    for i in relative_positions:
        if isPositionInMatrix((position + i[0], position + i[1]), state.dimension):
            neighbours += 1

    return neighbours


def returnValidMovesForFigure(row, col, stackInput, state):
    dim=state.dimension
    stekovi=state.stekovi
    #za svako neprazno mod isMoveValid
    moveIndexes=[(row-1, col-1), (row+1, col-1), (row-1, col+1), (row+1, col+1)]
    validMovesArray=[]
    moveEmptyIndexes=[]
    arrayOfClosestNonEmptyIndexes=[]
    for move in moveIndexes:
        if not isPositionInMatrix((move[0], move[1]),state.dimension):  #indeks van matrice
            continue
        elif coorToStack(move[0], move[1], state).is_empty():
            moveEmptyIndexes.append(move)
            continue 
        elif not isPositionValidDst(state,(move[0], move[1])):
            continue
        #kolko se prenosi iz stacka(row,col) na stack u DL
        elif not StackCapacity(HowMuchFromStack(stackInput,(move[0], move[1]), state),(move[0], move[1]), state):
            continue
        elif not isHeightValid(move[0], move[1], stackInput, state):
            continue
        validMovesArray.append(move)
    print('Empty indexes', moveEmptyIndexes)
    if len(moveEmptyIndexes)==numberOfNeighbours: #ako su sva polja susedna prazna
        if(stackInput != 0) :  #PRAVILO IGRE
            return []
        validMovesArray = movesToNonEmptyStack((row, col), state)
        #print('validMovesArray',validMovesArray)
        #andrijana nadje indekse na koje moze da ide i to stavlja u validMovesArray
    return validMovesArray

def movesToNonEmptyStack(startPosition : (int, int), state : GameState):
    relative_positions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    startingPositions = [startPosition]
    for i in range(len(relative_positions)):
        if isPositionInMatrix((startPosition[0] + relative_positions[i][0], startPosition[1] + relative_positions[i][1]), state.dimension):
            startingPositions.append((startPosition[0] + relative_positions[i][0], startPosition[1] + relative_positions[i][1]))

    pathLengths = []
    for position in startingPositions :
        minLen = 10000
        for stack in state.stekovi:
            if (stack.stackLen() == 0):
                continue    
            position = stackToCoor(stack, state)
            minLen = min(minLen, max(abs(startPosition[0] - position[0]), abs(startPosition[1] - position[1])))
        pathLengths.append(minLen)
    
    return [startingPositions[i] for i in range(1, len(pathLengths)) if pathLengths[i] == pathLengths[0] - 1]


def allValidStacks( state, row, col, stackInput):
    dim=state.dimension
    min=float('inf')
    result=[]
    result=[]
    for stek in state.stekovi:
        rowDest=stackToCoor(stek, state)[0]
        colDest=stackToCoor(stek, state)[1]
        #print([rowDest, colDest])
        if not coorToStack(rowDest, colDest, state).is_empty() and not (rowDest==row and colDest==col) :#razlicit od posmatranog i nije prazan,
            #provera validnosti
            if not StackCapacity(HowMuchFromStack(stackInput,(row,col), state),(rowDest,colDest), state):
                continue
            #za hsrc i hdst
            elif not isHeightValid(rowDest,colDest, stackInput, state):
                continue
            #print("ispunjava sve uslove")
            result.append((rowDest,colDest))

    #print(result)
    return result


def validMovesToNonEmptyStacks(arrayOfClosestNonEmptyIndexes : list, startPosition : (int, int), state : GameState) :
    minumumDistancePositions = [(startPosition, 10000)]
    distances = []
    noPathToThatStack = 0
    #print(arrayOfClosestNonEmptyIndexes)
    for currentStackIndex in arrayOfClosestNonEmptyIndexes :
        relative_positions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        noPathToThatStack = 0
        for dx, dy in relative_positions:
            new_position = (startPosition[0] + dx, startPosition[1] + dy)
            if isPositionInMatrix(new_position, state.dimension):
                #print(shortestPathBetweenPositions(state, new_position, currentStackIndex))
                x = shortestPathBetweenPositions(state, new_position, currentStackIndex)
                if (x > -1):
                    distance = x + 1
                    distances.append((new_position, distance))
                    #print("ovo ja sad proveravam")
                    #print((currentStackIndex[0], currentStackIndex[1]))
                    #print((new_position, distance))
                else:
                    noPathToThatStack+=1
        if (noPathToThatStack == 4):
            continue
        sortedDistances = sorted(distances, key=lambda x: x[1])
        if sortedDistances[0][1] <= minumumDistancePositions[0][1]:
            minumumDistancePositions.clear()
            for e in sortedDistances :
                if (e[1] == sortedDistances[0][1]) :
                    minumumDistancePositions.append(e)
    print(minumumDistancePositions)

    if (minumumDistancePositions == [(startPosition, 10000)]):
        return []

    return [item[0] for item in minumumDistancePositions]


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


#IZVRSENJE POTEZA



def transferFromStack(position : tuple, stackInput, moveInput, state):
     stekovi=state.stekovi
     dim=state.dimension
     row = position[0] #slovo
     col = position[1] #broj
     positionNew=newPostionCalc(position, moveInput)
     rowNew=positionNew[0]
     colNew=positionNew[1]
     transfer=[]
     x = int(dim/2)
     y = col + 2
     yNew=colNew+2
    
     for i in range (HowMuchFromStack(stackInput, position, state)):
           transfer.append(stekovi[(int)(((row)*x)+y//2 - 1)].pop())
     for i in range (1, len(transfer)+1):

        stekovi[int(((rowNew)*x)+yNew//2 - 1)].push(transfer[-i])


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

   
    if state.currentTurn == "X":
        print(colored(f'\nPotez {state.currentTurn}:', 'magenta', attrs=['bold']))
        while(True):
        
            rowInput = getValidCharToIntInput(0, state.dimension, "row (A,B,C...)")
            colInput = getValidIntInput(0, state.dimension, "column (1,2,3...)")

            if not isPositionValidSrc(state,(rowInput, colInput)):
                print(colored("There is no stack here or it is empty, try again!", 'red', attrs=['bold']))
                continue
            
            stackInput=getValidStackInput(0,8,"stack (0,1,2..)")   #0 do 7

            if not isStackPosValid(stackInput,(rowInput, colInput),state):
                print(colored("There are not enough figures on a stack, try again!", 'red', attrs=['bold']))
                continue
            
            moveInput=getValidMoveInput()

            if not isMoveValid( (rowInput, colInput),moveInput,stackInput, state):
                print(colored("You can't place stack here, try again!", 'red', attrs=['bold']))
                continue
            
            else: break

        #push i pop 
        transferFromStack((rowInput, colInput), stackInput, moveInput, state)
        pointsUpdate(state)
        state.currentTurn = "O"
        gameIsOver()
        printWholeTable(state)


    elif state.currentTurn == "O":
        print(colored(f'\nPotez {state.currentTurn}:', 'magenta', attrs=['bold']))
        while(True):
        
            rowInput = getValidCharToIntInput(0, state.dimension, "row (A,B,C...)")
            colInput = getValidIntInput(0, state.dimension, "column (1,2,3...)")

            if not isPositionValidSrc(state,(rowInput, colInput)):
                print(colored("There is no stack here or it is empty, try again!", 'red', attrs=['bold']))
                continue
            
            stackInput=getValidStackInput(0,8,"stack (0,1,2..)")   #0 do 7
            
            if not isStackPosValid(stackInput, (rowInput, colInput),state):
                print(colored("There are not enough figures on a stack, try again!", 'red', attrs=['bold']))
                continue
            
            moveInput=getValidMoveInput()

            if not isMoveValid((rowInput, colInput),moveInput,stackInput, state):
                print(colored("You can't place stack here, try again!", 'red', attrs=['bold']))
                continue
            
            else: break

        #push i pop 
        transferFromStack((rowInput, colInput), stackInput, moveInput, state)
        pointsUpdate(state)
        state.currentTurn = "X"
        gameIsOver()
        printWholeTable(state)

    return state


