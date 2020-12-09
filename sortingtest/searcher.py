#
# searcher.py (ps18)
#
# classes for objects that perform state-space search on Eight Puzzles  
#
# name: 
# email:
#
# If you worked with a partner, put their contact info below:
# partner's name:
# partner's email:
#

import random
from state import *
import time

class Searcher:
    """ A class for objects that perform random state-space
    search on an Eight Puzzle.
    This will also be used as a superclass of classes for
    other state-space search algorithms.
    """
    ### Add your Searcher method definitions here. ###
    def __init__(self, depth_limit):
        """constructs a new Searcher object
        """
        self.states = []
        self.num_tested = 0
        self.depth_limit = depth_limit

    def add_state(self, new_state):
        """that adds takes a single State object called new_state
        and adds it to the Searcher‘s list of untested states
        """
        self.states+=[new_state]

    def should_add(self, state):
        """that takes a State object called state and returns
        True if the called Searcher should add state to its
        list of untested states, and False otherwise
        """

        if self.depth_limit != -1 and state.num_moves > self.depth_limit:
            return False
        elif state.creates_cycle()==True:
            return False
        else:
            return True

    def add_states(self, new_states):
        """that takes a list State objects called new_states, and
        that processes the elements of new_states one at a time
        """
        for i in new_states:
            if self.should_add(i):
                self.add_state(i)

    def __repr__(self):
        """ returns a string representation of the Searcher object
        referred to by self.
        """
        # You should *NOT* change this method.
        s = type(self).__name__ + ': '
        s += str(len(self.states)) + ' untested, '
        s += str(self.num_tested) + ' tested, '
        if self.depth_limit == -1:
            s += 'no depth limit'
        else:
            s += 'depth limit = ' + str(self.depth_limit)
        return s
    
    def next_state(self):
        """ chooses the next state to be tested from the list of
        untested states, removing it from the list and returning it
        """
        s = random.choice(self.states)
        self.states.remove(s)
        return s

    def find_solution(self, init_state):
        
        """that performs a full random state-space search, stopping when
        the goal state is found or when the Searcher runs out of untested
        states
        """
        self.add_state(init_state)
        while self.states != []:
            s = self.next_state()
            self.num_tested += 1
            if s.is_goal():
                return s
            else:
                self.add_states(s.generate_successors())   
        return None

### Add your BFSeacher and DFSearcher class definitions below. ###
class BFSearcher(Searcher):

    def next_state(self):
            """that overrides (i.e., replaces) the next_state method that is inherited
            from Searcher. Rather than choosing at random from the list of untested
            states, this version of next_state should follow FIFO (first-in first-out)
            ordering – choosing the state that has been in the list the longest"""


            s = self.states[0]
            self.states.remove(s)
            return s
class DFSearcher(Searcher):

    def next_state(self):
            """that overrides (i.e., replaces) the next_state method that is inherited
            from Searcher. Rather than choosing at random from the list of untested
            states, this version of next_state should should follow LIFO (last-in first-out)
            ordering – choosing the state that was most recently added to the list"""


            s = self.states[-1]
            self.states.remove(s)
            return s

def h0(state):
            """ a heuristic function that always returns 0 """
            return 0
### Add your other heuristic functions here. ###
def h1(state):
            """computes and returns an estimate of how many additional moves
            are needed to get from state to the goal state"""
            return state.board.num_misplaced()

def h2(state):
    """computes and returns the manhattan distance
    between state and the goal state"""
    goal_board = [0,1,2,3,4,5,6,7,8]
    current_board = state.board.digit_string()
    initial_config = [int(x) for x in current_board]
    manDict = 0
    for i,item in enumerate(initial_config):
        prev_row,prev_col = int(i/ 3) , i % 3
        goal_row,goal_col = int(item /3),item % 3
        manDict += abs(prev_row-goal_row) + abs(prev_col - goal_col)
    return manDict
            
class GreedySearcher(Searcher):
    """ A class for objects that perform an informed greedy state-space
        search on an Eight Puzzle.
    """
    ### Add your GreedySearcher method definitions here. ###
    def __init__(self, depth_limit, heuristic):
            """ constructor for a GreedySearcher object
            inputs
            """
            super().__init__(-1)
            self.heuristic = heuristic
    
    def priority(self, state):
            """ computes and returns the priority of the specified state,
            based on the heuristic function used by the searcher
            """
            return -1 * self.heuristic(state)
    def add_state(self, state):
            """that overrides (i.e., replaces) the add_state method that is inherited from Searcher.
            Rather than simply adding the specified state to the list of untested states, the method
            should add a sublist that is a [priority, state] pair, where priority is the priority of
            state, as determined by calling the priority method"""

            self.states+=[[self.priority(state), state]]

    def next_state(self):
            """that overrides (i.e., replaces) the next_state method that is inherited from Searcher.
            This version of next_state should choose one of the states with the highest priority."""
            s=max(self.states)
            self.states.remove(s)
            return s[1]

    def __repr__(self):
            """ returns a string representation of the GreedySearcher object
            referred to by self.
            """
            # You should *NOT* change this method.
            s = type(self).__name__ + ': '
            s += str(len(self.states)) + ' untested, '
            s += str(self.num_tested) + ' tested, '
            s += 'heuristic ' + self.heuristic.__name__
            return s
            

    ### Add your AStarSeacher class definition below. ###
class AStarSearcher(GreedySearcher):
        
    def priority(self, state):
            """that takes a State object called state, and that computes and returns the priority
            of that state
            """
            priority= -1 *(self.heuristic(state) + state.num_moves)
            return priority