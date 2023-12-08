# -*- coding: utf-8 -*-
import random
import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def GenerateRandomEnv(case_num, time_limit):
    env_file = "random_env.txt"
    with open(env_file, '+w') as efile:
        target_prob_list = []
        threat_prob_list = []
        for i in range(case_num):
            for j in range(time_limit):
                target_prob_list.append(random.random())
                threat_prob_list.append(random.random())
            target_list = ""
            threat_list = ""
            for j in range(time_limit):
                if(random.random() > target_prob_list[j]):
                    target = 1
                else:
                    target = 0
                if(random.random() > threat_prob_list[j]):
                    threat = 1
                else:
                    threat = 0
                target_list += str(target) + " "
                threat_list += str(threat) + " "
            target_list += "\n"
            threat_list += "\n"
            efile.writelines(target_list)
            efile.writelines(threat_list)

def CollectRes(showfig=True):
    files = os.listdir("./Results")
    #print(files)
    util_event = []
    reward_event = []
    principal_event = []
    interest_event = []
    util_lazymc = []
    reward_lazymc = []
    principal_lazymc = []
    interest_lazymc = []
    util_busymc = []
    reward_busymc = []
    principal_busymc = []
    interest_busymc = []
    util_latest_busymc = []
    reward_latest_busymc = []
    principal_latest_busymc = []
    interest_latest_busymc = []
    for file in files:
        if(file.find("log") == -1):
            continue
        filename = "./Results/" + file
        with open(filename, encoding='ISO-8859-1') as resfile:
            res = resfile.readlines()
            res = res[-1].split()
            #print(filename)
            #print("res:")
            #print(res)
            reward = float(res[3].split(",")[0])
            principal = float(res[7].split(",")[0])
            interest = float(res[11])
            
            if(file.split("-")[2] == "event"):
                util_event.append(reward + principal + interest) 
                reward_event.append(reward)
                principal_event.append(principal)
                interest_event.append(interest)
            elif(file.split("-")[2] == "lazymc"):
                util_lazymc.append(reward + principal + interest) 
                reward_lazymc.append(reward)
                principal_lazymc.append(principal)
                interest_lazymc.append(interest)
            elif(file.split("-")[1] == "fuse" and file.split("-")[2] == "busymc"):
                util_busymc.append(reward + principal + interest) 
                reward_busymc.append(reward)
                principal_busymc.append(principal)
                interest_busymc.append(interest)
            elif(file.split("-")[1] == "latest"):
                util_latest_busymc.append(reward + principal + interest) 
                reward_latest_busymc.append(reward)
                principal_latest_busymc.append(principal)
                interest_latest_busymc.append(interest)
    
    print(np.mean(util_event))
    print(np.mean(util_lazymc))
    print(np.mean(util_busymc))
    print(np.mean(util_latest_busymc))
    
    if(showfig):
        util_details = {
            "Reward": np.array([np.mean(reward_event),np.mean(reward_lazymc),np.mean(reward_busymc),np.mean(reward_latest_busymc)]),
            "Principal": np.array([np.mean(principal_event),np.mean(principal_lazymc),np.mean(principal_busymc),np.mean(principal_latest_busymc)]),
            "Interest": np.array([np.mean(interest_event),np.mean(interest_lazymc),np.mean(interest_busymc),np.mean(interest_latest_busymc)])
        }
        fig, ax = plt.subplots()
        bottom = np.zeros(4)
        width = 0.2
        for name, value in util_details.items():
            p = ax.bar(("event","lazy model check","busy model check","latest pred"), value, width, label=name, bottom=bottom)
            bottom += value

        ax.set_title("Utility of different planning method")
        ax.legend(loc="upper right")

        plt.show()

        labels = ["Event","Lazy Model Check","Busy Model Check","Latest Pred"]
        fig, ax = plt.subplots()
        bplot1 = ax.boxplot([util_event,util_lazymc,util_busymc,util_latest_busymc],
                     vert=True,  # vertical box alignment
                     patch_artist=True,  # fill with color
                     labels=labels)  # will be used to label x-ticks
        ax.set_title('Rectangular box plot')
        plt.show()
    
def CollectResAll(showfig=True):
    files = os.listdir("./Results")
    util = []
    reward = []
    principal= []
    interest = []
    for i in range(4):
        util.append([])
        reward.append([])
        principal.append([])
        interest.append([])

    for file in files:
        if(file.find("log") == -1 or file.find("all-random") == -1):
            continue
        filename = "./Results/" + file
        with open(filename, encoding='ISO-8859-1') as resfile:
            
            resall = resfile.readlines()
            res = [0] * 4
            #l = len(resall)
            #print(resall[-2])
            index = -1
            for i in range(4):
                res[i] = resall[-(i+1)].split()
                
                R = float(res[i][4].split(",")[0])
                P = float(res[i][8].split(",")[0])
                I = float(res[i][12])
                reward[i].append(R)
                principal[i].append(P)
                interest[i].append(I)
                util[i].append(R + P + I)
    
    for i in range(4):
        print(np.mean(util[i]))
        print(np.mean(reward[i]))
        print(np.mean(principal[i]))
        print(np.mean(interest[i]))

    if(showfig):
        util_details = {
            "Reward": np.array([np.mean(re) for re in reward]),
            "Principal": np.array([np.mean(pr) for pr in principal]),
            "Interest": np.array([np.mean(inte) for inte in interest])
        }
        fig, ax = plt.subplots()
        bottom = np.zeros(4)
        width = 0.25
        for name, value in util_details.items():
            p = ax.bar(("Ours","wo prediction fusion","wo similarity analysis","rule-base"), value, width, label=name, bottom=bottom)
            bottom += value

        ax.set_title("Utility of different adaptation mechanisms")
        ax.legend(loc="best")

        plt.show()

        labels = ["Ours","wo prediction fusion","wo similarity analysis","rule-base"]
        fig, ax = plt.subplots()
        bplot1 = ax.boxplot([ut for ut in util],
                     vert=True,  # vertical box alignment
                     patch_artist=True,  # fill with color
                     labels=labels)  # will be used to label x-ticks
        ax.set_title('Utility distribution of different adaptation mechanisms')
        plt.show()
            

if __name__ == "__main__":
    arg_len = len(sys.argv)
    mode = "res"
    if(arg_len == 1):
        print("usage:")
        print("help.py env: generate random environment")
        print("help.py res: collect experiment results")
    elif(arg_len > 1):
        mode = sys.argv[1]
    
    if(mode == "env"):
        GenerateRandomEnv(20,20)
    elif(mode == "res"):
        CollectRes()
    elif(mode == "resall"):
        CollectResAll()
    else:
        print("unknown arg:" + str(mode))