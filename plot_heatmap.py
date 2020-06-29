from __future__ import print_function
from __future__ import unicode_literals


import matplotlib
# This defines the Python GUI backend to use for matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import numpy as np 
import math
from drawboard import boardsize,drawBoard
import IPython
from astropy.modeling.functional_models import Gaussian2D
from astropy.convolution import convolve_fft as fft
from tkinter import *

#First: make a score function. This returns the score given an x,y
#Then: Build matrix for a grid in x,y
#then: Put in a Gaussian function
#then: Convolve the two
#Convolution is a heat map of expected scores. 

def score(x,y,board=None):
    """
    Given an x and y, this function returns the score.
    """
    if board is None: board = boardsize()

    r = np.sqrt(x**2.+y**2.)

    if r > board.c2od: return 0  #off the board
    if r <= board.c2db: return 50 #double bull
    if r <= board.c2sb: return 25 #single bull

    #angular size of a segment
    ang_size = 2*np.pi/len(board.arr)


    th = math.atan2(x,y) + ang_size/2 #switched x,y; left edge of 20 = 0, then clockwise. 
    if th < 0: th = 2*np.pi + th 

    n = board.arr[int(np.floor(th/ang_size))]

    if r <= board.c2it: return n #single, inside the triple ring.
    if r <= board.c2ot: return 3*n #triple
    if r <= board.c2id: return n #single, outside triple ring

    return 2*n #double by exclusion.

def score_grid(N=201):
    board = boardsize()
    r = np.linspace(-board.c2od,board.c2od,N)
    return np.vectorize(score)(*np.meshgrid(r,r,sparse=True))

def plot_heatmap(parent=None):
    #get the scores on the board
    if parent is not None:
        frame = Frame(parent,width=600,height=500,bg='grey')
        frame.grid(row=0,column=1,padx=10,pady=50)

    s = score_grid()

    board = boardsize()
    N = 201
    buff = 40 #buffer for plotting
    fsize = 14
    r = np.linspace(-board.c2od,board.c2od,N)
    x,y = np.meshgrid(r,r)
    fig,ax = plt.subplots(2,2)
    for j,sigma in enumerate([3,15,30,60]):
      g = Gaussian2D(1,0,0,sigma,sigma)(x,y) #Gaussian throw distribution

      Ex = fft(s,g,normalize_kernel=True) #expected 1-dart score

      axi = ax.flatten()[j]

      aim = np.where(Ex == Ex.max())
      xc,yc = np.median(x[aim]),np.median(y[aim])

      im = axi.imshow(Ex*3,cmap='inferno',origin='lower',extent=[x.min(),x.max(),y.min(),y.max()])
      axi.scatter(xc,yc,color='w',s=40,zorder=4)
      axi.scatter(xc,yc,color='r',s=20,zorder=5)
      axi.set_xticklabels([])
      axi.set_yticklabels([])
      axi.set_title('$\sigma=$%.1f mm'%sigma,fontsize=fsize)
      axi.set_xlim([x.min()-buff,x.max()+buff])
      axi.set_ylim([x.min()-buff,x.max()+buff])

      cbar = plt.colorbar(im,ax=axi)
      cbar.set_label('Expected 3-dart score',fontsize=fsize-3)

      drawBoard(ax=axi,color_on=False,zorder=3)

    plt.tight_layout()
    #plt.show()
    if parent is not None:
        canvas = FigureCanvasTkAgg(fig, master=frame)
        #canvas.show()
        canvas.get_tk_widget().place(x=5,y=5,width=590,height=490) 
    else:
        plt.show()

def plot_heatmap_sigma(sigma,axi=None):
    if axi is None:
      fig,axi = plt.subplots(1)

    s = score_grid()
    board = boardsize()
    N = 201
    fsize = 14
    buff = 30
    r = np.linspace(-board.c2od,board.c2od,N)
    x,y = np.meshgrid(r,r)
    g = Gaussian2D(1,0,0,sigma,sigma)(x,y) #Gaussian throw distribution

    Ex = fft(s,g,normalize_kernel=True) #expected 1-dart score

    aim = np.where(Ex == Ex.max())
    xc,yc = np.median(x[aim]),np.median(y[aim])

    im = axi.imshow(Ex*3,cmap='inferno',origin='lower',extent=[x.min(),x.max(),y.min(),y.max()])
    axi.scatter(xc,yc,color='w',s=40,zorder=4)
    axi.scatter(xc,yc,color='r',s=20,zorder=5)
    axi.set_xticklabels([])
    axi.set_yticklabels([])
    axi.set_title('$\sigma=$%.1f mm'%sigma,fontsize=fsize)
    axi.set_xlim([x.min()-buff,x.max()+buff])
    axi.set_ylim([x.min()-buff,x.max()+buff])

    cbar = plt.colorbar(im,ax=axi)
    cbar.set_label('Expected 3-dart score',fontsize=fsize-3)

    drawBoard(ax=axi,color_on=False,zorder=3)

   # IPython.embed()
if __name__ == "__main__":
    plot_heatmap()



