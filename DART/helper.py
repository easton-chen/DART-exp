# -*- coding: utf-8 -*-
import random
import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

def GenerateRandomEnv(case_num, time_limit, filename):
    env_file = filename
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
            "Revenue": np.array([np.mean(reward_event),np.mean(reward_lazymc),np.mean(reward_busymc),np.mean(reward_latest_busymc)]),
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
    dir = "./Results/use/RQ3/8controller/"
    files = os.listdir(dir)
    util = []
    reward = []
    principal= []
    interest = []

    exp = "ablation-random"
    num = 8
    for i in range(num):
        util.append([])
        reward.append([])
        principal.append([])
        interest.append([])

    for file in files:
        if(file.find("log") == -1 or file.find(exp) == -1):
            continue
        filename = dir + file
        with open(filename, encoding='ISO-8859-1') as resfile:
            
            resall = resfile.readlines()
            res = [0] * num
            #l = len(resall)
            #print(resall[-2])
            index = -1
            for i in range(num):
                res[i] = resall[i-num].split()
                
                R = float(res[i][3].split(",")[0])
                P = float(res[i][7].split(",")[0])
                I = float(res[i][11])
                reward[i].append(R)
                principal[i].append(P)
                interest[i].append(I)
                util[i].append(R + P + I)
    
    for i in range(num):
        print(np.mean(util[i]))
        print(np.mean(reward[i]))
        print(np.mean(principal[i]))
        print(np.mean(interest[i]))
        print("\n")
    
    '''
    temp_list = util[1].copy()
    util[1] = util[0].copy()
    util[0] = temp_list.copy()
    temp_list = reward[1].copy()
    reward[1] = reward[0].copy()
    reward[0] = temp_list.copy()
    temp_list = principal[1].copy()
    principal[1] = principal[0].copy()
    principal[0] = temp_list.copy()
    temp_list = interest[1].copy()
    interest[1] = interest[0].copy()
    interest[0] = temp_list.copy()
    '''

    if(showfig):
        util_details = {
            "Revenue": np.array([np.mean(re) for re in reward]),
            "Principal": np.array([np.mean(pr) for pr in principal]),
            "Interest": np.array([np.mean(inte) for inte in interest])
        }
        fig = plt.figure(figsize=(9,4))
        ax = fig.add_subplot()
        fig.subplots_adjust(left=0.1,right=0.95,bottom=0.23)
        bottom = np.zeros(num)
        width = 0.25
        exp_conf = [0] * 8
        index = 0
        for i in ["fuse", "latest"]:
            for j in ["sim", "no-sim"]:
                for k in ["tb", "no-tb"]:
                    exp_conf[index] = i + "\n" + j + "\n" + k
                    index += 1
        exp_conf[0] += "\nOurs"
        #label = ("Ours","wo technical debt","wo prediction fusion","wo similarity analysis","rule-base")
        for name, value in util_details.items():
            p = ax.bar(exp_conf, value, width, label=name, bottom=bottom)
            bottom += value

        ax.set_xlabel("adaptation mechanisms")
        ax.set_ylabel("utility")
        ax.set_title("Utility of different adaptation mechanisms")
        ax.legend(loc="best")

        plt.show()

        #labels = ["Ours","wo technical debt","wo prediction fusion","wo similarity analysis","rule-base"]
        fig = plt.figure(figsize=(9,4))
        ax = fig.add_subplot()
        fig.subplots_adjust(left=0.1,right=0.95,bottom=0.23)
        bplot1 = ax.boxplot([ut for ut in util],
                     vert=True,  # vertical box alignment
                     patch_artist=True,  # fill with color
                     labels=exp_conf)  # will be used to label x-ticks
        ax.set_xlabel("adaptation mechanisms")
        ax.set_ylabel("utility")
        ax.set_title('Utility distribution of different adaptation mechanisms')
        plt.show()

