'''
File: search_tree.py

minmax search tree with basic heuristics
'''

import random

DIRECTIONS = [(-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)]

def is3(x1, x2, x3, x4, player):
	val = x1 + x2 + x3 + x4
	if abs(val) == 3:
		if (val < 0) == (player < 0):
			return 1
		return -1
	return 0

def showBoard(board):
	output = ""
	for row in range(6):
		output += "|"
		for space in range(7):
			output += " X |" if board[row*7 + space] == -1 else "   |" if board[row*7 + space] == 0 else " O |"
		output += "\n"
	print(output)

def checkDiagonal(direction, player, row, column, board):
	for i in range(3):
		row += DIRECTIONS[direction][1]
		column += DIRECTIONS[direction][0]
		if not 0 <= row <= 5 or not 0 <= column <= 6:
			return False
		if board[row*7 + column] != player:
			return False
	return True

def checkWin(row, column, board):
	player = board[row*7 + column]
	row_array = board[row*7:row*7+7]
	streak = 0
	prev = -1
	if row < 3:
		vertical_victory = True
		for i in range(4):
			if row+i < 6 and board[(row+i)*7 + column] != player:
				vertical_victory = False
		if vertical_victory:
			#print("vertical victory")
			return True
	for space in row_array:
		if space != 0 and space == prev:
			streak += 1
			if streak == 4:
				#print("horizontal victory")
				return True
		else:
			prev = space
			streak = 1
	for row in range(6):
		for column in range(7):
			space = board[row*7 + column]
			if space != 0:
				for i in range(4):
					if checkDiagonal(i, space, row, column, board):
						#print("diagonal victory")
						return True
	return False

def addPiece(column, player, board):
	if column < 0 or column > 6 or (player != -1 and player != 1):
		return False
	for i in range(6):
		row_search = 5 - i
		if board[row_search*7 + column] == 0:
			board[row_search*7 + column] = player
			if checkWin(row_search, column, board):
				return True
			return False
	return False

def newBoard(column, player, board):
	new_board = board.copy()
	if column < 0 or column > 6 or (player != -1 and player != 1):
		return []
	for i in range(6):
		row_search = 5 - i
		if board[row_search*7 + column] == 0:
			new_board[row_search*7 + column] = player
			return new_board, row_search
	return []

def scoreBoard(player, board):
	score = 0
	for i in range(6):
		for j in range(4):
			score += is3(board[i*7+j], board[i*7+j+1], board[i*7+j+2], board[i*7+j+3], player)
	for i in range(3):
		for j in range(7):
			score += is3(board[i*7+j], board[(i+1)*7+j], board[(i+2)*7+j], board[(i+3)*7+j], player)
	for i in range(3):
		for j in range(4):
			score += is3(board[i*7+j], board[(i+1)*7+j+1], board[(i+2)*7+j+2], board[(i+3)*7+j+3], player)
			score += is3(board[(i+3)*7+j], board[(i+2)*7+j+1], board[(i+1)*7+j+2], board[i*7+j+3], player)
	return score

class State:
	def __init__(self, state, player, move, score):
		self.state = state
		self.score = score
		self.player = player
		self.children = []
		self.move = move
	
	def findMoves(self, player):
		out = []
		for i in range(7):
			for j in range(6):
				if self.state[j*7+i] == 0:
					out.append(i)
					break
		return out
	
	def generateChildren(self):
		moves = self.findMoves(self.player)
		for move in moves:
			potential_board, row = newBoard(move, self.player, self.state)
			if checkWin(row, move, potential_board):
				self.score = self.player*(-1000)
				self.children = [State(potential_board, self.player*-1, move, self.player*(-1000))]
				break
			#pot_score = scoreBoard(self.player, potential_board)
			self.children.append(State(potential_board, self.player*-1, move, 0))
	
	def getScore(self, depth):
		if depth == 4 or len(self.children) <= 1:
			if self.player == -1:
				maxi = 0
				for child in self.children:
					if child.score:
						maxi = max(maxi, child.score)
					else:
						maxi = max(maxi, scoreBoard(child.player, child.state))
				return maxi
			mini = 0
			for child in self.children:
				if child.score:
					mini = min(mini, child.score)
				else:
					mini = min(mini, scoreBoard(child.player, child.state))
			return mini
		for child in self.children:
			if len(child.children) == 0:
				child.generateChildren()
			score = child.getScore(depth+1)
			score += scoreBoard(child.player, child.state)
			child.score = score
		if self.player == -1:
			maxi = 0
			for child in self.children:
				maxi = max(maxi, child.score)
			return maxi
		mini = 0
		for child in self.children:
			mini = min(mini, child.score)
		return mini
	
	def showScores(self):
		for child in self.children:
			print(str(child.move) + ": " + str(child.score))
			if child.children:
				for grandchild in child.children:
					print("\t" + str(grandchild.move) + ": " + str(grandchild.score))
		print("----"*7+"-")


class Tree:
	def __init__(self, board):
		self.board = board
		self.children= []

test = [-1, -1, -1, 0, -1, -1, 0, 
		-1, -1, -1, 0, 1, 1, 0, 
		1, 1, 1, 0, -1, -1, 1, 
		-1, -1, -1, -1, 1, 1, -1, 
		1, 1, 1, -1, -1, -1, 1, 
		-1, -1, -1, -1, 1, 1, -1, ]
#practice = [0]*42
practice = [  0,  0,  0,  0,  0,  0,  0,
			  0,  0,  0,  0,  0,  0,  0,
			  0,  0,  0,  0,  0,  0,  0,
			  0,  0,  0,  0,  0,  0,  0,
		      0,  0,  0,  0,  0,  0,  0,
			  0,  0,  0,  0,  0,  0,  0,]

'''showBoard(test)
test_state = State(test, -1, -1)
test_state.generateChildren()
score = test_state.getScore(0)
for child in test_state.children:
	if child.score == score:
		if addPiece(child.move, child.player, test):
			print("Win:", child.player)
			break
		test_state = child
showBoard(test)'''


test_state = State(practice, 1, -1, 0)
test_state.generateChildren()
showBoard(practice)

while(1):
	move = int(input("Add a piece (1-7): "))
	if addPiece(move-1, 1, practice):
		showBoard(practice)
		print("Player 1 Win")
		break
	showBoard(practice)
	for child in test_state.children:
		if child.move == move-1:
			test_state = child
			if len(test_state.children) == 0:
				test_state.generateChildren()
	print("num children", len(test_state.children))
	test_state.getScore(0)
	test_state.showScores()
	maxi = test_state.children[0].score
	for child in test_state.children:
		score = child.score
		if score > maxi:
			maxi = score
	picks = []
	for child in test_state.children:
		if child.score == maxi:
			picks.append(child.move)
	cp_move = random.choice(picks)
	for child in test_state.children:
		if child.move == cp_move:
			test_state = child
			if len(test_state.children) == 0:
				test_state.generateChildren()
	if addPiece(cp_move, -1, practice):
		showBoard(practice)
		print("Computer Win")
		break
	showBoard(practice)