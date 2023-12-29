import copy
from Controllers.GameState import GameState
from Controllers.TurnController import returnAllValidMovesForSign
def evaluateState(state:GameState, whoPlayed=None, whoIsOpponent = None):
    score = 0
    multiplier = -1 if state.currentTurn == "X" else 1
    opponentSign = "O" if state.currentTurn == "X" else "X"
    score+=state.playerScore * 1000 - state.cpuScore * 1000
    score+= len(returnAllValidMovesForSign(state, state.currentTurn)) - len(returnAllValidMovesForSign(state, opponentSign))
    #ukoliko sledeće potencijalno stanje vodi ka poentiranju suprotnog igrača nikako ne izvršiti taj potez
    #ukoliko postoje potezi koji ne utiču direktno na protivnika -- safe moves -- oni se poslednji igraju -- rangiraju se manjom vednosšću(nikolino) --
    # npr kad se na jednom delu table nalazi samo jedan stek čijim pomeranje ne utičemo na figure na drugoj polovini table
    # ukoliko vode ka ivici -- smanjuju mogućnost za sledeći potez --izbegavati (nikola) ima smisla i za nas jer nema gde da pobegne - "mora da odigra ako postoji valjani potez čak i sebi na štetu"
    #stvaranje prepreke -- visinski neogovarajuci -- npr stek od 7 i oko njega svi stekovi od 6 a na vrhu suparnička figurica koju ne može da pomeri
    #stvaranje prepreke protivniku -- ako postavljaš figuru u stek na određeno polje, pripazi da ta postavka ne olakšava protivniku postizanje bodova u narednim potezima. Recimo, postaviš svoju figuru na polje koje će stvoriti situaciju 
    #u kojoj će protivnik imati težak zadatak da postigne bodove iz svojih figura(chatgpt)
    #Balansiranje između napada i obrane --- da nam prednost ima nepobeda suparnika u odnosu na našu pobedu 0 > 1

    return score * multiplier