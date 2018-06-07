# Tunnel Checker API
# Author : Seung Hun Lee
# Email  : lee.seunghu@husky.neu.edu

# Class GameBoard:

# Data representation:

# game_board : List of List of CheckerPiece; is the game board; game board is 8x8
#              , however, the implementation is 8x4 by choosing not to represent 
#              unusable grids. All 8x4 slots are occupied by CheckerPiece objects,
#              CheckerPiece object with color attribute set to None is considered
#              as a blank space, set to 0 is player1's piece and 1 is player2's piece.
# plyr1_score : Integer; is score of player 1 (Black pieces) in 2 player mode or 
#               AI in 1 player mode
# plyr2_score : Integer; is score of player 2 (Red pieces)
# plyr1_pieces : List of CheckerPiece; is list of player1's checker piece
#                currently on the board
# plyr2_pieces : List of CheckerPiece; is list of player2's checker piece
#                currently on the board
# current_turn : Integer; is current turn player; 0 is player1 (or AI) and 1 is player2
# opponent     : Integer; is current turn player's opponent; 0 is player1 (or AI) 
#                and 1 is player2
# current_direction : Integer; the forward direction of the current turn player 
# winner : Integer; is the winner of the game

import copy
from .CheckerPiece import CheckerPiece as cp

### Global Constants ###

_PLAYER1 = 0
_PLAYER2 = 1
_PLAYER1_FORWARD = 1
_PLAYER2_FORWARD = -1
_STEP_SIZE = 1
_GAME_BOARD_DIMENSION = 8
_MAX_SCORE = 12
_LEFT_END = 0
_RIGHT_END = (int(_GAME_BOARD_DIMENSION/2)-1)
_TOP_END = 0
_BOTTOM_END = (_GAME_BOARD_DIMENSION-1)
_MINIMAX_RECURSION_DEPTH = 3


