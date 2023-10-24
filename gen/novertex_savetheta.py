import ROOT
import sys
import pars
import numpy as np
from tqdm import tqdm
import uproot

def diff_bhabha(t):
  #dsigma/dt
  return ((1 + np.cos(t/2)**4)/(np.sin(t/2)**4) - 2*(np.cos(t/2)**4)/(np.sin(t/2)**2) + (1 + np.cos(t)**2)/2)*np.sin(t)

if __name__ == "__main__":
  nev = int(float(sys.argv[1])) #glielo dai da terminale
  p = 0.25
  tm_vec = ROOT.TLorentzVector(p, 0, 0, 0.000511 + np.sqrt(0.000511*0.000511 + p*p)) #mettere boost e sqrt(s) padme
  tm_ps = ROOT.TGenPhaseSpace()
  tm_ps.SetDecay(tm_vec, 2, np.array([0.000511, 0.000511])) #se fai bhabha è giusto sennò va messa la massa a 0 se fai gammagamma
  e_comp = np.zeros((nev, 3))
  e_mom = np.zeros((nev,))
  p_comp = np.zeros((nev, 3))
  p_mom = np.zeros((nev,))
  w = np.zeros((nev,))
  n = np.zeros((nev,))
  theta_e = np.zeros((nev,))
  theta_p = np.zeros((nev,))
  for i in tqdm(range(nev)):
    while True:
      _w = tm_ps.Generate()
      e = tm_ps.GetDecay(0)
      p = tm_ps.GetDecay(1)
      e_copy = ROOT.TLorentzVector(e)
      e_copy.Boost(-tm_vec.Beta(), 0, 0)
      theta_cm = e_copy.Theta()
      theta_lab_e = e.Theta()
      theta_lab_p = p.Theta()
      break
    e_comp[i, :] = e.Vect()
    e_mom[i] = e.P()
    p_comp[i, :] = p.Vect()
    p_mom[i] = p.P()
    w[i] = _w * diff_bhabha(theta_cm)
    theta_e[i] = theta_lab_e
    theta_p[i] = theta_lab_p
  f = uproot.recreate("padme_gen.root")
  f["events"] = {"e_mom": e_mom, "e_comp": e_comp, "p_mom": p_mom, "p_comp": p_comp, "w": w, "theta_e": theta_e, "theta_p": theta_p}
  f.close()
