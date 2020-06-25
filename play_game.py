import numpy as np 
from numpy.random import multivariate_normal as multinorm
from drawboard import boardsize

#TO DO:
#Make a GUI for this. 

class Player():
	def __init__(self,name):
		self.name = name

		self.legs_won = 0 #number of legs won 
		self.legs_played = 0 #number of legs played

		self.score = 0 #current score
		self.total = 0 #total score - used for average calculation. 
		self.darts = 0 #number of darts thrown - used for average calculation

		self.board = boardsize()

		self.dbl_pref = 32 #preferred double. Defaults to 32 because powers of 2

		#function to determine the ideal way to 0 (best doubles?)

	def _get_score(self,value): 
		if (value > self.score - 1)&(value!=self.score):
			#too high - keep score
			self.darts += 3
		else:
			self.score -= value 
			self.total += value
			self.darts += 3 #Adjust when ended with a double. 

	def checkout(self):
		"""
		This function makes a suggestion for the checkout to pursue
		"""
		if self.score > 170: return -1
		last = np.append(np.arange(1,21)*2,50)


class Bot(Player):
	def __init__(self,name='Bot',sigma=20):
		super().__init__(name=name)
		self.board = boardsize()
		self.sigma = np.identity(2)*sigma**2. #Gaussian skill of the bot.
		self.score = 0 #initialize score 

		self.legs_won = 0 
		self.legs_played = 0

		self.xc,self.yc = self.board.get_optimal_aim(sigma)

	def activate(self,player2):
		"""Take a turn"""
		xy = multinorm([self.xc,self.yc],self.sigma)
		sc = self.board._score(xy[0],xy[1])

		#player2.

	def deactivate(self):
		pass

	def _get_score_old(self):
		xy = multinorm([self.xc,self.yc],self.sigma)
		return self.board._score(xy[0],xy[1])

class Human(Player):
	def __init__(self,name):
		super().__init__(name=name)
		self.inp = 0 #initialize input 

	def activate(self,player2):
		"""
		Take a turn. For humans: activate their 
		"""
		self.inp.configure(state='normal')

	def deactivate(self):
		self.inp.configure(state='disabled')

	def _get_score_old(self):
		while True:
			score = input('Score: ')
			try:
				score = int(score)
			except:
				continue
			if (score <= 180)&(score>=0): break
		return score

class leg():
	def __init__(self,P1,P2,start_value = 501):
		assert isinstance(P1,Player), "Player 1 should be a 'Player'-object!"
		assert isinstance(P2,Player), "Player 2 should be a 'Player'-object!"
		self.P1 = P1
		self.P2 = P2
		P1.score, P2.score = start_value, start_value
		while True:
			tmp = self.turn()
			if tmp > 0: break

	def turn(self):
		sc1 = self.P1._get_score()
		if self.P1.score == sc1: 
			print('Player 1 won!')
			self.P1.legs_won +=1
			self.P1.legs_played +=1
			self.P2.legs_played +=1
			return 1
		elif sc1 > self.P1.score - 2: #dead
			print('Dead!')
		else:
			self.P1.score -= sc1
			print('Player 1 now has %d left'%self.P1.score)
		sc2 = self.P2._get_score()
		if self.P2.score == sc2:
			print("Player 2 won!")
			self.P1.legs_won +=1
			self.P1.legs_played +=1
			self.P2.legs_played +=1
			return 2
		elif sc2 > self.P2.score - 2: #dead
			print('Dead!')
		else:
			self.P2.score -= sc2
			print('Player 2 now has %d left'%self.P2.score)

		return 0 



if __name__ == "__main__":
	P1 = Human('Josha')
	#P1._get_score()
	P2 = Bot(20)

	leg(P1,P2)


#check that the final dart was on a double...
#Calculate optimal path to double.
#Print 3-dart average. 
#Let a bot aim at a double (or any other square)
#Simulate how long it would take for a player of a given skill level to finish a leg. (make a nice plot for that)
#check for a double with the bot...!
#Output plots in a plot/ directory. 
#Gaussian in phase space, somewhere mid-flight? 



