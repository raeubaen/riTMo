#!/bin/bash
mkdir -p /eos/user/r/rgargiul/www/babatm/$1
cd /eos/user/r/rgargiul/www/babatm/$1
/afs/cern.ch/work/r/rgargiul/BabaYaga/babayaga << eof
ecms 0.211
thmin 60.
thmax 120.
zmax 180.
emin 0.09
nphot 0
nev 10000000
path run
ntuple yes
eps 0.01
sprb1 0.00021
sprb2 0.00021
run
eof

source /afs/cern.ch/work/r/rgargiul/gpuenv/bin/activate

echo 0

/afs/cern.ch/work/r/rgargiul/gpuenv/bin/python3 /afs/cern.ch/work/r/rgargiul/ritmo/gen/process_babayaga.py $1
