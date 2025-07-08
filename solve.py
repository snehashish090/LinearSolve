import math
import copy

class Subtraction:

    def __init__(self, var1, var2):
        self.var1 = var1
        self.var2 = var2

    def __str__(self):
        return f"({self.var1} - {self.var2})"
    
    def __repr__(self):
        return f"({self.var1} - {self.var2})"

class Addition:

    def __init__(self, var1, var2):
        self.var1 = var1
        self.var2 = var2

    def __str__(self):
        return f"({self.var1} + {self.var2})"
    
    def __repr__(self):
        return f"({self.var1} + {self.var2})"

class MultiplyConst:
    def __init__(self, var1, const):
        self.var1 = var1
        self.const = const

    def __str__(self):
        return f"({self.var1} * {self.const})"
    
    def __repr__(self):
        return f"({self.var1} * {self.const})"

class Board:
    """
    Given a system of linear equations:

    2x + 3y + 4z = 20
    5x + 5y + 5z = 30
    4x + 3y + 2z = 16

    matrix = [
        [2, 3, 4],
        [5, 5, 5],
        [4, 3, 2]
    ]

    aug_matrix = [20, 30, 16]
    
    """
    matrix:list 
    aug_matrix:list


    def __init__(self, matrix, aug_matrix):

        if len(matrix) != len(aug_matrix):
            raise Exception("Error: matrix shape is incorrect")
        self.matrix = matrix
        self.aug_matrix = aug_matrix
        self.rows = len(self.matrix)
        self.columns = len(self.matrix[0]) if self.rows > 0 else 0

    def get_value(self, cords:tuple[int]):
        if len(cords) != 2:
            raise Exception("Co-ordinates need to be in the form of (row, column)")
        return self.matrix[cords[0], cords[1]]
    
    def get_row(self, index):
        return self.matrix[index]
    
    def get_aug(self, index):
        return self.aug_matrix[index]
    
    def add_row(self, row1:list[int], aug_row1, row2:list[int], aug_row2):

        resultant_row = []

        for i in range(0, len(row2)):
            resultant_row.append(row1[i]+row2[i])

        resultant_aug_row = aug_row1 + aug_row2

        return resultant_row, resultant_aug_row
    
    def subtract_row(self, row1:list[int], aug_row1, row2:list[int], aug_row2):

        resultant_row = []
        
        for i in range(0, len(row2)):
            resultant_row.append(row1[i] - row2[i])

        resultant_aug_row = aug_row1 - aug_row2

        return resultant_row, resultant_aug_row
    
    def multiply_row_const(self, row:list[int], aug:int, const:int):
        
        new_aug = aug*const
        resultant = []
        for i in row:
            resultant.append(int(i*const))
        return resultant, new_aug
    
    def divide_row_const(self, row:list[int], aug:int, const:int):

        new_aug = aug/const
        resultant = []
        for i in row:
            resultant.append(i/const)
        return resultant, new_aug
    
    def LCM(self, row1:list, row2:list):

        max_index = max(
            self.matrix.index(row1),
            self.matrix.index(row2)
        )
        
        row1 = [int(i) for i in row1]
        row2 = [int(i) for i in row2]

        factors = (1,1)
        least_lcm = math.lcm(row1[0], row2[0])
        if least_lcm != 0:
            factors = (least_lcm / row1[0], least_lcm/row2[0] )

        for i in range(0, max_index):

            if math.lcm(row1[i], row2[i]) == 0:
                continue
            if math.lcm(row1[i], row2[i]) < least_lcm:
                least_lcm = math.lcm(row1[i], row2[i])
                factors = (least_lcm / row1[i], least_lcm/row2[i])

        return factors

    def number_of_zeros(self, row:list[int]):
        count = 0
        for i in row:
            if i == 0:
                count += 1
        return count
    
    def __str__(self):

        string = ""

        for i in self.matrix:
            for j in i:
                string += str(j) + " "
            string += "| "+ str(self.aug_matrix[self.matrix.index(i)]) + "\n"

        return string
    
    def __repr__(self):
        string = ""

        for i in self.matrix:
            for j in i:
                string += str(j) + " "
            string += "| "+ str(self.aug_matrix[self.matrix.index(i)]) + "\n"

        return string

class Action:

    def __init__(self, action, input_state:Board, output_state:Board):
        self.action = action
        self.input_state = input_state
        self.output_state = output_state

    def __str__(self):
        return str(self.action)
    
    def __repr__(self):
        return str(self.action)
    
class Solver:

    actions:list
    states:list[Board]

    def __init__(self, state:Board):
        self.actions = []
        self.initial_state = state
        self.states = [state]

    def indexes_to_zero(self, state:Board):

        x = state.rows
        y = state.columns

        to_be_zero = []
        already_zero = []

        for col in range(0, y-1):
            for row in range(1+col, x):
                if state.matrix[row][col] != 0:
                    to_be_zero.append((row, col))
                else:
                    already_zero.append((row,col))

        return (to_be_zero, already_zero)
    
    def row_to_solve(self, state:Board):
        indexes_to_be_filled = self.indexes_to_zero(state)[0]
        max_row = 0

        for i in indexes_to_be_filled:
            if i[0] > max_row:
                max_row = i[0]

        return max_row
    
    def possible_actions(self, state:Board):

        actions = []

        action = None

        row = state.get_row(self.row_to_solve(state))
        aug = state.get_aug(self.row_to_solve(state))

        for i in state.matrix:

            _state = copy.deepcopy(state)

            if i != row:

                _aug = state.get_aug(state.matrix.index(i))
                factors = state.LCM(row, i)

                _row,_aug = state.multiply_row_const(row, aug, factors[0])
                _i, _aug_ = state.multiply_row_const(i,_aug, factors[1])

                addition = state.add_row(_row, _aug, _i, _aug_)
                subtraction = state.subtract_row(_row, _aug, _i, _aug_)
                index=_state.matrix.index(row)

                if _state.number_of_zeros(addition[0]) > _state.number_of_zeros(subtraction[0]):
                    action = Addition(MultiplyConst(row, factors[0]), MultiplyConst(row, factors[0]))
                    _state.matrix[index] = addition[0]
                    _state.aug_matrix[index] = addition[1]
                else:
                    action = Addition(MultiplyConst(row, factors[0]), MultiplyConst(row, factors[0]))
                    _state.matrix[index] = subtraction[0]
                    _state.aug_matrix[index] = subtraction[1]

                actions.append(Action(action, state, _state))

        return actions
    
board = Board(
    [
        [2, 3, 4],
        [5, 5, 5],
        [4, 3, 2]
    ], [20, 30, 16]
)

sol = Solver(board)

states = [board]

for i in range(5):
    pop = states[-1]
    print(pop)
    states.remove(pop)

    for i in sol.possible_actions(pop):
        print(i)
        states.append(i.output_state)