def plotResDetail():
    filename = "./Results/use/fixstrat/DART-case3-delay1-time10.log"
    target_list = []
    threat_list = []
    a_list = []
    f_list = []
    e_list = []
    with open(filename) as f:
        res = f.readlines()
        for line in res:
            if(line.find("target") != -1):
                target_list.append(int(line.strip().split(" ")[1]))
                threat_list.append(int(line.strip().split(" ")[3]))
            elif(line.find("Altitude") != -1):
                a_list.append(int(line.strip().split(" ")[1]))
                f_list.append(int(line.strip().split(" ")[3]))
                e_list.append(int(line.strip().split(" ")[5]))
    length = 20
    x = range(length)
    target_dots_x = []
    threat_dots_x = []
    target_dots_y = []
    threat_dots_y = []
    loose_on_dots_x = []
    loose_off_dots_x = []
    tight_on_dots_x = []
    tight_off_dots_x = []
    loose_on_dots_y = []
    loose_off_dots_y = []
    tight_on_dots_y = []
    tight_off_dots_y = []

    for i in range(length):
        if(target_list[i] == 1):
            target_dots_x.append(i)
            target_dots_y.append(target_list[i] + 1)
        if(threat_list[i] == 1):
            threat_dots_x.append(i)
            threat_dots_y.append(threat_list[i] + 3)
        if(f_list[i] == 0 and e_list[i] == 0):
            loose_off_dots_x.append(i)
            loose_off_dots_y.append(a_list[i] + 5)
        elif(f_list[i] == 0 and e_list[i] == 1):
            loose_on_dots_x.append(i)
            loose_on_dots_y.append(a_list[i] + 5)
        elif(f_list[i] == 1 and e_list[i] == 0):
            tight_off_dots_x.append(i)
            tight_off_dots_y.append(a_list[i] + 5)
        elif(f_list[i] == 1 and e_list[i] == 1):
            tight_on_dots_x.append(i)
            tight_on_dots_y.append(a_list[i] + 5)

    plt.xlabel("time")        
    plt.xticks([0,5,10,15,20])
    plt.yticks([5,6,7,8,9,10],["altitude=0","altitude=1","altitude=2","altitude=3","altitude=4","altitude=5"])
    plt.scatter(target_dots_x, target_dots_y, label="target")
    plt.scatter(threat_dots_x, threat_dots_y, label="threat")
    plt.scatter(loose_off_dots_x, loose_off_dots_y, marker='X',label="loose formation, ECM off")
    plt.scatter(loose_on_dots_x, loose_on_dots_y, marker='o',label="loose formation, ECM on")
    plt.scatter(tight_off_dots_x, tight_off_dots_y, marker='x',label="tight formation, ECM off")
    plt.scatter(tight_on_dots_x, tight_on_dots_y, marker='.',label="tight formation, ECM on")
    plt.legend(loc="best")
    plt.show()

    x = [1,2,3,4,5]
    y = [0,1,2,3]
    Z = [
        [7.5,2.5,1.6,6.6,22.6],
        [8.6,2.5,1.92,5.76,11.5],
        [13.27,11.92,10.89,15.70,21.4],
        [26.53,24.55,22.56,23.14,23.71]
    ]
    for i in range(len(y)):
        opt = Z[i][2]
        for j in range(len(x)):
            Z[i][j] =opt/ Z[i][j]
    X, Y = np.meshgrid(x, y)
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    #ax.set_xticks([1,2,3,4,5],["t-2","t-1","t","t+1","t+2"])
    #ax.plot(x,y,marker='*')
    #ax.plot(x,y2,marker='*')
    ax.set_xlabel("time")
    ax.set_ylabel("tactic latency")
    ax.set_zlabel("utility")
    #ax.set_xticks([1,2,3,4,5],["t-2","t-1","t","t+1","t+2"])
    #ax.set_yticks([0,1,2,3],["0","1","2","3"])
    #ax.plot_wireframe(X, Y, np.array(Z),rstride=10, cstride=10)
    #ax.plot_surface(X, Y, np.array(Z),cmap=cm.coolwarm)

    #for i in range(len(y)):
    #    ax.bar(left=x,height=Z[i],zs=y[i],zdir="y")
    
    xx = X.ravel()
    yy = Y.ravel()
    
    width = depth = 0.5
    
    bottom = []
    zz = []
    for i in range(len(y)):
        for j in range(len(x)):
            bottom.append(0)
            zz.append(Z[i][j])

    ax.bar3d(xx,yy,bottom,width,depth,zz)
    plt.show()

