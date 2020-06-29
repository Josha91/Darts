import matplotlib
# This defines the Python GUI backend to use for matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import numpy as np 
from numpy.random import multivariate_normal as multinorm
import math
from drawboard import boardsize, drawBoard
import IPython
from astropy.modeling.functional_models import Gaussian2D
from plot_heatmap import score,plot_heatmap_sigma
from tkinter import *

class probs(boardsize):

	def compute_probs(self,s):
		self.s = s
		R = self.R.copy()
		R.insert(0,0) #add 0 to beginning
		R.append(-1) 
		self.a = np.zeros(6)
		self.b = np.zeros(6)
		for i in range(len(R)-1):
			tmp = self.numerator(R[i],R[i+1])
			tmp2 = self.denominator(R[i],R[i+1])
			if tmp2 == 0 and tmp == 0: tmp2 = 1 #avoid zero division
			if (i>1)&(i<6):
				tmp/=20
				tmp2/=20
			if i == 4:
				self.a[2] += tmp
				self.b[2] += tmp2
			elif i > 4:
				self.a[i-1] = tmp
				self.b[i-1] = tmp2
			else:
				self.a[i] = tmp
				self.b[i] = tmp2

	def numerator(self,r1,r2):
		if r2 == -1:
			return (r1**2.+2*self.s)*np.exp(-r1**2./(2*self.s))
		else:
			return (r1**2.+2*self.s)*np.exp(-r1**2./(2*self.s)) - \
								(r2**2.+2*self.s)*np.exp(-r2**2/(2*self.s))

	def denominator(self,r1,r2):
		if r2 == -1:
			return np.exp(-r1**2./(2*self.s))
		else:
			return np.exp(-r1**2./(2*self.s)) - np.exp(-r2**2./(2*self.s))

def get_Ez(x,p):
	"""
	Compute the equation from appendix A2 in 
	Tibshirani, Price & Taylor
	""" 
	if x in [1,5,7,11,13,17,19]: #these scores can only be achieved in one way
		return p.a[2]/p.b[2]
	elif x in [2,4,8,10,14,16,20]: #two ways to achieve these
		return (p.a[2]+p.a[4])/(p.b[2]+p.b[4])
	elif x in [3,9,15]: 
		return (p.a[2]+p.a[3])/(p.b[2]+p.b[3])
	elif x in [6,12,18]:
		return (p.a[2]+p.a[3]+p.a[4])/(p.b[2]+p.b[3]+p.b[4])
	elif x in [24,30,36]:
		return (p.a[3]+p.a[4])/(p.b[3]+p.b[4])
	elif x in [22,26,28,32,34,38,40]:
		return p.a[4]/p.b[4]
	elif x in [21,27,33,39,42,45,48,51,54,57,60]:
		return p.a[3]/p.b[3]
	elif x == 25:
		return p.a[1]/p.b[1]
	elif x == 50:
		return p.a[0]/p.b[0]
	else:
		return p.a[5]/p.b[5]

def get_prob(x,p):
	"""
	Compute the equation from appendix A2 in 
	Tibshirani, Price & Taylor
	""" 
	if x in [1,5,7,11,13,17,19]: #these scores can only be achieved in one way
		return p.b[2]
	elif x in [2,4,8,10,14,16,20]: #two ways to achieve these
		return p.b[2]+p.b[4]
	elif x in [3,9,15]: 
		return p.b[2]+p.b[3]
	elif x in [6,12,18]:
		return p.b[2]+p.b[3]+p.b[4]
	elif x in [24,30,36]:
		return p.b[3]+p.b[4]
	elif x in [22,26,28,32,34,38,40]:
		return p.b[4]
	elif x in [21,27,33,39,42,45,48,51,54,57,60]:
		return p.b[3]
	elif x == 25:
		return p.b[1]
	elif x == 50:
		return p.b[0]
	else:
		return p.b[5]

def EMStep(x,p):
	e = 0
	n = x.size
	for i in range(n):
		e += get_Ez(x[i],p)
	return e/(2*n)

def LogLik(x,p):
	P = 0
	for i in range(x.size):
		tmp = get_prob(x[i],p)
		if tmp == 0:
			P += 0
		else:
			P += np.log(get_prob(x[i],p))
	return P

def EM(x):
	"""
	Compute the player's (assumed Gaussian) variance,
	given the input of single dart scores (x). Follows
	the EM algorithm as outlined in Tibshirani, Price & Taylor
	"""
	if type(x) == list:
		x = np.asarray(x)
	#while True:
	s_in = 10 #initial variance

	p = probs()
	s,ll = [],[]
	while True: #until convergence.
		p.compute_probs(s_in)
		s_tmp = EMStep(x,p=p)
		s.append(s_in)
		ll.append(LogLik(x,p))
		if round(s_in,2) == round(s_tmp,2):
			break
		s_in = s_tmp
	return s,ll


