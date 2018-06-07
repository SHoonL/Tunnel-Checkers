# Tunnel Checker API
# Author : Seung Hun Lee
# Email  : lee.seunghu@husky.neu.edu

#### CheckerGameGUI ####

### Attribute Summary ###

## grid_coords : Dictionary; maps coordinates on GameBoard to coordinates
##               on tkinter Canvas. 
##               ex) key = '1_1', self.grid_coords[key] -> (190,285)
## game_mode_control_objects : List; contains references to tkinter Canvas objects
##                         that controls game mode.
## game_state_obj_list: List; contains references to tkinter Canvas objects
##                      that defines a game state.
## move_preview_obj_list: List; contains references to tkinter Canvas objects
##                        created for move preview of a movable checker piece.
## move_info   : Dictionary; maps movable checker piece to its moves; uses Canvas
##               object tag as key; and the returned value is list of moves.
##               ex) key = '0_5', move_info[key] = [(3,4),(0,4)] 
## selected_piece_coord: Tuple; coordinate of currently selected checker piece.
## move_data   : List; contains the move information of the current player in form of
##               [piece_coordinate,destination]
## game_instance: CheckerGame; a reference to the game instance that instantiated
##                the current instance of CheckerGameGUI
## window_size : Float; current window size
## window_size_selected : Boolean; True if the user has selected the game window size
## window      : tk.Tk; the window of the gui
## canvas      : tk.Canvas; the canvas where the game is being drawn

from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo

### Global Constants ###

### Dimensions for gameboard and background drawing ###

_ORIGIN = (0,0)
_GAME_BOARD_ROW = 8
_GAME_BOARD_COL = 8
_GAME_BOARD_HEIGHT = 640
_GAME_BOARD_WIDTH = 640
_GAME_WINDOW_HEIGHT = 700
_GAME_WINDOW_WIDTH = 700
_GAME_BOARD_MARGIN = 30
_GRID_HEIGHT = 80
_GRID_WIDTH = 80
_TOP_SECTION = 175
_PIECE_DIAMETER = 60
_PIECE_MARGIN = 10

### Dimensions for banner drawing ###

_BANNER_LEFT_RIGHT_MARGIN = 142
_BANNER_HEIGHT = 60
_BANNER_TOP_MARGIN = 8
_BANNER_WIDTH = 410


### Dimensions for game control drawing ###

_WINDOW_SIZE_LABEL_X_COORD = 8
_WINDOW_SIZE_LABEL_Y_COORD = 15
_WINDOW_SIZE_SMALL_BUTTON_X_COORD = 20
_WINDOW_SIZE_SMALL_BUTTON_Y_COORD = 38
_WINDOW_SIZE_MEDIUM_BUTTON_X_COORD = 55
_WINDOW_SIZE_MEDIUM_BUTTON_Y_COORD = 38
_WINDOW_SIZE_LARGE_BUTTON_X_COORD = 90
_WINDOW_SIZE_LARGE_BUTTON_Y_COORD = 38
_PLAYER_MODE_BUTTONS_LABEL_X_COORD = 20
_PLAYER_MODE_BUTTONS_LABEL_Y_COORD = 70
_SINGLE_PLAYER_BUTTON_X_COORD = 20
_SINGLE_PLAYER_BUTTON_Y_COORD = 98
_TWO_PLAYERS_BUTTON_X_COORD = 20
_TWO_PLAYERS_BUTTON_Y_COORD = 130
_AI_MODE_BUTTONS_LABEL_X_COORD = 594
_AI_MODE_BUTTONS_LABEL_Y_COORD = 70
_MINIMAX_BUTTON_X_COORD = 590
_MINIMAX_BUTTON_Y_COORD = 98
_MINIMAX_WITH_PRUNE_BUTTON_X_COORD = 590
_MINIMAX_WITH_PRUNE_BUTTON_Y_COORD = 130
_RESET_BUTTON_X_COORD = 290
_RESET_BUTTON_Y_COORD = 142


### Dimensions for scoreboard drawing ###

_SCORE_BOARD_LEFT_RIGHT_MARGIN = 250
_SCORE_BOARD_HEIGHT = 60
_SCORE_BOARD_TOP_MARGIN = 8
_SCORE_BOARD_WIDTH = 200
_SCORE_BOARD_PIECE_DIAMETER = 40
_SCORE_INTEGER_LEFT_MARGIN = 17
_SCORE_INTEGER_BOTTOM_MARGIN = 22
_SCORE_BOARD_TOP_LEFT_Y_COORD = \
	(_BANNER_TOP_MARGIN+_BANNER_HEIGHT+_SCORE_BOARD_TOP_MARGIN)
