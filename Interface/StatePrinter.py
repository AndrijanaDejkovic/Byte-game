from Interface.Stack import Stack
from Controllers.GameState import GameState
from ImportedScripts.TextColorizer.ColorizeText import colored
def printNumbers(n):
    for i in range (1, n+1):
        if (i == 1):
            print("", end="")
        print(f"{i:7}", end="")

# Ovo je zamisljeno da bude ceo red tipa . . . (razmak) . . . (razmak) X . . (razmak) . . . (razmak) . . . (razmak)
# Hardkodirano je da na neparno i stampa stek a na parno prazan red
# prvoStack nam je obican flag da l' da se crta stek ili razmak tj ako je prvoStack == True, onda se stack crta na i%2==0, ako je False onda se razmaci crtaju na i%2==0
def printRow(dim, prvoStack, stekRowCounter, stekcounter, state):
    str = ""
    step = 0
    n = int(dim/2)
    if prvoStack:
        for i in range(dim):
            str += printStackRow(state.stekovi[stekcounter * n + step], stekRowCounter) if i % 2 == 0 else printEmptyRow() + "  "
            if i % 2 == 0:
                step+=1
    else:
        step = 0
        for i in range(dim):
            str += printEmptyRow() if i % 2 == 0 else printStackRow(state.stekovi[stekcounter * n + step], stekRowCounter) + "  "
            if i % 2 == 1:
                step+=1
    return str

def printStackRow(stek, row):
    a, b, c = ".", ".", "."  # Initialize variables with default values

    # Adjust row based on conditions
    if row == 2:
        row = 0
    elif row == 0:
        row = 2

    #print(len(stek.array))

    if len(stek.array) > (row * 3 + 2):
        a = stek.array[row * 3 + 2]

    if len(stek.array) > (row * 3 + 1):
        b = stek.array[row * 3 + 1]

    if len(stek.array) > (row * 3):
        c = stek.array[row * 3]

    return f"{c} {b} {a} "
    #stampa se drugim redosledom, znaci elementi od 1-9. pozicije idu ovako
    #987
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
    
    
def printWholeTable(state:GameState) -> None:
    
    printNumbers(state.dimension)
    print()
    
    row = ""
    dimension = state.dimension
    rowNumber = dimension*3
    prvoStack = True
    letters = generateLetters(dimension)
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
        row += printRow(dimension, prvoStack, stekRowCounter, stekcounter, state)
        row += "\n"
        stekRowCounter+=1 
        if stekRowCounter % 3 == 0 :
            stekRowCounter = 0
            stekcounter+=1
    print(row)
    print(f"{state.playerSign} : {state.playerScore}")
    print(f"{state.cpuSign} : {state.cpuScore}")