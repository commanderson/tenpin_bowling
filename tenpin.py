#Scores should be provided to the application through STDIN and the current
#recorded score should be printed to STDOUT after accepting the new score.
# The recently completed frame number and current score must be printed to
#STDOUT after each score submission.
# The application should exit once the score for the 10th frame is submitted and
#the final score is printed to STDOUT.
# The application must support at least 1 user. If you support more than 1 user,
#you must include user identifying information in the scoring output summary.
# You must include tests with your submission.
# Provide instructions for how to run your application. Preferably in a README.md
#at the root of your project.

#value of strike frame is 10 + next 2 throws
#value of spare frame is 10 + next throw
#value of open frame is face value

import argparse
import sys
import re

def ask_num_players(input_function = raw_input):
    """ Queries user for number of players, enforcing that it must
        be an integer number between 1 and 9 inclusive
        
        input_function: allows a function other than raw_input to 
            be used as a source of input; useful for testing purposes
            
        return value: an integer number between 1 and 9 inclusive,
            as given by the user on stdin
    """
    num_players = -1
    while (num_players < 1) or (num_players > 9):
            try:
                num_players = int(input_function("Please enter number of players "
                             + "(must be more than 0 and less than 10)\n"))
            except ValueError:
                print("Invalid input;")
    return num_players
    
def collect_player_names(num_players,input_function = raw_input):
    """ Queries user for a name for each player;
        names can be any string and don't have to be unique
        
        num_players: The number of players who will be participating
            in the game; expected to be between 1 and 9 inclusive
        input_function: allows a function other than raw_input to 
            be used as a source of input; useful for testing purposes
        
        return value: A list of strings corresponding to the 
            player names provided by the user as input
    """
    player_names = []
    for i in range(1,num_players+1):
        player_names.append(input_function("Enter the name of "
                                        + "player number %d.\n"%i))
    return player_names
    
def validate_frame_score(frame, tenth):
    """ Validates an entered frame score
        
        frame: a list to validate
        tenth: a boolean value, True if this is the 10th frame 
            and False otherwise

        Expected formats on non-thenth frames are ["X"], ["{int<=9}","/"] 
            or ["{int}","{int}"] where the sum of ints in the last 
            is never more than 10
            
        Expected formats on the tenth frame are either ["X","X","X"], 
            ["X","{int<=9}","/"], ["X","{int}","{int}"], "{int},/,X", "{int},/,{int}", "{int},/,{int}",
                or "{int},{int}" where no int is >9 and where the sum of ints in the last 
                is never more than 10
            
        return value: boolean True if the score is valid 
                    and boolean False otherwise
    """
    
    #int value of True is 1; 
    #this means 2 is max length for normal frames and
    #3 is max length for tenth frame;
    #1 is min length of normal frames and 2 is min length for tenth
    length=len(frame)
    if (length < 1 + tenth) or (length > (2 + tenth)):
        return false
    #validation logic for normal frames
    if not tenth:
        if length == 1:
            return frame == 'X'#the only valid 1 character frame is 'X'
        try:
            return ( (int(frame[0])<=9) and ( (frame[1]=="/") 
                        or (int(frame[1]) + int(frame[0]) < 10) ) )
        except ValueError:
            return False
    #validation logic for tenth frames
    else:
        if length == 2:
            try:
                return ( int(frame[0]) + int(frame[1]) < 10)
            except ValueError:
                return False
        else:
            #"X,X,X", "X,{int<=9},/", "X,{int},{int}", "{int},/,X", "{int},/,{int}",
            return frame[0]
    
       
def calculate_overall_scores(score_sheet):
    """ Returns a list of total scores for each 
        player's frame list in score_sheet.
        Can be called for finished or unfinished sheets.
        
        score_sheet: a list of lists  of strings
            each inner list is a list of frame throws for one player
    """
    return [0 for _ in score_sheet]
    

#begin standalone execution
if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--test', action='store_const',
        const=True,
        default=False,
        help='run tests'
        )
    
    args = parser.parse_args()
    
    #Test execution workflow
    if args.test:
        del sys.argv[1:]
        import unittest
        class TenpinUnitTests(unittest.TestCase):
                """ Tests general behavior of the functions of tenpin.py """
                
                def setUp(self):
                    #Placeholder setup code                                       'junctions.temp')
                    pass
                    
                #most of the unit tests take advantage of the input_function argument to take input
                #from a custom function instead of raw_input for testing purposes
                def test_ask_num_players_valid(self):
                    """ Tests that a valid integer num players can be entered
                    """
                    valid_pnum = ask_num_players(lambda _: '3')
                    self.assertEqual(valid_pnum, 3)
                    
                def test_ask_num_players_invalid(self):
                    """ Tests that invalid player number is rejected until
                        an acceptable entry is received
                    """
                    def two_invalid_then_valid_numplayers_input(_):
                        two_invalid_then_valid_numplayers_input.c += 1
                        returns = ['-','-3','4']
                        return returns[
                                two_invalid_then_valid_numplayers_input.c]
                    two_invalid_then_valid_numplayers_input.c = -1
                    
                    eventually_valid_pnum = ask_num_players(
                                    two_invalid_then_valid_numplayers_input)
                    self.assertEqual(eventually_valid_pnum, 4)
                
                def test_collect_player_names(self):
                    """ Tests that several player names are properly recorded
                    """
                    def three_playernames_input(_):
                        three_playernames_input.c += 1
                        returns = ['frumulo','','-=-=--=-=-==']
                        return returns[
                                three_playernames_input.c]
                    three_playernames_input.c = -1
                    
                    three_player_names = collect_player_names(3,three_playernames_input)
                    self.assertEqual(len(three_player_names), 3)
                    self.assertEqual(three_player_names, ['frumulo','','-=-=--=-=-=='])
        unittest.main()
                    
                    
    #Normal execution workflow
    else:
        num_players = ask_num_players()
        player_names = collect_player_names(num_players)
        score_sheet = [[] for names in player_names]
        for frame_index in range(9):#we are going to do frame 10 on its own
            for player_index in range(len(player_names)):
                throws = []
                
                while len(throws) < 1 or len(throws) > 3:
                    throws = raw_input(("Input frame %d for player '%s' " 
                                        + "as comma-separated list of pins hit"
                                        + " including X or / as appropriate\n")
                                        %((frame_index+1),player_names[
                                                    player_index]))
                score_sheet[player_index].append(throws.split(","))
                
        for player_index in range(len(player_names)):
            throws = []
            
            while len(throws) < 3 or len(throws) > 5:
                throws = raw_input(("Input frame 10 for player '%s' " 
                                    + "as comma-separated list of pins hit"
                                    + " including X or / as appropriate\n")
                                    %(player_names[player_index]))
                score_sheet[player_index].append(throws.split(","))
    
    
        for i,name in enumerate(player_names):
            print(name + ": " + str(score_sheet[i]))
    