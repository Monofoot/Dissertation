#!/usr/bin/env python
# Config file for moria2txt.
# Mostly holds constant and global variable declarations
# but may be expanded in scope to possibly hold convenience
# functions (for example - the entire Lehmer generator
# could be abstracted and placed in here so a developer wouldn't
# have to touch it again.)

# Random number generation

# Parameters for the Lehmer generator using
# Schrage's implementation.
# 2^31 - 1
RNG_M = 2**31 - 1
RNG_A = 48271
RNG_Q = RNG_M / RNG_A
RNG_R = RNG_M % RNG_A
rnd_seed = 0

MAX_SHORT = 32767
# Definitions for the normal distribution function
NORMAL_TABLE_SIZE = 256
NORMAL_TABLE_SD = 64
normal_table = [206,     613,    1022,    1430,    1838,    2245,    2652,    3058,
    3463,    3867,    4271,    4673,    5075,    5475,    5874,    6271,
    6667,    7061,    7454,    7845,    8234,    8621,    9006,    9389,
    9770,   10148,   10524,   10898,   11269,   11638,   12004,   12367,
    12727,   13085,   13440,   13792,   14140,   14486,   14828,   15168,
    15504,   15836,   16166,   16492,   16814,   17133,   17449,   17761,
    18069,   18374,   18675,   18972,   19266,   19556,   19842,   20124,
    20403,   20678,   20949,   21216,   21479,   21738,   21994,   22245,
    22493,   22737,   22977,   23213,   23446,   23674,   23899,   24120,
    24336,   24550,   24759,   24965,   25166,   25365,   25559,   25750,
    25937,   26120,   26300,   26476,   26649,   26818,   26983,   27146,
    27304,   27460,   27612,   27760,   27906,   28048,   28187,   28323,
    28455,   28585,   28711,   28835,   28955,   29073,   29188,   29299,
    29409,   29515,   29619,   29720,   29818,   29914,   30007,   30098,
    30186,   30272,   30356,   30437,   30516,   30593,   30668,   30740,
    30810,   30879,   30945,   31010,   31072,   31133,   31192,   31249,
    31304,   31358,   31410,   31460,   31509,   31556,   31601,   31646,
    31688,   31730,   31770,   31808,   31846,   31882,   31917,   31950,
    31983,   32014,   32044,   32074,   32102,   32129,   32155,   32180,
    32205,   32228,   32251,   32273,   32294,   32314,   32333,   32352,
    32370,   32387,   32404,   32420,   32435,   32450,   32464,   32477,
    32490,   32503,   32515,   32526,   32537,   32548,   32558,   32568,
    32577,   32586,   32595,   32603,   32611,   32618,   32625,   32632,
    32639,   32645,   32651,   32657,   32662,   32667,   32672,   32677,
    32682,   32686,   32690,   32694,   32698,   32702,   32705,   32708,
    32711,   32714,   32717,   32720,   32722,   32725,   32727,   32729,
    32731,   32733,   32735,   32737,   32739,   32740,   32742,   32743,
    32745,   32746,   32747,   32748,   32749,   32750,   32751,   32752,
    32753,   32754,   32755,   32756,   32757,   32757,   32758,   32758,
    32759,   32760,   32760,   32761,   32761,   32761,   32762,   32762,
    32763,   32763,   32763,   32764,   32764,   32764,   32764,   32765,
    32765,   32765,   32765,   32766,   32766,   32766,   32766,   32766 ]

# Dungeon Parameters

MAX_HEIGHT = 64
MAX_WIDTH = 198
SCREEN_HEIGHT = 22
SCREEN_WIDTH = 66
DUN_ROOMS_MEAN = 32
#TO-DO: Find Moria's min and max room size?
# Moria defines blank spaces as '.', but our tiles
# must correspond with the lexical semantics established in
# txt2pen. As such, a few of Moria's original tiles have been changed so
# that we don't break the txt>pen>map pipeline.
TILES = {'empty': ' ',
        'floor': ' ',
        'wall': '#',
        'door': '.'}
# Can't have a room be > 9 as it overloads the map.
# TO-DO: possibly add this overloadedroom to the TILES constant.
overloadedroom = ['a', 'b', 'c', 'd', 'e', 'f', 'g',
                  'h', 'i', 'j', 'k', 'l', 'm', 'n',
                  'o', 'p', 'q', 'r', 's', 't', 'u',
                  'v', 'w', 'x', 'y', 'z']
# To-do: Write the definitions at some point. Example:
# define 1 room 1 with the number 1 in the top left corner of each room.
# Should be easy enough.