class GameBoard:

	# Constructor
	def __init__(self):
		self.game_board = []
		self.plyr1_score = 0
		self.plyr2_score = 0
		self.plyr1_pieces = []
		self.plyr2_pieces = []
		self.current_turn = _PLAYER2
		self.opponent = _PLAYER1
		self.current_direction = _PLAYER2_FORWARD
		self.winner = None
		self.__game_initial_state()

	### Properties for class attributes ###

	#*** @property = getter method and @fn.setter = setter methods

	## game_board attribute
	@property
	def game_board(self):
		return self.__game_board

	@game_board.setter
	def game_board(self,val):
		if isinstance(val,list):
			self.__game_board = val
		else:
			raise AttributeError('Invalid type: game_board must be \
				<class \'list\'>.')

	## plyr1_score attribute
	@property
	def plyr1_score(self):
		return self.__plyr1_score

	@plyr1_score.setter
	def plyr1_score(self,val):
		if isinstance(val,int) and val >= 0 and val <= _MAX_SCORE:
			self.__plyr1_score = val
		else:
			raise AttributeError('Invalid type: plyr1_score must be \
				<class \'int\'>.')

	## plyr2_score attribute
	@property
	def plyr2_score(self):
		return self.__plyr2_score

	@plyr2_score.setter
	def plyr2_score(self,val):
		if isinstance(val,int) and val >= 0 and val <= _MAX_SCORE:
			self.__plyr2_score = val
		else:
			raise AttributeError('Invalid type: plyr2_score must be \
				<class \'int\'>.')

	## plyr1_pieces attribute
	@property
	def plyr1_pieces(self):
		return self.__plyr1_pieces

	@plyr1_pieces.setter
	def plyr1_pieces(self,val):
		if isinstance(val,list):
			self.__plyr1_pieces = val
		else:
			raise AttributeError('Invalid type: plyr1_pieces must be \
				<class \'list\'>.')

	## plyr2_pieces attribute
	@property
	def plyr2_pieces(self):
		return self.__plyr2_pieces

	@plyr2_pieces.setter
	def plyr2_pieces(self,val):
		if isinstance(val,list):
			self.__plyr2_pieces = val
		else:
			raise AttributeError('Invalid type: plyr2_pieces must be \
				<class \'list\'>.')

	## current_turn attribute
	@property
	def current_turn(self):
		return self.__current_turn

	@current_turn.setter
	def current_turn(self,val):
		if isinstance(val,int) and (val == _PLAYER1 or val == _PLAYER2):
			self.__current_turn = val
		else:
			raise AttributeError('Invalid type: current_turn must be \
				<class \'int\'>.')

	## opponent attribute
	@property
	def opponent(self):
		return self.__opponent

	@opponent.setter
	def opponent(self,val):
		if isinstance(val,int) and (val == _PLAYER1 or val == _PLAYER2):
			self.__opponent = val
		else:
			raise AttributeError('Invalid type: opponent must be \
				<class \'int\'>.')

	## current_direction attribute
	@property
	def current_direction(self):
		return self.__current_direction

	@current_direction.setter
	def current_direction(self,val):
		if isinstance(val,int) and \
			(val == _PLAYER1_FORWARD or val == _PLAYER2_FORWARD):
			self.__current_direction = val
		else:
			raise AttributeError('Invalid type: current_direction must be \
				<class \'int\'>.')

	## winner attribute
	@property
	def winner(self):
		return self.__winner

	@winner.setter
	def winner(self,val):
		if val == None or (isinstance(val,int) and \
			(val == _PLAYER1 or val == _PLAYER2)):
			self.__winner = val
		else:
			raise AttributeError('Invalid type: winner must be \
				<class \'int\'>.')


	### Public methods ###

	# returns a copy of the current game
	def get_game_copy(self):
		return copy.deepcopy(self)

	# returns the current game state
	def get_game_state(self):
		game_state = []
		game_state.append(self.__get_game_score())
		game_state.append(self.__get_opponent_piece_coords())
		game_state.append(self.__get_current_player_pieces_with_moves())
		return game_state

	# moves the given CheckerPiece object to the given destination
	def make_move(self,piece_coord,destn_coord):
		piece = self.game_board[piece_coord[1]][piece_coord[0]]
		move = self.__find_move(piece,destn_coord)
		self.__move_operation(piece,move)


	### Internal methods ###

	## initialize game board ##

	# initializes the game
	def __game_initial_state(self):
		self.__initialize_game_board()
		self.__set_available_moves()

	# initializes the game board
	def __initialize_game_board(self):
		board = []
		for row in range(_GAME_BOARD_DIMENSION):
			player = None
			checker_pieces = None
			if row < (int(_GAME_BOARD_DIMENSION/2)-1):
				player = _PLAYER1
			elif row > int(_GAME_BOARD_DIMENSION/2):
				player = _PLAYER2
			self.__generate_row(player,checker_pieces,board,row)
		self.game_board = board

	# returns a row of checker pieces
	def __generate_row(self,player,checker_pieces,board,row):
		if player is not None:
			checker_pieces = \
				[cp(player,col,row) for col in range(int(_GAME_BOARD_DIMENSION/2))]
			self.__set_reference_to_pieces(checker_pieces)
		else:
			checker_pieces = \
				[None for col in range(int(_GAME_BOARD_DIMENSION/2))]
		board.append(checker_pieces)

	# updates the references to each player's pieces
	def __set_reference_to_pieces(self,pieces):
		for piece in pieces:
			if piece.color is _PLAYER1:
				self.plyr1_pieces.append(piece)
			elif piece.color is _PLAYER2:
				self.plyr2_pieces.append(piece)

	## extract game state data ##

	# returns current game score
	def __get_game_score(self):	
		return [self.plyr1_score,self.plyr2_score]

	# returns coordinates of opponent's pieces
	def __get_opponent_piece_coords(self):
		piece_coords = []
		for piece in self.__get_player_pieces(self.opponent):
			piece_coords.append([piece.get_coords(),piece.is_king])
		return [self.opponent,piece_coords]

	# returns coordinates and moves of each of current player's pieces
	def __get_current_player_pieces_with_moves(self):
		piece_coords_with_moves = []
		for piece in self.__get_player_pieces(self.current_turn):
			piece_coords_with_moves.append([piece.get_coords(),
				piece.is_king,self.__collect_moves(piece)])
		return [self.current_turn,piece_coords_with_moves]

	# returns all possible destinations of movable pieces of current player
	def __all_available_destns(self,player_pieces,with_piece_coord):
		all_moves = []
		for piece in player_pieces:
			if with_piece_coord:
				all_moves.extend([[piece.get_coords(),move] for move in piece.single_step_moves])
				all_moves.extend([[piece.get_coords(),move[::-1][0]] for move in piece.elimination_moves])
			# only destinations
			else:
				all_moves.extend([move for move in piece.single_step_moves])
				all_moves.extend([move[::-1][0] for move in piece.elimination_moves])
		return all_moves

	# return all available moves of a given piece
	def __collect_moves(self,piece):
		piece_moves = []
		if len(piece.single_step_moves) > 0:
			piece_moves.extend(piece.single_step_moves)
		if len(piece.elimination_moves) > 0:
			for elimination_move in piece.elimination_moves:
				piece_moves.append(elimination_move[len(elimination_move)-1])
		return piece_moves

	# gets the list of the current turn player's checker pieces
	def __get_player_pieces(self,player):
		if player is _PLAYER1:
			return self.plyr1_pieces
		else:
			return self.plyr2_pieces

	# updates available moves (single and elimination) of the current turn player
	def __set_available_moves(self):
		for piece in self.__get_player_pieces(self.current_turn):
			self.__set_single_step_moves(piece)
			self.__set_elimination_moves(piece)

	# updates available single moves 
	def __set_single_step_moves(self,piece):
		piece.single_step_moves = []
		move_coords = self.__get_coords_for_move(piece)
		piece.single_step_moves = self.__collect_single_moves(move_coords)
	
	# returns all valid single moves
	def __collect_single_moves(self,move_coords):
		single_moves = []
		for coord in move_coords:
			if (coord is not None) and (coord[1] >= _TOP_END and \
				coord[1] <= _BOTTOM_END) and \
				(self.game_board[coord[1]][coord[0]] is None):
				single_moves.append(coord)
		return single_moves
	
	# finds and updates all possible elimination moves including chained moves
	def __set_elimination_moves(self,piece):
		piece.elimination_moves = []
		elimination_moves = self.__collect_all_elimination_moves(piece)
		piece.elimination_moves = elimination_moves

	# returns all valid elimination moves
	def __collect_all_elimination_moves(self,piece):
		single_step_coords = self.__get_coords_for_move(piece)
		result_list = []
		self.__search_paths(piece,piece.is_king,single_step_coords,result_list,[])
		return result_list

	# returns a valid elimination move of a given piece
	def __search_paths(self,piece,is_king,single_step_coords,result_list,path):
		if not single_step_coords:
			pass
		else:
			single_step_coord = single_step_coords.pop()
			if single_step_coord is not None:
				x_crd = single_step_coord[0]
				y_crd = single_step_coord[1]
				# test1: the grid at a single step is a valid location and is not empty
				if y_crd >= _TOP_END and y_crd <= _BOTTOM_END and \
					self.game_board[y_crd][x_crd] is not None:
					self.__continue_if_opponent(piece,is_king,
						single_step_coord,result_list,path)
			return self.__search_paths(piece,is_king,single_step_coords,
				result_list,path[:])

	# tests and searches for elimination path of the given piece
	def __continue_if_opponent(self,piece,is_king,coord,result_list,path):
		# test2: piece at the single step is an opponent piece and the coordinate is not
		#        already in the path
		if self.game_board[coord[1]][coord[0]].color != self.current_turn and \
			not coord in path:
			piece_after_step = cp(self.current_turn,coord[0],coord[1])
			piece_after_step.is_king = is_king
			next_single_step_coords = \
				self.__get_coords_for_move(piece_after_step)
			direction = \
				self.__find_direction(piece.x_coord,piece.y_coord,coord)
			next_coord = next_single_step_coords[direction]
			path_extension = [coord,next_coord]
			self.__complete_elimination_step(next_coord[0],next_coord[1],
				is_king,result_list,path[:],path_extension)

	# tests and searches for elimination path of the given piece
	def __complete_elimination_step(self,next_coord_x,next_coord_y,is_king,
		result_list,path,path_extension):
		if next_coord_y >= _TOP_END and next_coord_y <= _BOTTOM_END \
			and self.game_board[next_coord_y][next_coord_x] is None:
			path.extend(path_extension)
			result_list.append(path)
			piece_after_elimination = cp(self.current_turn,next_coord_x,next_coord_y)
			piece_after_elimination.is_king = is_king
			next_single_step_for_chain_eliminiation_move = \
				self.__get_coords_for_move(piece_after_elimination)
			self.__search_paths(piece_after_elimination,is_king,
				next_single_step_for_chain_eliminiation_move,
				result_list,path[:])


	# finds direction to continue using current location of 
	# piece object and first step move [0 == northwest, 1 == northeast
	# , 2 == southwest, 3 == southeast]
	def __find_direction(self,piece_x,piece_y,single_coord):
		if (piece_x == _LEFT_END or piece_x == _RIGHT_END) and piece_y%2 == 1:
			if (single_coord[1]-piece_y) == -1:
				if (single_coord[0]-piece_x) == 0:
					return 1
				else:
					return 0
			else:
				if (single_coord[0]-piece_x) == 0:
					return 3
				else:
					return 2
		else:
			if piece_y%2 == 0:
				if (single_coord[1]-piece_y) == -1:
					if (single_coord[0]-piece_x) == 0:
						return 0
					else:
						return 1
				else:
					if (single_coord[0]-piece_x) == 0:
						return 2
					else:
						return 3
			else:
				if (single_coord[1]-piece_y) == -1:
					if (single_coord[0]-piece_x) == -1:
						return 0
					else:
						return 1
				else:
					if (single_coord[0]-piece_x) == -1:
						return 2
					else:
						return 3

	
	# finds all coordinate within single step 
	def __get_coords_for_move(self,piece):
		x_coords = self.__get_x_coords_for_move(piece)
		y_coords = self.__get_y_coords_for_move(piece)
		move_coord_list = []
		for y_coord in y_coords:
			for x_coord in x_coords:
				move_coord_list.append((x_coord,y_coord))
		if not piece.is_king:
			if self.current_direction == _PLAYER1_FORWARD:
				move_coord_list = [None,None] + move_coord_list
			else:
				move_coord_list = move_coord_list + [None,None]
		return move_coord_list

	# finds x coordinates for move
	def __get_x_coords_for_move(self,piece):
		x_coords = []
		# when piece location is right end of game board
		if piece.x_coord == _RIGHT_END:
			if (piece.y_coord % 2) == 0:
				x_coords = [_RIGHT_END,_LEFT_END]
			else:
				x_coords = [(_RIGHT_END-_STEP_SIZE),_RIGHT_END]
		# when piece location is left end of game board
		elif piece.x_coord == _LEFT_END:
			if (piece.y_coord % 2) == 0:
				x_coords = [_LEFT_END,(_LEFT_END+_STEP_SIZE)]
			else:
				x_coords = [_RIGHT_END,_LEFT_END]
		else:
			if (piece.y_coord % 2) == 0:
				x_coords = [piece.x_coord,(piece.x_coord+_STEP_SIZE)]
			else:
				x_coords = [(piece.x_coord-_STEP_SIZE),piece.x_coord]
		return x_coords

	# finds y coordinates for move
	def __get_y_coords_for_move(self,piece):
		y_coords = []
		if piece.is_king:
			y_coords = [(piece.y_coord-_STEP_SIZE),(piece.y_coord+_STEP_SIZE)]
		else:
			y_coords = [piece.y_coord+self.current_direction]
		return y_coords
		
	# returns a move of the given piece that matches the given destination
	def __find_move(self,piece,destn_coord):
		moves = []
		moves.extend(piece.single_step_moves)
		moves.extend(piece.elimination_moves)
		for move in moves:
			last_coord = move
			if isinstance(move,list):
				last_coord = move[::-1][0]
			if last_coord == destn_coord:
				return move
	
	# eliminates opponent pieces in path and moves the given piece to its destination
	def __move_operation(self,piece,move):
		if isinstance(move,tuple):
			self.__move_piece(piece,move)
			self.__end_of_turn_update()
		else:
			first_step = move[0]
			# elimination operation continues till destination is reached
			if len(move) == 2:
				move.remove(first_step)
				self.__eliminate_piece(first_step)
				self.__move_operation(piece,move[0])
			else:
				self.__eliminate_piece(first_step)
				move = move[2:]
				self.__move_operation(piece,move)

	# eliminate an opponent's checker piece and increaments score
	def __eliminate_piece(self,piece_coord):
		eliminated_piece = self.game_board[piece_coord[1]][piece_coord[0]]
		self.game_board[piece_coord[1]][piece_coord[0]] = None
		self.__get_player_pieces(self.opponent).remove(eliminated_piece)
		self.__increment_current_player_score()

	# sets up the next turn
	def __set_next_turn(self):
		if self.current_turn == _PLAYER2:
			self.current_turn = _PLAYER1
			self.opponent = _PLAYER2
			self.current_direction = _PLAYER1_FORWARD
		else:
			self.current_turn = _PLAYER2
			self.opponent = _PLAYER1
			self.current_direction = _PLAYER2_FORWARD

	# sets the winner of the game if there is one
	# case1: a player elimianted all of opponent's pieces
	# case2: one or both players have no more available moves
	def __set_winner(self):
		if (self.plyr1_score != 0 and self.plyr2_score != 0) and \
			not self.__all_available_destns(self.__get_player_pieces(self.opponent),False):
			plyr1_eval = self.__evaluate_player(_PLAYER1)
			plyr2_eval = self.__evaluate_player(_PLAYER2)
			if plyr1_eval > plyr2_eval:
				self.winner = _PLAYER1
			else:
				self.winner = _PLAYER2
		else:
			if self.plyr1_score == _MAX_SCORE:
				self.winner = _PLAYER1
			elif self.plyr2_score == _MAX_SCORE:
				self.winner = _PLAYER2

	# makes adjustments by removing piece at the old location with
	# the piece at a new location after the turn
	def __end_of_turn_update(self):
		self.__set_winner()
		self.__set_next_turn()
		if self.winner is None:
			self.__set_available_moves()

	# increments current player's score when the player eliminates 
	# an opponent's checker piece
	def __increment_current_player_score(self):
		if self.current_turn == _PLAYER2:
			self.plyr2_score += 1
		else:
			self.plyr1_score += 1

	# moves the given piece to the given destination
	def __move_piece(self,piece,destn_coord):
		self.game_board[destn_coord[1]][destn_coord[0]] = piece
		self.game_board[piece.y_coord][piece.x_coord] = None
		piece.set_coords(destn_coord[0],destn_coord[1])
		# makes the moved piece king if it is not already a king and reaches 
		# top or bottom edge of the game board
		if (destn_coord[1] == _TOP_END or destn_coord[1] == _BOTTOM_END) \
			and not piece.is_king:
			piece.is_king = True

	# evaluates the given player and returns the total score
	# Total score = current score + non-king piece count + (2 *  king piece count)
	def __evaluate_player(self,player):
		score = self.__get_game_score()[player]
		piece_count = 0
		king_count = 0
		if self.current_turn == player:
			for piece in self.__get_player_pieces(player):
				if piece.is_king:
					king_count+=1
				else:
					piece_count+=1
		return score+piece_count+(king_count*2)

	# minimax algorithm returns the best possible move searching through 
	# the game tree of depth _MINIMAX_RECURSION_DEPTH
	def minimax(self,game,depth):
		available_moves = \
			game.__all_available_destns(game.__get_player_pieces(game.current_turn),True)
		if depth == _MINIMAX_RECURSION_DEPTH or not available_moves \
			or game.winner is not None:
			return [None,None,game.__evaluate_player(game.current_turn)]
		# maximize when odd numbered depth
		elif depth%2 == 1:
			max_path = [None,None,float('-inf')]
			for move in available_moves:
				game_copy = game.get_game_copy()
				game_copy.make_move(move[0],move[1])
				path = game.minimax(game_copy,depth+1)
				# update maximum score
				if path[2] > max_path[2]:
					max_path = [move[0],move[1],path[2]]
			return max_path
		# minimize when even numbered depth
		else:
			min_path = [None,None,float('inf')]
			for move in available_moves:
				game_copy = game.get_game_copy()
				piece_in_copied_game = game_copy.get_game_copy()
				game_copy.make_move(move[0],move[1])
				path = game.minimax(game_copy,depth+1)
				# update minimum score
				if path[2] < min_path[2]:
					min_path = [move[0],move[1],path[2]]
			return min_path
			

	# minimax algorithm with alpha and beta pruning works faster than pure minimax algorithm
	def minimax_with_alpha_beta_prune(self,game,depth,alpha,beta):
		available_moves = \
			game.__all_available_destns(game.__get_player_pieces(game.current_turn),True)
		if depth == _MINIMAX_RECURSION_DEPTH or not available_moves \
			or game.winner is not None:
			return [None,None,game.__evaluate_player(game.current_turn)]
		# maximize when odd numbered depth
		elif depth%2 == 1:
			max_path = [None,None,float('-inf')]
			for move in available_moves:
				game_copy = game.get_game_copy()
				game_copy.make_move(move[0],move[1])
				path = game.minimax(game_copy,depth+1)
				# update maximum score
				if path[2] > max_path[2]:
					max_path = [move[0],move[1],path[2]]
				alpha = max(alpha,max_path[2]) 
				# prune
				if beta <= alpha:
					break
			return max_path
		# minimize when even numbered depth
		else:
			min_path = [None,None,float('inf')]
			for move in available_moves:
				game_copy = game.get_game_copy()
				piece_in_copied_game = game_copy.get_game_copy()
				game_copy.make_move(move[0],move[1])
				path = game.minimax(game_copy,depth+1)
				# update minimum score
				if path[2] < min_path[2]:
					min_path = [move[0],move[1],path[2]]
				beta = min(beta,min_path[2])
				# prune
				if beta <= alpha:
					break
			return min_path