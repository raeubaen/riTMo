#!/bin/bash
echo 0
source /afs/cern.ch/work/r/rgargiul/gpuenv/bin/activate
echo 1
/afs/cern.ch/work/r/rgargiul/gpuenv/bin/python3.9 /afs/cern.ch/work/r/rgargiul/ritmo/reco/silicon_reco.py /afs/cern.ch/work/r/rgargiul/ritmo/gen/bhabha_gen.root 10000 /eos/user/r/rgargiul/prova.root

