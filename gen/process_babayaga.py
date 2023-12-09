import uproot
import pandas as pd
import sys
import numpy as np
import os
import pylorentz
import silicon_reco_fromarrays as silicon_reco
import sys

try:
  proc_id = sys.argv[1]
  n_phot = int(sys.argv[2])

  workfolder  = f"/eos/user/r/rgargiul/www/babatm/"

  df = pd.read_csv(f"{workfolder}/{proc_id}_{n_phot}/run/events.dat", delim_whitespace=True, header=None, names=["0", "1", "2", "3", "4"])

  n_rows_per_ev = 5 + n_phot

  weights = df[df.index % n_rows_per_ev == 1]["0"].astype(float).to_numpy()
  ele = df[df.index % n_rows_per_ev == 3].astype(float).to_numpy()
  pos = df[df.index % n_rows_per_ev == 4].astype(float).to_numpy()
  del df
  ele = pylorentz.Momentum4(ele[:, 0], ele[:, 1], ele[:, 2], ele[:, 3]).boost(-1, 0, 0, beta=np.sin(50e-3/2),).components.T
  pos = pylorentz.Momentum4(pos[:, 0], pos[:, 1], pos[:, 2], pos[:, 3]).boost(-1, 0, 0, beta=np.sin(50e-3/2),).components.T

  '''
  f = uproot.recreate(f"{workfolder}/bhabha_gen_{proc_id}_{i}.root")
  f["events"] = {
    "e_mom": np.sqrt(ele[:, 0]**2 - (0.511e-3)**2), 
    "e_comp": ele[:, 1:], 
    "p_mom": np.sqrt(pos[:, 0]**2 - (0.511e-3)**2), 
     "p_comp": pos[:, 1:], 
     "w": weights, 
     "v_comp": np.zeros((len(weights), 3))
  }
  f.close()
  del ele
  del pos
  del weights
  #silicon_reco.run(e_comp, e_mom, p_comp,p_mom, w, v_comp, outfile)
  '''

  silicon_reco.run(
    ele[:, 1:], np.sqrt(ele[:, 0]**2 - (0.511e-3)**2),
    pos[:, 1:], np.sqrt(pos[:, 0]**2 - (0.511e-3)**2),
    np.arccos((ele[:, 1]*pos[:, 1] + ele[:, 2]*pos[:, 2] + ele[:, 3]*pos[:, 3])/(ele[:, 0]*pos[:,0])),
    weights, np.zeros((len(weights), 3)), f"{workfolder}/bhabha_reco_{proc_id}_{n_phot}.root"
  )

except Exception as e:
  print(e)
else:
  os.system(f"rm -r {workfolder}/{proc_id}_{n_phot}")