def simulate_N(N = 250,ax=None):
	true_sigmas = np.linspace(5,70,50)
	recovered = []
	for true_sigma in true_sigmas:
		S = np.array([[true_sigma**2.,0],[0,true_sigma**2.]])
		xy = multinorm([0,0],S,N)
		scores = np.vectorize(score)(xy[:,0],xy[:,1])

		EM_sigma = EM(scores)
		sigma = np.sqrt(EM_sigma[0])
		recovered.append(sigma[-1])

	#fig,ax = plt.subplots(1)
	#drawBoard(ax=ax,color_on=False,zorder=3)
	#ax.scatter(xy[:,0],xy[:,1],color='r')
	#ax.set_title('Input $\sigma$=%.2f, recovered $\sigma$=%.2f'%(true_sigma,EM_sigma))
	if ax is None:
		fig,ax = plt.subplots(1)
		ax.set_xlabel('Input $\sigma$',fontsize=20)
		ax.set_ylabel('Recovered $\sigma$',fontsize=20)
	ax.scatter(true_sigmas,recovered)
	ax.plot([0,70],[0,70],color='r')

def simulate_2():
	fig,ax = plt.subplots(1)
	simulate_N(50,ax=ax)
	simulate_N(150,ax=ax)
	simulate_N(250,ax=ax)
	ax.set_xlabel('Input $\sigma$',fontsize=20)
	ax.set_ylabel('Recovered $\sigma$',fontsize=20)
	plt.tight_layout()
	plt.show()

def simulate(sigma_in=40):
	true_sigmas = np.ones(10)*sigma_in
	N = 50
	recovered = []
	for true_sigma in true_sigmas:
		S = np.array([[true_sigma**2.,0],[0,true_sigma**2.]])
		xy = multinorm([0,0],S,N)
		scores = np.vectorize(score)(xy[:,0],xy[:,1])

		EM_sigma = EM(scores)
		sigma = np.sqrt(EM_sigma[0])
		recovered.append(sigma[-1])

	fig,ax = plt.subplots(1)
	drawBoard(ax=ax,color_on=False,zorder=3)
	ax.scatter(xy[:,0],xy[:,1],color='r')
	#ax.set_title('Input $\sigma$=%.2f, recovered $\sigma$=%.2f'%(true_sigma,EM_sigma))

	fig,ax = plt.subplots(1)
	ax.hist(recovered)
	ax.set_ylim(ax.get_ylim())
	ax.plot([sigma_in,sigma_in],ax.get_ylim(),color='r')
	plt.show()

def test_zeroth_order(sigma_in=10):
	fig,ax = plt.subplots(1)
	sig = []
	mean = []
	for sigma_in in [5,10,15,20,30,40,50,60]:
		true_sigmas = np.ones(1500)*sigma_in
		N = 50
		frac = []
		for true_sigma in true_sigmas:
			S = np.array([[true_sigma**2.,0],[0,true_sigma**2.]])
			xy = multinorm([0,0],S,N)
			scores = np.vectorize(score)(xy[:,0],xy[:,1])

			use = (scores==25)|(scores==50)

			frac.append(np.sum(use)/scores.size)
	
		ax.hist(frac,histtype='step',lw=3,label='$\sigma_{in}$=%d mm'%sigma_in)
		perc = np.percentile(frac,[16,84])
		sig.append(perc[1]-perc[0])
		mean.append(np.mean(frac))
	plt.legend(fontsize=14)
	ax.tick_params('both',labelsize=14)
	ax.set_ylabel('Frequency',fontsize=20)
	ax.set_xlabel('Fraction of 25 and 50',fontsize=20)
	plt.tight_layout()
	plt.show()

	IPython.embed()


def Josha(N=50):
	x = [18,12,15,17,9,12,3,11,5,1,2,7,11,14,3,20,8,10,5,25,12,19,1,5,18,17,7,9,4,18,\
		9,1,17,20,19,3,5,25,12,50,5,12,9,1,1,25,5,51,12,19,14,12,20,25]

	EM_sigma = EM(x)
	sigma = np.sqrt(EM_sigma[0][-1])
	print('Josha throws with a $\sigma$ of about %.3f mm'%sigma)
	print('This is based on %d throws'%len(x))
	sigma = 10
	fig,ax = plt.subplots(1)
	plot_heatmap_sigma(sigma,ax)

	#Past scores:
	#16-6-2020: sigma of 40 mm.
	plt.show()

