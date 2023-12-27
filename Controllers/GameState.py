from Interface.Stack import Stack
from typing import List
class GameState:
        def __init__(self) -> None:
                self.playerSign = ""
                self.cpuSign = ""
                self.currentTurn = ""
                self.dimension = 0
                self.stekovi: List[Stack] = []
                self.maxDimension = 16
                self.playerScore = 0
                self.cpuScore = 0
                self.matrix = [[]]
                #sign score dim turn