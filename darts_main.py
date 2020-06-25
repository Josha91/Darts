#Make a pop-up when someone wins a leg.
#Record stuff about past legs; save averages etc, how many darts it took
#Disable input for Bots
#Make sure players take turns 


#TO DO:
#Toolbar
#Set window size
#if image already exists: replace
#Get a TEMPORRARY image; one that you can edit. 
#Class colormatch, with the default cvs (or whatever the name is)
#Make a README including the colorsystems and why you choose what you choose


#TO DO:
#--> Game setup. At what score to start, how many legs
#Enter the skill of the Bot.
#What to aim for for the bot? In particular, which double to go after.
#bull throwing to determine who starts. 

#Other simple games: 
#Just calculate the average of any number of darts.
#Calculate personal heat map

#Change the functionality a bit; use a Controller. 


# make print & unicode backwards compatible
from __future__ import print_function
from __future__ import unicode_literals


import matplotlib
# This defines the Python GUI backend to use for matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Import tkinter classes - handles python2 & python3
try:
	# for Python2
	from Tkinter import *
	import tkMessageBox as MessageBox
	import tkSimpleDialog as SimpleDialog
	from tkColorChooser import askcolor
	import tkFileDialog as filedialog
	import ScrolledText as scrolledtext
	import tkFont as tkFont
	# used to check if functions have a parameter
	from inspect import getargspec as getArgs
	PYTHON2 = True
	PY_NAME = "Python"
	UNIVERSAL_STRING = basestring
except ImportError:
	# for Python3
	from tkinter import *
	from tkinter import messagebox as MessageBox
	from tkinter import simpledialog as SimpleDialog
	from tkinter.colorchooser import askcolor
	from tkinter import filedialog
	from tkinter import scrolledtext
	from tkinter import font as tkFont
	from PIL import ImageTk,Image, ImageEnhance
	# used to check if functions have a parameter
	from inspect import getfullargspec as getArgs
	PYTHON2 = False
	PY_NAME = "python3"
	UNIVERSAL_STRING = str

import numpy as np 
from scipy.ndimage.filters import gaussian_filter
from tqdm import *
import pandas as pd
import colorsys
from colorsys import rgb_to_hsv, hsv_to_rgb
import colormath
from colormath.color_objects import LabColor, sRGBColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000 as dC
from copy import deepcopy as dc
from functools import partial
import math

from play_game import *


class Darts(object):

	def __init__(self):
		self.topLevel = Tk() #main screen
		self.topLevel.geometry("700x400")

		self.Frame = Frame(self.topLevel,background='SteelBlue1')
		self.Frame.pack(side=TOP)
		self.Frame2 = Frame(self.topLevel,background='SteelBlue1')
		self.Frame2.pack(side=BOTTOM)

		b = Button(self.topLevel,text='New game',command=self.new_game)
		b.pack(side=LEFT)

		c = Button(self.topLevel,text='Personal heatmap',command=self.heatmap)
		c.pack(side=LEFT)

		#f = plt.figure()
		#plt.plot([0,1],[0,1])
		#plt.ion()
		#canvas = FigureCanvasTkAgg(f, master=self.topLevel)
		#canvas.show()
		#canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
		#self.try_plot()

		button = Button(master=self.topLevel, text='Quit', command=self._quit)
		button.pack(side=LEFT)
