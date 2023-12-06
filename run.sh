#!/bin/bash 

#arg=$1

PRISM=~/Downloads/prism-4.8-src/prism/bin/prism 
PRISM_GUI=~/Downloads/prism-4.8-src/prism/bin/xprism 

DARTSIM=DARTSim.prism
PROP=prop1.props

STRATFILE=str.txt
STRATTYPE=actions #actions, induced, dot

ENVCONST=targetStateProb1=0.8,targetStateProb2=0.8,targetStateProb3=0.8,targetStateProb4=0.8,targetStateProb5=0.8,threatStateProb1=0.2,threatStateProb2=0.2,threatStateProb3=0.2,threatStateProb4=0.2,threatStateProb5=0.2
INITCONST=init_a=3,init_f=0,init_ecm=0

if [ "$1" != "" ] && [ $1 = "gui" ]; then
    $PRISM_GUI
else
    $PRISM -politer $DARTSIM $PROP -const $ENVCONST -const $INITCONST -exportstrat $STRATFILE:type=$STRATTYPE
fi

#$PRISM_GUI
#$PRISM $DARTSIM $PROP -exportstrat str.txt:type=$STRATTYPE