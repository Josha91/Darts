import numpy as np 
import matplotlib.pyplot as plt 
import emcee
from astropy.modeling.functional_models import Gaussian1D
from scipy.integrate import simps
import math
import IPython
import operator as op
from functools import reduce

def ncr(n, r):
	r = min(r, n-r)
	numer = reduce(op.mul, range(n, n-r, -1), 1)
	denom = reduce(op.mul, range(1, r+1), 1)
	return numer // denom  # or / in Python 2

def lnprior(p,bounds):
	if not bounds[0] < p < bounds[1]:
		return -np.inf
	return 0 

def lnlike(p,n,N):
	"""
	N: sample size
	n: number of 25/50
	p: probability of n given sigma
	"""
	return np.log(ncr(N,n)*p**n*(1-p)**(N-n))

def lnprob(p,n,N):

	x = np.linspace(0,170,10000)
	G = Gaussian1D(1,0,p)(x)
	use = x<15.9 #sb radius
	theta = simps(abs(x[use])*G[use],x[use])/simps(abs(x)*G,x)

	bounds = (0,100)
	lp = lnprior(p,bounds)
	if not np.isfinite(lp):
		return -np.inf

	ll = lnlike(theta,n,N)
	if np.isnan(ll): return -np.inf
	return ll+lp

def sampler(n,N):
	ndim,nwalkers = 1, 32
	p0 = np.array([30])
	p0 = [p0+1e-5*np.random.randn(ndim) for k in range(nwalkers)]

	sampler = emcee.EnsembleSampler(nwalkers,ndim,lnprob,args=(n,N))

	n_burnin = 50
	pos,_,_ = sampler.run_mcmc(p0,n_burnin)
	print('Burn-in finished')
	sampler.reset()
	sampler.run_mcmc(pos,200)
	print('Done!')

	return sampler.flatchain

def run_all():
	up,down,med = [],[],[]
	for i in np.arange(0,51):
		print(i)
		tmp = sampler(i,50)
		perc = np.percentile(tmp,[16,50,84])
		up.append(perc[2])
		med.append(perc[1])
		down.append(perc[0])


	IPython.embed()

run_all()
