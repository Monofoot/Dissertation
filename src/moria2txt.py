#!/usr/bin/env python
# Talk to Gaius about this. Easily reversible if it proves
# a bad idea.
from moria2txtconfig import *
import time
import argparse
# I'm really unhappy about doing this,
# but didn't want to write a function for random selection of strings.
# If I have time then I will come back and change this.
import random

# Allow user to input variables which will affect Moria's
# constants.
parser = argparse.ArgumentParser(description="Map generator for Penguin Tower's ASCII levels.")
parser.add_argument("--maxrooms", help="Set the maximum amount of rooms.")
parser.add_argument("--minrooms", help="Set the minimum amount of rooms.")
parser.add_argument("--maxsize", help="Set the maximum size of each room.")
parser.add_argument("--minsize", help="Set the minimum size of each room.")
parser.add_argument("--height", help="The height of the dungeon.")
parser.add_argument("--width", help="The width of the dungeon.")
parser.add_argument("--tunnelsize", help="The minimum width of each tunnel. Handy for arena-type maps.")
args = parser.parse_args()

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
def randomBetweenAB(min, max):
    # TO-DO:
    # this function is broken. It works with lower
    # order number but seems to fall apart when it comes to
    # generating the tunnels. For now I'm going to substitute it
    # with random.int, but it means that tunnels will be left out of
    # potential seed reproduction. This makes me very sad
    # and when I have enough time I will come back here to write a very
    # pretty and mathematical min max generator.
    # I've read online that something like:
    # Math.floor(Math.random() * (myMax - myMin +1)) + myMin;
    # should work? Much like the randomNumber() function below.
    # return int(rnd() * (max - min + 1) + min)
    return int(rnd() % (max - min + 1) + min)

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

