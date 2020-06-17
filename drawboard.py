import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.patheffects as pe


class boardsize():
    def __init__(self,arr='standard'):
      #Board measurements
      self.c2db = 6.35 #center to DB wire
      self.c2sb = 15.9 #center to SB wire
      self.c2it = 99 #center to inner triple ring
      self.c2ot = 107 #center to outer triple ring
      self.c2id = 162 #center to inner double ring
      self.c2od = 170 #center to outer double ring

      self.R = [self.c2db,self.c2sb,self.c2it,self.c2ot,self.c2id,self.c2od]

      #Dartboard scores arrangement, clockwise starting top center
      if arr == 'curtis':
          self.arr = [20,1,19,3,17,5,15,7,13,9,11,10,12,8,14,6,16,4,18,2]
      elif arr == 'linear':
          self.arr = [20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1]
      else: #default to standard
          self.arr = [20,1,18,4,13,6,10,15,2,17,3,19,7,16,8,11,14,9,12,5]

class drawBoard():
  def __init__(self,ax=None,color_on=True,**kwargs):
      #Plot the dartsboard.
      board = boardsize()

      if ax is None: fig,ax = plt.subplots(1)

      t = np.linspace(0,2*np.pi,5000)
      x,y = np.cos(t),np.sin(t)

      ax.plot(board.c2od*x,board.c2od*y,color='k',**kwargs)
      ax.plot(board.c2id*x,board.c2id*y,color='k',**kwargs)
      ax.plot(board.c2it*x,board.c2it*y,color='k',**kwargs)
      ax.plot(board.c2ot*x,board.c2ot*y,color='k',**kwargs)
      ax.plot(board.c2sb*x,board.c2sb*y,color='k',**kwargs)
      ax.plot(board.c2db*x,board.c2db*y,color='k',**kwargs)

      ax.axis('off')
      ax.set_aspect('equal')

      for i,lbl in enumerate(board.arr):
          theta = i*2*np.pi/len(board.arr)
          xi = np.sin(theta)*board.c2od
          yi = np.cos(theta)*board.c2od
          t = ax.text(xi*1.1,yi*1.1,str(lbl),va='center',ha='center',fontweight='bold',\
            path_effects=[pe.withStroke(linewidth=2, foreground='w')])

#          t.set_bbox(dict(facecolor='white', alpha=0.8, edgecolor='white'))

          xi2 = np.sin(theta+np.pi/len(board.arr))
          yi2 = np.cos(theta+np.pi/len(board.arr))

          ax.plot([xi2*board.c2sb,xi2*board.c2od],[yi2*board.c2sb,yi2*board.c2od],color='k',**kwargs)

          if i%2 == 0:
              clr1 = 'red'
              clr2 = 'black'
          else:
              clr1 = 'green'
              clr2 = 'white'

          if color_on:
              ths = np.linspace(i-0.5,i+0.5)*2*np.pi/len(board.arr)
              xii = np.concatenate((np.sin(ths)*board.c2id,np.sin(ths[::-1])*board.c2od))
              yii = np.concatenate((np.cos(ths)*board.c2id,np.cos(ths[::-1])*board.c2od))
              plt.fill(xii,yii,clr1)
              xii = np.concatenate((np.sin(ths)*board.c2it,np.sin(ths[::-1])*board.c2ot))
              yii = np.concatenate((np.cos(ths)*board.c2it,np.cos(ths[::-1])*board.c2ot))
              plt.fill(xii,yii,clr1)
              xii = np.concatenate((np.sin(ths)*board.c2ot,np.sin(ths[::-1])*board.c2id))
              yii = np.concatenate((np.cos(ths)*board.c2ot,np.cos(ths[::-1])*board.c2id))
              plt.fill(xii,yii,clr2)
              xii = np.concatenate((np.sin(ths)*board.c2sb,np.sin(ths[::-1])*board.c2it))
              yii = np.concatenate((np.cos(ths)*board.c2sb,np.cos(ths[::-1])*board.c2it))
              plt.fill(xii,yii,clr2)

      if color_on:
          ths = np.linspace(0,2*np.pi,100)
          plt.fill(np.cos(ths)*board.c2sb,np.sin(ths)*board.c2sb,color='green',zorder=0)
          plt.fill(np.cos(ths)*board.c2db,np.sin(ths)*board.c2db,color='red',zorder=1)


if __name__ == "__main__":
    drawBoard()
    plt.show()


#STUFF TO PUT IN:
#Play a game against Random opponent.
#Play a game (just input scores)
#GUI
#Function to calculate where is best to aim (the statistics paper)
#Heat map of where you've thrown (save past throws)
#Calculate possible checkouts




