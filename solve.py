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

        for r_idx in range(len(matrix)):
            for c_idx in range(len(matrix[r_idx])):
                matrix[r_idx][c_idx] = float(matrix[r_idx][c_idx])
                aug_matrix[r_idx] = float(aug_matrix[r_idx])

        if len(matrix) != len(aug_matrix):
            raise Exception("Error: matrix shape is incorrect")
            
        self.matrix = matrix
        self.aug_matrix = aug_matrix
        self.rows = len(self.matrix)
        self.columns = len(self.matrix[0]) if self.rows > 0 else 0

    def get_value(self, cords):
        if len(cords) != 2:
            raise Exception("Co-ordinates need to be in the form of (row, column)")
        return self.matrix[cords[0]][cords[1]]
    
    def get_row(self, index):
        return self.matrix[index]
    
    def get_aug(self, index):
        return self.aug_matrix[index]
    
    def add_row(self, row1, aug_row1, row2, aug_row2):

        resultant_row = []

        for i in range(0, len(row2)):
            resultant_row.append(row1[i]+row2[i])

        resultant_aug_row = aug_row1 + aug_row2

        return resultant_row, resultant_aug_row
    
    def subtract_row(self, row1, aug_row1, row2, aug_row2):

        resultant_row = []
        
        for i in range(0, len(row2)):
            resultant_row.append(row1[i] - row2[i])

        resultant_aug_row = aug_row1 - aug_row2

        return resultant_row, resultant_aug_row
    
    def multiply_row_const(self, row, aug, const):
        
        new_aug = aug*const
        resultant = []
        for i in row:
            resultant.append(i*const)
        return resultant, new_aug
    
    def divide_row_const(self, row, aug, const):

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
        
        row1 = [i for i in row1]
        row2 = [i for i in row2]

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

    def number_of_zeros(self, row):
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

    def __init__(self):
        self.actions = []

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
    
    
    def get_starting_point(self, state:Board):

        flags = [False, False]
        starting_point = (0,0)

        while starting_point[0] <= state.rows - 1 and starting_point[1] <= state.columns - 1:
            if starting_point[0] == state.rows - 1 and starting_point[1] == state.columns - 1:
                return -1 
            
            if state.get_value(starting_point) != 1:
                flags[0] = True
            
            for i in range(starting_point[0] + 1, state.rows):
                if state.get_value((i, starting_point[1])) != 0:
                    flags[1] = True

            if True not in flags:
                starting_point = (starting_point[0] + 1, starting_point[1] + 1)
            else:
                return starting_point
    
    def implicit_check(self, state:Board):
        point = self.get_starting_point(state)
        if point == -1: # Handle case where get_starting_point returns -1
            return None

        if state.get_value(point) == 0:
            for i in range(point[0]+1, state.rows):
                if state.get_value((i, point[1])) != 0:
                    # Perform row swap for both matrix and augmented matrix
                    temp_matrix_row = state.matrix[point[0]]
                    temp_aug_row = state.aug_matrix[point[0]]

                    state.matrix[point[0]] = state.matrix[i]
                    state.aug_matrix[point[0]] = state.aug_matrix[i]

                    state.matrix[i] = temp_matrix_row
                    state.aug_matrix[i] = temp_aug_row
                    return state # Return the modified state
        return None # Return None if no swap was needed or performed

    def get_backward_starting_point(self, state:Board):

        flags = [False, False]
        starting_point = (state.rows - 1, state.columns-1)

        while starting_point[0] <= state.rows - 1 and starting_point[1] <= state.columns - 1:
            if starting_point == (0,0):
                return -1 
            
            if state.get_value(starting_point) != 1:
                flags[0] = True
        
            for i in range(starting_point[0] - 1, -1, -1):
                if state.get_value((i, starting_point[1])) != 0:
                    flags[1] = True

            if True not in flags:
                starting_point = (starting_point[0] - 1, starting_point[1] - 1)
            else:
                return starting_point
            
    def algorithmic_solve(self, state:Board):

        while self.get_starting_point(state) != -1:
            point = self.get_starting_point(state)

            imp_check = self.implicit_check(state)
            if imp_check is not None:
                state = imp_check

            if state.get_value(point) != 0:
                if state.get_value(point) != 1:
                    row = state.matrix[point[0]]
                    aug_row = state.aug_matrix[point[0]]
                    transformed_row = state.divide_row_const(row, aug_row, state.get_value(point))
                    state.matrix[point[0]] = transformed_row[0]
                    state.aug_matrix[point[0]] = transformed_row[1]

                for i in range(point[0] + 1, state.rows):
                    row = state.matrix[point[0]]
                    aug_row = state.aug_matrix[point[0]]

                    coef = state.get_value((i, point[1]))
                    new_starting_row = state.multiply_row_const(row, aug_row, coef)
                    new_i_row = state.subtract_row(
                                                state.matrix[i],
                                                state.aug_matrix[i],
                                                new_starting_row[0],
                                                new_starting_row[1]
                                                )
                    
                    state.matrix[i] = new_i_row[0]
                    state.aug_matrix[i] = new_i_row[1]

        while self.get_backward_starting_point(state) != -1:
            point = self.get_backward_starting_point(state)
            if state.get_value(point) != 0:
                if state.get_value(point) != 1:
                    row = state.matrix[point[0]]
                    aug_row = state.aug_matrix[point[0]]
                    transformed_row = state.divide_row_const(row, aug_row, state.get_value(point))
                    state.matrix[point[0]] = transformed_row[0]
                    state.aug_matrix[point[0]] = transformed_row[1]
                for i in range(point[0] - 1, -1, -1):
                    row = state.matrix[point[0]]
                    aug_row = state.aug_matrix[point[0]]
                    coef = state.get_value((i, point[1]))
                    new_starting_row = state.multiply_row_const(row, aug_row, coef)
                    new_i_row = state.subtract_row(
                                                state.matrix[i],
                                                state.aug_matrix[i],
                                                new_starting_row[0],
                                                new_starting_row[1]
                                                )
                    state.matrix[i] = new_i_row[0]
                    state.aug_matrix[i] = new_i_row[1] 
        return state
        