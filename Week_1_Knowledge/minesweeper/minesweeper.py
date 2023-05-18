import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()       

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell) -> bool:
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell) -> int:
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self) -> bool:
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in (self.cells known to be mines).
        """
        # if self.cells known to be all mines, that is number of mines equals number of cells
        if self.count == len(self.cells) and (self.count != 0): # if self count == 0; there are no mine in self.cells
            # Return the cells set
            return self.cells     
        else: # return empty set because no cell can be conclude to be mine with current knowledge
            return set()
        
    def known_safes(self):
        """
        Returns the set of all cells in (self.cells known to be safe).
        """
        # if self.cells known to be all safes, that is number of mines equals 0
        if self.count == 0:
            # Return the cells set
            return self.cells
        else: # return empty set because no cell can be conclude to be safe with current knowledge
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # if cell is one of the cells included in the sentence.
        if cell in self.cells:
            #  update the sentence so that cell is no longer in the sentence, 
            self.cells.remove(cell)
            # update the senntence so that the count is still true given that cell is known to be a mine.
            self.count -= 1           
        #If cell is not in the sentence, then no action is necessary.
        else:
            pass

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        # if cell is one of the cells included in the sentence.
        if cell in self.cells:
            # update the sentence so that cell is no longer in the sentence,
            self.cells.remove(cell)
            # update the senntence so that the count is still true given that cell is known to be a safe.
            # self.count -= 0
        # If cell is not in the sentence, then no action is necessary.
        else: 
            pass

class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """

        # 1) mark the cell as one of the moves made in the game.
        self.moves_made.add(cell)
        
        # 2) mark the cell as a safe cell, updating any sentences that contain the cell as well.
        self.mark_safe(cell)
        
        # 3) add a new sentence to the AI’s knowledge base, based on the value of cell and count, to indicate that count of the cell’s neighbors are mines.
        # get neighbor cells
        neighbor_cells = self.get_neighbor_cells(cell)
        
        # Be sure to only include cells whose state is still undetermined in the sentence.
        neighbor_count_ai = len(neighbor_cells.intersection(self.mines))
        neighbor_count_in_sentence = count - neighbor_count_ai # neighbor_count_in_sentence = neighbor_count_by_environment - neighbor_count_by_ai
        
        neighbor_cells = neighbor_cells.difference(self.safes)
        neighbor_cells = neighbor_cells.difference(self.mines)
        neighbor_cells = neighbor_cells.difference(self.moves_made)
        
        # add new sentence based on neighbors cells and count
        new_sentence = Sentence(cells=neighbor_cells, count=neighbor_count_in_sentence )
        self.knowledge.append(new_sentence)        
        
        # 4) # If, based on any of the sentences in self.knowledge, new cells can be marked as safe or as mines, then the function should do so.   
        # loop through every sentence in the knowledge base
        for each_sentence in self.knowledge:       
            # check if all cells in a sentence are safe cells by comparing the mine count versus 0        
            safe_cells = each_sentence.known_safes()    
            # let the AI remember that those cells are safe cells, and update (every sentence in) the knowledge base that those cells are safe
            for each_safe_cell in list(safe_cells):
                self.mark_safe(each_safe_cell)
                
            # check if all cells in a sentence are mine cells by comparing the mine count versus the number of cells  
            mines_cells = each_sentence.known_mines()
            # let the AI remember that those cells are mine cells, and update (every sentence in) the knowledge base that those cells are mine
            for each_mine_cell in list(mines_cells):
                self.mark_mine(each_mine_cell)
                
        # clean empty sentence
        for each_sentence in self.knowledge:
            if len(each_sentence.cells) == 0:
                self.knowledge.remove(each_sentence)
            
        # 5) If, based on any of the sentences in self.knowledge, new sentences can be inferred (using the subset method described in the Background), 
        # then those sentences should be added to the knowledge base as well.
                
        # subset method      
        # loop through every pair of different sentences   
        novel_knowledge = []
        for this_sentence in self.knowledge: 
            for that_sentence in self.knowledge:
                if this_sentence != that_sentence: # two sentence must be different                                                     
                    # if a sentence is a subset of another sentence
                    if this_sentence.cells.issubset(that_sentence.cells):
                        # inferere new sentence
                        novel_sentence_cells = that_sentence.cells.difference(this_sentence.cells)
                        novel_sentence_count = that_sentence.count - this_sentence.count

                        # if the inference result make sense
                        if (len(novel_sentence_cells) != 0) and (novel_sentence_count >= 0):
                            # Create a new sentence, and add it to the novel knowledge base if it is not currently in knowledge base
                            novel_sentence = Sentence(novel_sentence_cells, novel_sentence_count)
                            if (novel_sentence not in self.knowledge):
                                novel_knowledge.append(novel_sentence)
        
        # concatenate novel knowledge base with current knowledge base                        
        self.knowledge.extend(novel_knowledge)
        
        # clean empty sentence
        # loop through every sentence in the knowledge base
        for each_sentence in self.knowledge:   
            # if there is no cell left in a sentence, the knowledge base should remove that sentence
            if len(each_sentence.cells) == 0:
                self.knowledge.remove(each_sentence)
            

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        # The move returned must be known to be safe, and not a move already made.
        safe_movable_cells = self.safes.difference(self.moves_made)
        
        if len(safe_movable_cells) > 0: # if there is a safe movable cell
            return list(safe_movable_cells)[0]
        else: # If no safe move can be guaranteed, the function should return None.
            return None
            

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """

        # Possible moves
        board_cells = set()
        for row_idx in range(self.height):
            for col_idx in range(self.width):
                cell = (row_idx, col_idx)
                board_cells.add(cell)
        
        # The move must not be a move that has already been made.
        possible_cells = board_cells.difference(self.moves_made)
        
        # The move must not be a move that is known to be a mine.
        possible_cells = possible_cells.difference(self.mines)
        
        # If there is numerous moves, randomly choose one of them
        num_possible_cells = len(possible_cells)
        if num_possible_cells > 0:
            random_idx = random.randrange(num_possible_cells)
            random_cell = list(possible_cells)[random_idx]
            # random_cell = list(possible_cells)[0]
            return random_cell
        else: # If no such moves are possible, the function should return None.
            return None
        
        
    
    def get_neighbor_cells(self, cell):
        """
            Return a set of neighbor cells of the input cell. 
        """
        neighbor_cells = set() 
        
        input_cell_row, input_cell_col = cell
        if (input_cell_row < 0) or (input_cell_row >= self.height) or (input_cell_col < 0) or (input_cell_col >= self.width):
            raise Exception(f"cell has illegal position{input_cell_row}{input_cell_col}")
        
        for row_value in [-1, 0, 1]:
            for col_value in [-1, 0, 1]:
                if (row_value == 0) and (col_value == 0):
                    continue
                
                new_cell_row = input_cell_row + row_value
                new_cell_col = input_cell_col + col_value
                
                if (new_cell_row < 0) or (new_cell_row >= self.height) or (new_cell_col < 0) or (new_cell_col >= self.width):
                    continue
                
                new_cell = (new_cell_row, new_cell_col)
                neighbor_cells.add(new_cell)
                
        return neighbor_cells