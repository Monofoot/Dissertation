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
	clock_var += 113452
	setRandomSeed(clock_var)

# The magic.
# Notes: my testing is near non-existent for this Lehmer
# generator. It looks to work perfectly fine to me,
# but should problems arise in the future then I shoulder the blame
# as I did a shoddy job in writing any tests for this.
def rnd():
	global rnd_seed
	high = (rnd_seed // RNG_Q)
	low = (rnd_seed % RNG_Q)
	test = (RNG_A * low - RNG_R * high)

	if test > 0:
		rnd_seed = test
	else:
		rnd_seed = (test + RNG_M)

	return rnd_seed

# I wrote this one myself so it might not be very elegant,
# I'm sure it wouldn't pass any speed tests... but it does the job for now, anyway.
# I know randint() exists but if a seed initializer exists in this script
# I'd prefer to use that seed than spool a new one for the random module.
def randomBetweenAB(A, B):
    result = 0
    test = randomNumber(B)
    while test < A or test > B:
        test = randomNumber(B)
        if test > A or test < B:
            result = test
            break
    result = test
    return result

# Return a random number with a max constraint.
def randomNumber(max):
	return int((rnd() % max) + 1)

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
	
	offset = ((standard * iindex) + (NORMAL_TABLE_SD >> 1)) // NORMAL_TABLE_SD

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
    def __init__(self, min_size = 5, max_size = 15,
                height = MAX_HEIGHT, width = MAX_WIDTH, 
				random_room_count = 0, max_rooms = 10):
        self.min_size = min_size
        self.max_size = max_size
        self.height = height
        self.width = width
        self.random_room_count = randomNumberNormalDistribution(DUN_ROOMS_MEAN, 2)
        self.rooms = []
        self.dungeon = []
        self.max_rooms = max_rooms
        self.tiles = TILES
        self.tiles_level = []

        # Soon I'd like to be able to set these parameters
        # through the command line, it should be easy enough.

    def dungeonBuildRoom(self):
		# generateCave will return a list with four entries:
		# [x, y, width, height]
		# Where x and y are the co-ordinates where the room will initially
		# be drawn, and the width and height are by which magnitude
		# So if x is 10 and y is 13, go to point 10, 13 - if height is 4, place
		# 4 walls up and return back to 10, 13 - if width is 9, place 9 walls to the
		# left.
        vertical   = 0
        horizontal = 0
        x          = 0
        y          = 0

        vertical   = randomBetweenAB(self.min_size, self.max_size)
        horizontal = randomBetweenAB(self.min_size, self.max_size)
        x          = randomBetweenAB(1, (self.width - vertical - 1))
        y          = randomBetweenAB(1, (self.height - horizontal - 1))

		# Return a list of the four integers.
		# This list will be the main driver for the dungeon generation. 
		# It sets where the rooms wil be built and their size.
        print ("w:", vertical, "h: ", horizontal, "x: ", x, "y: ", y)
        return [x, y, vertical, horizontal]

    # Function to sort the rooms and make sure there are connecting doors
    # or entries so the map is traverseable. This fixes the problem I was having
    # of rooms existing detached from each other.
    def DungeonConnections(self, rooma, roomb):
        # Store room a and b in a list.
        list_of_rooms = [rooma, roomb]
        # Big shout out to pcg.wiki.com for providing this amazing lambda.
        list_of_rooms.sort(key=lambda x_y: x_y[0])
        
        rooma_x      = list_of_rooms[0][0]
        rooma_y      = list_of_rooms[0][1]
        rooma_width  = list_of_rooms[0][2]
        rooma_height = list_of_rooms[0][3]
        rooma_test_x = rooma_x + rooma_width - 1
        rooma_test_y = rooma_y + rooma_height - 1

        # Now the same for the second room.
        roomb_x      = list_of_rooms[1][0]
        roomb_y      = list_of_rooms[1][1]
        roomb_width  = list_of_rooms[1][2]
        roomb_height = list_of_rooms[1][3]
        roomb_test_x = roomb_x + roomb_width - 1
        roomb_test_y = roomb_y + roomb_height - 1

        # Now check if there are any unwanted collisions between rooms.
        # First do this by checking collisions along the vertical plane, and then
        # in another loop we can check the horizontal plane.
        # TEMPORARY -> this calls so infrequently it might not be needed, but if later
        # down the line we get some problems then we can solve it here. Lazy coding,
        # sorry future Rob.
        if rooma_x < (roomb_x + roomb_width) and roomb_x < (rooma_x + rooma_width):
            i = 1

        


    def DungeonGenerate(self):
		# Start by building a dungeon of empty tiles.
        for x in range(self.height):
            self.dungeon.append(['stone'] * self.width)
		# Double check we're setting the rooms list to empty - it's done in the
		# constructor but may have been changed in other functions.
        self.rooms = []

		# Probably a bad variable name.
        room_iterator = self.max_rooms * 5

        for i in range(room_iterator):
            # In this for loop we cycle through the iterator and
            # generate new rooms with random coordinates.
            # After storing these in temporary lists we append them to the global rooms list.
            new_room = self.dungeonBuildRoom()
            self.rooms.append(new_room)
			# Make sure we're sticking to the defined maximum rooms.
			# At the moment this is a constant, but should be changeable from command line.
            if len(self.rooms) >= self.max_rooms:
                 break

            for aroom in range(len(self.rooms) - 1):
                self.DungeonConnections(self.rooms[aroom], self.rooms[aroom + 1])
		# Begin setting the tiles.
		# Can maybe split this into a function call...
        # The first run sets the floors.
        for room_id, room in enumerate(self.rooms):
            for second_run in range(room[2]):
                for third_run in range(room[3]):
                    self.dungeon[room[1] + third_run][room[0] + second_run] = 'floor'


        for across in range(1, self.height - 1):
            for up in range(1, self.width - 1):
                if self.dungeon[across][up] == 'floor':
                    # If we've reached a floor, check the adjacent tiles.
                    # At this point we're decided whether or not to add a wall
                    # or a door.
                    if self.dungeon[across - 1][up - 1] == 'stone':
                        self.dungeon[across - 1][up - 1] = 'wall'

                    if self.dungeon[across - 1][up] == 'stone':
                        self.dungeon[across - 1][up] = 'wall'

                    if self.dungeon[across - 1][up + 1] == 'stone':
                        self.dungeon[across - 1][up + 1] = 'wall'

                    if self.dungeon[across][up - 1] == 'stone':
                        self.dungeon[across][up - 1] = 'wall'

                    if self.dungeon[across][up + 1] == 'stone':
                        self.dungeon[across][up + 1] = 'wall'

                    if self.dungeon[across + 1][up - 1] == 'stone':
                        self.dungeon[across + 1][up - 1] = 'wall'

                    if self.dungeon[across + 1][up] == 'stone':
                        self.dungeon[across + 1][up] = 'wall'

                    if self.dungeon[across + 1][up + 1] == 'stone':
                        self.dungeon[across + 1][up + 1] = 'wall'

    def drawDungeon(self):
        for x_num, x in enumerate(self.dungeon):
            tmp = []
            for y_num, y in enumerate(x):
                if y == 'stone':
                    tmp.append(self.tiles['stone'])
                if y == 'floor':
                    tmp.append(self.tiles['floor'])
                if y == 'wall':
                    tmp.append(self.tiles['wall'])
            self.tiles_level.append(''.join(tmp))
        print('Room List: ', self.rooms)
        [print(x) for x in self.tiles_level]






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
	
	print(dg.tile)

def DungeonGenerate():
	# Initialize a room with rows and columns.
	row_rooms = 2 * (dg.height // SCREEN_HEIGHT)
	col_rooms = 2 * (dg.width // SCREEN_WIDTH)

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
    dg.panel.max_rows = (dg.height // SCREEN_HEIGHT) * 2 - 2
    dg.panel.max_cols = (dg.width // SCREEN_WIDTH) * 2 - 2

    dg.panel.row = dg.panel.max_rows
    dg.panel.col = dg.panel.max_cols

    DungeonGenerate()

def main():
	seedsInitialize(0)
	testGen = DungeonGenerator()
	testGen.DungeonGenerate()
	testGen.drawDungeon()
	#generateCave()


main()