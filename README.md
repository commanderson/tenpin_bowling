# tenpin_bowling
This is a 10-pin bowling scoring application that uses traditional scoring rules to score each frame.
 
## Control flow

The application is launched with by invoking `python tenpin.py` on the command line. Alternately, `python tenpin.py --test` can be invoked to launch unit tests.

Once the application is launched, the user will be prompted to enter a number of players. This prompt will be repeated until the user inputs via stdin an integer between 1 and 9 inclusive.

For each player specified, the application will then ask for a name. This prompt will appear once for each player specified previously and will accept on stdin any string (including an empty string) as input. Names do not need to be unique.

After each player name is entered, scorekeeping begins. For each of 10 frames, a frame score will be requested for each player. This must be given in the form of a string on stdin, following traditional [ten-pin bowling scoring notation](https://www.thoughtco.com/bowling-scoring-420895 "ten-pin scoring").
Please note the following:
The tenth frame is special, and will have either two or three comma-separated throws; other frames will contain either one or two.

Frames are are validated internally and will not be accepted until a valid string for the frame in question is entered.

For any frame but the 10th, valid frames match the regular expression `^(X)$|^([0-9]),([0-9\/])$` and the sum of digits entered will not exceed 9

For the 10th frame, valid frames match the regular expression `^([0-9]),([0-9])$|^([0-9]),(\/),([0-9X])$|^(X),([0-9X]),([0-9X\/])$`, the sum of digits when matching the first or last pattern will not exceed 9, and a spare ('/') will always follow a digit.
After each frame is entered, the frame (and corresponding player) which was just completed will be displayed, as well as that player's current score. If a player's current score is unavailable because the value of a strike or spare is still being determined, a notification that the current score is unavailable will be displayed instead. On the final frame(frame 10), the score is always available, and will be displayed as "Final Score" instead of "Current Score".
If more than one player is playing, the application will print "Completed frame {n} for all players." after each frame.

Once ten frames have been entered for all players, the application will display "Game Complete." A list of players and their corresponding final scores will be displayed, and the application will exit.
