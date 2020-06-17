import numpy as np
import matplotlib.pyplot as plt 


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
                                       
class EM():
  def __init__(self,x,sinit=100,niter=100,which='simple'):
      self.board = boardsize()

      if which == 'simple':
          self.EMalg(x,n=len(x),sinit=sinit,s=np.zeros(niter),\
                  ll=np.zeros(niter),niter=niter,\
                  R=self.board.R)
        #return(list(s.final=out$s[niter], s.init=s.init, s=out$s,
      elif which == 'general':
          pass

  def EMalg(self,x,np,sinit,s,ll,niterp,R):
      n = np[0]
      niter = niterp[0]
      scur = sinit[0]
      for i in np.arange(niter):
          s[i] = EMStep(x,n,scur,R)
          ll[i] = LogLik(x,n,s[i],R)
          scur = s[i]

  def EMStep(x,n,s,R):
      a,b = np.zeros(6),np.zeros(6)
      ComputeExpConstants(s,R,a) # make sure this works
      ComputeProbConstants(s,R,b)

      e = 0
      for i in np.arange(n):
          e += ComputeExp(x[i],a,b)

      return e/(2*n)

  def _ComputeExpConstants(self,s,R,a):
      a[0] = self._Integ1(s,0,R[0])
      a[1] = self._Integ1(s,R[0],R[1])
      a[2] = self._Integ1(s,R[1],R[2])/20 +self._Integ1(s,R[3],R[4])/20
      a[3] = self._Integ1(s,R[4],R[5])/20
      a[4] = self._Integ1(s,R[2],R[3])/20
      a[5] = self._Integ1(s,R[5],-1)

  def _ComputeProbConstants(self,s,R,b):
      b[0] = self._Integ2(s,0,R[0]) 
      b[1] = self._Integ2(s,R[0],R[1]);
      b[2] = self._Integ2(s,R[1],R[2])/20 + self._Integ2(s,R[3],R[4])/20
      b[3] = self._Integ2(s,R[4],R[5])/20
      b[4] = self._Integ2(s,R[2],R[3])/20
      b[5] = self._Integ2(s,R[5],-1)

  def _Integ1(self,s, r1, r2):
      if r2 == -1: #r2 is assumed to be infinity
          return (r1*r1+2*s)*np.exp(-r1*r1/(2*s))
      else:
          return (r1*r1+2*s)*np.exp(-r1*r1/(2*s)) - \
                      (r2*r2+2*s)*np.exp(-r2*r2/(2*s))

  def _Integ2(self,s, r1, r2):
      if r2 == -1: #r2 is assumed to be infinity
          return np.exp(-r1*r1/(2*s))
      else:
          return np.exp(-r1*r1/(2*s)) - np.exp(-r2*r2/(2*s))

  def _Loglik(self,x, n, s, R):
      self._ComputeProbConstants(s,R,b)
      b = np.zeros(6)
      p = 0
      for i in arange(n):
          p += log(ComputeProb(x[i],b))
      return p




def computeExp(x,a,b):
  if x in [1,5,7,11,13,17,19]:
    return a[2]/b[2]
  elif x in [2,4,8,10,14,16,20]:
    return (a[2]+a[4])/(b[2]+b[4])
  elif x in [3,9,15]:
    return (a[2]+a[4])/(b[2]+b[4])
  elif x in [6,12,18]:
    return (a[2]+a[3]+a[4])/(b[2]+b[3]+b[4])
  elif x in [24,30,36]:
    return (a[3]+a[4])/(b[3]+b[4])
  elif x in [22,26,28,32,34,38,40]:
    return a[3]/b[3]
  elif x in [21,27,33,39,42,45,48,51,54,57,60]:
    return a[4]/b[4]
  elif x == 25:
    return a[1]/b[1]
  elif x == 50:
    return a[0]/b[0]
  else:
    return a[5]/b[5]


def ComputeProb(x,b):
    if x in [1,5,7,11,13,17,19]:
      return b[2]
    elif x in [2,4,8,10,14,16,20]:
      return b[2]+b[3]
    elif x in [3,9,15]:
      return b[2]+b[4]
    elif x in [6,12,18]:
      return b[2]+b[3]+b[4]
    elif x in [24,30,36]:
      return b[3]+b[4]
    elif x in [22,26,28,32,34,38,40]:
      return b[3]
    elif x in [21,27,33,39,42,45,48,51,54,57,60]:
      return b[4]
    elif x == 25:
      return b[1]
    elif x == 50:
      return b[0]
    else: 
      return b[5]

def EMcov(x,npi,Sinit,S1,S2,S3,ll,niterp,computellp,R,ar,ii):
    n = np[0]
    niter = niterp[0]
    computell = computellp[0]
    Scur = Sinit
    A = np.zeros(3)

    for i in range(niter):
        EMCovStep(x,n,Scur,R,ar,ii,A)
        S1[i] = A[0]
        S2[i] = A[1]
        S3[i] = A[2]
        if computell == 0:
            ll[i] = 0
        else:
            ll[i] = LoglikCov(x,n,A,R,ar)
        Scur[0] = S1[i]
        Scur[1] = S2[i]
        Scur[2] = S3[i]

def EMCovStep(x,n,S,R,ar,ii,A):
  B = np.zeros(3)
  C = np.zeros(3)

  for i in range(n):
      SimulateExp(x[i],S,R,ar,ii,B)
      C[0] += B[0]
      C[1] += B[1]
      C[2] += B[2]

  A[0] = C[0]/n
  A[1] = C[1]/n
  A[2] = C[2]/n

