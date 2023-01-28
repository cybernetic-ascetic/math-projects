# -*- coding: utf-8 -*-
"""LinearSystemsSolver.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1R7MaUS7Sw9UVJytngWHzrTo5Q84G-q_2

#Libraries
"""

import math

"""#Rational Numbers"""

class Rational:

  def __init__(self, a, b=1):

    if b == 0:
      raise Exception("Undefined: denominator cannot be zero.")

    self.numerator = a
    self.denominator = b

    self.reduce()

  def __add__(self, other):

    if isinstance(other, Rational):

      new_numerator = (self.numerator * other.denominator) + (self.denominator * other.numerator)
      new_denominator = self.denominator * other.denominator

    elif isinstance(other, int):

      rational = self + Rational(other, 1)
      new_numerator = rational.numerator
      new_denominator = rational.denominator

    return Rational(new_numerator, new_denominator)

  def __eq__(self, other):

    flag = False

    if isinstance(other, Rational):

      flag = (self.numerator == other.numerator) and (self.denominator == other.denominator)

    elif isinstance(other, int):

      flag = (self.numerator == other) and (self.denominator == 1)

    return flag
  
  def __lt__(self, other):

    flag = False

    if isinstance(other, Rational):

      flag = self.to_float() < other.to_float()

    elif isinstance(other, int):

      flag = self.to_float() < other

    return flag
  
  def __mul__(self, other):

    if isinstance(other, Rational):

      new_numerator = self.numerator * other.numerator
      new_denominator = self.denominator * other.denominator

    elif isinstance(other, int):

      new_numerator = self.numerator * other
      new_denominator = self.denominator

    return Rational(new_numerator, new_denominator)

  def __neg__(self):
    
    return self * -1
  
  def __radd__(self, other):

    return self + other
  
  def __repr__(self):

    return str(self)

  def __str__(self):

    if self.denominator == 1:

      string = str(self.numerator)

    else:

      string = str(self.numerator) + "/" + str(self.denominator)

    return string

  def __sub__(self, other):

    return self + (other * -1)
  
  def __truediv__(self, other):

    if isinstance(other, Rational):

      rational = self * other.inverse()
      new_numerator = rational.numerator
      new_denominator = rational.denominator

    elif isinstance(other, int):

      new_numerator = self.numerator
      new_denominator = self.denominator * other

    return Rational(new_numerator, new_denominator)

  def inverse(self):

    return Rational(self.denominator, self.numerator)
  
  def reduce(self):

    gcd = math.gcd(self.numerator, self.denominator)
    self.numerator //= gcd
    self.denominator //= gcd

    if self.denominator < 1:

      self.numerator *= -1
      self.denominator *= -1

  # returns n such that self + (other * n) = 0
  def scale_of_add_inverse(self, other):

    return -self / other

  def to_float(self):

    return self.numerator / self.denominator

def prepare_rational_array(array):
  result_array = []

  for element in array:

    if isinstance(element, tuple):

      result_array.append(Rational(element[0], element[1]))

    elif isinstance(element, int):

      result_array.append(Rational(element))

  return result_array

"""#Matrices"""

