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
time_limit = 20
horizon = 5
init_a = 0
init_f = 0
init_ecm = 0


# argv
arg_len = len(sys.argv)
exp_type = "single"     # single, all ,fixstart, sim-anal
env_type = "random"     # random, fix, random-long
env_case = 0
pred_type = "fuse"      # fuse, latest
contr_type = "event"    # event, busymc, lazymc
err_rate = 0.15
pred_param = 1
if(arg_len > 1):
    exp_type = sys.argv[1]
if(arg_len > 2):
    env_type = sys.argv[2]
if(arg_len > 3):
    env_case = int(sys.argv[3])
if(arg_len > 4):
    pred_type = sys.argv[4]
if(arg_len > 5):
    contr_type = sys.argv[5]
if(arg_len > 6):
    err_rate = float(sys.argv[6])
if(arg_len > 7):
    pred_param = int(sys.argv[7])


# class init

env = Environment(time_limit, env_type, env_case)
env.generateEnv()
predictor = Predictor(horizon, 0)


if(exp_type == "single"):
    # single exp
    dart = Dart(init_a, init_f, init_ecm)
    controller = Controller(contr_type)
    reward_list = []
    principal_list = []
    interest_list = []
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
    time_limit = len(env.target)
    predictor.err_p = 0.15
    predictor.thres = 0.8
    predictor.sigma = 0.01
    delibError = False
    # all exp, 5 controller, same env and predictor
    # 1 fusion, busy, event
    dart_1 = Dart(init_a, init_f, init_ecm)
    controller_1 = Controller("event")
    reward_list_1 = []
    principal_list_1 = []
    interest_list_1 = []

    # 2 fusion, busy, mc
    dart_2 = Dart(init_a, init_f, init_ecm)
    controller_2 = Controller("busymc")
    reward_list_2 = []
    principal_list_2 = []
    interest_list_2 = []

    # 3 latest, lazy, mc
    dart_3 = Dart(init_a, init_f, init_ecm)
    controller_3 = Controller("lazymc")
    reward_list_3 = []
    principal_list_3 = []
    interest_list_3 = []

    # 4 fusion, lazy, mc
    dart_4 = Dart(init_a, init_f, init_ecm)
    controller_4 = Controller("lazymc")
    reward_list_4 = []
    principal_list_4 = []
    interest_list_4 = []

    # 5 fusion, lazy, wotb
    dart_5 = Dart(init_a, init_f, init_ecm)
    controller_5 = Controller("wotb")
    reward_list_5 = []
    principal_list_5 = []
    interest_list_5 = []
    for t in range(time_limit):
        print("\ntime: " + str(t))
        dart_1.CompleteAction()
        dart_2.CompleteAction()
        dart_3.CompleteAction()
        dart_4.CompleteAction()
        dart_5.CompleteAction()
        # get env
        target_list = env.target[t:t+horizon]
        threat_list = env.threat[t:t+horizon]

        target_prob_list, threat_prob_list = predictor.getEnvPred2(target_list, threat_list)
        if(delibError):
            print("target pred:" + str(target_prob_list))
            print("target pred fusion" + str(fused_target_prob_list))
            print("target pred:" + str(threat_prob_list))
            print("target pred fusion" + str(fused_threat_prob_list))
            if(t == 10 or t == 11 or t == 12):
                for i in range(len(target_prob_list)):
                    if(random.random() > 0.7):
                        target_prob_list[i] = 1 - target_prob_list[i]
                    if(random.random() > 0.7):
                        threat_prob_list[i] = 1 - threat_prob_list[i]
        predictor.storePrediction(target_prob_list, threat_prob_list)
        fused_target_prob_list, fused_threat_prob_list = predictor.DSPredictionFusion()
        

        # get action list
        action_list_1 = controller_1.Control(dart_1, fused_target_prob_list, fused_threat_prob_list, t)
        action_list_2 = controller_2.Control(dart_2, fused_target_prob_list, fused_threat_prob_list, t)
        action_list_3 = controller_3.Control(dart_3, target_prob_list, threat_prob_list, t)
        action_list_4 = controller_4.Control(dart_4, fused_target_prob_list, fused_threat_prob_list, t)
        action_list_5 = controller_5.Control(dart_5, fused_target_prob_list, fused_threat_prob_list, t)

        # adapt
        print("DART1 adapt:")
        dart_1.Adapt(action_list_1)
        print("DART2 adapt:")
        dart_2.Adapt(action_list_2)
        print("DART3 adapt:")
        dart_3.Adapt(action_list_3)
        print("DART4 adapt:")
        dart_4.Adapt(action_list_4)
        print("DART5 adapt:")
        dart_5.Adapt(action_list_5)
        
        # reward
        
        target,threat = env.getEnvState(t)
        #target_prob, threat_prob = env.getEnvStateProb(t)
        #print("target prob: " + str(target_prob) + " threat prob: " + str(threat_prob))
        print("target: " + str(target) + " threat: " + str(threat))

        dart_1.showState()
        #reward = dart.getMeanReward(target_prob, threat_prob)
        reward_1 = dart_1.getReward(target, threat)
        principal_1 = dart_1.getPrincipal(action_list_1,controller_1)
        interest_1 = dart_1.getInterest()
        print("DART1 Reward: " + str(reward_1) + " Principal: " + str(principal_1) + " Interest: " + str(interest_1))
        reward_list_1.append(reward_1)
        principal_list_1.append(principal_1)
        interest_list_1.append(interest_1)

        dart_2.showState()
        reward_2 = dart_2.getReward(target, threat)
        principal_2 = dart_2.getPrincipal(action_list_2,controller_2)
        interest_2 = dart_2.getInterest()
        print("DART2 Reward: " + str(reward_2) + " Principal: " + str(principal_2) + " Interest: " + str(interest_2))
        reward_list_2.append(reward_2)
        principal_list_2.append(principal_2)
        interest_list_2.append(interest_2)

        dart_3.showState()
        reward_3 = dart_3.getReward(target, threat)
        principal_3 = dart_3.getPrincipal(action_list_3,controller_3)
        interest_3 = dart_3.getInterest()
        print("DART3 Reward: " + str(reward_3) + " Principal: " + str(principal_3) + " Interest: " + str(interest_3))
        reward_list_3.append(reward_3)
        principal_list_3.append(principal_3)
        interest_list_3.append(interest_3)

        dart_4.showState()
        reward_4 = dart_4.getReward(target, threat)
        principal_4 = dart_4.getPrincipal(action_list_4,controller_4)
        interest_4 = dart_4.getInterest()
        print("DART4 Reward: " + str(reward_4) + " Principal: " + str(principal_4) + " Interest: " + str(interest_4))
        reward_list_4.append(reward_4)
        principal_list_4.append(principal_4)
        interest_list_4.append(interest_4)

        dart_5.showState()
        reward_5 = dart_5.getReward(target, threat)
        principal_5 = dart_5.getPrincipal(action_list_5,controller_5)
        interest_5 = dart_5.getInterest()
        print("DART5 Reward: " + str(reward_5) + " Principal: " + str(principal_5) + " Interest: " + str(interest_5))
        reward_list_5.append(reward_5)
        principal_list_5.append(principal_5)
        interest_list_5.append(interest_5)

    total_reward_1 = 0
    total_principal_1 = 0
    total_interest_1 = 0
    for r in reward_list_1:
        total_reward_1 += r
    for p in principal_list_1:
        total_principal_1 += p
    for i in interest_list_1:
        total_interest_1 += i

    total_reward_2 = 0
    total_principal_2 = 0
    total_interest_2 = 0
    for r in reward_list_2:
        total_reward_2 += r
    for p in principal_list_2:
        total_principal_2 += p
    for i in interest_list_2:
        total_interest_2 += i

    total_reward_3 = 0
    total_principal_3 = 0
    total_interest_3 = 0
    for r in reward_list_3:
        total_reward_3 += r
    for p in principal_list_3:
        total_principal_3 += p
    for i in interest_list_3:
        total_interest_3 += i

    total_reward_4 = 0
    total_principal_4 = 0
    total_interest_4 = 0
    for r in reward_list_4:
        total_reward_4 += r
    for p in principal_list_4:
        total_principal_4 += p
    for i in interest_list_4:
        total_interest_4 += i

    total_reward_5 = 0
    total_principal_5 = 0
    total_interest_5 = 0
    for r in reward_list_5:
        total_reward_5 += r
    for p in principal_list_5:
        total_principal_5 += p
    for i in interest_list_5:
        total_interest_5 += i

    print("Dart1 total reward = " + str(total_reward_1) + ", total principal = " + str(total_principal_1) + ", total interest = " + str(total_interest_1))
    print("Dart2 total reward = " + str(total_reward_2) + ", total principal = " + str(total_principal_2) + ", total interest = " + str(total_interest_2))
    print("Dart3 total reward = " + str(total_reward_3) + ", total principal = " + str(total_principal_3) + ", total interest = " + str(total_interest_3))
    print("Dart4 total reward = " + str(total_reward_4) + ", total principal = " + str(total_principal_4) + ", total interest = " + str(total_interest_4))
    print("Dart5 total reward = " + str(total_reward_5) + ", total principal = " + str(total_principal_5) + ", total interest = " + str(total_interest_5))


