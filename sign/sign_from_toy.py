import numpy as np
import sys
from scipy.stats import norm
import pars
import math
import ROOT

#per dr bhabha e vertice assunto piatto

def signal_yield_all_n(signal_th1, total_tm, cut):
  return signal_th1.Integral(int(1+cut/100), signal_th1.GetNbinsX())/8329 * total_tm #binw 100um #8318 integral of all th2 histogram without cuts

def bhabha_yield(bhabha_f, total_bhabha, cut):
  return bhabha_f.Integral(cut/1000, 10)*total_bhabha

def poissonian_likelihood(n, s, b, mu):
  return (mu*s+b)**n/math.gamma(n+1)*np.exp(-mu*s-b) + 1e-100 #math.gamma(n+1) = math.factorial(n)

def poissonian_chi2_low_b(s, b):
  n = s+b
  LR = poissonian_likelihood(n, s, b, 0)/poissonian_likelihood(n, s, b, 1)
  return -2*np.log(LR)

def poissonian_chi2_high_b(s, b):
  n = s+b
  return 2*(n*np.log(n/b) + b - n)

def get_sign_from_s_b(s, b):
  if b<20: return np.sqrt(poissonian_chi2_low_b(s, b))
  else: return np.sqrt(poissonian_chi2_high_b(s, b))

def get_sign_from_reso_cut(signalth1, bhabha_f, total_tm, total_bhabha, cut):
    s = signal_yield_all_n(signalth1, total_tm, cut)
    b = bhabha_yield(bhabha_f, total_bhabha, cut) + pars.other_bkg*pars.days #for numerical stability
    return get_sign_from_s_b(s, b)

if __name__ == "__main__":
  np.seterr(all="ignore")
  print("reso,cut,s,b")

  days = pars.days

  total_tm = pars.tm_cross_section * pars.lumi_per_day * days
  total_bhabha = pars.bhabha_cross_section * pars.lumi_per_day * days

  cut_array = np.arange(pars.mincut, pars.vertex_x_acc, 500)

  signalth1file = ROOT.TFile("../reco/signal_dr_v3-40_th1.root")
  signalth1, bhabha_f = signalth1file.Get("h"), ROOT.TF1("f", "gaus", 0, 10)
  bhabha_f.SetParameters(5.49763e+04/1.199e6, 2.35540e+00, 4.54693e-01)

  for cut in cut_array:
    sign = get_sign_from_reso_cut(signalth1, bhabha_f, total_tm, total_bhabha, cut)
    exp_signal = signal_yield_all_n(signalth1, total_tm, cut)
    exp_bkg = bhabha_yield(bhabha_f, total_bhabha, cut) + pars.other_bkg*pars.days
    print(",".join([str(v) for v in [sign, cut, round(exp_signal, 10), round(exp_bkg, 10)]]))
