#!/usr/bin/env python

# Dungeon_t
class Dungeon_t:
	height = None
	width = None
	
	# Declare a panel instance here too.

# Coord_t
class Coord_t:
    x = None
	y = None

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