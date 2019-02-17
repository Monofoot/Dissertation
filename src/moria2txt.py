#!/usr/bin/env python
import time

# TO-DO: Make another Python file for your constants and import from them.

# Parameters for the Lehmer generator using
# Schrage's implementation.
# 2^31 - 1
RNG_M = 2**31 - 1
RNG_A = 48271
RNG_Q = RNG_M / RNG_A
RNG_R = RNG_M % RNG_A

# All constants should be stored here #
# Hold a parameter for MAX_SHORT int.
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
# Constants for the dungeon parameters
MAX_HEIGHT = 66
MAX_WIDTH = 198
SCREEN_HEIGHT = 22
SCREEN_WIDTH = 66
DUN_ROOMS_MEAN = 32
QUART_HEIGHT = SCREEN_HEIGHT / 4
QUART_WIDTH = SCREEN_WIDTH / 4

# Get the current unix time and store it in a clock variable.
# Use the clock variable to parse a new random seed in
# setRandomSeed()
def getUnixTime():
	clock = int(time.time())
	return clock

def setRandomSeed(seed):
	# Set seed between value 1 and m-1
	# IMPORTANT VARIABLE #
	# Driver for most of the RNG. Pay attention as any problems
	# are likely derived from rnd_seed!
	global rnd_seed
	rnd_seed = seed % (RNG_M - 1)
	return rnd_seed

def seedsInitialize(seed):
	clock_var = 0
	# If seed is equal to 0 then generate a new seed
	if seed == 0:
		clock_var = getUnixTime()
	# else set the seed to the parsed seed
	else:
		clock_var = seed
	setRandomSeed(clock_var)

# The magic.
# Notes: my testing is near non-existent for this Lehmer
# generator. It looks to work perfectly fine to me,
# but should problems arise in the future then I shoulder the blame
# as I did a shoddy job in writing any tests for this.
def rnd():
	high = rnd_seed / RNG_Q
	low = rnd_seed % RNG_Q
	test = RNG_A * low - RNG_R * high

	# I really, really wanted the return to be rnd_seed
	# but I'm having a local variable problem. It's near 11pm and
	# I'm shattered, so for now test will do - horrible, I know,
	# but probably easily fixable.
	return test

# Return a random number with a max constraint.
def randomNumber(max):
	return rnd() % max + 1

# Generate a random number of normal distribution.
def randomNumberNormalDistribution(mean, standard):
	# Start by grabbing a random number from MAX_SHORT constant.
	tmp = randomNumber(MAX_SHORT)

	# If tmp is equal to MAX_SHORT then re-randomize it
	if tmp == MAX_SHORT:
		offset = 4 * standard + randomNumber(standard)
		if randomNumber(2) == 1:
			offset = -offset
		return mean + offset
	
	low = 0
	iindex = NORMAL_TABLE_SIZE >> 1
	high = NORMAL_TABLE_SIZE

	# Loop through the values until we have a satisfactory value
	while True:
		if normal_table[iindex] == tmp or high == low + 1:
			break
		if normal_table[iindex] > tmp:
			high = iindex
			iindex = low + (iindex - low) >> 1
		else:
			low = iindex
			iindex = iindex + ((high - iindex) >> 1)

	# Check that we're not one below target
	if normal_table[iindex] < tmp:
		iindex = iindex + 1
	
	offset = ((standard * iindex) + (NORMAL_TABLE_SD >> 1)) / NORMAL_TABLE_SD

	# Want some of the return values to be negative - such is how
	# random normal distribution works.
	if randomNumber(2) == 1:
		offset = -offset
	
	return mean + offset

# Coord_t
class Coord_t:
    x = 0
    y = 0

# Tile_t
# Note: not sure if we'll need this just yet.
class Tile_t:
	# ID of a room feature; walls, floors, door etc
	feature_id = None
	
# Panel_t
# Again not too sure about needing to include this.
# Will see how it goes.
class Panel_t:
	row = None
	col = None
	
	top = None
	bottom = None
	left = None
	right = None
	
	col_prt = None
	row_prt = None
	
	max_rows = None
	max_cols = None

# Dungeon_t
class Dungeon_t:
    height = 0
    width = 0

    panel = Panel_t

# Create a new dungeon object here.
dg = Dungeon_t

def dungeonBuildRoom(y, x):
	print y, x

def DungeonGenerate():
	# Initialize a room with rows and columns.
	row_rooms = 2 * (dg.height / SCREEN_HEIGHT)
	col_rooms = 2 * (dg.width / SCREEN_WIDTH)

	# Create a tuple of rooms and columns.
	room_map = []

	# Create a random_room_count using the dungeon mean constant.
	random_room_count = randomNumberNormalDistribution(DUN_ROOMS_MEAN, 2)

	# Store the rows and columns in the room_map tuple.
	# The purpose of this isn't so much for the integers as it is
	# a test to see if an entry exists.
	for i in range(random_room_count):
		room_map.append((row_rooms, col_rooms))

	location_id = 0
	y_locations = []
	x_locations = []

	for row in range(row_rooms):
		for col in range(col_rooms):
			if row or col in room_map:
				y_locations.append((row * SCREEN_HEIGHT >> 1) + QUART_HEIGHT)
				x_locations.append((col * SCREEN_WIDTH >> 1) + QUART_WIDTH)

				# Build a room at each of these locations.
				dungeonBuildRoom(y_locations[location_id], x_locations[location_id])
				
				# A bit sloppy, I know, but increment location_id by 1.
				location_id = location_id + 1
			



def generateCave():
	# Double check we're setting everything back
	# to 0.
    dg.panel.top = 0
    dg.panel.bottom = 0
    dg.panel.left = 0
    dg.panel.right = 0

	# Start by setting the dungeon 
	# height and width equal to
	# max height and
	# width constants
    dg.height = MAX_HEIGHT
    dg.width = MAX_WIDTH

	# Set the max rows and cols.
    dg.panel.max_rows = (dg.height / SCREEN_HEIGHT) * 2 - 2
    dg.panel.max_cols = (dg.width / SCREEN_WIDTH) * 2 - 2

    dg.panel.row = dg.panel.max_rows
    dg.panel.col = dg.panel.max_cols

    DungeonGenerate()


def main():
	seedsInitialize(0)
	generateCave()

main()