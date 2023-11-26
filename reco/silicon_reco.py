import numpy as np
from skspatial.objects import Cylinder, Line, LineSegment
import pars
import uproot
from tqdm import tqdm
import sys

# si fitta poi il vertice con breit_wigner + gaussiana
'''
   1  p0           1.73835e+06   1.17614e+05   3.24825e+01   1.75651e-10
   2  p1           3.44210e+03   1.91498e+02   4.22778e-01  -7.34294e-08
   3  p2           2.44073e+02   8.51980e+00   8.94765e-03   8.20437e-06
   4  p3           0.00000e+00     fixed
   5  p4           8.92661e+03   3.08846e+02   6.04666e-01   1.01047e-07
'''

def closest_line_seg_line_seg(int_e_1, int_e_2, int_p_1, int_p_2):
    p1 = int_e_1 - (int_e_2 - int_e_1)*100
    p2 = int_e_2
    p3 = int_p_1 - (int_p_2 - int_p_1)*100
    p4 = int_p_2
    P1 = p1
    P2 = p3
    V1 = p2 - p1
    V2 = p4 - p3
    V21 = P2 - P1
    v22 = np.dot(V2, V2)
    v11 = np.dot(V1, V1)
    v21 = np.dot(V2, V1)
    v21_1 = np.dot(V21, V1)
    v21_2 = np.dot(V21, V2)
    denom = v21 * v21 - v22 * v11
    if np.isclose(denom, 0.):
        s = 0.
        t = (v11 * s - v21_1) / v21
    else:
        s = (v21_2 * v21 - v22 * v21_1) / denom
        t = (-v21_1 * v21 + v11 * v21_2) / denom
    s = max(min(s, 1.), 0.)
    t = max(min(t, 1.), 0.)
    p_a = P1 + s * V1
    p_b = P2 + t * V2
    return p_a, p_b

def smear(p):
  p_r = np.sqrt(p[0]*p[0] + p[1]*p[1])
  p_phi = np.arctan2(p[1]/p_r, p[0]/p_r)
  p_phi += np.random.normal(0, 10)/p_r
  p_z = p[2] + np.random.normal(0, 10)
  return np.array([p_r*np.cos(p_phi), p_r*np.sin(p_phi), p_z])

def rotate_by_theta_phi(vec, theta, phi):
  R_phi = np.array([[np.cos(phi), -np.sin(phi), 0],
                           [np.sin(phi), np.cos(phi), 0],
                           [0, 0, 1]])

  R_theta = np.array([[np.cos(theta), 0, np.sin(theta)],
                             [0, 1, 0],
                             [-np.sin(theta), 0, np.cos(theta)]])
  return np.dot(R_phi, np.dot(R_theta, vec))

def mcs_new_direction(x, x0, direction):
  s_theta = 13.6/105.7*np.sqrt(x/x0) # va modificato per prendere l'energia dal ttree
  theta = np.random.normal(0, s_theta)
  phi = np.random.uniform(0, 2*np.pi)
  scatt_vec = rotate_by_theta_phi([0, 0, 1], theta, phi)
  r_orig = np.linalg.norm(direction)
  theta_orig = np.arccos(direction[2]/r_orig)
  phi_orig = np.arccos(direction[0]/r_orig)*np.sign(direction[1])
  return rotate_by_theta_phi(scatt_vec, theta_orig, phi_orig)


def get_e_p_intersections(cylinder, e_start, e_dir, p_start, p_dir):
    e_line = Line(point=e_start, direction=e_dir)
    p_line = Line(point=p_start, direction=p_dir)
    e_seg = LineSegment(e_start, e_start+100e4*e_dir)
    p_seg = LineSegment(p_start, p_start+100e4*p_dir)
    e_int = 0
    p_int = 0
    points_e = cylinder.intersect_line(e_line)
    for p in points_e:
      if e_seg.contains_point(p): e_int = smear(p)
    points_p = cylinder.intersect_line(p_line)
    for p in points_p:
      if p_seg.contains_point(p): p_int = smear(p)
    return (e_int, p_int)

