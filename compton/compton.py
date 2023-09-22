import scipy.integrate as integrate
from scipy.optimize import minimize
import numpy as np
import uproot
import ROOT

def lolp(t):
  return 1/(1 + 207*(1 - np.cos(t)))

def diff_klein_nishina(t):
  #dsigma/domega
  _lolp = lolp(t)
  return 1/2 * 79.4e-3 * _lolp * _lolp * (_lolp + 1/_lolp - np.sin(t)*np.sin(t))*2*np.pi*np.sin(t)

'''
def _compton_cs_integral(tc):
  return 2*np.pi*integrate.quad(lambda theta: diff_klein_nishina(theta)*np.sin(theta), 0, tc)[0]

compton_cs_norm_integral_norm = _compton_cs_integral(np.pi)
compton_cs_integral = np.vectorize(_compton_cs_integral)
_diff_klein_nishina = np.vectorize(diff_klein_nishina)

get_compton_random_tc = lambda rnd_unif: minimize(lambda tc: (compton_cs_integral(tc)/compton_cs_norm_integral_norm - rnd_unif)**2, 0.1)
'''

max_pdf = minimize(lambda t: - diff_klein_nishina(t), 0.1).x[0]

print(max_pdf)

def extract_theta():
    while True: # Do the following until a value is returned
       # Choose an X inside the desired sampling domain.
       x=np.random.uniform(0, np.pi)
       # Choose a Y between 0 and the maximum PDF value.
       y=np.random.uniform(0, max_pdf)
       # Calculate PDF
       pdf = diff_klein_nishina(x)
       # Does (x,y) fall in the PDF?
       if y<pdf:
           # Yes, so return x
           return x

if __name__ == "__main__":
  t1lst = []
  t2lst = []
  opanglelst = []
  e1lst = []
  e2lst = []
  e1recolst = []
  e2recolst = []

  for i in range(int(1e5)):

    if i%100 == 0: print(i)
    tp1 = extract_theta()
    tp2 = extract_theta()
    ee1 = 105.7*(1 - lolp(t1))
    ee2 = 105.7*(1 - lolp(t2))
    e1reco = e1+np.random.normal(0, e1*0.02/np.sqrt(e1/1000))
    e2reco = e2+np.random.normal(0, e2*0.02/np.sqrt(e2/1000))
    p1v = ROOT.TLorentzVector((105.7-ee)*, 0, 0, 0)
    p1v.SetPtEtaPhiM()
    t1lst.append(t1)
    t2lst.append(t2)
    e1lst.append(e1)
    e1recolst.append(e1reco)
    e2lst.append(e2)
    e2recolst.append(e2reco)
    p1v = ROOT.TLorentzVector()
    p1v.Set
    p1v.SetTheta(t1)
    p2v.SetTheta(np.pi-t2)
    p1v.SetPhi(np.random.uniform()*2*np.pi - np.pi)
    p2v.SetPhi(np.random.uniform()*2*np.pi - np.pi)
    opanglelst.append(np.arccos(e1v.Vect().Dot(e2v.Vect())/(e1v.P()*e2v.P())) )

  f = uproot.recreate("comptonanglesprova2.root")
  f["tree"] = {"t1": t1lst, "t2": t2lst, "e1": e1lst, "e1reco": e1recolst, "e2reco": e2recolst, "e2": e2lst, "opangle": opanglelst}
  f.close()
