import numpy as np
import sys
from scipy.stats import norm
import pars
import math

def signal_yield_n_state(tm, n, cut):
  length = pars.tm_1s_length * (n**3)
  return tm * pars.tm_1s_weight / (n**3) * (np.exp(-cut/length) - np.exp(-pars.vertex_x_acc/length))

def signal_yield_all_n(total_tm, cut):
  return [signal_yield_n_state(total_tm, n, cut) for n in range(1, pars.n_max)] # per debug salvo tutto poi magari uno se lo cerca

def bhabha_yield(total_bhabha, reso, cut):
  sigma = np.sqrt(reso*reso + pars.x_ip_sigma*pars.x_ip_sigma)
  suppression = norm.sf(cut, loc=0, scale=sigma) - norm.sf(pars.vertex_x_acc, loc=0, scale=sigma)
  return total_bhabha * suppression

def poissonian_likelihood(n, s, b, mu):
  return (mu*s+b)**n/math.gamma(n+1)*np.exp(-mu*s-b) + 1e-100 #math.gamma(n+1) = math.factorial(n)

def get_observed_events_at_2sigma(exp_events):
  pcdf = 0
  lim_obs = 0 #per essere conservativi non valutiamo la poissoniana fino a s+b-1, ma fino al valore che ha alla sua destra il 95% della distrubuzione poissoniana aspettata
  # per esempio se il numero di eventi aspettati è 3, nella realtà difficilmente si osservano 3 eventi ma più facilmente 1 o 2
  if exp_events > 20: return exp_events - 1.644*np.sqrt(exp_events) #norm.cdf(-1.644) = 0.05
  else:
    for i in range(int(exp_events)):
      pcdf += np.exp(-exp_events)*math.pow(exp_events, i)/math.gamma(i+1)
      if pcdf > 0.05:
        lim_obs = i
        break
    return lim_obs

def poissonian_chi2_low_b(s, b):
  n = get_observed_events_at_2sigma(s+b)
  LR = poissonian_likelihood(n, s, b, 0)/poissonian_likelihood(n, s, b, 1)
  return -2*np.log(LR)

def poissonian_chi2_high_b(s, b):
  n = get_observed_events_at_2sigma(s+b)
  return 2*(n*np.log(n/b) + b - n)

def get_sign_from_s_b(s, b):
  if b<20: return np.sqrt(poissonian_chi2_low_b(s, b))
  else: return np.sqrt(poissonian_chi2_high_b(s, b))

def get_sign_from_reso_cut(total_tm, total_bhabha, reso, cut):
    exp_signal_list = signal_yield_all_n(total_tm, cut)
    s = sum(exp_signal_list)
    b = bhabha_yield(total_bhabha, reso, cut) + pars.other_bkg*pars.days #for numerical stability
    return get_sign_from_s_b(s, b)

if __name__ == "__main__":
  np.seterr(all="ignore")
  print("reso,cut,s,b")

  cut_array = np.arange(pars.mincut, pars.vertex_x_acc, 10)

  for reso in [500, 1000, 2000, 3000, 4000, 5000]:
    for d in np.arange(1, 60, 0.1): #risoluzioni vertice
      pars.days = d
      total_tm = pars.tm_cross_section * pars.lumi_per_day * pars.days
      total_bhabha = pars.bhabha_cross_section * pars.lumi_per_day * pars.days

      opt_cut = 0
      for cut in cut_array:
        sign = get_sign_from_reso_cut(total_tm, total_bhabha, reso, cut)
        if sign > 5:
          opt_cut = cut
          break
      else:
        continue
      opt_sign = get_sign_from_reso_cut(total_tm, total_bhabha, reso, opt_cut)
      exp_signal_list = signal_yield_all_n(total_tm, opt_cut)
      exp_signal = sum(exp_signal_list)
      exp_bkg = bhabha_yield(total_bhabha, reso, opt_cut) + pars.other_bkg*pars.days
      #sys.stderr.write(f"{[d, reso, opt_cut, round(exp_signal, 10), round(exp_bkg, 10), [f'{i+1}: {j}' for i,j in enumerate(np.asarray(exp_signal_list).round(1))]]}\n")
      print(",".join([str(v) for v in [d, reso, opt_cut, round(exp_signal, 10), round(exp_bkg, 10)]]))
      break