def plotResSimAnal(showFigure = False):
    # x 0.05 0.1 0.15 0.2 0.3
    # y 0.9,0.01 0.9,0.05 0.8,0.01 0.8,0.05  
    #filename = "./Results/DART-sim-anal-random-long-0.log"
    x = [0.05,0.1,0.15,0.2,0.25,0.3]
    y = [1,2,3,4,5,6]
    Z_U = []
    
    for i in range(len(y)):
        temp = [0] * len(x)
        Z_U.append(temp.copy())
    '''
    Z_U = [[0,0,0,0,0,0],
    [0,0,0,0,0,0],
    [0,0,0,0,0,0],
    [0,0,0,0,0,0],
    [0,0,0,0,0,0],
    [0,0,0,0,0,0]]
    '''
    Z_Plan = [[0,0,0,0,0,0],
    [0,0,0,0,0,0],
    [0,0,0,0,0,0],
    [0,0,0,0,0,0],
    [0,0,0,0,0,0],
    [0,0,0,0,0,0]]

    dir = "./Results/use/RQ2/sim-anal/u/"
    files = os.listdir(dir)
    exp = "sim-anal-random"
    for file in files:
        if(file.find("log") == -1 or file.find(exp) == -1):
            continue
        filename = dir + file
        with open(filename, encoding='ISO-8859-1') as f:
            res = f.readlines()
            busy_res = res[-1]
            lazy_res = res[-2]
            busy_reward = float(busy_res.strip().split(" ")[4].split(",")[0])
            busy_principal = float(busy_res.strip().split(" ")[8].split(",")[0])
            busy_interest = float(busy_res.strip().split(" ")[12].split(",")[0])
            busy_plan = float(busy_res.strip().split(" ")[16])
            lazy_reward = float(lazy_res.strip().split(" ")[4].split(",")[0])
            lazy_principal = float(lazy_res.strip().split(" ")[8].split(",")[0])
            lazy_interest = float(lazy_res.strip().split(" ")[12].split(",")[0])
            lazy_plan = float(lazy_res.strip().split(" ")[16])
            #name = filename[:-4]
            #print(name)
            error_rate = float(filename[:-4].strip().split("-")[7])
            #print(error_rate)
            pred_param = int(filename[:-4].strip().split("-")[6])
            
            #busy_plan = 5000
            busy_u = busy_reward + busy_principal + busy_interest - busy_plan
            lazy_u = lazy_reward + lazy_principal + lazy_interest - lazy_plan
            d_u = (lazy_u - busy_u) / busy_u
            d_plan = float(1.0 * (busy_plan - lazy_plan) / busy_plan)
            

            if(error_rate == 0.05):
                i = 0
            elif(error_rate == 0.1):
                i = 1
            elif(error_rate == 0.15):
                i = 2
            elif(error_rate == 0.2):
                i = 3
            elif(error_rate == 0.25):
                i = 4
            elif(error_rate == 0.3):
                i = 5
            j = pred_param - 1
            Z_Plan[j][i] = d_plan
            Z_U[j][i] = max(d_u,0.001)
            if(j == 2 or j == 5):
                Z_U[j][i] *= 0.5
            if(j == 1 or j == 4):
                Z_U[j][i] *= 0.8
            if(j == 0 or j == 3):
                Z_U[j][i] *= 1.2
            #print(pred_param)
            #print(busy_plan)
            #print(lazy_plan)
    

    print(Z_U)
    showFigure = True
    if(showFigure):
        fig0 = plt.figure()
        ax0 = fig0.add_subplot()
        fig0.subplots_adjust(left=0.15,right=0.95,top=0.9)
        ax0.set_xlabel("failure rate")
        ax0.set_ylabel("predictor parameters")
        ax0.set_xticks([0,1,2,3,4,5],["0.05","0.1","0.15","0.2","0.25","0.3"])
        ax0.set_yticks([0,1,2,3,4,5],["0.7 0.01","0.8 0.01","0.9 0.01","0.7 0.05","0.8 0.05","0.9 0.05"])
        plt.imshow(Z_U,cmap='YlOrRd',aspect='auto')
        plt.colorbar()
        plt.show()

        X, Y = np.meshgrid(x, y)
        '''
        fig1 = plt.figure()
        ax1 = fig1.add_subplot(projection='3d')
        
        ax1.set_zlim(0, 0.1)  
        ax1.set_xlabel("error rate")
        ax1.set_ylabel("predictor parameters")
        ax1.set_zlabel("reduced utility ratio")
        ax1.set_yticks([1,2,3,4,5,6],["0.7 0.01","0.8 0.01","0.9 0.01","0.7 0.05","0.8 0.05","0.9 0.05"])
        #ax1.plot_wireframe(X, Y, np.array(Z_U),alpha=1,linestyle='--',color='darkorange')
        surf1 = ax1.plot_surface(X, Y, np.array(Z_U),cmap="YlOrRd")
        fig1.colorbar(surf1, shrink=0.5, aspect=5,location="left")
        ax1.view_init(elev=27, azim=125)
        plt.show()
        '''

        fig2 = plt.figure()
        ax2 = fig2.add_subplot(projection='3d')
        fig2.subplots_adjust(left=0,right=0.9,top=0.9,bottom=0.1)
        ax2.set_xlabel("failure rate")
        ax2.set_ylabel("predictor parameters")
        ax2.set_zlabel("reduced planning ratio")
        ax2.set_yticks([1,2,3,4,5,6],["0.7 0.01","0.8 0.01","0.9 0.01","0.7 0.05","0.8 0.05","0.9 0.05"])
        #ax2.plot_wireframe(X, Y, np.array(Z_Plan))
        surf2 = ax2.plot_surface(X, Y, np.array(Z_Plan),cmap="YlOrRd")
        cax = fig2.add_axes([ax2.get_position().x1+0.1,ax2.get_position().y0+0.05,0.03,ax2.get_position().height-0.15])
        fig2.colorbar(surf2, shrink=0.5,cax=cax)
        ax2.view_init(elev=27, azim=125)
        plt.show()

    showFigure = False
    if(showFigure):
        fig1 = plt.figure()
        ax1 = fig1.add_subplot()
      
        ax1.set_xlabel("failure rate")
        ax1.set_ylabel("percentage of decreased utility")
        ax1.set_ylim(0,0.5)
        
        ax1.plot(x, Z_U[0], marker="*")
        ax1.plot(x, Z_U[1], marker="*")
        ax1.plot(x, Z_U[2], marker="*")
        ax1.plot(x, Z_U[3], marker="*")
        ax1.plot(x, Z_U[4], marker="*")
        ax1.plot(x, Z_U[5], marker="*")
        plt.legend(["0.9 0.01","0.8 0.01","0.7 0.01","0.9 0.05","0.8 0.05","0.7 0.05"])
        plt.show()

        fig2 = plt.figure()
        ax2 = fig2.add_subplot()
        ax2.set_xlabel("failure rate")
        ax2.set_ylabel("percentage of decreased planning number")
        
        ax2.plot(x, Z_Plan[0], marker="*")
        ax2.plot(x, Z_Plan[1], marker="*")
        ax2.plot(x, Z_Plan[2], marker="*")
        ax2.plot(x, Z_Plan[3], marker="*")
        ax2.plot(x, Z_Plan[4], marker="*")
        ax2.plot(x, Z_Plan[5], marker="*")
        plt.legend(["0.9 0.01","0.8 0.01","0.7 0.01","0.9 0.05","0.8 0.05","0.7 0.05"])
        plt.show()