class Matrix:

  def __init__(self, rows):

    if not all([len(row) == len(rows[0]) for row in rows]):
      raise Exception("Undefined: all rows of a matrix must have the same length.")

    self.rows = rows
    self.height = len(rows)
    self.width = len(rows[0])
  
  def __repr__(self):

    return str(self)
  
  def __str__(self):

    string = ""

    for row in self.rows[:-1]:
      string += str(row) + '\n'

    return string + str(self.rows[-1])
  
  def get_column(self, index):

    return [row[index] for row in self.rows]
  
  def is_in_reduced_row_echelon_form(self):

    pivots = []
    pivot_columns = []

    for row in self.rows:

      if not is_array_zeros(row):

        pivots.append(get_pivot_element(row))

        pivot_index = get_pivot_index(row)
        pivot_columns.append(self.get_column(pivot_index))

    return self.is_in_row_echelon_form() and all([pivot == 1 for pivot in pivots]) and all([is_array_hot(column) for column in pivot_columns])
  
  def is_in_row_echelon_form(self):

    pivot_column_indices = []
    pivot_row_indices = []
    zero_rows = []

    for index, row in enumerate(self.rows):

      if is_array_zeros(row):

        zero_rows.append(index)

      else:

        pivot_column_indices.append(get_pivot_index(row))
        pivot_row_indices.append(index)

    monotonic_pivots_flag = is_array_strictly_monotonic(pivot_column_indices)
    zeros_at_bottom_flag = all(index > max(pivot_row_indices) for index in zero_rows) or not zero_rows

    return monotonic_pivots_flag and zeros_at_bottom_flag
  
  def reduce(self):

    if not self.is_in_reduced_row_echelon_form():
      
      self.rows_triangulate()
      self.reduce_pass(1)
      self.rows_triangulate()
      self.reduce_pass(-1)
      self.rows_normalize()

  def reduce_pass(self, direction):

    if direction == 1:

      search_area = list(enumerate(self.rows[:-1]))
      replacement_test = lambda i, j: i > j

    if direction == -1:

      search_area = reversed(list(enumerate(self.rows[1:], start = 1)))
      replacement_test = lambda i, j: i < j

    for row_index, row in search_area:

      pivot = get_pivot_element(row)
      pivot_index = get_pivot_index(row)
      pivot_column = self.get_column(pivot_index)

      if not (is_array_zeros(row) or is_array_hot(pivot_column)):

        replacement_row_indices = [index for index in get_array_nonzero_indices(pivot_column) if replacement_test(index, pivot_index)]

        for replacement_row_index in replacement_row_indices:

          scale = pivot_column[replacement_row_index].scale_of_add_inverse(pivot)
          self.row_replace(replacement_row_index, row_index, scale)
  
  def row_replace(self, row1_index, row2_index, scale):

    if row1_index != row2_index:

      print("Operation: replaced row " + str(row1_index + 1) + " with row " + str(row1_index + 1) + " + row " + str(row2_index + 1) + " times " + str(scale) + ".")
      
      row1 = self.rows[row1_index]
      row2 = self.rows[row2_index]

      for index, (element1, element2) in enumerate(zip(row1, row2)):

        self.rows[row1_index][index] += scale * element2

      print(self)
      print()
  
  def row_scale(self, row_index, scale):

    print("Operation: scaled row " + str(row_index + 1) + " by " + str(scale) + ".")

    self.rows[row_index] = [element * scale for element in self.rows[row_index]]

    print(self)
    print()

  
  def row_swap(self, row1_index, row2_index):

    print("Operation: swapped row " + str(row1_index + 1) + " and row " + str(row2_index + 1) + ".")

    row1 = self.rows[row1_index]
    row2 = self.rows[row2_index]

    self.rows[row1_index] = row2
    self.rows[row2_index] = row1

    print(self)
    print()

  def rows_normalize(self):

    for row_index, row in enumerate(self.rows):

      pivot = get_pivot_element(row)

      if not is_array_zeros(row) and pivot != 1:

        scale = pivot.inverse()
        self.row_scale(row_index, scale)
  
  def rows_triangulate(self):

    swap_path = find_swap_sort_path(self.rows, (lambda x: get_pivot_index(x) if not is_array_zeros(x) else len(x)))

    for swap in swap_path:

      self.row_swap(swap[0], swap[1])

# returns a list of tuples of indices corresponding to the swaps needed to order the array
# performs key_function on each element to find correct ordering
def find_swap_sort_path(array, key_function):

  indices = [index for index, element in enumerate(array)]
  indexed_array = [(index, key_function(element)) for index, element in enumerate(array)]
  target_array = sorted(indexed_array, key = lambda x: x[1])
  target_indices = [element[0] for element in target_array]

  swaps = []

  for k in range(len(array)):
    
    current_index = indices.index(k)
    target_index = target_indices.index(k)

    if current_index != target_index:

      swaps.append((current_index, target_index))
      swap_array_elements(indices, current_index, target_index)
    
  return swaps

