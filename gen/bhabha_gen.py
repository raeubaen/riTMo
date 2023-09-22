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
  nev = int(float(sys.argv[1]))
  tm_vec = ROOT.TLorentzVector(0.0053, 0, 0, 0.2114)
  tm_ps = ROOT.TGenPhaseSpace()
  tm_ps.SetDecay(tm_vec, 2, np.array([0.000511, 0.000511]))
  e_comp = np.zeros((nev, 3))
  e_mom = np.zeros((nev,))
  p_comp = np.zeros((nev, 3))
  p_mom = np.zeros((nev,))
  w = np.zeros((nev,))
  n = np.zeros((nev,))
  v_comp = np.zeros((nev, 3))
  for i in tqdm(range(nev)):
    v_comp[i, :] = np.array([ROOT.gRandom.Gaus(0, pars.x_ip_sigma), 0, ROOT.gRandom.Gaus(0, pars.z_ip_sigma)])
    while True:
      _w = tm_ps.Generate()
      e = tm_ps.GetDecay(0)
      p = tm_ps.GetDecay(1)
      e_copy = ROOT.TLorentzVector(e)
      e_copy.Boost(-tm_vec.Beta(), 0, 0)
      theta_cm = e_copy.Theta()
      theta_lab_e = e.Theta()
      theta_lab_p = p.Theta()
      if theta_lab_e > 60/180*np.pi and theta_lab_e < 120/180*np.pi and theta_lab_p > 60/180*np.pi and theta_lab_p < 120/180*np.pi: break
    _w *= diff_bhabha(theta_cm)
    e_comp[i, :] = e.Vect()
    e_mom[i] = e.P()
    p_comp[i, :] = p.Vect()
    p_mom[i] = p.P()
    w[i] = _w
  f = uproot.recreate("bhabha_gen.root")
  f["events"] = {"e_mom": e_mom, "e_comp": e_comp, "p_mom": p_mom, "p_comp": p_comp, "w": w, "v_comp": v_comp}
  f.close()