if(exp_type == "fixstrat"):
    time_limit = len(env.target)
    # 1 fusion, busy, mc
    dart_1 = Dart(init_a, init_f, init_ecm)
    controller_1 = Controller("fix")
    controller_1.loadFixStrategy()
    reward_list_1 = []
    principal_list_1 = []
    interest_list_1 = []


    for t in range(time_limit):
        print("\ntime: " + str(t))
        dart_1.CompleteAction()
        
        # get env
        target_list = env.target[t:t+horizon]
        threat_list = env.threat[t:t+horizon]

        target_prob_list, threat_prob_list = predictor.getEnvPred2(target_list, threat_list)
        predictor.storePrediction(target_prob_list, threat_prob_list)
        fused_target_prob_list, fused_threat_prob_list = predictor.DSPredictionFusion()

        # get action list
        action_list_1 = controller_1.Control(dart_1, fused_target_prob_list, fused_threat_prob_list, t)
        
        # adapt
        print("DART1 adapt:")
        dart_1.Adapt(action_list_1)
        
        # reward
        
        target,threat = env.getEnvState(t)
        #target_prob, threat_prob = env.getEnvStateProb(t)
        #print("target prob: " + str(target_prob) + " threat prob: " + str(threat_prob))
        print("target: " + str(target) + " threat: " + str(threat))

        dart_1.showState()
        #reward = dart.getMeanReward(target_prob, threat_prob)
        reward_1 = dart_1.getReward(target, threat)
        principal_1 = dart_1.getPrincipal(action_list_1,controller_1)
        interest_1 = dart_1.getInterest()
        print("DART1 Reward: " + str(reward_1) + " Principal: " + str(principal_1) + " Interest: " + str(interest_1))
        reward_list_1.append(reward_1)
        principal_list_1.append(principal_1)
        interest_list_1.append(interest_1)



    total_reward_1 = 0
    total_principal_1 = 0
    total_interest_1 = 0
    for r in reward_list_1:
        total_reward_1 += r
    for p in principal_list_1:
        total_principal_1 += p
    for i in interest_list_1:
        total_interest_1 += i


    print("Dart1 total reward = " + str(total_reward_1) + ", total principal = " + str(total_principal_1) + ", total interest = " + str(total_interest_1))
    