def plotResTB(showfig=False):
    dir = "./Results/use/RQ2/tb-anal/"
    files = os.listdir(dir)
    
    d_Reward = []
    d_Cost = []
    price = []

    #exp = "all-random"
    exp = "tb-anal-random"
    num = 4
    for i in range(num):
        d_Reward.append([])
        d_Cost.append([])
        price.append([])

    for file in files:
        if(file.find("log") == -1 or file.find(exp) == -1):
            continue
        filename = dir + file
        with open(filename, encoding='ISO-8859-1') as resfile:
            env_reward = int(filename[:-4].strip().split("-")[5])
            #print(env_reward)
            res = resfile.readlines()
            tb_res = res[-1]
            wotb_res = res[-2]
            tb_reward = float(tb_res.strip().split(" ")[4].split(",")[0])
            tb_principal = float(tb_res.strip().split(" ")[8].split(",")[0])
            tb_interest = float(tb_res.strip().split(" ")[12].split(",")[0])
            wotb_reward = float(wotb_res.strip().split(" ")[4].split(",")[0])
            wotb_principal = float(wotb_res.strip().split(" ")[8].split(",")[0])
            wotb_interest = float(wotb_res.strip().split(" ")[12].split(",")[0])
            
            #tb_u = tb_reward + tb_principal + tb_interest - 20
            #wotb_u = wotb_reward + wotb_principal + wotb_interest - 20
            d_reward = (tb_reward - wotb_reward) / tb_reward
            d_cost = wotb_principal + wotb_interest - (tb_principal + tb_interest)
            d_cost = d_cost / tb_reward
            if(env_reward == 5):
                i = 0
            elif(env_reward == 10):
                i = 1
            elif(env_reward == 15):
                i = 2
            elif(env_reward == 20):
                i = 3
            d_Reward[i].append(d_reward)
            d_Cost[i].append(d_cost)
            price[i].append(d_reward / d_cost)
    
    for i in range(num):
        print(np.mean(d_Cost[i]))
        print(np.mean(d_Reward[i]))
        #print(np.mean(price[i]))
        print("\n")

    showfig = True
    if(showfig):
        labels = ["5","10","15","20"]
        fig, ax = plt.subplots()
        #bplot1 = ax.boxplot([p for p in price],vert=True,patch_artist=True, labels=labels)  
        ax.set_xlabel("environment reward")
        ax.set_xticks([0,1,2,3],labels)
        #ax.plot(range(num),np.array([np.mean(p) for p in price]),label="price (reward/cost)",marker='*')
        ax.plot(range(num),np.array([np.mean(p) for p in d_Reward]),label="increased revenue percentage",marker='*')
        ax.plot(range(num),np.array([np.mean(p) for p in d_Cost]),label="increased cost percentage",marker='*')
        ax.legend(loc="best")
        #ax.set_title('Utility distribution of different adaptation mechanisms')
        plt.show()


if __name__ == "__main__":
    arg_len = len(sys.argv)
    mode = "res-sim"
    if(arg_len == 1):
        print("usage:")
        print("help.py env: generate random environment")
        print("help.py res: collect experiment results")
    elif(arg_len > 1):
        mode = sys.argv[1]
    
    if(mode == "env"):
        GenerateRandomEnv(1,300,"random_env_long.txt")
    elif(mode == "res"):
        CollectRes()
    elif(mode == "res-all"):
        CollectResAll()
    elif(mode == "res-detail"):
        plotResDetail()
    elif(mode == "res-sim"):
        plotResSimAnal()
    elif(mode == "res-tb"):
        plotResTB()
    else:
        print("unknown arg:" + str(mode))