#        self.board = board_layout([1,1],boardsize=50)
		#palette(topLevel=self.topLevel)
	  #  self.menubar()
		self.topLevel.mainloop()

	def _quit(self):
		self.topLevel.quit()     # stops mainloop
		self.topLevel.destroy()

	def try_plot(self,frame=0):
		plt.ion()
		fig = plt.figure(1)
		t = np.arange(0.0,3.0,0.01)
		s = np.sin(np.pi*t)
		plt.plot(t,s)

		def update():
			s = np.cos(np.pi*t)
			plt.plot(t,s)
			fig.canvas.draw()

		canvas = FigureCanvasTkAgg(fig, master=self.topLevel)
		plot_widget = canvas.get_tk_widget().pack(side=BOTTOM,fill=BOTH,expand=1)

		#plot_widget.grid(row=0, column=0,expand=1)
		#plt.show()
		#Button(self.topLevel,text="Update",command=update).grid(row=1, column=0)

	def heatmap(self):
		window = Toplevel(self.topLevel)
		fr = Frame(window)
		fr.pack()

		f = plt.figure()
		plt.plot([0,1],[0,1])
		#plt.ion()
		canvas = FigureCanvasTkAgg(f, master=fr)
		canvas.show()
		canvas.get_tk_widget().pack(side=LEFT,  expand=True) #fill=BOTH

	def _layout(self):
		titleframe = Frame(self.game_window, bg ="green")	
		titleframe.grid(row=10, column=2, columnspan=5, sticky='ew')

	def new_game(self):
		self.new_player()
		self.game_window = Toplevel(self.topLevel)
		self.game_window.geometry("700x500")
		self.game_window.columnconfigure(1, weight=1)

		fr = Frame(self.game_window)
		fr.pack(side=BOTTOM)
		fr2 = Frame(self.game_window)
		fr2.pack(side=TOP)
		#self._layout()
		#self.player1 = Human(self.player1.name)
		#self.player2 = Human(self.player2.name)
		titleframe = Frame(self.game_window, bg ="green")	
		titleframe.grid(row=2, column=0, columnspan=5, sticky='ew')
		Label(titleframe,text='3-dart average: ',bg='green').grid(row=2,column=0)
		titleframe = Frame(self.game_window, bg ="red")	
		titleframe.grid(row=3, column=0, columnspan=5, sticky='ew')
		Label(titleframe,text='Last score: ',bg='red').grid(row=3,column=0)
		titleframe = Frame(self.game_window, bg ="green")	
		titleframe.grid(row=4, column=0, columnspan=5, sticky='ew')
		Label(titleframe,text='Current score: ',bg='green').grid(row=4,column=0)

