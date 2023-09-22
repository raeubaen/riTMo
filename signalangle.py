import ROOT

f = ROOT.TFile("signalangle.root", "recreate")
treee = ROOT.TTree("tree", "tree")
e_vector = np.zeros((3,)).astype(np.float64)
p_vector = np.zeros((3,)).astype(np.float64)
tree.Branch("ele", e_vector, "ele[3]/D")
tree.Branch("pos", p_vector, "pos[3]/D")

tm_vec = ROOT.TLorentzVector(0.0053, 0, 0, 0.2114)
tm_ps = ROOT.TGenPhaseSpace()
tm_ps.SetDecay(tm_vec, 2, np.array([0.000511, 0.000511]))
for i in range(100000):
  tm_ps.Generate()
  e = tm_ps.GetDecay(0)
  p = tm_ps.GetDecay(1)
  e_vector[:] = np.array([e.Px(), e.Py(), e.Pz()])/e.P()
  p_vector[:] = np.array([p.Px(), p.Py(), p.Pz()])/p.P()
  tree.Fill()

tree.Write()
f.Close()
