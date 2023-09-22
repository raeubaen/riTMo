double beta(double cme){ return sqrt(1 - 4*105.7*105.7/(cme*cme));}
double cs(double cme){ return 197*197*1e24*1e-26*2*3.14/(137*137) * (beta(cme) * (3 - beta(cme)*beta(cme))) / (3*cme*cme) * 1e12;} //pb

void muons(){

  auto *hbeta = new TH1F("hbeta", "hbeta", 10000, 0, 1);
  auto *hcs = new TH1F("hcs", "hcs", 10000, 0, 1000000);
  auto *length12 = new TH2D("length12", "length12", 10, 0, 100, 10, 0, 100);

  for(int i=0; i<10000000; i++){ double cme = gRandom->Gaus(211.4, 0.3); hbeta->Fill(beta(cme)); hcs->Fill(cs(beta(cme)));}

  for(int i=0; i<1000000000; i++){ double b = hbeta->GetRandom(); length12->Fill(gRandom->Exp(b/sqrt(1-b*b) * 2110 * 300), gRandom->Exp(b/sqrt(1-b*b) * 2110 * 300), 1);}
  hbeta->SaveAs("muonsbeta.root");
  hcs->SaveAs("muonscs.root");
  length12->SaveAs("length12.root");
}

double michel_cutsuppression(){
  TF1 f("michel", "(3*x*x - 2*x*x*x)*[0]", 0, 1);
  f.SetParameter(0, 1000.);

  double p=0;
  for(int i=0; i<10000; i++){
    double eth = 53*f.GetRandom();
    p += 1e-4 * ( 1 - ROOT::Math::gaussian_cdf((90 - eth)/(eth*0.02/sqrt(eth/1000.)) ));
  }
  return p;
}