def get_array_elements_without_pivot(array):

  pivot_index = get_pivot_index(array)

  return [element for index, element in enumerate(array) if index != pivot_index]

def get_array_indices_without_pivot(array):

  pivot_index = get_pivot_index(array)

  return [index for index, element in enumerate(array) if index != pivot_index]

def get_array_nonzero_indices(array):

  return [index for index, element in enumerate(array) if element != 0]

def get_pivot_element(array):

  pivot = array[-1]

  if not is_array_zeros(array):

    pivot = next(element for element in array if element != 0)

  return pivot

def get_pivot_index(array):

  pivot_index = len(array) - 1

  if not is_array_zeros(array):

    pivot_index = next(index for index, element in enumerate(array) if element != 0)

  return pivot_index

def is_array_hot(array):

  flag = False

  if not is_array_zeros(array):

    pivot_index = get_pivot_index(array)
    non_pivot_array = [element for index, element in enumerate(array) if index != pivot_index]
    
    flag = is_array_zeros(non_pivot_array)

  return flag

def is_array_strictly_monotonic(array):

  flag = True

  if len(array) >= 2:

    search_area = array[1:]

    for index, element in enumerate(search_area):

      if element <= array[index]:

        flag = False
        break

  return flag

def is_array_zeros(array):

  return all([element == 0 for element in array])

def swap_array_elements(array, index1, index2):

  element1 = array[index1]
  element2 = array[index2]

  array[index1] = element2
  array[index2] = element1

"""#Systems of Equations"""

def is_equation_inconsistent(equation_array):

  return all(coefficient == 0 for coefficient in equation_array[0]) and equation_array != 0

# expects a tuple of tuples ((variable_indices, coefficients), (variable_indices, coefficients))
# a variable_index of None means the tuple is interpreted as a scalar
def represent_equation(equation_tuple):

  left_side_indices = equation_tuple[0][0]
  left_side_values = equation_tuple[0][1]
  right_side_indices = equation_tuple[1][0]
  right_side_values = equation_tuple[1][1]

  if is_array_zeros(left_side_values):

    equation_left_side = "0"

  else:

    left_term_pairs = zip(left_side_indices, left_side_values)
    left_term_reps = [represent_term(variable, coefficient) for variable, coefficient in left_term_pairs if coefficient != 0]
    equation_left_side = " + ".join(left_term_reps)

  if is_array_zeros(right_side_values):

    equation_right_side = "0"

  else:

    right_term_pairs = zip(right_side_indices, right_side_values)
    right_term_reps = [represent_term(variable, coefficient) for variable, coefficient in right_term_pairs if coefficient != 0]
    equation_right_side = " + ".join(right_term_reps)

  return " = ".join([equation_left_side, equation_right_side])

def represent_term(variable_index, coefficient):

  string = ""

  if variable_index is None:

    string += str(coefficient)

  else:

    if coefficient == 1:

      string += "x_" + str(variable_index)

    else:

      string += str(coefficient) + " x_" + str(variable_index)

  return string

