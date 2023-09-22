// This is the file rootlogon.C
{
   TStyle *myStyle  = new TStyle("MyStyle","My Root Styles");

   // from ROOT plain style
   myStyle->SetCanvasBorderMode(0);
   myStyle->SetPadBorderMode(0);
   myStyle->SetPadColor(0);
   myStyle->SetCanvasColor(0);
   myStyle->SetTitleColor(1);
   myStyle->SetStatColor(0);

   myStyle->SetLabelSize(0.03,"xyz"); // size of axis values

   myStyle->SetHistLineWidth(2);
   myStyle->SetHistLineColor(kBlack);

   myStyle->SetLineWidth(1);
   myStyle->SetMarkerStyle(20);
   myStyle->SetMarkerSize(1.1);
   //myStyle->SetLineStyleString(2,"[12 12]"); // postscript dashes
   //myStyle->SetErrorX(0.001);

   //myStyle->SetPadTickX(0);
   //myStyle->SetPadTickY(0);


   myStyle->SetFuncColor(kRed+1);
   myStyle->SetFuncWidth(3);
   //myStyle->SetLineColor(kRed+1);

   myStyle->SetTitleFont(62, "X");
   myStyle->SetTitleFont(62, "Y");
   myStyle->SetTitleFont(62, "Z");


   myStyle->SetLabelSize(0.045, "X");
   myStyle->SetTitleSize(0.045, "X");

   myStyle->SetLabelSize(0.045, "Y");
   myStyle->SetTitleSize(0.045, "Y");
    
   myStyle->SetLabelSize(0.045, "Z");
   myStyle->SetTitleSize(0.045, "Z");

   myStyle->SetTitleOffset(1.2, "X");
  // myStyle->SetTitleOffset(1.1, "Y");
   myStyle->SetTitleOffset(0.70, "Z");

    

   // default canvas positioning
   myStyle->SetCanvasDefX(900);
   myStyle->SetCanvasDefY(20);
   //myStyle->SetCanvasDefH(550);
   //myStyle->SetCanvasDefW(540);

   myStyle->SetPadBottomMargin(0.17);
   myStyle->SetPadTopMargin(0.12);
   myStyle->SetPadLeftMargin(0.17);
   myStyle->SetPadRightMargin(0.12);
   myStyle->SetPadTickX(1);
   myStyle->SetPadTickY(1);
   myStyle->SetFrameBorderMode(0);

   myStyle->SetTitleBorderSize(0);
   myStyle->SetOptTitle(0); //messo a 1

   // Din letter
   myStyle->SetPaperSize(21, 38);

   myStyle->SetStatBorderSize(0);
   //myStyle->SetStatX(0.85);
    myStyle->SetStatX(0.85); 
    //myStyle->SetStatX(0.55); //per plot esponenziali in alto a sinistra
   myStyle->SetLineWidth(1);
   myStyle->SetLineColor(kBlack);
   // myStyle->SetStatY(0.45); // per plot misc  (in basso a destra X=0.85)
   myStyle->SetStatY(0.85);
   myStyle->SetStatFont(42);
   //myStyle->SetStatFormat(".2f");
   myStyle->SetOptStat(1111);    // (1110)Show overflow and underflow as well
   //myStyle->SetOptStat(111110);// Show overflow and underflow as well
   myStyle->SetOptFit(0111); //(1111) con chi e prob
   myStyle->SetPalette(1);

   // apply the new style
   gROOT->SetStyle("MyStyle"); //uncomment to set this style
   gROOT->ForceStyle(); // use this style, not the one saved in root files

   printf("\n Beginning new ROOT session with private TStyle \n");

}
