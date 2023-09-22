import ROOT
import sys
import pars
import numpy as np
from tqdm import tqdm
import uproot

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
    _n = np.random.choice(range(1, 30), 1)[0]
    length = pars.tm_1s_length * _n**3
    v_comp[i, :] = np.array([ROOT.gRandom.Exp(length) + ROOT.gRandom.Gaus(0, pars.x_ip_sigma), 0, ROOT.gRandom.Gaus(0, pars.z_ip_sigma)]) #1mm in x as a try
    _w = 0
    while True:
      _w = tm_ps.Generate()
      e = tm_ps.GetDecay(0)
      p = tm_ps.GetDecay(1)
      theta_lab_e = e.Theta()
      theta_lab_p = p.Theta()
      if theta_lab_e > 60/180*np.pi and theta_lab_e < 120/180*np.pi and theta_lab_p > 60/180*np.pi and theta_lab_p < 120/180*np.pi: break
    e_comp[i, :] = e.Vect()
    e_mom[i] = e.P()
    p_comp[i, :] = p.Vect()
    p_mom[i] = p.P()
    w[i] = _w/_n**3
    n[i] = _n
  f = uproot.recreate("sign_gen.root")
  f["events"] = {"e_mom": e_mom, "e_comp": e_comp, "p_mom": p_mom, "p_comp": p_comp, "w": w, "n": n, "v_comp": v_comp}
  f.close()
