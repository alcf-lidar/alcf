import numpy as np
from scipy import optimize

def lognorm_reff(mu, sigma2):
	return np.exp(mu + 5./2.*sigma2)

def lognorm_sigma2eff(mu, sigma2):
	return (np.exp(4.*mu + 8.*sigma2) - np.exp(4.*mu + 7.*sigma2))/np.exp(2.*mu + 2.*sigma2)

def lognorm_find_mu_sigma2(reff, sigma2eff):
	def f(x):
		mu = x[0]**2.
		sigma2 = x[1]**2.
		return [
			lognorm_reff(mu, sigma2) - reff,
			lognorm_sigma2eff(mu, sigma2) - sigma2eff
		]
	res = optimize.root(f, [np.sqrt(np.log(reff)), np.sqrt(np.log(sigma2eff))])
	mu = res.x[0]**2.
	sigma2 = res.x[1]**2.
	return mu, sigma2

def lognorm_pdf(r, mu, sigma):
	return 1./r*np.exp(-((np.log(r) - mu)**2.)/(2.*sigma**2.))

def gamma_pdf(r, reff, sigmaeff):
	nueff = (sigmaeff/reff)**2.
	return r**((1. - 3.*nueff)/nueff)*np.exp(-r/(reff*nueff))

def reff_num(r, n):
	return np.sum(r**3.*n)/np.sum(r**2.*n)

def sigma2eff_num(r, n, reff):
	return np.sum((r - reff)**2.*r**2.*n)/np.sum(r**2.*n)

def calc_sd(r, n):
	mean = calc_mean(r, n)
	return np.sqrt(np.sum((r - mean)**2.*n)/np.sum(n))

def calc_mean(r, n):
	return np.sum(r*n)/np.sum(n)
