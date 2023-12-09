#!/bin/bash
source /afs/cern.ch/work/r/rgargiul/gpuenv/bin/activate

for i in $(seq 1 4); do
  mkdir -p /eos/user/r/rgargiul/www/babatm/$1_$i
  cd /eos/user/r/rgargiul/www/babatm/$1_$i
  /afs/cern.ch/work/r/rgargiul/ritmo/gen/run_babayaga.sh $i
  /afs/cern.ch/work/r/rgargiul/gpuenv/bin/python3.9 /afs/cern.ch/work/r/rgargiul/ritmo/gen/process_babayaga.py $1 $i
done
