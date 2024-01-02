#include <TSystem.h>
#include <TH2.h>
#include <TChain.h>
#include <iostream>
using namespace std;

void hist(int njob){

  TChain *c = new TChain("tree", "tree");

  for(int i=njob*20; i<(njob+1)*20; i++){
    for(int np=1; np<4+1; np++){
        TString fname = Form("/eos/user/r/rgargiul/www/babatm/bhabha_reco_%d_%d.root", i, np);
        if(!gSystem->AccessPathName(fname.Data())){
          cout << "adding file: " << fname.Data() << endl;
          c->Add(fname);
        }
    }
  }

  TH2F *h = new TH2F("h", "h", 400, 0, 40, 400, 0, 40);
  TH1F *k = new TH1F("sumw", "sumw", 1, 0.5, 1.5);
  c->Draw("dr/1000:v/1000>>h", Form("w*%f * (theta_ep/3.1415*180 > 177)", 1/3153.), "goff");
  c->Draw("1>>sumw", Form("w*%f", 1/3153.), "goff");
  h->SaveAs(Form("/eos/user/r/rgargiul/www/babatm/h_%i.root", njob));
  k->SaveAs(Form("/eos/user/r/rgargiul/www/babatm/sumw_%i.root", njob));
  delete h;
  delete k;
  delete c;
}
