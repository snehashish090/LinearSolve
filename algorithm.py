import math
import copy

class Board:
    matrix:list[list[float]]
    aug_matrix:list[float]

    def __init__(self, matrix:list[list[float]], aug_matrix:list[float]):
        """
        Parameters: 
            - matrix : 2-Dimensional Array of floating point values which
                      are corresponding the coefficients values from the equations
            - aug_matrix : The augment matrix for the system of linear euqation

        Given a system of linear equations:
        2x + 3y + 4z = 20 
        5x + 5y + 5z = 30
        4x + 3y + 2z = 16
        
        The equations have to be converted into the following format
        matrix = [[2, 3, 4],[5, 5, 5],[4, 3, 2]]
        aug_matrix = [20, 30, 16]   
    
        """
        # In the case that the given values in the arrays are integers,
        # those values will be converted into floating point values
        for r_idx in range(len(matrix)):
            for c_idx in range(len(matrix[r_idx])):
                matrix[r_idx][c_idx] = float(matrix[r_idx][c_idx])
                aug_matrix[r_idx] = float(aug_matrix[r_idx])

        # Checking if the augmented matrix is valid and corresponding to the main matrix
        if len(matrix) != len(aug_matrix):
            raise Exception("Error: matrix shape is incorrect")
            
        self.matrix = matrix
        self.aug_matrix = aug_matrix
        self.rows = len(self.matrix)
        self.columns = len(self.matrix[0]) if self.rows > 0 else 0

    def get_value(self, cords:tuple[int]):
        """
        Parameters:
            - cords: a set of coordinates in a 2-dimensional plane eg: (x,y)
        Return:
            - Value of the coefficient at the set of coordinates in the matrix
        """
        if len(cords) != 2:
            raise Exception("Co-ordinates need to be in the form of (row, column)")
        return self.matrix[cords[0]][cords[1]]
    
    def get_row(self, index):
        """
        Parameters:
            - index: the index of the row that is to be fetched
        Return:
            - a floating point array of the row at the index passed
        """
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

class Solver:

    def __init__(self):
        pass
    
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
        