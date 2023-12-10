#!/bin/bash 

EXP_TYPE="single"   # single, all, fixstrat, sim-anal
ENV_TYPE="random"   # random, fix, random-long
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

if [ $EXP_TYPE == "all" ]; then
    if [ $ENV_TYPE == "random" ]; then
        for ENV_CASE in {0..19}
        do
            echo "python3 ./DART/main.py $EXP_TYPE $ENV_TYPE $ENV_CASE $PRED_TYPE $CONTR_TYPE >${LOG_FILE}-${ENV_CASE}.log"
            python3 ./DART/main.py $EXP_TYPE $ENV_TYPE $ENV_CASE $PRED_TYPE $CONTR_TYPE >${LOG_FILE}-${ENV_CASE}.log
        done   
    fi
elif [ $EXP_TYPE == "sim-anal" ]; then
    for PRED_PARAM in 1 2 3 4 5 6
    do
        for ERR_RATE in 0.05 0.1 0.15 0.2 0.25 0.3
        do
            ENV_CASE=0
            echo "python3 ./DART/main.py $EXP_TYPE $ENV_TYPE $ENV_CASE $PRED_TYPE $CONTR_TYPE $ERR_RATE $PRED_PARAM >${LOG_FILE}-${PRED_PARAM}-${ERR_RATE}.log"
            python3 ./DART/main.py $EXP_TYPE $ENV_TYPE $ENV_CASE $PRED_TYPE $CONTR_TYPE $ERR_RATE $PRED_PARAM >${LOG_FILE}-${PRED_PARAM}-${ERR_RATE}.log
        done
    done
elif [ $EXP_TYPE == "tb-anal" ]; then
    if [ $ENV_TYPE == "random" ]; then
        for ENV_CASE in {0..19}
        do
            ENV_REWARD=20
            echo "python3 ./DART/main.py $EXP_TYPE $ENV_TYPE $ENV_CASE $PRED_TYPE $CONTR_TYPE >${LOG_FILE}-${ENV_REWARD}-${ENV_CASE}.log"
            python3 ./DART/main.py $EXP_TYPE $ENV_TYPE $ENV_CASE $PRED_TYPE $CONTR_TYPE >${LOG_FILE}-${ENV_REWARD}-${ENV_CASE}.log
        done   
    fi
else
    ENV_CASE=3
    echo "python3 ./DART/main.py $EXP_TYPE $ENV_TYPE $ENV_CASE $PRED_TYPE $CONTR_TYPE >${LOG_FILE}-${ENV_CASE}.log"
    python3 ./DART/main.py $EXP_TYPE $ENV_TYPE $ENV_CASE $PRED_TYPE $CONTR_TYPE >${LOG_FILE}-${ENV_CASE}.log
fi