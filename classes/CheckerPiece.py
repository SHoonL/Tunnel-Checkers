# Tunnel Checker API
# Author : Seung Hun Lee
# Email  : lee.seunghu@husky.neu.edu
 
#### CheckerPiece ####

### Data Representation ###

## color   : Integer; represents the color of the checker piece instance;
##           0 is black and 1 is red.
## x_coord : Integer; represents the x coordinate of the checker piece instance.
## y_coord : Integer; represents the y coordinate of the checker piece instance.
## is_king : Boolean; represents the king status of the checker piece instance.
## step    : Tuple  ; represents the single step in move; each step is a coordinate
##           in the form of (x,y) where the checker piece instance can move to or
##           through.
## single_step_moves : List of step; represents all locations that the checker piece
##                     instance can move to in single step.
## eliminate_moves   : List of step; represents all paths that the checker piece
##                     instance can move through by eliminating opponent's checker
##                     at each single step.

class CheckerPiece:

	# constructor
	def __init__(self, color, x_coord, y_coord):
		self.color = color
		self.x_coord = x_coord
		self.y_coord = y_coord
		self.is_king = False
		self.single_step_moves = []
		self.elimination_moves = []


	### Properties for class attributes ###
	#*** @property = getter method and @fn.setter = setter methods

	## color attribute
	@property
	def color(self):
		return self.__color

	@color.setter
	def color(self, val):
		if isinstance(val,int) and (val == 0 or val == 1):
			self.__color = val
		else:
			raise AttributeError("Invalid type or value: \
				color must be <class \'int\'> and its value must be \
				zero or one.")

	## x_coord attribute
	@property
	def x_coord(self):
		return self.__x_coord

	@x_coord.setter
	def x_coord(self, val):
		if isinstance(val,int) and val >= 0 and val < 4:
			self.__x_coord = val
		else:
			raise AttributeError("Invalid type or value: \
				x_coord must be <class \'int\'> and its value must be \
				greater than or equal to zero and smaller than four.")

	## y_coord attribute
	@property
	def y_coord(self):
		return self.__y_coord

	@y_coord.setter
	def y_coord(self, val):
		if isinstance(val,int) and val >= 0 and val < 8:
			self.__y_coord = val
		else:
			raise AttributeError("Invalid type or value: \
				y_coord must be <class \'int\'> and its value must be \
				greater than or equal to zero and less than eight.")

	## is_king attribute
	@property
	def is_king(self):
		return self.__is_king

	@is_king.setter
	def is_king(self, val):
		if isinstance(val,bool):
			self.__is_king = val
		else:
			raise AttributeError("Invalid type: is_king must be \
				<class \'bool\'>.")

	## single_step_moves attribute
	@property
	def single_step_moves(self):
		return self.__single_step_moves

	@single_step_moves.setter
	def single_step_moves(self, val):
		if isinstance(val,list):
			self.__single_step_moves = val
		else:
			raise AttributeError("Invalid type: single_step_moves \
				must be <class \'list\'>.")

	## elimination_moves attribute
	@property
	def elimination_moves(self):
		return self.__elimination_moves

	@elimination_moves.setter
	def elimination_moves(self, val):
		if isinstance(val,list):
			self.__elimination_moves = val
		else:
			raise AttributeError("Invalid type: elimination_moves \
				must be <class \'list\'>.")
	

	### public methods ###

	# returns x and y coordinate in a tuple (x,y)
	def get_coords(self):
		return (self.x_coord,self.y_coord)

	# assigns the given values as new x and y coordinates
	def set_coords(self,x_crd,y_crd):
		self.x_coord = x_crd
		self.y_coord = y_crd
	
	