_SCORE_BOARD_BOTTOM_RIGHT_X_COORD = \
	(_SCORE_BOARD_LEFT_RIGHT_MARGIN+_SCORE_BOARD_WIDTH)
_SCORE_BOARD_BOTTOM_RIGHT_Y_COORD = \
	((_BANNER_HEIGHT+_BANNER_TOP_MARGIN)+(_SCORE_BOARD_HEIGHT+ \
		_SCORE_BOARD_TOP_MARGIN))
_SCORE_BOARD_MIDDLE_LINE_TOP_X_COORD = \
	(_SCORE_BOARD_LEFT_RIGHT_MARGIN+(_SCORE_BOARD_WIDTH/2))
_SCORE_BOARD_MIDDLE_LINE_TOP_Y_COORD = \
	(_BANNER_TOP_MARGIN+_BANNER_HEIGHT+_SCORE_BOARD_TOP_MARGIN)
_SCORE_BOARD_MIDDLE_LINE_BOTTOM_X_COORD = \
	(_SCORE_BOARD_LEFT_RIGHT_MARGIN+(_SCORE_BOARD_WIDTH/2))
_SCORE_BOARD_MIDDLE_LINE_BOTTOM_Y_COORD = \
	(_BANNER_TOP_MARGIN+_BANNER_HEIGHT+_SCORE_BOARD_TOP_MARGIN+_SCORE_BOARD_HEIGHT)
_SCORE_BOARD_FOR_PLAYER_1_PIECE_TOP_X_COORD = \
	(_SCORE_BOARD_LEFT_RIGHT_MARGIN+_PIECE_MARGIN)
_SCORE_BOARD_FOR_PLAYER_1_PIECE_TOP_Y_COORD = \
	(_BANNER_TOP_MARGIN+_BANNER_HEIGHT+_SCORE_BOARD_TOP_MARGIN+_PIECE_MARGIN)
_SCORE_BOARD_FOR_PLAYER_1_PIECE_BOTTOM_X_COORD = \
	(_SCORE_BOARD_LEFT_RIGHT_MARGIN+_PIECE_MARGIN+_SCORE_BOARD_PIECE_DIAMETER)
_SCORE_BOARD_FOR_PLAYER_1_PIECE_BOTTOM_Y_COORD = \
	(_BANNER_TOP_MARGIN+_BANNER_HEIGHT+_SCORE_BOARD_TOP_MARGIN+ \
		_PIECE_MARGIN +_SCORE_BOARD_PIECE_DIAMETER)
_SCORE_BOARD_FOR_PLAYER_2_PIECE_TOP_X_COORD = \
	(_SCORE_BOARD_LEFT_RIGHT_MARGIN+(_SCORE_BOARD_WIDTH/2)+_PIECE_MARGIN)
_SCORE_BOARD_FOR_PLAYER_2_PIECE_TOP_Y_COORD = \
	(_BANNER_TOP_MARGIN+_BANNER_HEIGHT+_SCORE_BOARD_TOP_MARGIN+_PIECE_MARGIN)
_SCORE_BOARD_FOR_PLAYER_2_PIECE_BOTTOM_X_COORD = \
	(_SCORE_BOARD_LEFT_RIGHT_MARGIN+(_SCORE_BOARD_WIDTH/2)+_PIECE_MARGIN+ \
		_SCORE_BOARD_PIECE_DIAMETER)
_SCORE_BOARD_FOR_PLAYER_2_PIECE_BOTTOM_Y_COORD = \
	(_BANNER_TOP_MARGIN+_BANNER_HEIGHT+_SCORE_BOARD_TOP_MARGIN+_PIECE_MARGIN+ \
		_SCORE_BOARD_PIECE_DIAMETER)
_PLAYER1_SCORE_X_COORD = (_SCORE_BOARD_LEFT_RIGHT_MARGIN+_PIECE_MARGIN+ \
	_SCORE_BOARD_PIECE_DIAMETER+_SCORE_INTEGER_LEFT_MARGIN)
_PLAYER1_SCORE_Y_COORD = (_BANNER_TOP_MARGIN+_BANNER_HEIGHT+_SCORE_BOARD_TOP_MARGIN+ \
	_PIECE_MARGIN +_SCORE_BOARD_PIECE_DIAMETER-_SCORE_INTEGER_BOTTOM_MARGIN)
_PLAYER2_SCORE_X_COORD = (_SCORE_BOARD_LEFT_RIGHT_MARGIN+(_SCORE_BOARD_WIDTH/2)+
	_PIECE_MARGIN+_SCORE_BOARD_PIECE_DIAMETER+_SCORE_INTEGER_LEFT_MARGIN)
