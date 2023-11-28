class Stack:
    def __init__(self):
        self.array = []
        self.dimension = 9

    def push(self, value):
        if len(self.array) < self.dimension:
            self.array.append(value)
            print(f"Pushed {value} onto the stack")
        else:
            print("Stack overflow, cannot push onto a full stack")

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

    def peek(self):
        if self.is_empty():
            print("Cannot peek, the stack is empty")
            return None
        else:
            return self.array[-1]
    def makeBeginingStack(self, element):
        self.array = [".", ".", ".",".",".", ".",".",".",element]