# returns a tuple (variable_index, value) if a value can be computed
# returns a tuple (variable_index, "general equation") otherwise
def solve_equation(equation_array, known_variable_tuples):

  result = None

  coefficients = equation_array[0]
  value = equation_array[1]
  known_variable_indices = [variable_tuple[0] for variable_tuple in known_variable_tuples]
  variable_index = get_pivot_index(coefficients)

  if is_array_hot(coefficients):

    result = (variable_index, value)

  else:

    variable_inputs = [variable for variable in get_array_nonzero_indices(coefficients) if variable != variable_index]

    if all([variable in known_variable_indices for variable in variable_inputs]):

      coefficient_inputs = [coefficients[index] for index in variable_inputs]
      variable_values = [variable_tuple[1] for variable_tuple in known_variable_tuples if variable_tuple[0] in variable_inputs]

      new_value = value - sum([coefficient * variable for coefficient, variable in zip(coefficient_inputs, variable_values)], Rational(0, 1))
      result = (variable_index, value - sum([coefficient * variable for coefficient, variable in zip(coefficient_inputs, variable_values)], Rational(0, 1)))

    else:

      known_input_indices = [index for index in variable_inputs if index in known_variable_indices]
      known_input_coefficients = [coefficients[index] for index in known_variable_indices]
      known_input_values = [variable_tuple[1] for variable_tuple in known_variable_tuples if variable_tuple[0] in known_input_indices]
      unknown_input_indices = [index for index in variable_inputs if index not in known_variable_indices]
      unknown_input_coefficients = [-coefficients[index] for index in unknown_input_indices]
      constant_value = value - sum([coefficient * variable for coefficient, variable in zip(known_input_coefficients, known_input_values)], Rational(0, 1))

      left_side = ([variable_index], [1])
      right_side = (unknown_input_indices + [None], unknown_input_coefficients + [constant_value])
      equation_representation = represent_equation((left_side, right_side))
      result = (variable_index, equation_representation)

  return result

# assumes that it has received the rows of a reduced row echelon form matrix
# raises an exception if this is not the case
def solve_system_of_equations(arrays):

  test_matrix = Matrix(arrays)

  if not test_matrix.is_in_reduced_row_echelon_form():

    raise Exception("Error: must receive the rows of a matrix in reduced row echelon form to compute.")

  _arrays = arrays[::-1]

  variables = [index for index, variable in enumerate(_arrays[0][:-1])]
  solved_variables = [] # [(variable_index, value)]
  general_representations = [] # [(variable_index, "general equation")] stores variables that will receive general solutions

  equation_arrays = [(array[:-1], array[-1]) for array in _arrays if not is_array_zeros(array)] # returns a list of tuples ([coefficients], value)

  if any(is_equation_inconsistent(equation) for equation in equation_arrays):

    print("Result: this system of equations is inconsistent.")
    return None

  for equation in equation_arrays:

    solution = solve_equation(equation, solved_variables)

    if isinstance(solution[1], str):

      general_representations.append(solution)

    else:

      solved_variables.append(solution)

  solved_representations = [(variable[0], represent_equation((([variable[0]], [1]),([None], [variable[1]])))) for variable in solved_variables]

  free_variables = [i for i in variables if (i not in [var[0] for var in solved_variables]) and (i not in [var[0] for var in general_representations])]
  free_representations = [(index, represent_term(index, 1) + " is free.") for index in free_variables]

  return sorted(solved_representations + general_representations + free_representations, key = lambda x: x[0])

"""#Output"""

def calculate(equations):

  _equations = [prepare_rational_array(equation) for equation in equations]

  mat = Matrix(_equations)

  print("Starting Augmented Matrix:")
  print(mat)
  print()

  mat.reduce()

  print("Reduced Row Echelon Form Matrix:")
  print(mat)
  print()

  print("Resulting System of Equations:")
  for row in mat.rows:
    row_left_side = ([k for k in range(len(row[:-1]))], row[:-1])
    row_right_side = ([None], [row[-1]])
    print(represent_equation((row_left_side, row_right_side)))
  print()

  print("General Solution to System:")
  solution = solve_system_of_equations(mat.rows)

  if solution is not None:
    for answer in solution:
      print(answer[1])

"""#Test Environment"""

# each equation is a list of integers or tuples (a, b) that corresponds to the fraction a/b
eq1 = [1,0,1,0,1,10]
eq2 = [0,1,0,0,(1,2),-5]
eq3 = [0,1,1,0,0,10]
eq4 = [1,0,1,1,0,-20]
eqs = [eq1,eq2,eq3,eq4] # be sure to include every equation in this list

calculate(eqs) # don't touch this