if(exp_type == "sim-anal"):
    time_limit = len(env.target)
    predictor.err_p = err_rate

    # (1)0.7 0.01   (2)0.8,0.01   (3)0.9,0.01  
    # (4)0.7,0.025  (5)0.8,0.025  (6)0.9,0.025
    # (7)0.7 0.05   (8)0.8,0.05   (9)0.9,0.05
    if(pred_param <= 3):
        predictor.sigma = 0.01
    else:
        predictor.sigma = 0.05
    if(pred_param % 3 == 1):
        predictor.thres = 0.7
    elif(pred_param % 3 == 2):
        predictor.thres = 0.8
    elif(pred_param % 3 == 0):
        predictor.thres = 0.9
    #env.max_length = time_limit
    #env.generateEnv()
    # similar anaylsis
    # 1 fusion, busy, mc
    dart_1 = Dart(init_a, init_f, init_ecm)
    controller_1 = Controller("lazymc")
    reward_list_1 = []
    principal_list_1 = []
    interest_list_1 = []

    # 2 fusion, lazy, mc
    dart_2 = Dart(init_a, init_f, init_ecm)
    controller_2 = Controller("busymc")
    reward_list_2 = []
    principal_list_2 = []
    interest_list_2 = []

    
    for t in range(time_limit):
        print("\ntime: " + str(t))
        dart_1.CompleteAction()
        dart_2.CompleteAction()
        # get env
        target_list = env.target[t:t+horizon]
        threat_list = env.threat[t:t+horizon]

        target_prob_list, threat_prob_list = predictor.getEnvPred2(target_list, threat_list)
        predictor.storePrediction(target_prob_list, threat_prob_list)
        fused_target_prob_list, fused_threat_prob_list = predictor.DSPredictionFusion()
        #print("target pred:" + str(target_prob_list))
        #print("target pred fusion" + str(fused_target_prob_list))
        #print("target pred:" + str(threat_prob_list))
        #print("target pred fusion" + str(fused_threat_prob_list))

        # get action list
        action_list_1 = controller_1.Control(dart_1, fused_target_prob_list, fused_threat_prob_list, t)
        action_list_2 = controller_2.Control(dart_2, fused_target_prob_list, fused_threat_prob_list, t)
        

        # adapt
        print("DART1 adapt:")
        dart_1.Adapt(action_list_1)
        print("DART2 adapt:")
        dart_2.Adapt(action_list_2)
        
        # reward
        
        target,threat = env.getEnvState(t)
        #target_prob, threat_prob = env.getEnvStateProb(t)
        #print("target prob: " + str(target_prob) + " threat prob: " + str(threat_prob))
        print("target: " + str(target) + " threat: " + str(threat))

        dart_1.showState()
        #reward = dart.getMeanReward(target_prob, threat_prob)
        reward_1 = dart_1.getReward(target, threat)
        principal_1 = dart_1.getPrincipal(action_list_1,controller_1)
        interest_1 = dart_1.getInterest()
        print("DART1 Reward: " + str(reward_1) + " Principal: " + str(principal_1) + " Interest: " + str(interest_1))
        reward_list_1.append(reward_1)
        principal_list_1.append(principal_1)
        interest_list_1.append(interest_1)

        dart_2.showState()
        reward_2 = dart_2.getReward(target, threat)
        principal_2 = dart_2.getPrincipal(action_list_2,controller_2)
        interest_2 = dart_2.getInterest()
        print("DART2 Reward: " + str(reward_2) + " Principal: " + str(principal_2) + " Interest: " + str(interest_2))
        reward_list_2.append(reward_2)
        principal_list_2.append(principal_2)
        interest_list_2.append(interest_2)


    total_reward_1 = 0
    total_principal_1 = 0
    total_interest_1 = 0
    for r in reward_list_1:
        total_reward_1 += r
    for p in principal_list_1:
        total_principal_1 += p
    for i in interest_list_1:
        total_interest_1 += i

    total_reward_2 = 0
    total_principal_2 = 0
    total_interest_2 = 0
    for r in reward_list_2:
        total_reward_2 += r
    for p in principal_list_2:
        total_principal_2 += p
    for i in interest_list_2:
        total_interest_2 += i

    print("err rate=" + str(predictor.err_p))
    print("mu=" + str(predictor.thres))
    print("sigma=" + str(predictor.sigma))
    print("Dart1 total reward = " + str(total_reward_1) + ", total principal = " + str(total_principal_1) + ", total interest = " + str(total_interest_1) + ", plan number = " + str(controller_1.plan_num))
    print("Dart2 total reward = " + str(total_reward_2) + ", total principal = " + str(total_principal_2) + ", total interest = " + str(total_interest_2) + ", plan number = " + str(controller_2.plan_num))
    
