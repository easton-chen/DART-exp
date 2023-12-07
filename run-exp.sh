#!/bin/bash 

EXP_TYPE="single"   # single, all
ENV_TYPE="random"   # random, fix
PRED_TYPE="fuse"    # fuse, latest
CONTR_TYPE="event"  # event, busymc, lazymc

LOG_FILE="./Results/DART"

if [ "$1" != "" ]; then
    EXP_TYPE=$1
    LOG_FILE=${LOG_FILE}-${EXP_TYPE}
fi
if [ "$2" != "" ]; then
    ENV_TYPE=$2
    LOG_FILE=${LOG_FILE}-${ENV_TYPE}
fi
if [ "$3" != "" ]; then
    PRED_TYPE=$3
    LOG_FILE=${LOG_FILE}-${PRED_TYPE}
fi
if [ "$4" != "" ]; then
    CONTR_TYPE=$4
    LOG_FILE=${LOG_FILE}-${CONTR_TYPE}
fi

if [ $ENV_TYPE == "random" ]; then
    for ENV_CASE in {0..19}
    do
        python3 ./DART/main.py $EXP_TYPE $ENV_TYPE $ENV_CASE $PRED_TYPE $CONTR_TYPE >${LOG_FILE}-${ENV_CASE}.log
    done   
else
    python3 ./DART/main.py $EXP_TYPE $ENV_TYPE $PRED_TYPE $CONTR_TYPE >${LOG_FILE}.log
fi