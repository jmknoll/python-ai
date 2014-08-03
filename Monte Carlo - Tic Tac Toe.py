"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# Change as desired
NTRIALS = 20    # Number of trials to run
MCMATCH = 1.0  # Score for squares played by the machine player
MCOTHER = 1.0  # Score for squares played by the other player

PLAYERX = provided.PLAYERX #2
PLAYERO = provided.PLAYERO #3
DRAW = provided.DRAW #4
EMPTY = provided.EMPTY #1

# Add your functions here.

def mc_trial(board, player):
    """
    Runs a random trial of the game
    """
    
    while board.check_win() == None:    
        
        empty_squares = board.get_empty_squares() 
            # get empty squares and put into a new list
        
        random_choice = random.choice(empty_squares)
        board.move(random_choice[0],random_choice[1],player)    
            # make a move randomly
            
        provided.switch_player(player) 
            # switch players
    
def mc_update_scores(scores, board, player):
    """
    Continually updates the scores while mc_trial runs in order to determine the best move
    """
    if board.check_win() == DRAW:
        # if game is a tie, all squares scored 0
        for dummy_score in scores:
            pass 
  
    else:
        dimension = board.get_dim()
        for dummy_row in range(dimension):
            for dummy_col in range(dimension):
                
                square_status = board.square(dummy_row, dummy_col)
                    # status of square at position
                           
                if square_status == EMPTY:
                    # empty squares score 0
                    scores[dummy_row][dummy_col] += 0
                    
                elif board.check_win() == player:
                    # if player wins                 
                    if square_status == player:
                        # score played squares positively
                        scores[dummy_row][dummy_col] += MCMATCH
                    else:
                        # score opponent squares negatively
                        scores[dummy_row][dummy_col] += -MCOTHER
                        
                else:
                    # if player loses
                    if square_status == player:
                        # score played squares negatively
                        scores[dummy_row][dummy_col] += -MCMATCH
                    else:
                        scores[dummy_row][dummy_col] += MCOTHER 
                        
def get_best_move(board, scores):
    """
    Takes a current board and a grid of scores
    Finds all empty squares with the maximum score and
    randomly returns one of them as a (row, column) tuple
    Don't call this function with a full board
    """
    empty_tuples = board.get_empty_squares()
        # return list of (row, col) tuples for all empty squares
    
    if empty_tuples == None:
        # do nothing if no empty squares
        pass
    else:
        square_scores = {}
            # defines square_scores as a dictionary
        max_squares = []
            # defines max_squares as a list
        
        for dummy_tuple in empty_tuples:
            # find the scores for each of the empty squares
            row = dummy_tuple[0]
            col = dummy_tuple[1]
            square_scores[dummy_tuple] = scores[row][col]
                # dictionary with (rol, col) tuples of empty squares as keys 
                # and their corresponding scores as values
        max_score = max(square_scores.values())
            # determines maximum score of empty squares
        for dummy_tuple, dummy_score in square_scores.items():
            if dummy_score == max_score:
                #print dummy_tuple
                #print ""
                max_squares.append(dummy_tuple)
                # list of (rol, col) tuples of empty squares 
                # with the maximum score
                #print "max squares"
                #print max_squares
                #print "" 
        random_max_square = random.choice(max_squares)
            # randomly selects one of the maximally scored empty squares
        return random_max_square



def mc_move(board, player, trials):
    """
    Takes a current board, which player the machine player is,
    and the number of trials to run
    Uses the Monte Carlo simulation to return a move for the
    machine player in the form of a (row, column) tuple
    Use these functions already defined:
        mc_trial(board, player)
        mc_update_scores(scores, board, player)
        get_best_move(board, scores)
    """
    
    trial_board = board.clone()
        # defines trial_board as a copy of the current board

    dim = board.get_dim()
        # retrieves dimensions of the board

    scores = [[0 for dummy_col in range(dim)] for dummy_row in range(dim)]
        # creates scores as a grid of 0s with the same dimensions as board
    
    for dummy_trial in range(trials):
        mc_trial(trial_board, player)
            # plays out a trial

        mc_update_scores(scores, trial_board, player)
            # updates scores based on trial
        
        trial_board = board.clone()
            # resets trial board to current board
            
    return get_best_move(board, scores)


# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

#provided.play_game(mc_move, NTRIALS, False)        
#poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
