# Tunnel Checker Game
# Author : Seung Hun Lee
# Email  : lee.seunghu@husky.neu.edu

### CheckerGame Class ###
# This class connects the CheckerGameGUI instance with GameBoard instance.
# Once instantiated, GUI take input from the player and calls GameBoard
# class methods; GameBoard methods updates the game state; and updates
# game GUI using CheckerGameGUI method.

from classes.GameBoard import GameBoard as gb
from classes.CheckerGameGUI import CheckerGameGUI as cg_gui
import tkinter as tk

## Global constants ##

_AI_PLAYER = 0
_INITIAL_DEPTH = 0
_DEFAULT_WINDOW_SIZE = 1.0

class CheckerGame:

	# Constructor
	def __init__(self):
		self.single_player_mode = True
		self.ai_mode = 'with'
		self.game_board = gb()
		self.game_board_gui = cg_gui(self,_DEFAULT_WINDOW_SIZE,False)
		self.game_board_gui.canvas.pack()
		self.game_board_gui.window.mainloop()

	### Properties for class attributes ###

	#*** @property = getter method and @fn.setter = setter methods

	## single_player_mode attribute
	@property
	def single_player_mode(self):
		return self.__single_player_mode

	@single_player_mode.setter
	def single_player_mode(self,val):
		if isinstance(val,bool):
			self.__single_player_mode = val
		else:
			raise AttributeError('Invalid type: \
				single_player_mode must be Boolean')

	## ai_mode attribute
	@property
	def ai_mode(self):
		return self.__ai_mode

	@ai_mode.setter
	def ai_mode(self,val):
		if isinstance(val,str) and (val == 'with' or val == 'without'):
			self.__ai_mode = val
		else:
			raise AttributeError('Invalid type or value: \
				ai_mode must be <class \'str\'> and its value must be \
				either with or without.')

	## game_board attribute
	@property
	def game_board(self):
		return self.__game_board

	@game_board.setter
	def game_board(self,val):
		if isinstance(val,gb):
			self.__game_board = val
		else:
			raise AttributeError('Invalid type: \
				game_board must be GameBoard class object')

	## game_board_gui attribute
	@property
	def game_board_gui(self):
		return self.__game_board_gui

	@game_board_gui.setter
	def game_board_gui(self,val):
		if isinstance(val,cg_gui):
			self.__game_board_gui = val
		else:
			raise AttributeError('Invalid type: \
				game_board_gui must be CheckerGameGUI class object')


	### Public methods ###

	# generates turn until there is a winner
	def run(self):
		# winner ends the game
		if self.game_board.winner is not None:
			self.game_board_gui.end_game(self.game_board.winner)
		# AI's turn
		elif self.game_board.current_turn == _AI_PLAYER and \
			self.single_player_mode:
			game_state_copy = self.game_board.get_game_copy()
			best_move = []
			# pure minimax
			if self.ai_mode == 'without':
				best_move = game_state_copy.minimax(game_state_copy,_INITIAL_DEPTH)
			# minimax with alpha beta pruning
			else:
				best_move = game_state_copy.minimax_with_alpha_beta_prune(
			 		game_state_copy,_INITIAL_DEPTH,float('-inf'),float('inf'))
			self.make_move_update(best_move[0],best_move[1])
		# user turn
		else:
			self.__update_gui()

	# updates game state and GUI after a player makes a move
	def make_move_update(self,piece_coords,destn_coords):
		self.game_board.make_move(piece_coords,destn_coords)
		self.__update_gui()
		self.run()

	# resets the game to the initial state
	def reset(self):
		self.game_board = gb()
		self.game_board_gui.reset()

	# switches the game window size
	def change_window_size(self,new_wdw_size):
		self.game_board_gui = cg_gui(self,new_wdw_size,True)
		self.game_board_gui.change_window_control('disabled')
		self.game_board_gui.canvas.pack()
		self.game_board_gui.window.mainloop()

	### Internal methods ###

	# pass updated game state to CheckerGameGUI instance
	def __update_gui(self):
		current_game_state = self.game_board.get_game_state()
		self.game_board_gui.update_game_state(
			current_game_state[0],current_game_state[1],current_game_state[2])

# main function to start a game instance
def __main():
	game = CheckerGame()

# run the main() function
if __name__ == '__main__':
	__main()