_PLAYER2_SCORE_Y_COORD = (_BANNER_TOP_MARGIN+_BANNER_HEIGHT+_SCORE_BOARD_TOP_MARGIN+ \
	_PIECE_MARGIN+_SCORE_BOARD_PIECE_DIAMETER-_SCORE_INTEGER_BOTTOM_MARGIN)


### List of points for drawing a crown on King checker pieces ###

_CROWN_POLYGON = [(-18,0),(-20,-8),(-12,-3),(-14,-13),(-8,-6),(0,-20),
	(8,-6),(14,-13),(12,-3),(20,-8),(18,0),(18,11),(-18,11),(-18,0)]
_CROWN_JEWEL = [(-4,-9),(0,-15),(4,-9),(0,-3)]

### List of values for creating game mode control Checkbuttons ###

_CONTROL_BUTTON_LABEL_VAL_LIST = [[(_PLAYER_MODE_BUTTONS_LABEL_X_COORD,_PLAYER_MODE_BUTTONS_LABEL_Y_COORD),'Game Mode:'],
						[(_AI_MODE_BUTTONS_LABEL_X_COORD,_AI_MODE_BUTTONS_LABEL_Y_COORD),'AI Mode:'],
						[(_WINDOW_SIZE_LABEL_X_COORD,_WINDOW_SIZE_LABEL_Y_COORD),'Window Size:']]
_CONTROL_BUTTON_VAL_LIST = [[(_SINGLE_PLAYER_BUTTON_X_COORD,_SINGLE_PLAYER_BUTTON_Y_COORD),'1 Player'],
						[(_TWO_PLAYERS_BUTTON_X_COORD,_TWO_PLAYERS_BUTTON_Y_COORD),'2 Player'],
						[(_MINIMAX_BUTTON_X_COORD,_MINIMAX_BUTTON_Y_COORD),'Minimax'],
						[(_MINIMAX_WITH_PRUNE_BUTTON_X_COORD,_MINIMAX_WITH_PRUNE_BUTTON_Y_COORD),'w/ α&β'],
						[(_RESET_BUTTON_X_COORD,_RESET_BUTTON_Y_COORD),'RESET GAME']]

_CONTROL_BUTTON_WINDOW_SIZE = [[(_WINDOW_SIZE_SMALL_BUTTON_X_COORD,_WINDOW_SIZE_SMALL_BUTTON_Y_COORD),'Sm'],
							[(_WINDOW_SIZE_MEDIUM_BUTTON_X_COORD,_WINDOW_SIZE_MEDIUM_BUTTON_Y_COORD),'Md'],
							[(_WINDOW_SIZE_LARGE_BUTTON_X_COORD,_WINDOW_SIZE_LARGE_BUTTON_Y_COORD),'Lg']]

### List of hexidecimal color values used in drawing ### 

# 0 = greyish black, 1 = fading red, 2 = bright green, 3 = yellowish tan,
# 4 = brown, 5 = transparent
_COLORS = ["#2c2d2c","#aa1212","#3e913e","#ccc6af","#3f2713",""]

### List of font values used in drawing ### 

_FONT = 'Helvetica'

### List of Window size values ###

_SMALL = 2/3
_MEDIUM = 1.0
_LARGE = 1.3
_GAME_OVER_WIDTH = 450
_GAME_OVER_HEIGHT = 130
_INSTRUCTIONS_WIDTH = 450
_INSTRUCTIONS_HEIGHT = 180

