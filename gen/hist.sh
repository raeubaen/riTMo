#!/bin/bash
njob=$(expr $1 + 0)
source /cvmfs/sft.cern.ch/lcg/app/releases/ROOT/6.24.08/x86_64-centos7-gcc48-opt/bin/thisroot.sh
/cvmfs/sft.cern.ch/lcg/app/releases/ROOT/6.24.08/x86_64-centos7-gcc48-opt/bin/root << eof
.L /afs/cern.ch/work/r/rgargiul/ritmo/gen/hist.C
hist($njob);
eof
