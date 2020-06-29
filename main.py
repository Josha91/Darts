"""
To do list:
1/ Bind <Return> to GO button.
2/ Get Heatmap working in the program
3/ Get Bot working. 

1/ Check if the game is won (won legs == required number of legs)
2/ Victory screen!!! 
3/ Reset 'current score', update field
4/ Make a section somewhere with average scores in previous legs.
5/ Save previous legs 
6/ Make a simple game to save scores. 
7/ Here: give the option between individual darts, or all. 
8/ Change starting player in new legs. 
10/ Save functionality. To save to a file pertaining to a specific player. 
11/ On the bottom subframe, make tabs.  To switch between graphs, and match statistics. 
12/ Suggest a double to throw
13/ 9-darter celebratory screen
14/ Ask the player in a popup if he had a double finish, instead of a checkbox. 
"""


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
from matplotlib import style
from drawboard import drawBoard

from play_game import *

LARGE_FONT = ("Verdana",12)
BOLD_FONT = ("Verdana",14,"bold")
style.use("ggplot")

class controller(Tk):
	def __init__(self):
		Tk.__init__(self)
		self.geometry('820x580')
		self.maxsize(900,600)
		self.config(bg='salmon')#'skyblue')

		frame1 = menu(self)
		frame1.grid(row=0,column=0,sticky='nsew',pady=50,padx=10)

		#right = Frame(self,width=600,height=500,bg='grey')
		#right.grid(row=0,column=1,padx=10,pady=50)

		self.frames = {}
		self.frames['Menu'] = frame1

		#Frame1 = Frame(self,highlightbackground="black",highlightthickness=1,bg='grey')
		#Frame1.place(anchor='nw',height=200,width=200)

	def show_frame(self,tag):
		frame = self.frames[tag]
		frame.tkraise()

	def new_game(self):
		frame = GameHub(self)
		self.frames['Game'] = frame 


class menu(Frame):
	def __init__(self,root):
		self.root = root
		Frame.__init__(self,root,bg='grey',width=300,height=400)
		label = Label(self,text='Main menu',font=BOLD_FONT,bg='grey')#LARGE_FONT)
		label.pack()#grid(row=0,column=0,pady=50,padx=10)

		button = Button(self, text = 'Head-to-head',command =root.new_game ,highlightbackground='grey')
		button.pack()

		button = Button(self, text = 'Simple game',command = root.new_game,highlightbackground='grey')#self.heatmap)
		button.pack()

		button = Button(self, text = 'Heatmap',command = root.new_game,highlightbackground='grey')#self.heatmap)
		button.pack()

		button = Button(self, text = 'Quit',command = self._quit,highlightbackground='grey')
		button.pack()

	def _quit(self):
		self.root.quit()     # stops mainloop
		self.root.destroy()

