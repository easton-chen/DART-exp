import random
import os
from Strategy import Strategy
class Controller:
    def __init__(self, type):
        # IncAlt, DecAlt, GoLoose, GoTight, OnECM, OffECM
        self.strat_file = "str"
        self.strategy = Strategy()
        #self.strategy.loadStart()
        self.type = type

    def Control(self, dart, target_prob_list, threat_prob_list, t):
        if(self.type == "event"):
            return self.simpleEventControl(dart, target_prob_list, threat_prob_list, t)
        
        if(self.type == "lazymc"):
            return self.modelcheckControl(dart, target_prob_list, threat_prob_list, t, "lazy")
        
        if(self.type == "busymc"):
            return self.modelcheckControl(dart, target_prob_list, threat_prob_list, t, "busy")

    # 1) if future possible threat, then incalt
    # 2) if immediate threat, then go tight, if already tight, then ecm on
    # 3) else if future possible target, then decalt
    
    def simpleEventControl(self, dart, target_prob_list, threat_prob_list, t): 
        action_list = []
        h = len(target_prob_list)

        has_target = 0
        has_threat = 0
        for i in range(h):
            if(target_prob_list[i] > 0.7):
                has_target = 1
            if(threat_prob_list[i] > 0.7):
                has_threat = 1

        if(has_threat == 1 and dart.altitude <= dart.threat_range):
            action_list.append(0) # inc alt
        elif(has_target == 1 and dart.altitude > 0):
            action_list.append(1) # dec alt

        if(threat_prob_list[0] > 0.75):
            if(dart.formation == 0):
                action_list.append(3) # go tight
            if(dart.ECM == 0):
                action_list.append(4) # on ecm
        else:
            if(dart.formation == 1):
                action_list.append(2) # go loose
            if(dart.ECM == 1):
                action_list.append(5) # off ecm
        

        return action_list

    def modelcheckControl(self, dart, target_prob_list, threat_prob_list, t, mode="busy"):
        action_list = []
        flag = False
        if(mode == "lazy"):
            self.strategy.t += 1
            if(self.strategy.t == 2):
                flag = True
                self.strategy.t = 0
        if(mode == "busy" or flag):
            # call prism 
            PRISM="~/Downloads/prism-4.8-src/prism/bin/prism"
            DARTSIM="DARTSim.prism"
            PROP="prop1.props"
            ENVCONST = "-const "
            for i in range(0,5):
                ENVCONST += "targetStateProb" + str(i+1) + "=" + str(target_prob_list[i]) + "," 
                ENVCONST += "threatStateProb" + str(i+1) + "=" + str(threat_prob_list[i])
                if(i != 4):
                    ENVCONST += ","
            INITCONST = "-const "
            INITCONST += "init_a=" + str(dart.altitude) + ","
            INITCONST += "init_f=" + str(dart.formation) + ","
            INITCONST += "init_ecm=" + str(dart.ECM)
            STRATFILE=self.strat_file + ".txt"
            STRATTYPE="actions" #actions, induced, dot

            cmd = PRISM + " -politer " + DARTSIM + " " + PROP + " " + ENVCONST + " " + INITCONST + " -exportstrat " + STRATFILE + ":type=" + STRATTYPE + " >prism.log"
            #print(cmd)
            os.system(cmd)

            # get startegy from file
            self.strategy.loadStart(STRATFILE)
        
        # get action from startegy
        state = str(self.strategy.t) + ",0," + str(dart.altitude) + "," + str(dart.formation) + "," + str(dart.ECM) + ","
        tactic_list = self.strategy.getTactic(state)
        if(tactic_list != None):
            for tactic in tactic_list:
                if(tactic == "IncAlt_start"):
                    action_list.append(0)
                elif(tactic == "DecAlt_start"):
                    action_list.append(1)
                elif(tactic == "GoLoose_start"):
                    action_list.append(2)
                elif(tactic == "GoTight_start"):
                    action_list.append(3)
                elif(tactic == "TurnOnECM_start"):
                    action_list.append(4)
                elif(tactic == "TurnOffECM_start"):
                    action_list.append(5)
        
        return action_list