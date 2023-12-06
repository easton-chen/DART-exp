#!/bin/bash 

CONTR_TYPE="event"
ENV_TYPE="random"
PRED_TYPE="fuse"

if [ "$1" != "" ]; then
    CONTR_TYPE=$1
fi
if [ "$2" != "" ]; then
    ENV_TYPE=$2
fi
if [ "$3" != "" ]; then
    PRED_TYPE=$3
fi

if [ $ENV_TYPE == "random" ]; then
    for ENV_CASE in 0 1 2 3 4 5 6 7 8 9 
    do
        python3 ./DART/main.py $CONTR_TYPE $ENV_TYPE $ENV_CASE >./Results/DART-${PRED_TYPE}-${CONTR_TYPE}-${ENV_TYPE}-${ENV_CASE}.log
    done   
else
    python3 ./DART/main.py $CONTR_TYPE $ENV_TYPE >./Results/DART-${PRED_TYPE}-${CONTR_TYPE}-${ENV_TYPE}.log
fi