class GameHub(Frame):
	def __init__(self,parent):
		Frame.__init__(self,parent,width=600,height=500,bg='grey')
		self.parent = parent
		self.grid(row=0,column=1,padx=10,pady=50)
		#self.columnconfigure(1, weight=1)

		self.subframe = Frame(self,width=580,height=250,bg='white')
		#subframe.grid(row=0,column=1,padx=10,pady=50)
		self.subframe.place(x=5,y=5,height=195,width=500)

		self.subframe2 = Frame(self,width=580,height=250,bg='white')
		#subframe.grid(row=0,column=1,padx=10,pady=50)
		self.subframe2.place(x=5,y=205,height=290,width=590)

		self.subframe3 = Frame(self,width=580,height=250,bg='white')
		#subframe.grid(row=0,column=1,padx=10,pady=50)
		self.subframe3.place(x=510,y=5,height=195,width=85)
		self.new_player()

	def leglist(self):
		Label(self.subframe3,text='Legs won',font=BOLD_FONT).grid(row=0,column=0)
		Label(self.subframe3,text='%s'%self.player1.name).grid(row=2,column=0)
		self.legtext1 = StringVar()
		self.legtext1.set('%d/%d'%(self.player1.legs_won,self.gamesize))
		legs1 = Label(self.subframe3,textvariable=self.legtext1).grid(row=3,column=0)
		Label(self.subframe3,text='%s'%self.player2.name).grid(row=4,column=0)
		self.legtext2 = StringVar()
		self.legtext2.set('%d/%d'%(self.player2.legs_won,self.gamesize))
		self.legs2 = Label(self.subframe3,textvariable=self.legtext2).grid(row=5,column=0)


	def main_game(self):
		lab = Label(self.subframe,text='3-dart average')#,bg='green')
		lab.grid(row=2,column=0)

		lab = Label(self.subframe,text='Last score')#,bg='red')
		lab.grid(row=3,column=0)

		lab = Label(self.subframe,text='Current score')#,bg='green')
		lab.grid(row=4,column=0)

		self.player1.inp = self.player_output(self.player1,self.player2,col=1)
		self.player2.inp = self.player_output(self.player2,self.player1,col=2)

		self.fig1 = plt.figure(figsize=(3,3))
		plt.hist(self.player1.scores,alpha=0.5,lw=3,color='r',label='Player 1')
		plt.hist(self.player2.scores,alpha=0.5,lw=3,color='b',label='Player 2')
		plt.legend()
		plt.ylim([-0.01,1])
		plt.tight_layout()
		self.ax = plt.gca()
		self.canvas = FigureCanvasTkAgg(self.fig1, master=self.subframe2)
		#canvas.show()
		self.canvas.get_tk_widget().place(x=285,y=5,width=280,height=280) #fill=BOTH

		self.fig2,self.ax2 = plt.subplots(1)
		drawBoard(ax=self.ax2)
		canvas2 = FigureCanvasTkAgg(self.fig2,master=self.subframe2)
		canvas2.show()
		canvas2.get_tk_widget().place(x=5,y=5,width=280,height=280)
		plt.ion() #be able to update figures

		self.leglist()

	def player_output(self,player,player2,col=1):
		Label(self.subframe,text='%s'%player.name).grid(row=0,column=col)
		#lab1 = Label(self.subframe,text='%s'%str(player.score))
		##self.player.current_label = lab1
		#self.legtext1 = StringVar()
		#self.legtext1.set('%d/%d'%(self.player1.legs_won,self.gamesize))
		#legs1 = Label(self.subframe3,textvariable=self.legtext1).grid(row=3,column=0)
		player.current_label = StringVar()
		player.current_label.set('%s'%str(player.score))
		Label(self.subframe,textvariable=player.current_label).grid(row=4,column=col)

		lab2 = Label(self.subframe,text='')
		lab3 = Label(self.subframe,text='')
		#lab1.grid(row=4,column=col)
		lab2.grid(row=3,column=col)
		lab3.grid(row=2,column=col)

		if isinstance(player,Bot):
			inp1 = Entry(self.subframe,state='disabled')
			inp1.grid(row=5,column=col)
			return inp1
		else:
			inp1 = Entry(self.subframe,state='normal')
			inp1.grid(row=5,column=col)
			var1 = IntVar()
			Checkbutton(self.subframe,text='Double finish',variable=var1,bg='red').grid(row=6,column=col)

			b = Button(self.subframe,text='Go!')
			b['command'] = lambda arg1=inp1,arg2=[player.current_label,lab2,lab3],arg3=player,arg4=player2, arg5=var1: \
												self._update(arg1,arg2,arg3,arg4,arg5)
			b.grid(row=7,column=col)

			self.subframe.bind('<Return>', lambda x: print('You did this')) #You can hit enter instead of clicking
			return inp1,b

	def _update(self,value,labels,player,player2,dbl_finish):
		try:
			value = int(value.get())
		except:
			MessageBox.showinfo('Input warning','Are you sure that was a valid number?')
			return
		if value <= 180: 
			if (player.score == value)&(dbl_finish.get() == 0):
				value = 0
			player._get_score(value)
			labels[0].set('%s'%str(player.score))
			labels[1].configure(text=value)
			labels[2].configure(text='%.1f'%(player.total/player.darts*3))
			if (player.score == 0)&(dbl_finish.get() == 1):
				MessageBox.showinfo('Leg finished','%s won!'%player.name)
				player.legs_won+=1
				if player.legs_won == self.gamesize:
					#player wins the game! Victory screen
					MessageBox.showinfo('%s won the game!'%player.name)
				self.reset()
				self.leglist()
			self.refreshFigure()
			player.deactivate()#inp.configure(state='disabled')
			player2.activate(player)
		else:
			MessageBox.showinfo('Input warning','That value is a little high!')

	def refreshFigure(self):
		self.ax.cla()
		self.ax.hist(self.player1.scores,alpha=0.5,lw=3,color='r',label='Player 1')
		self.ax.hist(self.player2.scores,alpha=0.5,lw=3,color='b',label='Player 2')
		plt.legend()
		ymax = self.ax.get_ylim()[1]
		self.ax.set_ylim([-0.01,ymax])
		plt.tight_layout()
		self.canvas.draw()

	def reset(self):
		self.player1.reset()
		self.player2.reset()
		self.legtext1.set('%d/%d'%(self.player1.legs_won,self.gamesize))
		self.legtext2.set('%d/%d'%(self.player2.legs_won,self.gamesize))
		self.player1.current_label.set('%s'%self.player1.score)
		self.player2.current_label.set('%s'%self.player2.score)

		if np.sum(self.player1.legs_won+self.player2.legs_won) % 2 == 0:
			self.player1.activate(self.player2)
			self.player2.deactivate()
		else:
			self.player1.deactivate()
			self.player2.activate(self.player1)

	def new_player(self):
		#create a container that can be destroyed once players are selected
		self.tmp = Frame(self.subframe)#self.subframe
		self.tmp.grid(row=0,column=1,padx=10,pady=50)
		widths = [18,18,6,6]
		labels = ['Player: ','Player 2: ','Number of legs: ','Starting score: ']
		entries = []
		for i in range(4):
			etmp = Entry(self.tmp,width=widths[i])
			entries.append(etmp)
			etmp.grid(row=i,column=1)
			Label(self.tmp,text=labels[i]).grid(row=i)

		vari = [IntVar(),IntVar()]
		Checkbutton(self.tmp,text='Bot',variable=vari[0]).grid(row=0,column=2)
		Checkbutton(self.tmp,text='Bot',variable=vari[1]).grid(row=1,column=2)

		def _players(entries,bots):
			name1,name2,gamesize,start_score = entries
			name1 = name1.get()
			name2 = name2.get()
			if name1 == '': name1 = 'Player 1'
			if name2 == '': name2 = 'Player 2'
			if int(bots[0].get()) == 1:
				self.player1 = Bot(name1)
			else:
				self.player1 = Human(name1)
			if int(bots[1].get()) == 1:
				self.player2 = Bot(name2)
			else:
				self.player2 = Human(name2)
			try:
				self.gamesize = int(gamesize)
				if self.gamesize > 5: 
					print('Too many legs, defaulting to 3')
					self.gamesize = 3
			except:
				self.gamesize = 3
			try:
				sc = int(start_score.get())
				if sc < 50: 
					print("That's a very low score... let's start at 201!")
					sc = 201
			except:
				sc = 201
			self.player1.startscore,self.player1.score = sc,sc
			self.player2.startscore,self.player2.score = sc,sc
			self.tmp.destroy()
			self.main_game()

		g = Button(self.tmp,text='Done')
		g['command'] = lambda arg1=entries,arg2=vari:\
									_players(arg1,arg2)
		g.grid(row=i+1,columns=2)

t = controller()
t.mainloop()
