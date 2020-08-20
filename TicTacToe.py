import random
import copy


class TTT:
	# things to add: ask player what mode they want (instead of constructor)
	# who goes first (player, computer, or random)
	def __init__(self):
		self.game_winner = False # no game winner yet

		self.create_board() # makes the 2d array
		self.play() # actually plays the game


	def create_board(self):
		# literally just makes the 3x3 game board
		self.board = [[1, 2, 3],[4, 5, 6],[7, 8, 9]]


	def print_board(self):
		# prints the current state of the board
		print(f'\n{self.board[0][0]} {self.board[0][1]} {self.board[0][2]}\n{self.board[1][0]} {self.board[1][1]} {self.board[1][2]}\n{self.board[2][0]} {self.board[2][1]} {self.board[2][2]}')


	# play method actually plays the game
	def play(self):
		# the playing method
		self.get_XO()
		self.get_mode()
		self.get_first()

		while not self.game_over():
			if self.mode == 'pvp':
				if self.current % 2 == 0:
					self.print_board()
					self.player_turn(self.player_XO_1)
					self.current += 1
				else:
					self.print_board()
					self.player_turn(self.player_XO_2)
					self.current += 1

			else:
				if self.current % 2 == 0: # if computer turn
					self.computer_turn()
					self.current += 1
				else: # if player's turn
					self.print_board()
					self.player_turn(self.player_XO_1)
					self.current += 1
		self.game_over_message()


	#sets x and o characters for player and computer
	def get_XO(self):
		while True: # decides what character each competitor will be
			xo = input('Would you rather be X or O?\n')
			try:
				if xo[0].upper() == 'X':
					self.player_XO_1 = 'X'
					self.computer_XO = 'O'
					self.player_XO_2 = 'O'
					print('You chose X.')
					break
				elif xo[0].upper() == 'O':
					self.player_XO_1 = 'O'
					self.computer_XO = 'X'
					self.player_XO_2 = 'X'
					print('You chose O.')
					break
				else:
					raise Exception('Illegal character')
			except:
				pass


	# sets the game to easy or hard difficulty
	def get_mode(self):
		while True: # difficulty
			try:
				difficulty = input('Would you like to play easy, hard, or PvP?\n')
				if difficulty[0].lower() == 'e':
					self.mode = 'easy'
					print(f'You chose easy. The computer will be {self.computer_XO}.')
					break
				elif difficulty[0].lower() == 'h':
					self.mode = 'hard'
					print(f'You chose hard. The computer will be {self.computer_XO}.')
					break
				elif difficulty[0].lower() == 'p':
					self.mode = 'pvp'
					print(f'You chose PvP. The other player will be {self.player_XO_2}.')
					break
				else:
					raise Exception('Not a difficulty.')
			except:
				pass


	# decides who will be first to play
	def get_first(self):
		while True:
			try:
				# if we are in pvp mode, we will go through these options:
				if self.mode[0] == 'p':
					first_player = input('Who will start? (X or O)\n')
					if first_player[0].upper() == self.player_XO_1:
						self.current = 0
						print(f'{self.player_XO_1} will start')
						break
					elif first_player[0].upper() == self.player_XO_2:
						self.current = 1
						print(f'{self.player_XO_2} will be first.')
						break
					else:
						raise Exception('Illegal choice.')
				# Otherwise, since we are playing against a computer, we will go through this sequence:
				else:
					first = input('Who will begin? (player, computer, random)\n')
					if first[0].lower() == 'p':
						self.current = 1
						print(f'The player, {self.player_XO_1}, will be first.')
						break
					elif first[0].lower() == 'c':
						self.current = 0
						print(f'The computer, {self.computer_XO}, will be first.')
						break
					elif first[0].lower() == 'r':
						self.current = random.randint(0, 2)
						print('You chose random:  ', end='')
						if self.current == 0:
							print(f'The computer, {self.computer_XO}, will be first.')
						else:
							print(f'The player, {self.player_XO_1}, will be first.')
						break
					else:
						raise Exception('Illegal choice.')
			except:
				pass


	# allows a player to choose a spot on the board to play
	def player_turn(self, player_char):
		while True:
			choice = input(f'Where does {player_char} want to play? (1 - 9)\n')
			if self.take_spot(choice, player_char, self.board):
				break
			else:
				print('Illegal spot! Try again.')


	# the computer chooses the best possible location
	def computer_turn(self):
		if self.mode == 'easy':
			self.easy_computer()
		else:
			self.hard_computer()

	# easy computer chooses a spot randomly
	def easy_computer(self):
		while True:
			choice = random.randint(1, 9)
			if self.take_spot(choice, self.computer_XO, self.board):
				break

	# hard computer takes turns that
	def hard_computer(self):
		if self.check_winner(self.computer_XO):
			pass
		if self.check_winner(self.player_XO_1):
			pass
		else:
			self.take_turn()


	# see if computer a player can win, and take that move if possible
	def check_winner(self, competitor):
		for i in range(1, 10):
			board = copy.deepcopy(self.board)
			#[i for i in self.board]

			self.take_spot(i, competitor, board)
			winner = self.find_win(board)
			if winner == competitor:
				self.take_spot(i, self.computer_XO, self.board)
				return True
		return False


	# take a corner piece (1, 3, 7, 9), then center piece (5), then remaining piece (2, 4, 6, 8)
	def take_turn(self):
		for i in (1, 3, 7, 9):
			board = self.board.copy()
			if (self.take_spot(i, self.computer_XO, board)):
				self.take_spot(i, self.computer_XO, self.board)
				return

		five_board = self.board.copy()
		if self.take_spot(5, self.computer_XO, board):
			self.take_spot(5, self.computer_XO, self.board)
			return

		for i in (2, 4, 6, 8):
			board = self.board.copy()
			if (self.take_spot(i, self.computer_XO, board)):
				self.take_spot(i, self.computer_XO, self.board)
				return


	def take_spot(self, choice, character, board):
		try:
			spot = int(choice)
			if spot < 1 or spot > 9:
				raise Exception('Illegal spot')

			space = [(spot-1)//3, (spot-1)%3]
			if type( board[space[0]][space[1]] ) is int:
				board[space[0]][space[1]] = character
				return True
			else:
				raise Exception('Illegal spot')
		except:
			return False


	# used to check if the game is over, returns True or False and updates self.game_winner
	def game_over(self):
		if self.find_win(self.board) == 'X' or self.find_win(self.board) == 'O':
			self.game_winner = self.find_win(self.board)
			return True
		elif self.find_tie():
			self.game_winner = 'T'
			return True
		else:
			return False


	# used to find the actual winner
	def find_win(self, board):
		for ch in [self.computer_XO, self.player_XO_1]:
			#check horizontals
			if board[0][0] == ch and board[0][1] == ch and board[0][2] == ch:
				return ch
			elif board[1][0] == ch and board[1][1] == ch and board[1][2] == ch:
				return ch
			elif board[2][0] == ch and board[2][1] == ch and board[2][2] == ch:
				return ch
			#check verticals
			elif board[0][0] == ch and board[1][0] == ch and board[2][0] == ch:
				return ch
			elif board[0][1] == ch and board[1][1] == ch and board[2][1] == ch:
				return ch
			elif board[0][2] == ch and board[1][2] == ch and board[2][2] == ch:
				return ch
			#check diagonals
			elif board[0][0] == ch and board[1][1] == ch and board[2][2] == ch:
				return ch
			elif board[0][2] == ch and board[1][1] == ch and board[2][0] == ch:
				return ch
		return False


	# finds out if there is a tied game
	def find_tie(self):
		count_letters = 0
		for r in range(len(self.board)):
			for c in range(len(self.board[r])):
				if type(self.board[r][c]) is str:
					count_letters += 1
		return count_letters == 9


	# plays the message that game is over
	def game_over_message(self):
		if self.find_win(self.board) is False:
			print('Well, you tied.')
		else:
			winner = self.find_win(self.board)
			self.print_board()
			print(f'The winner is {winner}!')
		self.play_again()


	# asks if player wants to play again, and resets everything if so
	def play_again(self):
		while True:
			try:
				choice = input('Would you like to play again? (yes or no)\n')
				if choice.lower()[0] == 'y':
					self.create_board()
					self.current = 1
					self.play()
					break
				elif choice.lower()[0] == 'n':
					break
			except:
				pass




TTT()