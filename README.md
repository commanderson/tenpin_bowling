# tenpin_bowling
This is a 10-pin bowling scoring application that uses traditional scoring rules to score each frame.
 
## Control flow

The application is launched with by invoking `python tenpin.py` on the command line. Alternately, `python tenpin.py --test` can be invoked to launch unit tests.

Once the application is launched, the user will be prompted to enter a number of players. This prompt will be repeated until the user inputs via stdin an integer between 1 and 9 inclusive.

For each player specified, the application will then ask for a name. This prompt will appear once for each player specified previously and will accept on stdin any string (including an empty string) as input.

After each player name is entered, scorekeeping begins. For each of 10 frames, a frame score will be requested for each player. This must be given in the form of a string on stdin, following traditional [ten-pin bowling scoring notation](https://www.thoughtco.com/bowling-scoring-420895 "ten-pin scoring")
Please note the following:
The tenth frame is special, and will have either two or three comma-separated throws; other frames will contain either one or two
```AT PRESENT, NO VALIDATION BEYOND LENGTH CHECKING IS DONE ON FRAME INPUTS```
While a number of approaches suggest themselves, it will take a while to code on its own and I would rather this exercise serve as a brief demo of ability than a lengthy showcase of string validation logic

After each frame is entered, the frame (and corresponding player) which was just completed will be displayed, as well as that player's current score

Once ten frames have been entered for all players, a list of players and their corresponding final scores will be displayed, and the application will exit.