def Arianna(N=50):
	x = [5,7,2,9,25,4,7,20,15,5,8,3,14,3,15,13,20,14,14,16,10,17,13,\
		32,18,12,8,15,8,7,15,19,7,54,16,16,7,19,18,12,14,15,2,13,17,12,13,28]

	EM_sigma = EM(x)
	sigma = np.sqrt(EM_sigma[0][-1])
	print('Arianna throws with a $\sigma$ of about %.3f mm'%sigma)
	print('This is based on %d throws'%len(x))
	fig,ax = plt.subplots(1)
	plot_heatmap_sigma(sigma,ax)
	plt.show()

def profs(N=50):
	x = [50,25,50,8,25,50,25,25,4,25,25,50,25,50,50,25,25,25,25,11,25,25,25,25,9,13,6,25,25,25,25,25,6,19,12,5,25,25,25]
	x2 = [25,50,25,50,16,6,50,25,25,25,50,25,25,25,9,25,50,8,2,50,25,25,25,19,25,50,25,25,25,17,25,50,50,25,25,50]
	#x is from Van Gerwen & Anderson
	#x2 is from Wright, Smith and Cross. 

	EM_sigma = EM(x)
	sigma = np.sqrt(EM_sigma[0][-1])
	print('Arianna throws with a $\sigma$ of about %.3f mm'%sigma)
	print('This is based on %d throws'%len(x))
	fig,ax = plt.subplots(1)
	plot_heatmap_sigma(sigma,ax)
	plt.show()

#Arianna()
#profs()
#test_zeroth_order()
#simulate()

class EMWidget(Frame):
	def __init__(self,parent):
		Frame.__init__(self,parent,width=600,height=500,bg='grey')
		self.parent = parent
		self.grid(row=0,column=1,padx=10,pady=50)

		inp1 = Entry(self,state='normal',width=5,highlightbackground='grey')
		inp1.grid(row=0,column=0)

		b = Button(self,text='Ok',highlightbackground='grey')
		b['command'] = lambda x=inp1: self.score(x)
		b.grid(row=0,column=1)

		b = Button(self,text='Calculate your skill!',highlightbackground='grey',command=self.calc_skill)
		b.grid(row=3,column=1)

		b = Button(self,text='To main menu...',highlightbackground='grey',command=self._quit)
		b.grid(row=4,column=1)

		self.label = StringVar()
		self.label.set('Number of scores entered: %s'%0)
		Label(self,textvariable=self.label,bg='grey').grid(row=1,column=1)

		self.scores = []

	def _quit(self):
		pass

	def score(self,inp):
		try:
			self.scores.append(int(inp.get()))
		except:
			pass
		inp.delete(0, 'end')
		self.label.set('Number of scores entered: %s'%len(self.scores))

	def calc_skill(self):
		if len(self.scores) < 50:
			msg = 'You only entered %s scores. For an accurate assessment, I would '%len(self.scores)+\
				'recommend using at least 50. Proceed anyway?'
			MsgBox = messagebox.askquestion ('Calculate skill',msg,icon = 'warning')
			if MsgBox == 'no':
				messagebox.showinfo('Return','You will now return to the score input')
				return
		EM_sigma = EM(self.scores)
		sigma = np.sqrt(EM_sigma[0][-1])
		#print('Arianna throws with a $\sigma$ of about %.3f mm'%sigma)
		#print('This is based on %d throws'%len(x))
		fig,ax = plt.subplots(1)
		plot_heatmap_sigma(sigma,ax)
		#plt.show()
		subframe = Frame(self,width=580,height=250,bg='white')
		#subframe.grid(row=0,column=1,padx=10,pady=50)
		subframe.place(x=5,y=150,height=195,width=500)
		canvas = FigureCanvasTkAgg(fig, master=subframe)
		canvas.get_tk_widget().place(x=5,y=5,width=590,height=490) 

	def ExitApplication():
		msg = 'You only entered '
		MsgBox = tk.messagebox.askquestion ('Calculate skill','You only entered %s scores. ',icon = 'warning')
		if MsgBox == 'yes':
			self.destroy()
		else:
			tk.messagebox.showinfo('Return','You will now return to the application screen')



"""
----
Make some simulations: put in Gaussian scores and see if you can recover this. Do this for different 
\sigma
---
Also: test how many throws you need for this. 
----
Test how accurate it is as a function of number of throws.
"""





