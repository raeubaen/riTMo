import scipy.integrate as integrate
import numpy as np

#calcoleremo significatività vs. theta_cut, serve il massimo e non il valore assoluto per cui le costanti moltiplicative davanti alle sezioni d'urto sono ininfluenti
1#vedi articolo

def bhabha(theta):
  return 0.5*(197*197)*1e-2/(137*137*211.4*211.4)*((1 + np.cos(theta/2)**4)/(np.sin(theta/2)**4) - 2*(np.cos(theta/2)**4)/(np.sin(theta/2)**2) + (1 + np.cos(theta)**2)/2) #dsigma/domega senza costanti

def _bhabha_integral(tc):
  return 2*np.pi*integrate.quad(lambda theta: bhabha(theta)*np.sin(theta), tc, np.pi-tc)[0] #dsigma integrato in domega; domega è 2pi sin(theta)

def _tm_integral(tc):
  return 124/2*integrate.quad(lambda theta: np.sin(theta), tc, np.pi-tc)[0] #idem come prima ma dsigma/domega è piatto # pb

bhabha_integral = np.vectorize(_bhabha_integral)
tm_integral = np.vectorize(_tm_integral)