def run(filename, n, outfile):
  inf = uproot.open(filename)
  t = inf["events"]
  n = min(t.num_entries, n)
  e_comp = t["e_comp"].array(library="np")[:n]
  e_mom = t["e_mom"].array(library="np")[:n]
  p_comp = t["p_comp"].array(library="np")[:n]
  p_mom = t["p_mom"].array(library="np")[:n]
  w = t["w"].array(library="np")[:n]
  v_comp = t["v_comp"].array(library="np")[:n]
  vl = []
  dxl = []
  drl = []
  cdal = []
  beampipein = Cylinder(point=[0, 0, 0], vector=[0, 0, 50e4], radius=4.4e4) #50cm long in z; radius 12 cm
  beampipeout = Cylinder(point=[0, 0, 0], vector=[0, 0, 50e4], radius=4.4e4+50) #50cm long in z; radius 12 cm
  cylinder1in = Cylinder(point=[0, 0, 0], vector=[0, 0, 50e4], radius=5e4) #50cm long in z; radius 12 cm
  cylinder1out = Cylinder(point=[0, 0, 0], vector=[0, 0, 50e4], radius=5e4+100) #50cm long in z; radius 12 cm
  cylinder2 = Cylinder(point=[0, 0, 0], vector=[0, 0, 50e4], radius=7e4) #50cm long in z; radius 12 cm
  for ind in tqdm(range(int(n))):
    e_vec = e_comp[ind]/e_mom[ind]
    p_vec = p_comp[ind]/p_mom[ind]
    vertex = v_comp[ind]
    try:
      point_e_bp_in, point_p_bp_in = get_e_p_intersections(beampipein, vertex, e_vec, vertex, p_vec)
      point_e_bp_out, point_p_bp_out = get_e_p_intersections(beampipeout, vertex, e_vec, vertex, p_vec)
      e_pathlength = np.linalg.norm(point_e_bp_out - point_e_bp_in)
      p_pathlength = np.linalg.norm(point_p_bp_out - point_p_bp_in)
      e_vec = mcs_new_direction(e_pathlength, 17.8e4, e_vec)
      p_vec = mcs_new_direction(p_pathlength, 17.8e4, p_vec)

      point_e_c1_in, point_p_c1_in = get_e_p_intersections(cylinder1in, point_e_bp_out, e_vec, point_p_bp_out, p_vec)
      point_e_c1_out, point_p_c1_out = get_e_p_intersections(cylinder1out, point_e_bp_out, e_vec, point_p_bp_out, p_vec)
      e_pathlength = np.linalg.norm(point_e_c1_out - point_e_c1_in)
      p_pathlength = np.linalg.norm(point_p_c1_out - point_p_c1_in)
      e_vec = mcs_new_direction(e_pathlength, 9.3e4, e_vec)
      p_vec = mcs_new_direction(p_pathlength, 9.3e4, p_vec)

      point_e_c1 = (point_e_c1_out + point_e_c1_in)/2
      point_p_c1 = (point_p_c1_out + point_p_c1_in)/2

      point_e_c2, point_p_c2 = get_e_p_intersections(cylinder2, point_e_c1_out, e_vec, point_p_c1_out, p_vec)

      closest_approach_points = closest_line_seg_line_seg(point_e_c1, point_e_c2, point_p_c1, point_p_c2)
      cda = np.linalg.norm(closest_approach_points[0] - closest_approach_points[1])
      v = (closest_approach_points[0] + closest_approach_points[1])/2
      d = closest_line_seg_line_seg(np.array([0, 0, 0]), np.array([1e5, 0, 0]), point_e_c1, point_p_c1)
      vl.append(v[0])
      dxl.append(d[0][0])
      lor = Line(point_e_c1, point_p_c1)
      drl.append(lor.distance_line(Line([0, 0, -1e5], [0, 0, 1e5])))
      cdal.append(cda)
    except ValueError as error:
      #print('An exception occurred: {}'.format(error))
      vl.append(-99)
      dxl.append(-99)
      drl.append(-99)
      cdal.append(-99)

  f = uproot.recreate(outfile)
  f["tree"] = {"v": vl, "dx": dxl, "dr": drl, "cda": cdal, "e_mom": e_mom, "e_comp": e_comp, "p_mom": p_mom, "p_comp": p_comp, "w": w, "v_comp": v_comp}
  f.close()

if __name__ == "__main__":
  run(sys.argv[1], int(sys.argv[2]), sys.argv[3])
