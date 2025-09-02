# Linear Equation Solver

A Python implementation of the Gaussian elimination algorithm for solving systems of linear equations using forward and backward substitution.

## Overview

This project provides a complete solution for solving systems of linear equations through matrix operations. The implementation uses Gaussian elimination with partial pivoting to transform a coefficient matrix into reduced row echelon form (RREF).

## Features

- **Matrix Operations**: Support for basic matrix operations including row addition, subtraction, multiplication, and division
- **Gaussian Elimination**: Forward elimination to create upper triangular form
- **Back Substitution**: Backward elimination to achieve reduced row echelon form
- **Partial Pivoting**: Automatic row swapping to handle zero diagonal elements
- **Flexible Input**: Accepts coefficient matrix and augmented vector separately

## Classes

### Board

Represents the augmented matrix system and provides matrix manipulation methods.

**Constructor:**
```python
Board(matrix: list[list[float]], aug_matrix: list[float])
```

**Parameters:**
- `matrix`: 2D list of coefficients from the system of equations
- `aug_matrix`: 1D list of constants from the right-hand side of equations

**Methods:**
- `get_value(cords)`: Get coefficient at specified coordinates
- `get_row(index)`: Get entire row at specified index
- `get_aug(index)`: Get augmented value at specified index
- `add_row()`: Add two rows together
- `subtract_row()`: Subtract one row from another
- `multiply_row_const()`: Multiply row by a constant
- `divide_row_const()`: Divide row by a constant

### Solver

Implements the Gaussian elimination algorithm.

**Methods:**
- `algorithmic_solve(state)`: Main solving method that performs complete Gaussian elimination
- `get_starting_point(state)`: Find the next pivot point for forward elimination
- `get_backward_starting_point(state)`: Find the next pivot point for backward elimination
- `implicit_check(state)`: Handle row swapping when pivot element is zero

## Usage Example

```python
# System of equations:
# 2x + 3y + 4z = 20
# 5x + 5y + 5z = 30
# 4x + 3y + 2z = 16

# Define coefficient matrix
matrix = [[2, 3, 4], [5, 5, 5], [4, 3, 2]]

# Define augmented vector
aug_matrix = [20, 30, 16]

# Create board and solver
board = Board(matrix, aug_matrix)
solver = Solver()

# Solve the system
solution = solver.algorithmic_solve(board)

# Display result
print(solution)
```

## Algorithm Steps

1. **Forward Elimination:**
   - Find pivot element in current column
   - Swap rows if pivot is zero (partial pivoting)
   - Scale pivot row to make pivot element equal to 1
   - Eliminate all elements below pivot

2. **Backward Substitution:**
   - Starting from bottom-right, work backwards
   - Eliminate all elements above each pivot
   - Result is reduced row echelon form

## Input Format

The system of linear equations must be converted to matrix form:

**Example:**
```
2x + 3y + 4z = 20
5x + 5y + 5z = 30
4x + 3y + 2z = 16
```

**Becomes:**
```python
matrix = [[2, 3, 4], [5, 5, 5], [4, 3, 2]]
aug_matrix = [20, 30, 16]
```

## Error Handling

- Validates matrix dimensions match augmented vector length
- Automatically converts integer inputs to floating-point values
- Handles coordinate validation for matrix access
- Implements row swapping for zero pivot elements

## Requirements

- Python 3.x
- No external dependencies required

## Limitations

- Does not handle systems with no solution or infinite solutions explicitly
- Assumes square coefficient matrix
- Limited error checking for singular matrices

## Mathematical Background

This implementation uses Gaussian elimination, a fundamental algorithm in linear algebra for solving systems of linear equations. The method systematically eliminates variables to reduce the system to a form where solutions can be easily determined.

The algorithm achieves O(n³) time complexity for an n×n system, making it efficient for moderately-sized systems of equations.