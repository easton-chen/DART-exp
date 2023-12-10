import random

class Dart:
    def __init__(self, init_a, init_f, init_ecm):
        self.altitude = init_a
        self.formation = init_f
        self.ECM = init_ecm
        self.max_altitude = 10
        self.wait_list = []
        self.target_range = 4
        self.threat_range = 4
        self.fix_delay = False
        self.tactic_latency = 1
        self.incalt_progress = 0
        self.decalt_progress = 0

    def IncAlt(self):
        print("Execute IncAlt")
        #self.altitude += 1
        self.incalt_progress = self.tactic_latency
        if(self.incalt_progress == 0):
            self.altitude += 1
        else:
            self.wait_list.append("IncAlt")

    def DecAlt(self):
        print("Execute DecAlt")
        #self.altitude -= 1
        self.decalt_progress = self.tactic_latency
        if(self.decalt_progress == 0):
            self.altitude -= 1
        else:
            self.wait_list.append("DecAlt")

    def GoLoose(self):
        print("Execute GoLoose")
        self.formation = 0

    def GoTight(self):
        print("Execute GoTight")
        self.formation = 1  

    def OnECM(self):  
        print("Execute OnECM")
        self.ECM = 1
    
    def OffECM(self):  
        print("Execute OffECM")
        self.ECM = 0

    def CompleteAction(self):
        complete_actions = []
        for i in range(len(self.wait_list)):
            if(self.wait_list[i] == "IncAlt"):
                self.incalt_progress -= 1
                if(self.incalt_progress == 0):
                    self.altitude += 1
                    print("Finish IncAlt")
                    complete_actions.append(i)
            if(self.wait_list[i] == "DecAlt"):
                self.decalt_progress -= 1
                if(self.decalt_progress == 0):
                    self.altitude -= 1
                    print("Finish DecAlt")
                    complete_actions.append(i)
        for i in complete_actions:
            self.wait_list.pop(i)


    def Adapt(self, action_list):
        for action in action_list:
            if(action == 0):
                self.IncAlt()
            elif(action == 1):
                self.DecAlt()
            elif(action == 2):
                self.GoLoose()
            elif(action == 3):
                self.GoTight()
            elif(action == 4):
                self.OnECM()
            elif(action == 5):
                self.OffECM()
            else:
                print("action error:" + str(action))

    def getReward(self, target, threat):
        rT = self.threat_range # threat range
        rS = self.target_range # sensor target range
        f_factor = 1.3
        ecm_factor = 1.2
        detect_bonus = 10
        destory_penalty = 10
        destory_prob = max(0,rT - self.altitude) / rT * ((1 - self.formation) + self.formation/f_factor) * ((1 - self.ECM) + self.ECM / ecm_factor)
        detect_prob = max(0,rS - self.altitude) / rS * ((1 - self.formation) + self.formation/f_factor) * ((1 - self.ECM) + self.ECM / ecm_factor)
        #ran = random.random()

        total_reward = 0
        total_reward += target * (1 - detect_prob) * detect_bonus + threat * destory_prob * destory_penalty
        
        return total_reward
    
    def getMeanReward(self, target_prob, threat_prob):
        rT = self.threat_range # threat range
        rS = self.target_range # sensor target range
        f_factor = 1.3
        ecm_factor = 1.2
        detect_bonus = 10
        destory_penalty = 10
        destory_prob = max(0,rT - self.altitude) / rT * ((1 - self.formation) + self.formation/f_factor) * ((1 - self.ECM) + self.ECM / ecm_factor)
        detect_prob = max(0,rS - self.altitude) / rS * ((1 - self.formation) + self.formation/f_factor) * ((1 - self.ECM) + self.ECM / ecm_factor)

        total_reward = 0
        total_reward += target_prob * (1 - detect_prob) * detect_bonus + threat_prob * destory_prob * destory_penalty
        return total_reward

    def getPrincipal(self, action_list, controller):
        cost_plan = 0
        if(controller.strategy.t == 0 or controller.type == "event"):
            cost_plan = 1
        cost_adapt = 0
        for action in action_list:
            if(action == 0):
                cost_adapt += 1
            elif(action == 1):
                cost_adapt += 1
            elif(action == 2):
                cost_adapt += 1
            elif(action == 3):
                cost_adapt += 1
            
        return cost_plan + cost_adapt
    
    def getInterest(self):
        cost_ecm = 0.5
        return self.ECM * cost_ecm

    def showState(self):
        print("Altitude: " + str(self.altitude) + " Formation: " + str(self.formation) + " ECM: " + str(self.ECM))