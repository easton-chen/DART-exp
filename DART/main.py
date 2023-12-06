from Dart import Dart
from Controller import Controller
from Environment import Environment
from Predictor import Predictor
from DS import *
import random
import sys
import numpy as np

####################################
#
#   python main.py controller environment
#
####################################

# main function
time_limit = 10
horizon = 5
init_a = 0
init_f = 0
init_ecm = 0


# argv
arg_len = len(sys.argv)
exp_type = "single"
contr_type = "event"
env_type = "random"
pred_type = "fuse"
env_case = 0
if(arg_len > 1):
    exp_type = sys.argv[1]
if(arg_len > 2):
    contr_type = sys.argv[2]
if(arg_len > 3):
    env_type =  sys.argv[3]
if(arg_len > 4):
    env_case = sys.argv[4]
if(arg_len > 5):
    pred_type = sys.argv[5]

# class init

env = Environment(time_limit, env_type, env_case)
env.generateEnv()
predictor = Predictor(horizon, 0.1)

# single exp
dart = Dart(init_a, init_f, init_ecm)
controller = Controller(contr_type)
reward_list = []
principal_list = []
interest_list = []

# all exp, 4 controller, same env and predictor
# 1 fusion, busy, event
dart1 = Dart(init_a, init_f, init_ecm)
controller1 = Controller("event")
reward_list = []
principal_list = []
interest_list = []

# 2 fusion, busy, mc
dart2 = Dart(init_a, init_f, init_ecm)
controller2 = Controller("busymc")
reward_list = []
principal_list = []
interest_list = []

# 3 latest, lazy, mc
dart3 = Dart(init_a, init_f, init_ecm)
controller3 = Controller("lazymc")
reward_list = []
principal_list = []
interest_list = []

# 4 fusion, lazy, mc
dart4 = Dart(init_a, init_f, init_ecm)
controller4 = Controller("lazymc")
reward_list = []
principal_list = []
interest_list = []

if(exp_type == "single"):
    for t in range(time_limit):
        print("\ntime: " + str(t))
        dart.CompleteAction()
        # get env
        target_list = env.target[t:t+horizon]
        threat_list = env.threat[t:t+horizon]

        target_prob_list, threat_prob_list = predictor.getEnvPred2(target_list, threat_list)
        predictor.storePrediction(target_prob_list, threat_prob_list)
        fused_target_prob_list, fused_threat_prob_list = predictor.DSPredictionFusion()
        #print(target_prob_list)
        #print(fused_target_prob_list)
        
        # get action list
        if(pred_type == "fuse"):
            action_list = controller.Control(dart, fused_target_prob_list, fused_threat_prob_list, t)
        elif(pred_type == "latest"):
            action_list = controller.Control(dart, target_prob_list, threat_prob_list, t)
        # adapt
        dart.Adapt(action_list)
        
        # reward
        dart.showState()
        target,threat = env.getEnvState(t)
        target_prob, threat_prob = env.getEnvStateProb(t)
        #print("target prob: " + str(target_prob) + " threat prob: " + str(threat_prob))
        print("target: " + str(target) + " threat: " + str(threat))
        #reward = dart.getMeanReward(target_prob, threat_prob)
        reward = dart.getReward(target, threat)
        principal = dart.getPrincipal(action_list,controller)
        interest = dart.getInterest()
        print("Reward: " + str(reward) + " Principal: " + str(principal) + " Interest: " + str(interest))
        reward_list.append(reward)
        principal_list.append(principal)
        interest_list.append(interest)

    total_reward = 0
    total_principal = 0
    total_interest = 0
    for r in reward_list:
        total_reward += r
    for p in principal_list:
        total_principal += p
    for i in interest_list:
        total_interest += i

    print("total reward = " + str(total_reward) + ", total principal = " + str(total_principal) + ", total interest = " + str(total_interest))

if(exp_type == "all"):
    for t in range(time_limit):
        print("\ntime: " + str(t))
        dart1.CompleteAction()
        dart2.CompleteAction()
        dart3.CompleteAction()
        dart4.CompleteAction()
        # get env
        target_list = env.target[t:t+horizon]
        threat_list = env.threat[t:t+horizon]

        target_prob_list, threat_prob_list = predictor.getEnvPred2(target_list, threat_list)
        predictor.storePrediction(target_prob_list, threat_prob_list)
        fused_target_prob_list, fused_threat_prob_list = predictor.DSPredictionFusion()
        #print(target_prob_list)
        #print(fused_target_prob_list)
        
        # get action list
        action_list1 = controller1.Control(dart1, fused_target_prob_list, fused_threat_prob_list, t)
        action_list2 = controller2.Control(dart2, fused_target_prob_list, fused_threat_prob_list, t)
        action_list3 = controller3.Control(dart3, target_prob_list, threat_prob_list, t)
        action_list4 = controller4.Control(dart4, fused_target_prob_list, fused_threat_prob_list, t)
        
        # adapt
        dart1.Adapt(action_list1)
        dart2.Adapt(action_list2)
        dart3.Adapt(action_list3)
        dart4.Adapt(action_list4)
        
        # reward
        #dart.showState()
        target,threat = env.getEnvState(t)
        #target_prob, threat_prob = env.getEnvStateProb(t)
        #print("target prob: " + str(target_prob) + " threat prob: " + str(threat_prob))
        print("target: " + str(target) + " threat: " + str(threat))
        #reward = dart.getMeanReward(target_prob, threat_prob)
        reward = dart.getReward(target, threat)
        principal = dart.getPrincipal(action_list,controller)
        interest = dart.getInterest()
        print("Reward: " + str(reward) + " Principal: " + str(principal) + " Interest: " + str(interest))
        reward_list.append(reward)
        principal_list.append(principal)
        interest_list.append(interest)

    total_reward = 0
    total_principal = 0
    total_interest = 0
    for r in reward_list:
        total_reward += r
    for p in principal_list:
        total_principal += p
    for i in interest_list:
        total_interest += i

    print("total reward = " + str(total_reward) + ", total principal = " + str(total_principal) + ", total interest = " + str(total_interest))
