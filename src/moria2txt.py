#!/usr/bin/env python
# Talk to Gaius about this. Easily reversible if it proves
# a bad idea.
from moria2txtconfig import *
import time

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
	rnd_seed = ((seed % (RNG_M - 1)) + 1)
	return rnd_seed

def seedsInitialize(seed):
	clock_var = 0
	# If seed is equal to 0 then generate a new seed
	if seed == 0:
		clock_var = getUnixTime()
	# else set the seed to the parsed seed
	else:
		clock_var = seed
	
	# Make it a litte more random. Problem before was that it's just the clock!
	clock_var += 8762
	clock_var += 113452L
	setRandomSeed(clock_var)

# The magic.
# Notes: my testing is near non-existent for this Lehmer
# generator. It looks to work perfectly fine to me,
# but should problems arise in the future then I shoulder the blame
# as I did a shoddy job in writing any tests for this.
def rnd():
	global rnd_seed
	high = (rnd_seed / RNG_Q)
	low = (rnd_seed % RNG_Q)
	test = (RNG_A * low - RNG_R * high)

	if test > 0:
		rnd_seed = test
	else:
		rnd_seed = (test + RNG_M)

	return rnd_seed


# Return a random number with a max constraint.
def randomNumber(max):
	tmp = rnd()
	print "rnd is: ", tmp
	mod = tmp % max
	print "modded is: ", mod
	return (rnd() % max) + 1

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

    current_level = 0

    panel = Panel_t

	# Tile is a tuple containing two entries:
	# the x and y of the tile and the feature id.
	# Feature id is a constant int.
    tile = []

# Create a new dungeon object here.
dg = Dungeon_t

class DungeonGenerator():
	# Constructor takes:
	# the width, height and max_rooms FOR NOW.
	def _init__(self, height, width, max_rooms, max_rows, max_cols):
		self.height = height
		self.width = width
		self.max_rooms = max_rooms
		self.max_rows = max_rows
		self.max_cols = max_cols

	def generateCave(self):
		top = 0
		bottom = 0
		left = 0
		right = 0
		
		top = randomNumber((randomNumber(5) + randomNumber(15)))
		
		print top





def dungeonFloorTileForLevel():
	# Essentially test whether or not we're in the town.
	# Not too sure if we'll be using a town for this iteration
	# of a Moria port but we'll see.
	if dg.current_level <= randomNumber(25):
		return TILE_LIGHT_FLOOR
	return TILE_DARK_FLOOR

def dungeonBuildRoom(y, x):
	# Parse the floor tile.
	floor = dungeonFloorTileForLevel()

	# Use randomNumber to randomize the height, depth and l + r values.
	height = y - randomNumber(4)
	depth = y + randomNumber(3)
	left = x - randomNumber(11)
	right = x + randomNumber(11)

	for height in range(depth):
		for left in range(right):
			dg.tile.append((height, left, floor))
	
	# Begin setting coordinates for the walls.
	# This is done by accessing the tile tuple and setting the:
	# y, x and feature id.
	# Note: I'm nooooot too sure if using iheight and idepth is a great solution
	# to a C++ for loop which says for int i = height - 1, but it seems to be working
	# for the time being...
	iheight = height -1
	idepth = depth + 1
	for iheight in range(idepth):
		dg.tile.append((iheight, left - 1, TILE_GRANITE_WALL))
		dg.tile.append((iheight, right + 1, TILE_GRANITE_WALL))
	
	for left in range(right):
		dg.tile.append((height - 1, left, TILE_GRANITE_WALL))
		dg.tile.append((depth + 1, left, TILE_GRANITE_WALL))

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

	# things acting weird here. double check if things break.

	door_index = 0

	# TO-DO: Continue this function and then move on. Looks like a lot more work to do.
	# This is the dungeon build for loop. Ignore it for now, and come back to it when
	# you actually get something pritning.
	# Check the dungeon generator for Python example for maybe some hints on how to
	#format some stuff. That's the next thing to do.

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
	testGen = DungeonGenerator()
	testGen.generateCave()


main()