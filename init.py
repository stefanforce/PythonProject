import sys

PLAYER = 1
AI = 3
PLAYER2 = 2

if len(sys.argv) < 4:
    print("You must follow the template: python 4inaROW.py <Player2/AI> <NumberOnX> <NumberOnY> [firstPlayer] ")
    exit()

if sys.argv[1] == "human":
    opponent = PLAYER2
elif sys.argv[1] == "computer":
    opponent = AI
else:
    print("You must insert human/computer as first argument to choose your opponent")
    exit()

try:

    ROW_COUNT = int(sys.argv[2])
    COLUMN_COUNT = int(sys.argv[3])
except TypeError as e:
    print("ROW_COUNT and COLUMN_COUNT must be integers")
    exit()

if ROW_COUNT < 6 or ROW_COUNT > 9 or COLUMN_COUNT < 6 or COLUMN_COUNT > 9:
    print("ROW_COUNT and COLUMN_COUNT must be between 6 and 10 lines")
    exit()

if sys.argv[4] == "player1":
    turn = PLAYER
elif sys.argv[4] == "computer":
    turn = AI
elif sys.argv[4] == "player2":
    turn = PLAYER2
else:
    print("You must insert player1/player2/computer as 4th argument to choose who goes first")
    exit()
