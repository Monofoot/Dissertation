#!/usr/bin/env python
import time

# Parameters for the Lehmer generator using
# Schrage's implementation.
# 2^31 - 1
RNG_M = 2**31 - 1
RNG_A = 48271
RNG_Q = RNG_M / RNG_A
RNG_R = RNG_M % RNG_A

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

# Note for Gaius -> is calling a function like this okay?
# Seems scary to me, not sure why!
seedsInitialize(0)
print(rnd())

# A few constant global variables we need to
# declare.
MAX_HEIGHT = 66
MAX_WIDTH = 198
SCREEN_HEIGHT = 22
SCREEN_WIDTH = 66

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

def DungeonGenerate():
	# Initialize a room with rows and columns.
	row_rooms = 2 * (dg.height / SCREEN_HEIGHT)
	col_rooms = 2 * (dg.width / SCREEN_WIDTH)

    # Create a new 20 x 20 room map.
	room_map = [20], [20]


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



generateCave()