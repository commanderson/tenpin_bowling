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
    """ Uses simple length checking and regular expressions 
        to validate an entered frame score in string form
        
        frame: a string to validate
        tenth: a boolean value, True if this is the 10th frame 
            and False otherwise

        Expected formats on non-thenth frames are "X", 
            or strings which fit the regular expression 
            "^([0-9]),([0-9\/])$"
            where the sum of digits is never more than 10
            
        Expected formats on the tenth frame are either "X,X,X", 
            ["X","{int<=9}","/"], ["X","{int}","{int}"], "{int},/,X", "{int},/,{int}", "{int},/,{int}",
                or "{int},{int}" where no int is >9 and where the sum of ints in the last 
                is never more than 10
            
        return value: boolean True if the score is valid 
                    and boolean False otherwise
    """
    
    #int value of True is 1; 
    #1 is min length of normal frames and 3 is min length for tenth
    #this means 3 is max length for normal frames and
    #5 is max length for tenth frame;
    
    min_length = 1
    max_length = 3
    if tenth:
        min_length+=2
        max_length+=2
    length=len(frame)
    if (length < min_length) or (length > max_length):
        return False
    #validation logic for normal frames
    if not tenth:
        if length == 1:
            return frame == 'X'#the only valid 1 character frame is 'X'
        try:
            nexpression = "^([0-9]),([0-9\/])$"
            m = re.search(nexpression, frame)
            return (m.groups()[1]=="/" or (int(m.groups()[0]) + int(m.groups()[1])) < 10)
        except (AttributeError, ValueError) as e:#the regex didn't match
            return False
  
    #validation logic for tenth frames
    else:
        if length == 3:
            try: #the only valid length 3 frame is 2 digits
                 #which sum < 10
                texpression = "^([0-9]),([0-9])$"
                m = re.search(texpression, frame)
                return ((int(m.groups()[0]) + int(m.groups()[1])) < 10)
            except (AttributeError, ValueError) as e:#the regex didn't match
                return False
        else:
            #"X,X,X", "X,{int<=9},/", "X,{int},{int}", "{int},/,X", "{int},/,{int}",
            try:
                texpression = "^([0-9]),(\/),([0-9X])$|^(X),([0-9]),([0-9\/])$|^(X),(X),([0-9X])$"
                m = re.search(texpression, frame)
                if m.groups()[0]:#first pattern, always valid
                    return True
                if m.groups()[3] is not None:#second pattern (starting X)
                    if m.groups()[5] == '/':#always valid for final spare
                        return True
                    else:#otherwise only valid if digits sum < 10
                        return ((int(m.groups()[4]) + int(m.groups()[5])) < 10)
                if m.groups()[6]:#Third pattern, always valid
                    return True
                    
                
            except (AttributeError, ValueError) as e:#the regex didn't match
                return False
    return False #should be unreachable, as long as the logic is good


def next_throws_value(frames, f, n):
    """ Returns the total pin value of the next n throws after 
            frame f in frames. When called with f=9 (the 10th frame),
            will instead return the value of the third throw of frame 10
            (if n==1) or the second + third throw of frame 10 (if n==2)
        
        frames: a list of lists of strings;
            each inner list will be
            either ["X"] 
            or ["{int 0<=a<=9}","/"] 
            or ["{int a}","{int b}"] where 0<=a+b<=9
        
        f: in index for f; will start counting throw value _after_ frame f
            (so this is useful for calculating the value of a spare or strike
            in frame f)
            
        n: integer number of throws to tally value for after frame f;
            will be either 1 or 2 in practice (for spares or strikes respectively)
            
        return value: an integer value for the next 1 or 2 throws after frame f;
            a strike has value 10, and a spare has value 10 when considered
            as two throws
    """
    counted = 0
    total = 0
    #if we are on a special three-throw last frame
    if f == 9 and len(frames[9]) == 3:
        if n == 1:#check last throw to fill out a spare
            if frames[9][2]=='X':
                return 10
            else:
                return int(frames[9][2])
        else:#check last 2 frames to fill out a strike
            if frames[9][2]=='/':#last 2 frame spare
                return 10
            elif frames[9][2]=='X':#last 2 frame double strike
                return 20
            else:
                return int(frames[9][1]) + int(frames[9][2])
        return total
    while counted < n:
        for throw in frames[f+1]:
            if throw == 'X':#in case of strike, one throw was worth 10
                total += 10
                counted +=1
            elif throw == '/':#in case of spare
                rem = total % 10#we fill out the current 10 pins
                total -= rem
                total += 10
                counted +=1
            else: #a numerical throw
                total += int(throw)
                counted +=1
            if counted >=n:
                break
        if counted < n:
            f += 1
    return total
