#
# eight_puzzle.py
#
# driver/test code for state-space search on Eight Puzzles
#
# name: 
# email:
#
# If you worked with a partner, put their contact info below:
# partner's name:
# partner's email:
#

from searcher import *
from timer import *

def create_searcher(algorithm, depth_limit = -1, heuristic = None):
    """ a function that creates and returns an appropriate
        searcher object, based on the specified inputs. 
        inputs:
          * algorithm - a string specifying which algorithm the searcher
              should implement
          * depth_limit - an optional parameter that can be used to
            specify a depth limit 
          * heuristic - an optional parameter that can be used to pass
            in a heuristic function
            
        Note: If an unknown value is passed in for the algorithm parameter,
        the function returns None.
    """
    searcher = None
    
    if algorithm == 'random':
        searcher = Searcher(depth_limit)
    elif algorithm == 'BFS':
        searcher = BFSearcher(depth_limit)
    elif algorithm == 'DFS':
        searcher = DFSearcher(depth_limit)
    elif algorithm == 'Greedy':
        searcher = GreedySearcher(depth_limit, heuristic)
    elif algorithm == 'A*':
        searcher = AStarSearcher(depth_limit, heuristic)
    else:  
        print('unknown algorithm:', algorithm)

    return searcher

def eight_puzzle(init_boardstr, algorithm, depth_limit = -1, heuristic = None):
    """ a driver function for solving Eight Puzzles using state-space search
        inputs:
          * init_boardstr - a string of digits specifying the configuration
            of the board in the initial state
          * algorithm - a string specifying which algorithm you want to use
          * depth_limit - an optional parameter that can be used to
            specify a depth limit 
          * heuristic - an optional parameter that can be used to pass
            in a heuristic function
    """
    init_board = Board(init_boardstr)
    init_state = State(init_board, None, 'init')

    searcher = create_searcher(algorithm, depth_limit, heuristic)
    if searcher == None:
        return

    soln = None
    timer = Timer(algorithm)
    timer.start()
    
    try:
        soln = searcher.find_solution(init_state)
    except KeyboardInterrupt:
        print('Search terminated.')

    timer.end()
    print(str(timer) + ', ', end='')
    print(searcher.num_tested, 'states')

    if soln == None:
        print('Failed to find a solution.')
    else:
        print('Found a solution requiring', soln.num_moves, 'moves.')
        show_steps = input('Show the moves (y/n)? ')
        if show_steps == 'y':
            soln.print_moves_to()

def process_file(filename, algorithm, depth_limit=-1, heuristic=None):
    """ Processes a .txt file of different combinations
    """

    file = open(filename, 'r')
    puzzles = 0
    moves = 0
    tested_states = 0
    for line in file:
        string = line[:-1]
        init_board = Board(string)
        init_state = State(init_board, None, 'init')
        searcher = create_searcher(algorithm, depth_limit, heuristic)
        if searcher == None:
            return
            soln = None
        try:
            soln = searcher.find_solution(init_state)
            if soln == None:
                    print(string + ':','no solution')
            else:
                    print(string + ':', soln.num_moves, 'moves,', searcher.num_tested, 'states tested')
                    puzzles += 1
                    moves += soln.num_moves
                    tested_states += searcher.num_tested
        except KeyboardInterrupt:
            print('search terminated, ', end='')
    if puzzles != 0:
        print('\n','solved', puzzles, 'puzzles')
        print('average:', moves/puzzles, 'moves,', tested_states/puzzles, 'states tested')
    else:
        print('\n','solved', puzzles, 'puzzles')


process_file('24_moves.txt', 'Greedy', -1, h2)