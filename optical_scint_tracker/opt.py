import numpy as np
import ROOT
from skspatial.objects import Line
import sys
import matplotlib.pyplot as plt

id = sys.argv[1]

debug = 0
# cylindrical vertex locator
if __name__ == "__main__":
  tree = ROOT.TTree("tree", "tree")
  var = np.zeros( (3), dtype=np.float64)
  tree.Branch("pe", var, "pe[3]/D")
  xax = Line([-10, 0], [10, 0])
  for ev in range(int(1000)):
    print(f"ev: {ev}")
    var = var*0
    for y_step in range(int(1e1)):
      print(y_step)
      for n_ph in range(int(1e3)):
        t = (ROOT.gRandom.Uniform()*2-1)*3.14
        pin = np.asarray([0, y_step/1e1+0.5/1e1])
        pfi = pin + 2*np.asarray([np.cos(t), np.sin(t)])
        ph = Line(pin, pfi)
        if debug: plt.plot([pin[0], pfi[0]], [pin[1], pfi[1]])
        try:
          x = ph.intersect_line(xax)[0]
        except:
          continue
        if debug:
          for i in range(3): plt.plot([-1.5+i,-0.5+i],[0,0])
        if abs(x) < 1.5:
          sipm = int(x+1.5)
          var[sipm]+=1*(1e4*0.4*0.3)/2e4
          if debug: print(f"hit{sipm}")
        else:
          if debug: print("no hit")
        if debug: plt.show()
    for i in range(3): var[i] += var[i] + np.random.normal(0, np.sqrt(var[i]))
    print(var)
    tree.Fill()
  tree.SaveAs(f"prova{id}.root")
