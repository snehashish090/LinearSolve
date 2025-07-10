import re
from typing import List, Tuple, Dict

def equations_to_matrix(equations: List[str]) -> Tuple[List[List[float]], List[float]]:
    """
    Convert a list of linear equations to augmented matrix form.
    
    Args:
        equations: List of strings representing linear equations like "2x + 3y - z = 5"
        
    Returns:
        Tuple of (coefficient_matrix, constants_vector)
        - coefficient_matrix: 2D list representing the coefficient matrix
        - constants_vector: List of constants from the right side of equations
    """
    if not equations:
        return [], []
    
    # Find all unique variables across all equations
    variables = set()
    for eq in equations:
        # Extract variable names (letters that appear before or after coefficients)
        vars_in_eq = re.findall(r'[a-zA-Z]+', eq.split('=')[0])
        variables.update(vars_in_eq)
    
    # Sort variables for consistent ordering
    variables = sorted(list(variables))
    var_count = len(variables)
    
    coefficient_matrix = []
    constants_vector = []
    
    for equation in equations:
        # Split equation into left and right sides
        left_side, right_side = equation.replace(' ', '').split('=')
        
        # Parse the constant (right side)
        constant = float(right_side)
        constants_vector.append(constant)
        
        # Initialize coefficient row
        coefficients = [0.0] * var_count
        
        # Parse left side for coefficients
        # Add '+' at the beginning if it doesn't start with '-'
        if not left_side.startswith('-'):
            left_side = '+' + left_side
        
        # Find all terms (coefficient + variable)
        terms = re.findall(r'[+-][^+-]*', left_side)
        
        for term in terms:
            term = term.strip()
            if not term:
                continue
                
            # Extract coefficient and variable
            # Handle cases like +x, -x, +2x, -3y, etc.
            match = re.match(r'([+-]?\d*\.?\d*)([a-zA-Z]+)', term)
            if match:
                coeff_str, var = match.groups()
                
                # Handle implicit coefficient of 1 or -1
                if coeff_str == '' or coeff_str == '+':
                    coeff = 1.0
                elif coeff_str == '-':
                    coeff = -1.0
                else:
                    coeff = float(coeff_str)
                
                # Find variable index and set coefficient
                if var in variables:
                    var_index = variables.index(var)
                    coefficients[var_index] = coeff
        
        coefficient_matrix.append(coefficients)
    
    return coefficient_matrix, constants_vector
