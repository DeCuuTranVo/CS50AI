import sys
from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        
        for var, var_domain in self.domains.items():
            new_var_domain = set()
            for word in var_domain:
                if len(word) == var.length: # constrait: every word must have the same length as variable
                    new_var_domain.add(word)
                    
            self.domains[var] = new_var_domain

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # determine constraint for crossword problem between two vertex x and y
        binary_constraint = self.crossword.overlaps[x, y]
        
        # if there is no arc constraint: x and y are not overlapping
        if binary_constraint == None:
            # no revision is made
            return False
        
        # print("var x", x)
        # print("var y", y)
        # print("binary constrant", binary_constraint)
        # print("domain x", self.domains[x])
        # print("domain y", self.domains[y])
        
        # revised = false
        revised = False
        
        words_x_to_remove = set()
        # for x in X.domain:
        for word_x in self.domains[x]:
            # if no y in Y.domain satisfies constraint for (X, Y):
            # calculate number of y in Y.domain that satisfies constraint for (X, Y):
            num_satisfied_y = 0
            for word_y in self.domains[y]:           
                # constaint: two letters of each words at a specified position must be the same. Should we check if all words are different in this part?
                if (word_x[binary_constraint[0]] == word_y[binary_constraint[1]]): # and (word_x != word_y):
                    num_satisfied_y += 1
                    # print(word_x, word_y, word_x[binary_constraint[0]], word_y[binary_constraint[1]], num_satisfied_y)
                    
            if num_satisfied_y == 0:
                # delete x from X.domain
                    # self.domains[x].remove(word_x) # sometime this line wil return error: RuntimeError: Set changed size during iteration
                # add x to words_x_to_remove:
                words_x_to_remove.add(word_x)                
                # revised = true
                revised = True
                
        # print("words_x_to_remove", words_x_to_remove)
        # remove words in words_x_to_remove
        self.domains[x] = self.domains[x].difference(words_x_to_remove)
        # print("domain x", self.domains[x])
        # print("domain y", self.domains[y])
          
        # return revised
        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs == None:
            queue = list(self.crossword.overlaps)
        else:
            queue = list(arcs)
                 
        while len(queue) > 0:
            (var_X, var_Y) = queue.pop(0) #
            if self.revise(var_X, var_Y):
                if len(self.domains[var_X]) == 0:
                    return False
                
                for var_Z in list(self.crossword.neighbors(var_X).difference({var_Y})):
                    queue.append((var_Z, var_X))
                    
        # print(self.domains)
        # for key, value  in self.crossword.overlaps.items():
        #     if value != None:
        #         print(key, value)
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """        
        # all variables (keys) must be in assignment.keys 
        for var in self.crossword.variables:
            if var not in list(assignment.keys()):
                return False
        
        # all variables (keys) must have non-null values
        for var, value in list(assignment.items()):
            if value == None:
                return False
            
        return True
        

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        distinct_value_set = set() 
        for var_key, value in assignment.items():
            if value != None:
                # check if all values are distinct
                if value not in distinct_value_set:
                    # print(type(value), value)
                    distinct_value_set.add(value)
                else:
                    return False
                
                # check if all value have a correct length
                if len(value) != var_key.length: 
                    return False

        # check if there are no conflicts between neighboring variables.
        for var_x in assignment.keys():
            for var_y in assignment.keys():
                if (var_x != var_y) and (assignment[var_x] != None) and (assignment[var_y] != None):
                    binary_constraint = self.crossword.overlaps[var_x, var_y]
                    # print(binary_constraint)
                    if binary_constraint != None:
                        # print(binary_constraint, "not None")
                        value_x = assignment[var_x]
                        value_y = assignment[var_y]
                        if value_x[binary_constraint[0]] != value_y[binary_constraint[1]]: 
                            return False
            
        return True        

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # add heuristics later
        # print(self.domains[var])
        
        # a dictionary that map word value to number of neighbors ruled out if that word is chosen for this variable assignment.
        var_word_to_num_eliminated_choice = dict()
        
        # get set of unassigned neighbors for this variable
        unassigned_neighbor_var_set = self.crossword.neighbors(var).difference(set(assignment.keys()))
        
        # loop through each value in the domain of var 
        for var_word in self.domains[var]:
            num_eliminated_choice = 0
            # for each neighbor_var in unassigned_neighbor_var_set:
            for neighbor_var in unassigned_neighbor_var_set:      
                var_overlap_idx, neighbor_overlap_idx = self.crossword.overlaps[var, neighbor_var] # self.crossword.neighbors => overlaps[var_word, neighbor_word] is not None
                          
                # for each value in the domain of neigbor_var
                for neighbor_word in self.domains[neighbor_var]:
                    # constraint 1: var_word != neighbor_word
                    if var_word == neighbor_word:
                        num_eliminated_choice += 1
                        continue
                    
                    # constrait 2: if overlaps[var, neighbor_var] exist, var_word[overlaps[var, neighbor_var][0]] != neighbor_var_word[overlaps[var, neighbor_var][1]]
                    if var_word[var_overlap_idx] != neighbor_word[neighbor_overlap_idx]:
                        num_eliminated_choice += 1
                        continue
                    
            # record num_eliminated_choice for each value of this var
            var_word_to_num_eliminated_choice[var_word] = num_eliminated_choice
                      
        # sort var_word according to number of eliminated choices
        sorted_var_word_dict = dict(sorted(var_word_to_num_eliminated_choice.items(), key=lambda item: item[1]))
        # print("sorted_var_word_dict:", sorted_var_word_dict)
        # print("return sorted_var_word_list", list(sorted_var_word_dict.keys()))
        # print("return unsorted_list", list(self.domains[var]))
        return list(sorted_var_word_dict.keys())
        

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        
        # calculate the set of unassigned variables            
        all_var_set = self.crossword.variables
        assigned_var_set = set(assignment.keys())    
        unassigned_var_set = all_var_set.difference(assigned_var_set)
        # an_unassigned_var = next(iter(unassigned_var_set))

        # choose variable with the fewest number of remaining values in its domain.
        lowest_domain_value_count = float("inf")
        
        # compute smallest domain value count
        for var in unassigned_var_set:
            var_domain_size = len(self.domains[var]) 
            if var_domain_size < lowest_domain_value_count:
                lowest_domain_value_count = var_domain_size
                
        # compute set of var which have smallest domain value count
        smallest_domain_var_set = set() 
        for var in unassigned_var_set:
            var_domain_size = len(self.domains[var])
            if var_domain_size == lowest_domain_value_count:
                smallest_domain_var_set.add(var)
                
        # print("=======================")
        # print("smallest_domain_var_set")
        # print(smallest_domain_var_set, lowest_domain_value_count)
                
        # if there is only one var with smallest domain count, return it; else: compare degree
        if len(smallest_domain_var_set) == 1:
            return next(iter(smallest_domain_var_set))
        else: # len(smallest_domain_var_set) > 1
            # If there is a tie between variables, choose the variable with the largest degree (has the most neighbors).
            
            # compute largest degree within smallest_domain_var_set
            highest_degree = float("-inf")    
            for var in smallest_domain_var_set:
                var_num_neigbors = len(self.crossword.neighbors(var))
                if var_num_neigbors > highest_degree:
                    highest_degree = var_num_neigbors
                    
            # compute set of variables with the largest degree 
            highest_degree_var_set = set() 
            for var in smallest_domain_var_set:
                var_num_neigbors = len(self.crossword.neighbors(var))
                if var_num_neigbors == highest_degree:
                    highest_degree_var_set.add(var)
                    
            # print("=======================")
            # print("highest_degree_var_set")
            # print(highest_degree_var_set, highest_degree)
                    
            # return a var in highest_degree_var_set
            return next(iter(highest_degree_var_set))                
            

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # print("======================>")
        # print("backtrack:", assignment)
        
        FAILURE = -1
        
        if self.assignment_complete(assignment):
            return assignment
        
        var = self.select_unassigned_variable(assignment)
        
        for value in self.order_domain_values(var, assignment):
            
            # print("try assignment:", var, " = ", value)            
            assignment[var] = value
            
            if self.consistent(assignment):
                # print("consistent")             
                result = self.backtrack(assignment)
                if result != FAILURE:
                    # print("result:", result)
                    return result
                
            # print("try failed, remove", var, " = ", value)  
            assignment.pop(var)
            
        return FAILURE              
    

def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