def SimulateExp(x,S,R,ar,ii,B):
  det = S[0]*S[1]-S[2]*S[2]
  z = np.zeros(2)
  w,W = 0,0
  B[0] = 0
  B[1] = 0
  B[2] = 0

  for i in range(1000):
      RandomPt(x,R,ar,ii,z)
      w = np.exp(-(S[1]*z[0]*z[0] - 2*S[2]*z[0]*z[1] + S[0]*z[1]*z[1])/(2*det))
      B[0] += z[0]*z[0]*w 
      B[1] += z[1]*z[1]*w
      B[2] += z[0]*z[1]*w 
      W += w

  B[0] /= W;
  B[1] /= W;
  B[2] /= W;

def RandomPt(x,R,ar,ii,z):
  u = np.random.uniform(0,1)
  if x in [1,5,7,11,13,17,19]:
    if u <= ar[2]/(ar[2]+ar[3]):
      RandomSlicePt(x,R[1],R[2],ii,z)
    else:
      RandomSlicePt(x,R[3],R[4],ii,z)
  elif x in [2,4,8,10,14,16,20]:
    if u <= ar[4]/(ar[4]+ar[2]+ar[3]):
      RandomSlicePt(x/2,R[4],R[5],ii,z)
    elif u <= (ar[4]+ar[2])/(ar[4]+ar[2]+ar[3]):
      RandomSlicePt(x,R[1],R[2],ii,z)
    else:
      RandomSlicePt(x,R[3],R[4],ii,z)
  elif x in [3,9,15]:
    if u <= ar[5]/(ar[5]+ar[2]+ar[3]):
      RandomSlicePt(x/3,R[2],R[3],ii,z)
    elif u < (ar[5]+ar[2])/(ar[5]+ar[2]+ar[3]):
      RandomSlicePt(x,R[1],R[2],ii,z)
    else:
      RandomSlicePt(x,R[3],R[4],ii,z)
  elif x = [6,12,18]:
    if u <= ar[5]/(ar[5]+ar[4]+ar[2]+ar[3]):
      RandomSlicePt(x/3,R[2],R[3],ii,z)
    elif u <= (ar[5]+ar[4])/(ar[5]+ar[4]+ar[2]+ar[3]):
      RandomSlicePt(x/2,R[4],R[5],ii,z)
    elif u <= (ar[5]+ar[4]+ar[2])/(ar[5]+ar[4]+ar[2]+ar[3]):
      RandomSlicePt(x,R[1],R[2],ii,z)
    else:
      RandomSlicePt(x,R[3],R[4],ii,z)
  elif x in [24,30,36]:
    if u <= ar[5]/(ar[5]+ar[4]):
      RandomSlicePt(x/3,R[2],R[3],ii,z)
    else:
      RandomSlicePt(x/2,R[4],R[5],ii,z)
  elif x in [22,26,28,32,34,38,40]:
      RandomSlicePt(x/2,R[4],R[5],ii,z)  
  elif x in [21,27,33,39,42,45,48,51,54,57,60]:
      RandomSlicePt(x/3,R[2],R[3],ii,z)
  elif x == 25:
      RandomCirclePt(R[0],R[1],z)
  elif x == 50:
      RandomCirclePt(0,R[0],z)

def RandomSlicePt(x, r1, r2, ii, z):
  k = ii[x-1]
  th = -2*np.pi/40 + (k-1)*2*np.pi/20 + 2*np.pi/20*np.random.uniform(0,1)
  th = np.pi/2 - th
  r = RandomR(r1,r2)
  z[0] = r*np.cos(th)
  z[1] = r*np.sin(th)

def RandomCirclePt(r1, r2, z):
  th = 2*np.pi*np.random.uniform(0,1)
  r = RandomR(r1, r2)
  z[0] = r*np.cos(th)
  z[1] = r*np.sin(th)

def RandomR(r1, r2):
  return np.sqrt(r1*r1 + (r2*r2-r1*r1)*np.random.uniform(0,1))

def LoglikCov(x, n, S, R, ar):
  return 0

def BuildScoreMatrix(A, R, S):
  for i in range(681):
    for j in range(681):
      A[i+681*j] = Score(float(i-340),float(j-340),R,S)

def Score(x, y, R, S):
  #compute the radius
  r = np.sqrt(x*x+y*y)

  #Check if it's off the board (do this for speed)
  if r > R[5]: return 0
  
  #Check for a center bullseye
  if r <= R[0]: return 50

  #Check for a donut bullseye
  if r <= R[1]: return 25

  #Now get the angle
  theta = np.arctan2(y, x) 
  phi = MyMod(np.pi/2 - theta + 2*np.pi/40, 2*np.pi)

  #Now get the number
  i = int(np.floor(phi/(2*np.pi)*20) + 1)
  if i > 20: i = 20
  n = S[i-1]

  #Check for a single
  if r <= R[2]: return n

  #Check for a triple
  if r <= R[3]: return 3*n

  #Check for a single
  if r <= R[4]: return n

  #If we got here, it must be a double
  return 2*n

def MyMod(x, y):
  return x-y*np.floor(x/y)


class drawBoard():
  def __init__(self,ax=None)
      #Plot the dartsboard.
      size = boardsize()

      if ax is None: fig,ax = plt.subplots(1)

      t = np.linspace(0,2*np.pi,length=5000)
      x,y = np.cos(t),np.sin(t)