class DungeonGenerator():
    def __init__(self, min_size = 5, max_size = 10,
                height = MAX_HEIGHT, width = MAX_WIDTH, 
				random_room_count = 0):
        # Moria uses 32 dungeons consistently, but this should hopefully randomize that.
        # Check some user validation here.
        if args.maxrooms or args.minrooms:
            # Add an extra layer of validation for the maxrooms.
            # This is because we cannot allow them to exceed 19.
            # Moria usually defaults to around 32 but because of the Chisel porting
            # we run out of character spaces for rooms above 19.
            # Actually... this might not be true..... double check this
            # If we just have a max room, default the min room
            if not args.minrooms: 
            # Else if we just have the min room, default the max room
            # Uhh.... For now let's default it to 1, that seems safe.
                args.minrooms = 1
            elif not args.maxrooms:
                # Moria uses the mean of 32 rooms as default.
                args.maxrooms = randomNumber(DUN_ROOMS_MEAN)
            self.random_room_count = randomBetweenAB(int(args.maxrooms), int(args.minrooms))
        else:
            self.random_room_count = randomNumber(DUN_ROOMS_MEAN)
        if args.maxsize:
            self.max_size = int(args.maxsize)
        else:
            self.max_size = max_size
        if args.minsize:
            self.min_size = int(args.minsize)
        else:
            self.min_size = min_size
        if args.height:
            self.height = int(args.height)
        else:
            self.height = height
        if args.width:
            self.width = int(args.width)
        else:
            self.width = width
        self.rooms = []
        self.dungeon = []
        self.tiles = TILES
        self.tiles_level = []
        self.tunnels = []

        # Soon I'd like to be able to set these parameters
        # through the command line, it should be easy enough.

    def DungeonBuildRoom(self):
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
        return [x, y, vertical, horizontal]

    def CreateTunnel(self, x, y, x1, y1, join='xy'):
        if x == x1 and y == y1 or x == x1 or y == y1:
            return [(x, y), (x1, y1)]
        else:
            # Hopefully our 'join' parameter works here. ...currently experimental.
            jtype = None
            # Do some set theory here. Thankfully we don't need to do the math ourself as
            # the magic of Python provides a function for this.
            if join is 'xy' and set([0, 1]).intersection(set([x, x1, y, y1])):
                jtype = 'bottom'
            elif join is 'xy' and set([self.width - 1, self.width - 2]).intersection(set([x, x1])) or set(
                 [self.height - 1, self.height - 2]).intersection(set([y, y1])):
                jtype = 'top'
            # We must have at least one choice (otherwise we're returning None), so use random choice to decide a top
            # or bottom. To-do would be to write my own random choice function if I have time.
            elif join is 'xy':
                jtype = random.choice(['top', 'bottom'])
            else:
                # Last case. If we're not random enough, force this.
                jtype = join
            # Finally, perform actions based on whether we're top or bottom:
            if jtype is 'bottom':
                return [(x, y), (x1, y), (x1, y1)]
            elif jtype is 'top':
                return [(x, y), (x, y1), (x1, y1)]
            # NOTE: If we're running into issues, put a print statement in the DungeonGenerate function.
            # If self.tunnels is returning ANY none, then something is wrong in this function. We are expecting
            # none nones! In the future I'd like to add some validation here to make sure that never happens,
            # but for the time being it doesn't seem to be an issue.

    # Function to sort the rooms and make sure there are connecting doors
    # or entries so the map is traverseable. This fixes the problem I was having
    # of rooms existing detached from each other.
    # TO-DO: Tunnel generation is currently breaking my min max generator.
    # Figure it out when you have enough time. :(
    def DungeonConnections(self, rooma, roomb, join='xy'):
        # Store room a and b in a list.
        sorted_room = [rooma, roomb]
        # Use a lambda to sort the rooms. This essentially sets the
        # lesser of the two rooms as the first room.
        sorted_room.sort(key=lambda x_y: x_y[0])
 
        rooma_x = sorted_room[0][0]
        rooma_y = sorted_room[0][1]
        rooma_width = sorted_room[0][2]
        rooma_height = sorted_room[0][3]
        rooma_x_2 = rooma_x + rooma_width - 1
        rooma_y_2 = rooma_y + rooma_height - 1
 
        # Now the same for the second room.
        roomb_x = sorted_room[1][0]
        roomb_y = sorted_room[1][1]
        roomb_width = sorted_room[1][2]
        h2 = sorted_room[1][3]
        roomb_x_2 = roomb_x + roomb_width - 1
        roomb_y_2 = roomb_y + h2 - 1
 
        # So what we're essentially doing here is checking if the x of room a is greater than
        # the width and x of room a and the x of room b is greater than the x of room a and room a's width.
        # If it is then we do a bit of randomBetweenAB magic and connect them with tunnels.
        if rooma_x < (roomb_x + roomb_width) and roomb_x < (rooma_x + rooma_width):
            jrooma_x = randomBetweenAB(roomb_x, rooma_x_2)
            jroomb_x = jrooma_x
            tmp_y = [rooma_y, roomb_y, rooma_y_2, roomb_y_2]
            tmp_y.sort()
            jrooma_y = tmp_y[1] + 1
            jroomb_y = tmp_y[2] - 1
 
            # Now that we have the coordinates we can
            # generate tunnels to link the rooms.
            tunnel = self.CreateTunnel(jrooma_x, jrooma_y, jroomb_x, jroomb_y)
            self.tunnels.append(tunnel)
 
        # Do the same as above but for the y coordinates now.
        elif rooma_y < (roomb_y + h2) and roomb_y < (rooma_y + rooma_height):
            if roomb_y > rooma_y:
                jrooma_y = randomBetweenAB(roomb_y, rooma_y_2)
                jroomb_y = jrooma_y
            else:
                jrooma_y = randomBetweenAB(rooma_y, roomb_y_2)
                jroomb_y = jrooma_y
            tmp_x = [rooma_x, roomb_x, rooma_x_2, roomb_x_2]
            tmp_x.sort()
            jrooma_x = tmp_x[1] + 1
            jroomb_x = tmp_x[2] - 1
 
            tunnel = self.CreateTunnel(jrooma_x, jrooma_y, jroomb_x, jroomb_y)
            self.tunnels.append(tunnel)
 
        # However, if there's no collisions then we generate our own links:
        else:
            jtype = None
                # Not happy using random choice here, hopefully will
                # have enough time to write my own random choice function.
            if join is 'xy':
                jtype = random.choice(['top', 'bottom'])
            # If it's not xy, then set our type to whatever is being parsed.
            # Most of the time this will just default to xy, though.
            else:
                jtype = join
 
            # Here is our logic. So, depending on what our jtype is, we can
            # generate our tunnels along this function.
            if jtype is 'top':
                if roomb_y > rooma_y:
                    jrooma_x = rooma_x_2 + 1
                    jrooma_y = randomBetweenAB(rooma_y, rooma_y_2)
                    jroomb_x = randomBetweenAB(roomb_x, roomb_x_2)
                    jroomb_y = roomb_y - 1
                    # We're at the botton here, so set it to generate along the bottom.
                    tunnel = self.CreateTunnel(jrooma_x, jrooma_y, jroomb_x, jroomb_y, 'bottom')
                    self.tunnels.append(tunnel)
                # Else we must be at the top, so generate the top.
                else:
                    jrooma_x = randomBetweenAB(rooma_x, rooma_x_2)
                    jrooma_y = rooma_y - 1
                    jroomb_x = roomb_x - 1
                    jroomb_y = randomBetweenAB(roomb_y, roomb_y_2)
                    tunnel = self.CreateTunnel(jrooma_x, jrooma_y, jroomb_x, jroomb_y, 'top')
                    self.tunnels.append(tunnel)
 
            # Same as above but flipping the x - we're at the bottom now.
            elif jtype is 'bottom':
                if roomb_y > rooma_y:
                    jrooma_x = randomBetweenAB(rooma_x, rooma_x_2)
                    jrooma_y = rooma_y_2 + 1
                    jroomb_x = roomb_x - 1
                    jroomb_y = randomBetweenAB(roomb_y, roomb_y_2)
                    tunnel = self.CreateTunnel(jrooma_x, jrooma_y, jroomb_x, jroomb_y, 'top')
                    self.tunnels.append(tunnel)
                else:
                    jrooma_x = rooma_x_2 + 1
                    jrooma_y = randomBetweenAB(rooma_y, rooma_y_2)
                    jroomb_x = randomBetweenAB(roomb_x, roomb_x_2)
                    jroomb_y = roomb_y_2 + 1
                    tunnel = self.CreateTunnel(jrooma_x, jrooma_y, jroomb_x, jroomb_y, 'bottom')
                    self.tunnels.append(tunnel)
        

    def DungeonGenerate(self):
		# Start by building a dungeon of empty tiles.
        for x in range(self.height):
            self.dungeon.append(['empty'] * self.width)
		# Double check we're setting the rooms list AND tunnels to empty - it's done in the
		# constructor but may have been changed in other functions.
        self.rooms = []
        self.tunnels = []

		# Probably a bad variable name.
        room_iterator = self.random_room_count * 5

        for i in range(room_iterator):
            # In this for loop we cycle through the iterator and
            # generate new rooms with random coordinates.
            # After storing these in temporary lists we append them to the global rooms list.
            new_room = self.DungeonBuildRoom()
            self.rooms.append(new_room)
			# Make sure we're sticking to the defined maximum rooms.
			# At the moment this is a constant, but should be changeable from command line.
            if len(self.rooms) >= self.random_room_count:
                 break

        for aroom in range(len(self.rooms) - 1):
            self.DungeonConnections(self.rooms[aroom], self.rooms[aroom + 1])

		# Begin setting the tiles.
		# Can maybe split this into a function call...
        # The first run sets the floors.
        # The second run sets the room numbers in the corner of each room.
        for room_id, room in enumerate(self.rooms):
            for second_run in range(room[2]):
                for third_run in range(room[3]):
                    self.dungeon[room[1] + third_run][room[0] + second_run] = 'floor'
                    self.dungeon[room[1] + 1][room[0] + 1] = room_id

        # Draw the tunnels here. We're doing the same for the room generation up above,
        # but this time we use the tunnels list instead of the rooms list.
        # It's important we allow validation for the third element in the tunnel list -
        # lots of time spent tracking down that bug.
        # Important to keep the spacing +2, as Chisel will not understand a one-space tunnel.
        # The argparse kind of works here, but is very prone to going out of bounds...
        # It might be worth just leaving it at a +2 default?
        if args.tunnelsize:
            for tunnel in self.tunnels:
                x, y = tunnel[0] # Start
                x1, y1 = tunnel[1] # End
                for across in range(abs(x - x1) + int(args.tunnelsize)):
                    for up in range(abs(y - y1) + int(args.tunnelsize)):
                        # If across is ever greater than one then it means
                        # we're travelling along the x axis. This means
                        # that we need to draw the doors up.
                        if across > 1:
                            self.dungeon[min(y, y1) + up][min(x, x1)] = 'door'
                        elif up > 1:
                            self.dungeon[min(y, y1)][min(x, x1) + across] = 'door'
                        self.dungeon[min(y, y1) + up][min(x, x1) + across] = 'floor'
                
                # Corners.
                if len(tunnel) == 3:
                    x2, y2 = tunnel[2]

                    for across in range(abs(x1 - x2) + int(args.tunnelsize)):
                        for up in range(abs(y1 - y2) + int(args.tunnelsize)):
                            if across > 1:
                                self.dungeon[min(y1, y2) + up][min(x1, x2)] = 'door'
                            elif up > 1:
                                self.dungeon[min(y1, y2)][min(x1, x2) + across] = 'door'
                            self.dungeon[min(y1, y2) + up][min(x1, x2) + across] = 'floor'
        else:
            for tunnel in self.tunnels:
                x, y = tunnel[0] # Start
                x1, y1 = tunnel[1] # End
                for across in range(abs(x - x1) + 2):
                    for up in range(abs(y - y1) + 2):
                        # If across is ever greater than one then it means
                        # we're travelling along the x axis. This means
                        # that we need to draw the doors up.
                        if across > 1:
                            #self.dungeon[min(y, y1) + up][min(x, x1)] = 'door'
                            i = 1
                        elif up > 1:
                            #self.dungeon[min(y, y1)][min(x, x1) + across] = 'door'
                            i =1 
                        self.dungeon[min(y, y1) + up][min(x, x1) + across] = 'floor'
                
                # Corners.
                # Door generation with corners is suuuuuper iffy right now.
                # I've got it working for the most part, but as dungeons get more complex
                # it seems to sometimes push against the very end of the tunnel corner
                # and delete the wall there. Currently this isn't a problem with dungeons with around 4 - 8 rooms,
                # but any more and it can get very buggy.
                # I have a theory it could be because there are two tunnels heading in the same direction
                # when this happens and it causes the doors to be placed in the middle of them (the very corner).
                # BUG HUNTING UPDATE: The bug ONLY occurs when the tunnel goes UP and then ACROSS. ACROSS and UP works fine?

                # ###################
                #  bug in corners like this
                # ###################
                # # 
                # # 
                if len(tunnel) == 3:
                    x2, y2 = tunnel[2]

                    for across in range(abs(x1 - x2) + 2):
                        for up in range(abs(y1 - y2) + 2):
                            if across > 1:
                                # This seems to be where the bug is coming from..
                                print("We are in the across tunnel.")
                                self.dungeon[min(y, y1)][min(x, x1) + up] = 'door'
                                # I think we might need an extra conditional here. 
                            elif up > 1:
                                self.dungeon[min(y, y1) + across][min(x, x1)] = 'door'
                            self.dungeon[min(y1, y2) + up][min(x1, x2) + across] = 'floor'
                
        # Set the walls by deciding if we're at the edge of a floor tile.
        for across in range(1, self.height - 1):
            for up in range(1, self.width - 1):
                if self.dungeon[across][up] == 'floor':
                    # If we've reached a floor, check the adjacent tiles.
                    # At this point we're decided whether or not to add a wall
                    # or a door.
                    if self.dungeon[across - 1][up - 1] == 'empty':
                        self.dungeon[across - 1][up - 1] = 'wall'

                    if self.dungeon[across - 1][up] == 'empty':
                        self.dungeon[across - 1][up] = 'wall'

                    if self.dungeon[across - 1][up + 1] == 'empty':
                        self.dungeon[across - 1][up + 1] = 'wall'

                    if self.dungeon[across][up - 1] == 'empty':
                        self.dungeon[across][up - 1] = 'wall'

                    if self.dungeon[across][up + 1] == 'empty':
                        self.dungeon[across][up + 1] = 'wall'

                    if self.dungeon[across + 1][up - 1] == 'empty':
                        self.dungeon[across + 1][up - 1] = 'wall'

                    if self.dungeon[across + 1][up] == 'empty':
                        self.dungeon[across + 1][up] = 'wall'

                    if self.dungeon[across + 1][up + 1] == 'empty':
                        self.dungeon[across + 1][up + 1] = 'wall'

    def DrawDungeon(self):
        for x_num, x in enumerate(self.dungeon):
            tmp = []
            for y_num, y in enumerate(x):
                if y == 'empty':
                    tmp.append(self.tiles['empty'])
                if y == 'floor':
                    tmp.append(self.tiles['floor'])
                if y == 'wall':
                    tmp.append(self.tiles['wall'])
                if y == 'door':
                    tmp.append(self.tiles['door'])
                # Also scan for the room_no key so we know this is
                # where our room numbers are.
                if isinstance(y, int):
                    tmp.append(str(y + 1))
            self.tiles_level.append(''.join(tmp))
        # Must pay strict attention to syntax in existing .txt maps.
        # Follow this format:
        #\n
        # define 1 room 1
        # define x room x
        #\n
        # define y extra
        #\n
        # map
        for room_id in enumerate(self.rooms):
            print("define", room_id[0] + 1, "room ", room_id[0] + 1)
        print("\n")
        [print(x) for x in self.tiles_level]

def main():
    # The seed initializer is GOOD .... but until we get rid of
    # the use of random.choice it won't be perfect. Shame.
	seedsInitialize(0)
	testGen = DungeonGenerator()
	testGen.DungeonGenerate()
	testGen.DrawDungeon()


main()