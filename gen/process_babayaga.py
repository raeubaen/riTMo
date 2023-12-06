import uproot
import pandas as pd
import sys
import numpy as np
import os
import pylorentz

try:
  proc_id = sys.argv[1]
  workfolder  = f"/eos/user/r/rgargiul/www/babatm/"

  for i in range(10):
    df = pd.read_csv(f"{workfolder}/{proc_id}/run/events.dat", delim_whitespace=True, header=None, names=["0", "1", "2", "3", "4"], nrows=int(1e6*5), skiprows=int(1e6*5*i))
    weights = df[df.index %5 == 1]["0"].astype(float).to_numpy()
    ele = df[df.index % 5 == 3].astype(float).to_numpy()
    pos = df[df.index % 5 == 4].astype(float).to_numpy()
    del df
 
    ele = pylorentz.Momentum4(ele[:, 0], ele[:, 1], ele[:, 2], ele[:, 3]).boost(-1, 0, 0, beta=np.sin(50e-3/2),).components.T
    pos = pylorentz.Momentum4(pos[:, 0], pos[:, 1], pos[:, 2], pos[:, 3]).boost(-1, 0, 0, beta=np.sin(50e-3/2),).components.T

    print(ele.shape)
    print(pos.shape)

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

except Exception as e:
  print(e)
else:
  os.system(f"rm -r {workfolder}/{proc_id}")
