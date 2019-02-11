#!/usr/bin/env python

# Parameters for the Lehmer generator using
# Schrage's implementation.
# 2^31 - 1
RNG_M = 2147483647
RNG_A = 48271
RNG_Q = RNG_M / RNG_A
RNG_R = RNG_M % RNG_A
rnd_seed = 0

print RNG_R

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

def getRandomSeed():
	return rnd_seed

print getRandomSeed()

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