if(exp_type == "tb-anal"):
    time_limit = len(env.target)
    #predictor.err_p = 0.3
    #predictor.err_p = err_rate
    #env.max_length = time_limit
    #env.generateEnv()
    # similar anaylsis
    # 1 fusion, busy, mc
    dart_1 = Dart(init_a, init_f, init_ecm)
    controller_1 = Controller("wotb")
    reward_list_1 = []
    principal_list_1 = []
    interest_list_1 = []

    # 2 fusion, lazy, mc
    dart_2 = Dart(init_a, init_f, init_ecm)
    controller_2 = Controller("busymc")
    reward_list_2 = []
    principal_list_2 = []
    interest_list_2 = []

    
    for t in range(time_limit):
        print("\ntime: " + str(t))
        dart_1.CompleteAction()
        dart_2.CompleteAction()
        # get env
        target_list = env.target[t:t+horizon]
        threat_list = env.threat[t:t+horizon]

        target_prob_list, threat_prob_list = predictor.getEnvPred2(target_list, threat_list)
        predictor.storePrediction(target_prob_list, threat_prob_list)
        fused_target_prob_list, fused_threat_prob_list = predictor.DSPredictionFusion()
        #print("target pred:" + str(target_prob_list))
        #print("target pred fusion" + str(fused_target_prob_list))
        #print("target pred:" + str(threat_prob_list))
        #print("target pred fusion" + str(fused_threat_prob_list))

        # get action list
        action_list_1 = controller_1.Control(dart_1, fused_target_prob_list, fused_threat_prob_list, t)
        action_list_2 = controller_2.Control(dart_2, fused_target_prob_list, fused_threat_prob_list, t)
        
        # adapt
        print("DART1 adapt:")
        dart_1.Adapt(action_list_1)
        print("DART2 adapt:")
        dart_2.Adapt(action_list_2)
        
        # reward
        
        target,threat = env.getEnvState(t)
        #target_prob, threat_prob = env.getEnvStateProb(t)
        #print("target prob: " + str(target_prob) + " threat prob: " + str(threat_prob))
        print("target: " + str(target) + " threat: " + str(threat))

        dart_1.showState()
        #reward = dart.getMeanReward(target_prob, threat_prob)
        reward_1 = dart_1.getReward(target, threat)
        principal_1 = dart_1.getPrincipal(action_list_1,controller_1)
        interest_1 = dart_1.getInterest()
        print("DART1 Reward: " + str(reward_1) + " Principal: " + str(principal_1) + " Interest: " + str(interest_1))
        reward_list_1.append(reward_1)
        principal_list_1.append(principal_1)
        interest_list_1.append(interest_1)

        dart_2.showState()
        reward_2 = dart_2.getReward(target, threat)
        principal_2 = dart_2.getPrincipal(action_list_2,controller_2)
        interest_2 = dart_2.getInterest()
        print("DART2 Reward: " + str(reward_2) + " Principal: " + str(principal_2) + " Interest: " + str(interest_2))
        reward_list_2.append(reward_2)
        principal_list_2.append(principal_2)
        interest_list_2.append(interest_2)


    total_reward_1 = 0
    total_principal_1 = 0
    total_interest_1 = 0
    for r in reward_list_1:
        total_reward_1 += r
    for p in principal_list_1:
        total_principal_1 += p
    for i in interest_list_1:
        total_interest_1 += i

    total_reward_2 = 0
    total_principal_2 = 0
    total_interest_2 = 0
    for r in reward_list_2:
        total_reward_2 += r
    for p in principal_list_2:
        total_principal_2 += p
    for i in interest_list_2:
        total_interest_2 += i

    print("Dart1 total reward = " + str(total_reward_1) + ", total principal = " + str(total_principal_1) + ", total interest = " + str(total_interest_1))
    print("Dart2 total reward = " + str(total_reward_2) + ", total principal = " + str(total_principal_2) + ", total interest = " + str(total_interest_2))
    