#!/bin/bash

if [ -d /eos/user/r/rgargiul/www/babatm/$1 ]; then
  echo folder exist
  source /afs/cern.ch/work/r/rgargiul/gpuenv/bin/activate
  echo 0
  /afs/cern.ch/work/r/rgargiul/gpuenv/bin/python3.9 /afs/cern.ch/work/r/rgargiul/ritmo/gen/process_babayaga.py $1
fi

if [ ! -d /eos/user/r/rgargiul/www/babatm/$1 ]; then
  echo folder not exist
  if [ ! -f /eos/user/r/rgargiul/www/babatm/bhabha_gen_$1_0.root ]; then
    echo file not exist
    /afs/cern.ch/work/r/rgargiul/ritmo/gen/job.sh $1
  fi
fi

