def printWelcomeText():
    print(colored("\n-----------------------------------\n", 'red', attrs=['bold']))
    print(colored(" Welcome to the BYTE GAME!", 'red', attrs=['bold']))
    print(colored("\n-----------------------------------\n", 'red', attrs=['bold']))

def getWhoPlaysFirst():
    whoPlaysFirst = ""
    while(whoPlaysFirst != "me" and whoPlaysFirst != "cpu"):
        whoPlaysFirst = input(colored("Who do you want to play first? Type me/cpu: ", 'cyan')).lower()
    return whoPlaysFirst

def getTableDimensions(maxRowDim:int, maxColDim:int):
    print(colored("\nLet's create the table!", 'yellow'))
    print(f' Tip: Recommended dimensions are 8x8\n Rule: Max dimensions are {maxRowDim}x{maxColDim}, Minimum dimensions are 5x5!\n')
    
    rows = -1
    cols = -1
    #promenjeno na <1 zbog testa, bilo <5
    while(rows < 1 or rows > maxRowDim):
        try:
            rows = int(input(colored("Enter the number of rows: ", 'cyan')))
        except:
            print(colored("Invalid input", 'red', attrs=['bold']))

    while(cols < 1 or cols > maxColDim):
        try:
            cols = int(input(colored("Enter the number of columns: ", 'cyan')))
        except:
            print(colored("Invalid input", 'red', attrs=['bold']))

    return (rows, cols)

def initializeEmptyMatrixState(rowDim:int, colDim:int):
    emptyMatrix = []
    for i in range (0, rowDim):
        emptyMatrix.append([])
        for j in range(0,colDim):
            emptyMatrix[i].append(" ")
    return emptyMatrix

def initializeGameState(rowDim:int, colDim:int, whoPlaysFirst:str):
    state:GameState = GameState()
    state.playerSign = "X" if whoPlaysFirst == "me" else "O"
    state.cpuSign = "X" if whoPlaysFirst == "cpu" else "O"
    state.currentTurn = "X"
    state.rowDim = rowDim
    state.colDim = colDim
    state.stateMatrix = initializeEmptyMatrixState(rowDim, colDim)
    
    return state

def intializeGame(maxRowDimension:int, maxColDimension:int):
    printWelcomeText()
    whoPlaysFirst = getWhoPlaysFirst()
    dimensions = getTableDimensions(maxRowDimension, maxColDimension)
    return initializeGameState(dimensions[0], dimensions[1], whoPlaysFirst)


#andrijana

def printNumbers(n):
    for i in range (0, n):
        if (i == 0):
            print("      ", end="")
        print(f"{i}      ", end="") 

# Ovo je zamisljeno da bude ceo red tipa . . . (razmak) . . . (razmak) X . . (razmak) . . . (razmak) . . . (razmak)
# Hardkodirano je da na neparno i stampa stek a na parno prazan red
# prvoStack nam je obican flag da l' da se crta stek ili razmak tj ako je prvoStack == True, onda se stack crta na i%2==0, ako je False onda se razmaci crtaju na i%2==0
def printRow(dim, prvoStack, stekRowCounter, stekcounter):
    str = ""
    step = 0
    if prvoStack:
        for i in range(dim):
            str += printStackRow(stek[stekcounter * 4 + step], stekRowCounter) if i % 2 == 0 else printEmptyRow() + "  "
            if i % 2 == 0:
                step+=1
    else:
        step = 0
        for i in range(dim):
            str += printEmptyRow() if i % 2 == 0 else printStackRow(stek[stekcounter * 4 + step], stekRowCounter) + "  "
            if i % 2 == 1:
                step+=1
    return str

def printStackRow(stek, row):
    return f"{stek[row * 3]} {stek[row*3 + 1]} {stek[row*3 + 2]} "

# Ovde stampam razmake
def printEmptyRow():
    return "      "  
    
def makeStack(n):
    flag = 0
    stek = []
    for i in range(0, n * 4):
        stek.append([])
    for i in range(0, n * 4):
        if flag == 0:
            stek[i] = ["X", ".", ".",".",".", ".",".",".","."]
        else:
            stek[i] = ["O", ".", ".",".",".",".",".",".","."]
        if i % 4 == 3:
            flag = not flag
    
    return stek
            
def generateLetters(n):
    start_char = ord('A')  # ASCII code for 'A'
    array_of_letters = [chr(start_char + i) for i in range(n)]
    return array_of_letters

printNumbers(8)
print()

row = ""
dimension = 8
rowNumber = 8*3
prvoStack = True
letters = generateLetters(8)
stekcounter=0
stekRowCounter=0
lettersCounter = 0
stek = makeStack(8)

for i in range(rowNumber):
    if i > 0 and i % 3 == 0:
        prvoStack = not prvoStack
    if i % 3 == 1:
        row+= f"{letters[lettersCounter]}   "
        lettersCounter+=1
    else:
        row+= "    "
    row += printRow(dimension, prvoStack, stekRowCounter, stekcounter)
    row += "\n"
    stekRowCounter+=1 
    if stekRowCounter % 3 == 0 :
        stekRowCounter = 0
        stekcounter+=1
    

print(row) 
