#!/bin/bash

/afs/cern.ch/work/r/rgargiul/BabaYaga/babayaga << eof
fs ee
ecms 0.211
thmin 60.
thmax 120.
zmax 180.
emin 0.06
nphot $1
nev 250000
path run
ntuple yes
sprb1 0.00021
sprb2 0.00021
run
eof
