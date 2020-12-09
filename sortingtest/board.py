#
# board.py (ps17pr1)
#
# A Board class for the Eight Puzzle
#
# name: 
# email:
#
# If you worked with a partner, put their contact info below:
# partner's name:
# partner's email:
#


class Board:
    """ A class for objects that represent an Eight Puzzle board.
    """
    def __init__(self, digitstr):
        """ a constructor for a Board object whose configuration
            is specified by the input digitstr
            input: digitstr is a permutation of the digits 0-9
        """
        # check that digitstr is 9-character string
        # containing all digits from 0-9
        assert(len(digitstr) == 9)
        for x in range(9):
            assert(str(x) in digitstr)

        self.tiles = [[0] * 3 for x in range(3)]
        self.blank_r = -1
        self.blank_c = -1

        # Put your code for the rest of __init__ below.
        # Do *NOT* remove our code above.

        for r in range(3):
            for c in range(3):
                self.tiles[r][c] = int(digitstr[3 * r + c])
                if self.tiles[r][c] == 0:
                    self.blank_r = r
                    self.blank_c = c
    ### Add your other method definitions below. ###

    def __repr__(self):
        '''returns a string representation of a Board object'''

        b = '' #begin with an empty string

        #add one row of slots at a time
        for row in range(3):
            for col in range(3):
                if self.tiles[row][col] == 0:
                    b += '_'
                else:
                    b += str(self.tiles[row][col])
                b += ' '
            b += '\n'
        return b

    def move_blank(self, direction):
        '''takes as input a string designation for the direction the 
        the blank should move and attempts to modify the contents of the called
        Board'''
        blank_r = self.blank_r
        blank_c = self.blank_c
        if direction == 'up':
            blank_r = self.blank_r - 1
        elif direction == 'down':
            blank_r = self.blank_r + 1
        elif direction == 'left':
            blank_c = self.blank_c - 1
        elif direction == 'right':
            blank_c = self.blank_c + 1
        else:
            print("Error:Uknown Direction")
            return False
        if blank_r >= 3 or blank_c >= 3 or blank_r < 0 or blank_c < 0:
            return False
        else:
            substitute = self.tiles[blank_r][blank_c]
            self.tiles[blank_r][blank_c] = 0
            self.tiles[self.blank_r][self.blank_c] = substitute
            self.blank_r = blank_r
            self.blank_c = blank_c
            return True

    def digit_string(self):
        '''creates and returns a string of digits that corresponds to the current
        contents of the called Board object's tiles attribute'''

        digitstring = ''
        for r in range(3):
            for c in range(3):
                if self.tiles[r][c] == '_':
                    digitstring += '0'
                else:
                    digitstring += str(self.tiles[r][c])
        return digitstring

    def copy(self):
        '''returns a newly-constructed Board object that is a deep copy of the called object'''

        first_board_str = self.digit_string()
        new_board = Board(first_board_str)
        return new_board

    def num_misplaced(self):
        """counts and returns the number of tiles in the called Board object that
            are not where they should be in the goal state.
        """
        count = 0
        goal_board = '012345678'
        current_board = self.digit_string()
        for i in range(9):
            if current_board[i] != '0' and current_board[i] != goal_board[i]:
                count += 1
        return count


    def how_far(self):
        '''counts and returns how far the number of misplaced tiles are from
           where they are supposed to be'''

        proper_board = '012345678'
        current_board = self.digit_string()

        how_far_sum = 0

        for x in current_board:
            if x == 0:
                how_far_sum = how_far_sum
            else:
                proper_index = proper_board.index(str(x))
                current_index = current_board.index(str(x))
                how_far_sum += abs(proper_index - current_index)

        return how_far_sum
      
    def __eq__(self, other):
        '''overloads the == operator and creates a version of the operator that
        works for Board objects'''

        if self.tiles == other.tiles:
            return True
        else:
            return False

