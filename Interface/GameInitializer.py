from Stack import Stack
def printWelcomeText():
    print(colored("\n-----------------------------------\n", 'red', attrs=['bold']))
    print(colored(" Welcome to the BYTE GAME!", 'red', attrs=['bold']))
    print(colored("\n-----------------------------------\n", 'red', attrs=['bold']))

def getWhoPlaysFirst():
    whoPlaysFirst = ""
    while(whoPlaysFirst != "me" and whoPlaysFirst != "cpu"):
        whoPlaysFirst = input(colored("Who do you want to play first? Type me/cpu: ", 'cyan')).lower()
    return whoPlaysFirst

def getTableDimensions(maxDim:int):
    print(colored("\nLet's create the table!", 'yellow'))
    print(f' Tip: Recommended dimensions are 8x8\n Rule: Max dimensions are {maxDim}x{maxDim}, Minimum dimensions are 5x5!\n')
    
    dim = -1
    #parno, maks 16, valjda ne moze manje od 4 zbog onog da treba prva dva steka na pocetku da su prazna, a i ovaj uslov da broj figurica mora da je deljiv sa 8
    while(dim < 4 or dim > maxDim or dim % 2 != 0 or ((int(dim/2) * (n-2)) % 8 != 0)):
        try:
            dim = int(input(colored("Enter the number of rows: ", 'cyan')))
        except:
            print(colored("Invalid input", 'red', attrs=['bold']))

    return (dim)

def initializeEmptyMatrixState(rowDim:int, colDim:int):
    emptyMatrix = []
    for i in range (0, rowDim):
        emptyMatrix.append([])
        for j in range(0,colDim):
            emptyMatrix[i].append(" ")
    return emptyMatrix

def initializeGameState(Dim:int, whoPlaysFirst:str):
    state:GameState = GameState()
    state.playerSign = "X" if whoPlaysFirst == "me" else "O"
    state.cpuSign = "X" if whoPlaysFirst == "cpu" else "O"
    state.currentTurn = "X"
    state.rowDim = Dim
    state.colDim = Dim
    state.stateMatrix = initializeEmptyMatrixState(rowDim, colDim)
    
    return state

def intializeGame(maxRowDimension:int, maxColDimension:int):
    printWelcomeText()
    whoPlaysFirst = getWhoPlaysFirst()
    dimensions = getTableDimensions(maxRowDimension, maxColDimension)
    return initializeGameState(dimensions, whoPlaysFirst)


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
    n = int(dim/2)
    if prvoStack:
        for i in range(dim):
            str += printStackRow(stekovi[stekcounter * n + step], stekRowCounter) if i % 2 == 0 else printEmptyRow() + "  "
            if i % 2 == 0:
                step+=1
    else:
        step = 0
        for i in range(dim):
            str += printEmptyRow() if i % 2 == 0 else printStackRow(stekovi[stekcounter * n + step], stekRowCounter) + "  "
            if i % 2 == 1:
                step+=1
    return str

def printStackRow(stek, row):
    return f"{stek.array[row * 3 + 2]} {stek.array[row * 3 + 1]} {stek.array[row * 3]} "
    #stampa se drugim redosledom, znaci elementi od 1-9. pozicije idu ovako
    #321
    #654
    #321
    #ovako izgleda stek na tabli

# Ovde stampam razmake
def printEmptyRow():
    return "      "  
            
def generateLetters(n):
    start_char = ord('A')  # ASCII code for 'A'
    array_of_letters = [chr(start_char + i) for i in range(n)]
    return array_of_letters
    
def makeStacks(n):
    flag = 0
    stekovi = []
    dim = int(n /2)
        
    for i in range(0, n * dim):
        stek = Stack()
        stekovi.append(stek)
        if i < dim or i >= (n-1)* dim :
             stek.makeBeginingStack(".")
        
        elif flag == 0:
            stek.makeBeginingStack("X")
        else :
            stek.makeBeginingStack("Y")
        if i % 4 == 3:
            flag = not flag
    
    return stekovi
    
def printWholeTable(n, stekovi):
  
    printNumbers(n)
    print()
    
    row = ""
    dimension = n
    rowNumber = n*3
    prvoStack = True
    letters = generateLetters(n)
    stekcounter=0
    stekRowCounter=0
    lettersCounter = 0
    
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
    

n = int(input("Unesite zeljenu velicinu polja: "))
stekovi = makeStacks(n)
printWholeTable(n, stekovi)