#Potentially you can put in a handicap, starting at a lower score. 
#		self.player1.inp = self.player_output(self.player1,self.player2,initial_score=501,col=1)
	#	self.player2.inp = self.player_output(self.player2,self.player1,initial_score=501,col=2)


		#window = Toplevel(self.game_window)
		#fr = Frame(window)
		#fr.pack(side=BOTTOM)

		"""
		Right now, the program is working with a small plot at the bottom.
		To do:
		1/ Make a controller that separates plot from buttons.
		2/ Put out the dartsboard in the plot.
		3/ Lines 185 and 186 are currently not working with the figure. Again: that can be controlled.
		4/ Show the latest bot-throws, with larger alpha for older trows.
		5/ Also indicate where the bot is throwing. 
		"""


		f = plt.figure(figsize=(3,3))
		plt.plot([0,1],[0,1])
		#plt.ion()
		canvas = FigureCanvasTkAgg(f, master=fr)
		canvas.show()
		canvas.get_tk_widget().pack(side=LEFT,  expand=True) #fill=BOTH


		#exit = Button(self.game_window,text='Exit game',command=self.game_window.destroy).grid(row=7,column=4)

	def player_output(self,player,player2,initial_score,col=1):
		Label(self.game_window,text='%s'%player.name).grid(row=0,column=col)
		player.score = initial_score
		lab1 = Label(self.game_window,text='%s'%str(player.score)) #current score
		lab2 = Label(self.game_window,text='') #last score
		lab3 = Label(self.game_window,text='') #3-dart average
		lab1.grid(row=4,column=col)
		lab2.grid(row=3,column=col)
		lab3.grid(row=2,column=col)

		if isinstance(player,Bot):
			inp1 = Entry(self.game_window,state='disabled')
			inp1.grid(row=5,column=col)
		else:
			inp1 = Entry(self.game_window,state='normal')
			inp1.grid(row=5,column=col)
			var1 = IntVar()
			Checkbutton(self.game_window,text='Double finish',variable=var1,bg='purple').grid(row=6,column=col)
			b = Button(self.game_window,text='Go!')
			b['command'] = lambda arg1=inp1,arg2=[lab1,lab2,lab3],arg3=player,arg4=player2, arg5=var1: \
												self._update(arg1,arg2,arg3,arg4,arg5)
			b.grid(row=7,column=col)
		return inp1


	def _update(self,value,labels,player,player2,dbl_finish):
		player._get_score(int(value.get()))
		labels[0].configure(text=str(player.score))
		labels[1].configure(text=value.get())
		labels[2].configure(text='%.1f'%(player.total/player.darts*3))
		if (player.score == 0)&(dbl_finish.get() == 1):
			print('%s won!'%player.name)
		player.deactivate()#inp.configure(state='disabled')
		player2.activate(player)

	def new_player(self):
		self.window = Toplevel(self.topLevel)
		e1 = Entry(self.window,width=18)
		e2 = Entry(self.window,width=18)
		e3 = Entry(self.window,width=3)
		
		e1.grid(row=0,column=1)
		e2.grid(row=1,column=1)
		e3.grid(row=2,column=1)

		Label(self.window,text='Player 1: ').grid(row=0)
		Label(self.window,text='Player 2: ').grid(row=1)
		Label(self.window,text='Number of legs: ').grid(row=2)

		var1 = IntVar()
		var2 = IntVar()
		Checkbutton(self.window,text='Bot',variable=var1).grid(row=0,column=2)
		Checkbutton(self.window,text='Bot',variable=var2).grid(row=1,column=2)

		def _players(entries,bot1,bot2):
			name1,name2,gamesize = entries
			name1 = name1.get()
			name2 = name2.get()
			if name1 == '': name1 = 'Player 1'
			if name2 == '': name2 = 'Player 2'
			if int(bot1.get()) == 1:
				self.player1 = Bot(name1)
			else:
				self.player1 = Human(name1)
			if int(bot2.get()) == 1:
				self.player2 = Bot(name2)
			else:
				self.player2 = Human(name2)
			try:
				self.gamesize = int(gamesize)
				if self.gamesize > 5: print('Too many legs, defaulting to 3')
			except:
				self.gamesize = 3
			self.window.destroy()

		g = Button(self.window,text='Done')
		#g['command'] = lambda arg1=e1.get(),arg2=e2.get(),arg3=e3.get(),arg4=e4.get(): _players(arg1,arg2,arg3,arg4)
		#g['command'] = lambda arg1=e1,arg2=e2,arg3=var1,arg4=var2:\
		#							 _players(arg1,arg2,arg3,arg4)
		g['command'] = lambda arg1=[e1,e2,e3],arg2=var1,arg3=var2:\
									_players(arg1,arg2,arg3)
		g.grid(row=3,columns=2)

		self.topLevel.wait_window(self.window)

	def open_window(self):
		self.window = Toplevel(self.topLevel)

	def _openfilename(self):
		filename = filedialog.askopenfilename(title ='"pen') 
		return filename 

	def menubar(self):
		menubar = Menu(self.topLevel)
		filemenu = Menu(menubar,tearoff=0)
		filemenu.add_command(label='Quite',command=self.topLevel.quit)
		filemenu.add_command(label='Hello',command=self.hello)
		filemenu.add_command(label='Set board...',command=self.make_board)
		filemenu.add_separator()
		menubar.add_cascade(label='File',menu=filemenu)

		editmenu = Menu(menubar,tearoff=0)
		editmenu.add_command(label='Cut',command=self.hello)
		editmenu.add_command(label='Copy',command=self.hello)
		editmenu.add_command(label='Paste',command=self.hello)
		menubar.add_cascade(label='Edit',menu=editmenu)

		helpmenu = Menu(menubar,tearoff=0)
		helpmenu.add_command(label='About',command=self.hello)
		menubar.add_cascade(label='Help',menu=helpmenu)
		self.topLevel.config(menu=menubar)

Darts()