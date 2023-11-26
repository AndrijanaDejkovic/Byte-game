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
    
