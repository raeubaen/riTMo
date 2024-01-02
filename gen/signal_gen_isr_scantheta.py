import ROOT
import sys
import pars
import numpy as np
from tqdm import tqdm
import uproot
import silicon_reco_fromarrays as silicon_reco

if __name__ == "__main__":
  nev = int(float(sys.argv[1]))
  #egamma_h = ROOT.TFile("egamma_signal_h.root").Get("h")
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
    egamma = float(sys.argv[2]) #h.GetRandom() poi si trova il bin e si mappa per trovare il theta peggiore - dopo lo scan
    egamma /= 1000 #deve essere in GeV
    theta = float(sys.argv[3])
    pt = egamma*np.sin(theta)
    phi = np.random.uniform(-np.pi, np.pi)
    eta = -np.log(np.arctan(theta/2))
    gamma = TLorentzVector()
    gamma.SetPtEtaPhiM(pt, eta, phi, 0)
    tm_vec = ROOT.TLorentzVector(0.0053, 0, 0, 0.2114) - gamma
    tm_ps = ROOT.TGenPhaseSpace()
    tm_ps.SetDecay(tm_vec, 2, np.array([0.000511, 0.000511]))

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
  theta_ep = np.arccos((e_comp[:, 1]*p_comp[:, 1] + e_comp[:, 2]*p_comp[:, 2] + e_comp[:, 3]*p_comp[:, 3])/(e_comp[:, 0]*p_comp[:,0]))
  sumw_nocuts = w.sum()

  reco_arrays = silicon_reco.run(
    e_comp, e_mom, p_comp, p_mom, theta_ep,
    w, v_comp, f"signal_scan_{egamma}_{theta}.root"
  )

  vl = reco_arrays["v"]
  dr = reco_arrays["dr"]

  presel_cuts = (theta_ep > 177/180.*np.pi)
  final_cuts = np.logical_and(vl/1000 > 3, dr/1000 > 5) #va messo quello vero col cerchio
  sumw_aftercuts = w[np.logical_and(presel_cuts, final_cuts)].sum()
  eff = sumw_aftercuts/sumw_nocuts
  print(egamma, theta, eff)
