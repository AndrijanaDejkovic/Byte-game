class Stack:
    def __init__(self):
        self.array = []
        self.dimension = 9

#dodavanje na stek
    def push(self, value):
        if len(self.array) < self.dimension:
            self.array.append(value)
            #print(f"Pushed {value} onto the stack")
        else:
            print("Stack overflow, cannot push onto a full stack")

#brisanje sa steka
    def pop(self):
        if self.is_empty():
            print("Stack underflow, cannot pop from an empty stack")
            return None
        else:
            popped_value = self.array.pop()
            print(f"Popped {popped_value} from the stack")
            return popped_value

    def is_empty(self):
        return len(self.array) == 0
    

#vidi vrh steka
    def peek(self):
        if self.is_empty():
            print("Cannot peek, the stack is empty")
            return None
        else:
            return self.array[-1]
        
#inicijalno stanje steka
    def makeBeginingStack(self, element):
        self.push(element)