class CheckerGameGUI:

	# Constructor
	def __init__(self,game_inst,windw_size,windw_size_selected):
		self.grid_coords = {}
		self.move_info = {}
		self.game_mode_control_objects = {}
		self.game_state_obj_list = []
		self.move_preview_obj_list = []
		self.selected_piece_coord = ()
		self.game_instance = game_inst
		self.window_size = windw_size
		self.window_size_selected = windw_size_selected
		self.window = tk.Tk()
		self.canvas = None
		self.draw_game()

	### Properties for class attributes ###
	#*** @property = getter method and @fn.setter = setter methods

	# grid_coords attribute
	@property
	def grid_coords(self):
		return self.__grid_coords

	@grid_coords.setter
	def grid_coords(self,val):
		if isinstance(val,dict):
			self.__grid_coords = val
		else:
			raise AttributeError('Invalid type: grid_coords must be \
				<class \'dict\'>.')

	# game_mode_control_objects attribute
	@property
	def game_mode_control_objects(self):
		return self.__game_mode_control_objects

	@game_mode_control_objects.setter
	def game_mode_control_objects(self,val):
		if isinstance(val,dict):
			self.__game_mode_control_objects = val
		else:
			raise AttributeError('Invalid type: game_mode_control_objects \
				must be <class \'dict\'>.')

	# game_state_obj_list attribute
	@property
	def game_state_obj_list(self):
		return self.__game_state_obj_list

	@game_state_obj_list.setter
	def game_state_obj_list(self,val):
		if isinstance(val,list):
			self.__game_state_obj_list = val
		else:
			raise AttributeError('Invalid type: game_state_obj_list \
				must be <class \'list\'>.')

	# move_preview_obj_list attribute
	@property
	def move_preview_obj_list(self):
		return self.__move_preview_obj_list

	@move_preview_obj_list.setter
	def move_preview_obj_list(self,val):
		if isinstance(val,list):
			self.__move_preview_obj_list = val
		else:
			raise AttributeError('Invalid type: move_preview_obj_list \
				must be <class \'list\'>.')

	# move_info attribute
	@property
	def move_info(self):
		return self.__move_info

	@move_info.setter
	def move_info(self,val):
		if isinstance(val,dict):
			self.__move_info = val
		else:
			raise AttributeError('Invalid type: move_info \
				must be <class \'dict\'>.')

	# selected_piece_coord attribute
	@property
	def selected_piece_coord(self):
		return self.__selected_piece_coord

	@selected_piece_coord.setter
	def selected_piece_coord(self,val):
		if isinstance(val,tuple):
			self.__selected_piece_coord = val
		else:
			raise AttributeError('Invalid type: selected_piece_coord \
				must be <class \'tuple\'>.')

	# game_instance attribute
	@property
	def game_instance(self):
		return self.__game_instance

	@game_instance.setter
	def game_instance(self,val):
		self.__game_instance = val

	# window attribute
	@property
	def window(self):
		return self.__window

	@window.setter
	def window(self,val):
		if isinstance(val,tk.Tk):
			self.__window = val
		else:
			raise AttributeError('Invalid type: window \
				must be <class \'tk.Tk\'>.')

	# canvas attribute
	@property
	def canvas(self):
		return self.__canvas

	@canvas.setter
	def canvas(self,val):
		if isinstance(val,tk.Canvas) or val is None:
			self.__canvas = val
		else:
			raise AttributeError('Invalid type: canvas \
				must be <class \'tk.Canvas\'>.')

	# window_size attribute
	@property
	def window_size(self):
		return self.__window_size

	@window_size.setter
	def window_size(self,val):
		if isinstance(val,float) or val is None:
			self.__window_size = val
		else:
			raise AttributeError('Invalid type: window_size \
				must be <class \'float\'>.')

	# window_size_selected attribute
	@property
	def window_size_selected(self):
		return self.__window_size_selected

	@window_size_selected.setter
	def window_size_selected(self,val):
		if isinstance(val,bool):
			self.__window_size_selected = val
		else:
			raise AttributeError('Invalid type: window_size_selected \
				must be <class \'bool\'>.')

	### Public methods ###

	# gets updated game state to draw from GameBoard instance
	def update_game_state(self,scores,opponent,current_player):
		self.move_info = {}
		self.__reset_piece_obj_list()
		self.__reset_move_preview_object_list()
		self.__draw_score(scores[0],scores[1])
		self.__draw_pieces(opponent)
		self.__draw_pieces(current_player)
		self.window.update()

	# resets the game to the initial setup state
	def reset(self):
		self.__reset_piece_obj_list()
		self.__reset_move_preview_object_list()
		self.__reset_game_control()
		self.__instructions()
		self.window.update()

	# enables or disables the window size control buttons
	def change_window_control(self,control):
		self.game_mode_control_objects['Sm'].config(state=control)
		self.game_mode_control_objects['Md'].config(state=control)
		self.game_mode_control_objects['Lg'].config(state=control)

	# ends the game and anounces the winner
	def end_game(self,winner):
		self.__place_window(self.window,_GAME_WINDOW_WIDTH,
			(_GAME_WINDOW_HEIGHT+_TOP_SECTION))
		winner_is = self.__who_is_winner(winner)
		pop_up_window = tk.Toplevel()
		pop_up_window.wm_title('Game Over!')
		pop_up_window.resizable(False,False)
		label = ttk.Label(pop_up_window,text=winner_is+' has won the game!',anchor=tk.CENTER,
			padding=4,font=(_FONT, int(18*self.window_size)))
		label.pack(side='top',fill='x',pady=int(20*self.window_size))
		button = ttk.Button(pop_up_window,text='Play again',command=lambda:(
			pop_up_window.destroy(),self.game_instance.reset()))
		button.pack()
		self.__place_window(pop_up_window,_GAME_OVER_WIDTH,_GAME_OVER_HEIGHT)
		pop_up_window.lift(aboveThis=self.canvas)


	## game board draw methods ##

	# draws the game gui
	def draw_game(self):
		self.window.wm_title('Tunnel Checkers')
		self.window.resizable(False,False)
		self.canvas = tk.Canvas(
			self.window,width=int(_GAME_WINDOW_WIDTH*self.window_size),
			height=int((_GAME_WINDOW_HEIGHT+_TOP_SECTION)*self.window_size))
		self.__place_window(self.window,_GAME_WINDOW_WIDTH,
			(_GAME_WINDOW_HEIGHT+_TOP_SECTION))
		self.__draw_banner()
		self.__draw_game_board()
		self.__draw_score_board()
		self.__draw_game_control()
		if not self.window_size_selected:
			self.__instructions()


	### Internal methods ###

	# draws the banner (Title) part of game gui
	def __draw_banner(self):
		# banner rectangle
		self.canvas.create_rectangle(
			int(_BANNER_LEFT_RIGHT_MARGIN*self.window_size),
			int(_BANNER_TOP_MARGIN*self.window_size),
			int((_BANNER_LEFT_RIGHT_MARGIN+_BANNER_WIDTH)*self.window_size),
			int((_BANNER_HEIGHT+_BANNER_TOP_MARGIN)*self.window_size),
			fill=_COLORS[3])
		# title text
		self.canvas.create_text(
			int((_GAME_WINDOW_HEIGHT/2)*self.window_size),
			int(((_BANNER_TOP_MARGIN)+(_BANNER_HEIGHT/2))*self.window_size),
			text='Let\'s Play Tunnel Checkers!',
			font=(_FONT, int(20*self.window_size)))

	# draws the game board (Title) part of game gui
	def __draw_game_board(self):
		# draw game board background in green
		self.canvas.create_rectangle(
			_ORIGIN[0],
			int((_ORIGIN[0]+_TOP_SECTION)*self.window_size),
			int(_GAME_WINDOW_WIDTH*self.window_size),
			int((_GAME_WINDOW_HEIGHT+_TOP_SECTION)*self.window_size),
			fill=_COLORS[2])
		# draw game board unused grids
		self.canvas.create_rectangle(
			int(_GAME_BOARD_MARGIN*self.window_size),
			int((_GAME_BOARD_MARGIN+_TOP_SECTION)*self.window_size),
			int((_GAME_BOARD_WIDTH+_GAME_BOARD_MARGIN)*self.window_size),
			int((_GAME_BOARD_HEIGHT+_GAME_BOARD_MARGIN+_TOP_SECTION)*self.window_size),
			fill=_COLORS[3])
		# draw game board playable grids
		self.__generate_game_grid(0,0,0)

	
	# draws the playable grids of the game board
	def __generate_game_grid(self,row,col,offset):
		if row == _GAME_BOARD_ROW:
			pass
		elif col < (_GAME_BOARD_COL/2):
			if row%2 == 0:
					offset += 1
			# offset value corrects the coordinate values for placement
			# of canvas objects
			# unused grids do not have tags. Therefore, row = 0 ~ 7 and col = 0 ~ 3
			obj_tag = (str(row)+'_'+str(col))
			self.__draw_cell(row,(col+offset),obj_tag)
			if row%2 == 1:
					offset += 1
			col+=1
			self.__generate_game_grid(row,col,offset)
		else:
			row+=1
			self.__generate_game_grid(row,0,0)

	# draws a playable grid
	def __draw_cell(self,row,col,obj_tag):
		if (row%2 == 0 and col%2 == 1) or (row%2 == 1 and col%2 == 0):
			# draw grid
			self.canvas.create_rectangle(
				int((_GAME_BOARD_MARGIN+(col*_GRID_WIDTH))*self.window_size),
				int((_GAME_BOARD_MARGIN+ _TOP_SECTION+(row*_GRID_HEIGHT))*self.window_size),
				int((_GAME_BOARD_MARGIN+((col+1)*_GRID_WIDTH))*self.window_size),
				int((_GAME_BOARD_MARGIN+_TOP_SECTION+((row+1)*_GRID_HEIGHT))*self.window_size),
				fill=_COLORS[4])
			# insert coordinate reference entry to the dictionary
			self.grid_coords.update(
				{obj_tag : (int(((_GAME_BOARD_MARGIN+(col*_GRID_WIDTH))*self.window_size)),
				int(((_GAME_BOARD_MARGIN+_TOP_SECTION+(row*_GRID_HEIGHT))*self.window_size)))})

	# draws the score board part of game gui (excluding the acutal scores)
	def __draw_score_board(self):
		# box
		self.canvas.create_rectangle(
			int(_SCORE_BOARD_LEFT_RIGHT_MARGIN*self.window_size),
			int(_SCORE_BOARD_TOP_LEFT_Y_COORD*self.window_size),
			int(_SCORE_BOARD_BOTTOM_RIGHT_X_COORD*self.window_size),
			int(_SCORE_BOARD_BOTTOM_RIGHT_Y_COORD*self.window_size),
			fill=_COLORS[3])
		# middle divider
		self.canvas.create_line(
			int(_SCORE_BOARD_MIDDLE_LINE_TOP_X_COORD*self.window_size),
			int(_SCORE_BOARD_MIDDLE_LINE_TOP_Y_COORD*self.window_size),
			int(_SCORE_BOARD_MIDDLE_LINE_BOTTOM_X_COORD*self.window_size),
			int(_SCORE_BOARD_MIDDLE_LINE_BOTTOM_Y_COORD*self.window_size))
		# smaller version of player one checker piece
		self.canvas.create_oval(
			int(_SCORE_BOARD_FOR_PLAYER_1_PIECE_TOP_X_COORD*self.window_size),
			int(_SCORE_BOARD_FOR_PLAYER_1_PIECE_TOP_Y_COORD*self.window_size),
			int(_SCORE_BOARD_FOR_PLAYER_1_PIECE_BOTTOM_X_COORD*self.window_size),
			int(_SCORE_BOARD_FOR_PLAYER_1_PIECE_BOTTOM_Y_COORD*self.window_size),
			fill=_COLORS[0],width=3*self.window_size)
		# smaller version of player two checker piece
		self.canvas.create_oval(
			int(_SCORE_BOARD_FOR_PLAYER_2_PIECE_TOP_X_COORD*self.window_size),
			int(_SCORE_BOARD_FOR_PLAYER_2_PIECE_TOP_Y_COORD*self.window_size),
			int(_SCORE_BOARD_FOR_PLAYER_2_PIECE_BOTTOM_X_COORD*self.window_size),
			int(_SCORE_BOARD_FOR_PLAYER_2_PIECE_BOTTOM_Y_COORD*self.window_size),
			fill=_COLORS[1],width=3*self.window_size)

	# draws game controls for initial setup
	def __draw_game_control(self):
		# evenhandler fns for each game control button
		handler_func_list = [self.__onclick_single_player_mode,self.__onclick_two_player_mode,
			self.__onclick_minimax,self.__onclick_alpha_beta_prune,self.__onclick_reset]
		window_handler_func_list = [self.__onselect_small_window,self.__onselect_medium_window,
			self.__onselect_large_window]
		# draw labels
		for label_vals in _CONTROL_BUTTON_LABEL_VAL_LIST:
			label = Label(
				self.canvas,text=label_vals[1],
				font=(_FONT,int(16*self.window_size)))
			label.place(
				x=int(label_vals[0][0]*self.window_size),
				y=int(label_vals[0][1]*self.window_size))
		# draw game mode controls
		for cb_vals in _CONTROL_BUTTON_VAL_LIST:
			check_button = Checkbutton(
							self.canvas,activeforeground='red',
							bd=2,indicatoron=0,offrelief='raised',
							overrelief='ridge',pady=2,
							cursor='gumby',text=cb_vals[1],
							font=(_FONT,int(14*self.window_size)))
			check_button.bind('<ButtonRelease-1>',
				handler_func_list[_CONTROL_BUTTON_VAL_LIST.index(cb_vals)])
			check_button.place(
				x=int(cb_vals[0][0]*self.window_size),
				y=int(cb_vals[0][1]*self.window_size))
			self.game_mode_control_objects.update({cb_vals[1]:check_button})
		# draw window size controls
		for windw_size_button_vals in _CONTROL_BUTTON_WINDOW_SIZE:
			windw_size_button = Checkbutton(
								self.canvas,activeforeground='red',
								bd=2,indicatoron=0,offrelief='raised',
								overrelief='ridge',pady=2,font=(_FONT,int(12*self.window_size)),
								cursor='gumby',text=windw_size_button_vals[1],
								command=window_handler_func_list[
									_CONTROL_BUTTON_WINDOW_SIZE.index(windw_size_button_vals)])
			windw_size_button.place(
				x=int(windw_size_button_vals[0][0]*self.window_size),
				y=int(windw_size_button_vals[0][1]*self.window_size))
			self.game_mode_control_objects.update({windw_size_button_vals[1]:windw_size_button})
		# ai control buttons are only available in 1player mode
		self.__change_ai_mode_control_state('disabled')
		

	## game state draw methods ##

	# draw current score on the score board
	def __draw_score(self,player1_score,player2_score):
		# draw player1's score
		plyr1_score = self.canvas.create_text(
			int(_PLAYER1_SCORE_X_COORD*self.window_size),
			int(_PLAYER1_SCORE_Y_COORD*self.window_size),
			text=':'+str(player1_score),
			font=(_FONT,int(22*self.window_size)))
		# draw player2's score
		plyr2_score = self.canvas.create_text(
			int(_PLAYER2_SCORE_X_COORD*self.window_size),
			int(_PLAYER2_SCORE_Y_COORD*self.window_size),
			text=':'+str(player2_score),
			font=(_FONT,int(22*self.window_size)))
		# add the references to score drawing to the game state canvas obj list
		self.game_state_obj_list.extend([plyr1_score,plyr2_score])

	# draw current state of checker pieces
	def __draw_pieces(self,player_pieces_data):
		player = player_pieces_data[0]
		for piece_data in player_pieces_data[1]:
			piece_coord = piece_data[0]
			piece_king_status = piece_data[1]
			key = str(piece_coord[1]) + '_' + str(piece_coord[0])
			grid_coord = self.__grid_coords[key]
			if len(piece_data) == 3 and len(piece_data[2]) > 0:
				self.__add_to_movable(key,piece_data[2])
				self.__place_piece_at(grid_coord,player,key,piece_king_status,True)
			else:
				self.__place_piece_at(grid_coord,player,key,piece_king_status,False)

	# adds a movable object and its possible moves to display when selected
	def __add_to_movable(self,key,moves):
		self.move_info.update({key:moves})

	# draw a checker piece as a coordinate
	def __place_piece_at(self,coord,player,tag,is_king,movable):
		# draw a piece
		piece_canvas_obj = \
			self.canvas.create_oval(
				coord[0]+(_PIECE_MARGIN*self.window_size),
				coord[1]+(_PIECE_MARGIN*self.window_size),
				coord[0]+((_PIECE_MARGIN+_PIECE_DIAMETER)*self.window_size),
				coord[1]+((_PIECE_MARGIN+_PIECE_DIAMETER)*self.window_size),
				fill=_COLORS[player],width=int(3*self.window_size),
				tags=tag,stipple='gray75')
		self.game_state_obj_list.append(piece_canvas_obj)
		# draw crown too if it is a king
		if is_king:
			crown_center_coord = \
				[coord[0]+((_PIECE_MARGIN+(_PIECE_DIAMETER/2))*self.window_size),
				coord[1]+((_PIECE_MARGIN+(_PIECE_DIAMETER/2))*self.window_size)]
			self.__draw_crown(crown_center_coord)
		# set hover event if it is movable
		if movable:
			self.canvas.itemconfig(
				piece_canvas_obj,
				activeoutline='white')
			self.canvas.tag_bind(
				piece_canvas_obj,
				'<ButtonRelease-1>',
				self.__onclick_show_paths)
			
	# draws a crown on king checker piece
	def __draw_crown(self,coord):
		crown_coords_offset = []
		for point in _CROWN_POLYGON:
			crown_coords_offset.append(coord[0]+int(point[0]*self.window_size))
			crown_coords_offset.append(coord[1]+int(point[1]*self.window_size))
		jewel_coords_offset = []
		for point in _CROWN_JEWEL:
			jewel_coords_offset.append(coord[0]+int(point[0]*self.window_size))
			jewel_coords_offset.append(coord[1]+int(point[1]*self.window_size))
		crown = self.canvas.create_polygon(
					crown_coords_offset,
					outline='red',fill='gold',width=2)
		jewel = self.canvas.create_polygon(
					jewel_coords_offset,
					outline='black',fill='blue',width=1)
		self.game_state_obj_list.append(crown)
		self.game_state_obj_list.append(jewel)

	# draws possible moves of the selected piece
	def __draw_possible_moves(self,moves):
		for move in moves:
			key = str(move[1]) + '_' + str(move[0])
			# get canvas obj coordinates using key/tag
			coord = self.__grid_coords[key]
			# draw preview of moves
			piece_canvas_obj = self.canvas.create_oval(
				coord[0]+(_PIECE_MARGIN*self.window_size),
				coord[1]+(_PIECE_MARGIN*self.window_size),
				coord[0]+((_PIECE_MARGIN+_PIECE_DIAMETER)*self.window_size),
				coord[1]+((_PIECE_MARGIN+_PIECE_DIAMETER)*self.window_size),
				fill=_COLORS[4],outline='red',width=(3*self.window_size),
				activeoutline='white',tags=key)
			# add the references to the created object to destination obj list
			self.move_preview_obj_list.append(piece_canvas_obj)
			# add event-handler function to the created preview of move
			self.canvas.tag_bind(
				piece_canvas_obj,
				'<ButtonRelease-1>',
				self.__onclick_move_piece)

	# enables or disables the player mode control buttons
	def __change_player_mode_control(self,control):
		self.game_mode_control_objects['1 Player'].config(state=control)
		self.game_mode_control_objects['2 Player'].config(state=control)

	# enables or disables the ai mode control buttons
	def __change_ai_mode_control_state(self,control):
		self.game_mode_control_objects['Minimax'].config(state=control)
		self.game_mode_control_objects['w/ α&β'].config(state=control)


	## event handler methods ##

	# handles 1player button click event
	def __onclick_single_player_mode(self,event):
		self.game_instance.single_player_mode = True
		self.__change_player_mode_control(DISABLED)
		self.__change_ai_mode_control_state(NORMAL)

	# handles 2player button click event
	def __onclick_two_player_mode(self,event):
		self.game_instance.single_player_mode = False
		self.__change_player_mode_control(DISABLED)
		self.game_instance.run()

	# handles minimax button click event
	def __onclick_minimax(self,event):
		self.game_instance.ai_mode = 'without'
		self.__change_ai_mode_control_state(DISABLED)
		self.game_instance.run()

	# handle w/a&b button click event
	def __onclick_alpha_beta_prune(self,event):
		self.game_instance.ai_mode = 'with'
		self.__change_ai_mode_control_state(DISABLED)
		self.game_instance.run()

	# handle reset button click event
	def __onclick_reset(self,event):
		self.game_instance.reset()

	# the event-handler function for previewing possible moves when
	# a piece is selected
	def __onclick_show_paths(self,event):
		self.__reset_move_preview_object_list()
		piece_canvas_obj = self.canvas.find_closest(event.x,event.y)
		key = self.canvas.gettags(piece_canvas_obj)[0]
		piece_coord = key.split('_')
		self.selected_piece_coord = (int(piece_coord[1]),int(piece_coord[0]))
		moves = self.move_info[key]
		self.__draw_possible_moves(moves)

	# the event-handler function for handling player's move
	def __onclick_move_piece(self,event):
		piece_obj = self.canvas.find_closest(event.x,event.y)
		tag_chars = self.canvas.gettags(piece_obj)[0].split('_')
		destination_coord = (int(tag_chars[1]),int(tag_chars[0]))
		self.game_instance.make_move_update(
			self.selected_piece_coord,destination_coord)

	# the event-handler functions for window size selection
	def __onselect_small_window(self):
		self.window.destroy()
		self.game_instance.change_window_size(_SMALL)

	def __onselect_medium_window(self):
		self.window.destroy()
		self.game_instance.change_window_size(_MEDIUM)

	def __onselect_large_window(self):
		self.window.destroy()
		self.game_instance.change_window_size(_LARGE)

	## other methods ##

	# display game setup instructions with a pop-up window
	def __instructions(self):
		pop_up_window = tk.Toplevel()
		pop_up_window.wm_title('Instructions')
		pop_up_window.resizable(False,False)
		label = ttk.Label(pop_up_window,text='First: select the game window size; Second: select game modes; and enjoy the game! \n Tip: In Tunnel Checkers, you are allow to go off on either lateral sides and end up on the other side!',
						font=(_FONT, int(16*self.window_size)),anchor=tk.CENTER,
						padding=4,wraplength=int(400*self.window_size))
		label.pack(side='top',fill='x',pady=int(10*self.window_size))
		button = ttk.Button(pop_up_window,text='Got it!',
			command=lambda:pop_up_window.destroy())
		button.pack()
		self.__place_window(pop_up_window,_INSTRUCTIONS_WIDTH,_INSTRUCTIONS_HEIGHT)
		pop_up_window.lift(aboveThis=self.canvas)

	# return the winner as string
	def __who_is_winner(self,winner):
		if winner == 0:
			return 'Player 1'
		else:
			return 'Player 2'

	# places the given window at the given coordinates
	def __place_window(self,window,window_w,window_h):
		window_x_coord = int((window.winfo_screenwidth()/2)-((window_w/2)*self.window_size))
		window_y_coord = int((window.winfo_screenheight()/2)-((window_h/2)*self.window_size))
		window.geometry('%dx%d+%d+%d'%(int(window_w*self.window_size),
			int(window_h*self.window_size),window_x_coord,window_y_coord))

	# resets the game state to blank game board 
	def __reset_piece_obj_list(self):
		self.__remove_objs(self.game_state_obj_list)

	# resets the move previews list to empty
	def __reset_move_preview_object_list(self):
		self.__remove_objs(self.move_preview_obj_list)

	# resets the game control to the initial state
	def __reset_game_control(self):
		self.game_mode_control_objects = {}
		self.__draw_game_control()

	# deletes given list of canvas objects
	def __remove_objs(self,obj_list):
		for obj in obj_list:
			self.canvas.delete(obj)