def calculate_current_score(frames):
    """ Returns a current score for the given frames.
        Can be called for finished or unfinished sheets.
        
        frames: a list of lists of strings;
            each inner list will be
            either ["X"] 
            or ["{int 0<=a<=9}","/"] 
            or ["{int a}","{int b}"] where 0<=a+b<=9
            
        return value: null if the number can't currently be calculated 
        (if the value of a strike or spare is still being determined);
        otherwise, the current full value can be determined and displayed.
        
    """
    total = 0
    
    for f,frame in enumerate(frames):
        frame_total=0
        if len(frame)==2:#spare or numerical
            if frame[1]!='/':#if this isn't a spare
                frame_total = int(frame[0]) + int(frame[1])
            else: #if this is a spare
                try:
                    frame_total += (10 + next_throws_value(frames,f,1))
                except IndexError:
                    return None
        elif len(frame)==1:#a single strike
            try:
                frame_total += (10 + next_throws_value(frames,f,2))
            except IndexError:
                return None
        else: #a length 3 final frame
            if frame[0] == 'X': #started with strike
                frame_total += (10 + next_throws_value(frames,f,2))
            else: #started with spare
                frame_total += (10 + next_throws_value(frames,f,1))
        total += frame_total
    return total
    

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
                    #Placeholder setup code
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
                    
                    three_player_names = collect_player_names(3,
                                                three_playernames_input)
                    self.assertEqual(len(three_player_names), 3)
                    self.assertEqual(three_player_names, ['frumulo',
                                                    '','-=-=--=-=-=='])
                
                def test_validate_frame_score_normal(self):
                    """ Tests frame score validation function
                        behaves appropriately on normal (non-
                        tenth) frames
                    """
                    nframes_good = ["1,2","0,0","0,9","1,0","5,/","X","0,/"]
                    self.assertEqual([validate_frame_score(frame,False) 
                                                for frame in nframes_good],
                                                [True for _ in nframes_good])
                    nframes_bad = [",2","X,X","","7,8","/,/"]
                    self.assertEqual([validate_frame_score(frame,False) 
                                                for frame in nframes_bad],
                                                [False for _ in nframes_bad])
                    
                    
                def test_validate_frame_score_tenth(self):
                    """ Tests frame score validation function
                        behaves appropriately on tenth frames
                    """    
                    tframes_good = ["2,3","2,/,X","2,/,7","X,X,X",
                                                    "X,X,7","X,7,/"]
                    self.assertEqual([validate_frame_score(frame,True) 
                                                for frame in tframes_good],
                                                [True for _ in tframes_good])
                    tframes_bad = [",2","X,X","","7,8","/,/",
                                    "X,/,X","2,/,/","/,X,X","2,X,7","X,7,9"]
                    self.assertEqual([validate_frame_score(frame,True) 
                                                for frame in tframes_bad],
                                                [False for _ in tframes_bad])
                
                def test_next_throws_value_short(self):
                    """ Tests that next_throws_value can find the
                        value of the next 1 and 2 throws outside of the 
                        10th frame
                    """
                    easy_frames = [['1','2'],['3','4'],['5','/']]
                    self.assertEqual(next_throws_value(easy_frames,0,1),3)
                    self.assertEqual(next_throws_value(easy_frames,1,2),10)
                        
                def test_next_throws_value_end(self):
                    """ Tests that next_throws_value can find the
                        value of the next 1 and 2 throws within the 10th frame
                    """
                    ten_frames1 = [['1','2'],['3','4'],['5','/'],['1','2'],
                                   ['3','4'],['5','/'],['1','2'],['3','4'],
                                   ['5','/'],['3','/','X']]
                    ten_frames2 = [['1','2'],['3','4'],['5','/'],['1','2'],
                                   ['3','4'],['5','/'],['1','2'],['3','4'],
                                   ['5','/'],['X','3','/']]
                    ten_frames3 = [['1','2'],['3','4'],['5','/'],['1','2'],
                                   ['3','4'],['5','/'],['1','2'],['3','4'],
                                   ['5','/'],['3','/','3']]
                    ten_frames4 = [['1','2'],['3','4'],['5','/'],['1','2'],
                                   ['3','4'],['5','/'],['1','2'],['3','4'],
                                   ['5','/'],['X','2','5']]
                    self.assertEqual(next_throws_value(ten_frames1,9,1),10)
                    self.assertEqual(next_throws_value(ten_frames2,9,2),10)
                    self.assertEqual(next_throws_value(ten_frames3,9,1),3)
                    self.assertEqual(next_throws_value(ten_frames4,9,2),7)
                    
                def test_calculate_current_score_inprogress(self):
                    """ Tests that scores can be reported when possible in
                        a game in progress, and not reported when currently 
                        indeterminate
                    """
                    easy_frames = [['1','2'],['3','4'],['5','0']]
                    strike_good_frames = [['X'],['3','6'],['5','0']]
                    strike_bad_frames1 = [['1','2'],['3','4'],['X']]
                    strike_bad_frames2 = [['1','2'],['X'],['X']]
                    spare_good_frames = [['1','2'],['3','/'],['5','0']]
                    spare_bad_frames =  [['1','2'],['3','4'],['5','/']]
                    strike_spare_frames =  [['X'],['7','/'],['3','0']]
                    spare_strike_frames =  [['7','/'],['X'],['3','0'],['3','4']]
                    double_strike_frames =  [['X'],['X'],['3','0'],['3','4']]
                    double_spare_frames =  [['7','/'],['2','/'],['3','0'],['3','4']]
                    
                    self.assertEqual(calculate_current_score(easy_frames),15)
                    self.assertEqual(calculate_current_score(strike_good_frames),33)
                    self.assertEqual(calculate_current_score(strike_bad_frames1),None)
                    self.assertEqual(calculate_current_score(strike_bad_frames2),None)
                    self.assertEqual(calculate_current_score(spare_good_frames),23)
                    self.assertEqual(calculate_current_score(spare_bad_frames),None)
                    self.assertEqual(calculate_current_score(strike_spare_frames),36)
                    self.assertEqual(calculate_current_score(spare_strike_frames),43)
                    self.assertEqual(calculate_current_score(double_strike_frames),46)
                    self.assertEqual(calculate_current_score(double_spare_frames),35)
                    
                def test_calculate_current_score_final(self):
                    """ Tests that final scores are reported correctly
                    """
                    gutter_frames = [['0','0'],['0','0'],['0','0'],['0','0'],
                                   ['0','0'],['0','0'],['0','0'],['0','0'],
                                   ['0','0'],['0','0']]
                    perfect_frames = [['X'],['X'],['X'],['X'],
                                   ['X'],['X'],['X'],['X'],
                                   ['X'],['X','X','X']]
                    alternate_frames = [['X'],['0','0'],['X'],['0','/'],
                                   ['X'],['0','0'],['X'],['0','/'],
                                   ['X'],['0','/','0']]
                    ten_frames1 = [['1','2'],['3','4'],['5','/'],['1','2'],
                                   ['3','4'],['5','/'],['1','2'],['3','4'],
                                   ['5','/'],['3','/','X']]
                    ten_frames2 = [['1','2'],['3','4'],['5','/'],['1','2'],
                                   ['3','4'],['5','/'],['1','2'],['3','4'],
                                   ['5','/'],['X','3','/']]
                    ten_frames3 = [['1','2'],['3','4'],['5','/'],['1','2'],
                                   ['3','4'],['5','/'],['1','2'],['3','4'],
                                   ['5','/'],['3','/','3']]
                    ten_frames4 = [['1','2'],['3','4'],['5','/'],['1','2'],
                                   ['3','4'],['5','/'],['1','2'],['3','4'],
                                   ['5','/'],['X','2','5']]
                    ten_frames5 = [['1','2'],['3','4'],['5','/'],['1','2'],
                                   ['3','4'],['5','/'],['1','2'],['3','4'],
                                   ['5','/'],['2','5']]
                    self.assertEqual(calculate_current_score(gutter_frames),0)
                    self.assertEqual(calculate_current_score(perfect_frames),300)
                    self.assertEqual(calculate_current_score(alternate_frames),130)
                    self.assertEqual(calculate_current_score(ten_frames1),85)
                    self.assertEqual(calculate_current_score(ten_frames2),92)
                    self.assertEqual(calculate_current_score(ten_frames3),78)
                    self.assertEqual(calculate_current_score(ten_frames4),89)
                    self.assertEqual(calculate_current_score(ten_frames5),71)

        unittest.main()
                    
                    
    #Normal execution workflow
    else:
        num_players = ask_num_players()
        player_names = collect_player_names(num_players)
        score_sheet = [[] for names in player_names]
        for frame_index in range(9):#we are going to do frame 10 on its own
            for player_index in range(len(player_names)):
                throws = ""
                
                while not validate_frame_score(throws,False):
                    throws = raw_input(("Input frame %d for player '%s' " 
                                        + "as comma-separated list of pins hit"
                                        + " including X or / as appropriate:\n")
                                        %((frame_index+1),player_names[
                                                    player_index]))
                score_sheet[player_index].append(throws.split(","))
                print("Completed frame %d for player '%s'."
                        %((frame_index+1),player_names[player_index]))
                score = calculate_current_score(score_sheet[player_index])
                if score is not None:
                    print("Their current score is %d"%score)
                else:
                    print("(Their current score is unavailable)")
            if num_players > 1:
                print("Completed frame %d for all players."%(frame_index+1))
                
        for player_index in range(len(player_names)):
            throws = ""
            
            while not validate_frame_score(throws,True):
                throws = raw_input(("Input frame 10 for player '%s' " 
                                    + "as comma-separated list of pins hit"
                                    + " including X or / as appropriate:\n")
                                    %(player_names[player_index]))
            score_sheet[player_index].append(throws.split(","))
            print("Completed frame 10 for player '%s'"
                        %player_names[player_index])
            print("Final score: " + str(calculate_current_score(
                                                score_sheet[player_index])))
            
        
        print("Game Complete.\nFinal Scores:")
        
        for player_index,name in enumerate(player_names):
            print(name + ": " + str(calculate_current_score(score_sheet[player_index])))
    