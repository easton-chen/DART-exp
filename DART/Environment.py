import random
class Environment:
    def __init__(self, N, type="random", case=0):
        self.max_length = N
        self.target_gen_prob = [0.8] * N
        self.threat_gen_prob = [0.2] * N
        self.target = []
        self.threat = []
        self.target_case = []
        self.threat_case = []
        
        env_file = "random_env.txt"
        with open(env_file, 'r') as efile:
            env_lines = efile.readlines()
            length = int(len(env_lines) / 2)
            for i in range(length):
                target_line = env_lines[i * 2]
                threat_line = env_lines[i * 2 + 1]
                target_line = target_line.split(" ")
                threat_line = threat_line.split(" ")
                target_line = [float(target) for target in target_line[:-1]]
                threat_line = [float(threat) for threat in threat_line[:-1]]
                self.target_case.append(target_line)
                self.threat_case.append(threat_line)

        if(type == "threat"):
            self.target_gen_prob = [0.25] * N
            self.threat_gen_prob = [0.8] * N
        elif(type == "random"):
            self.target_gen_prob = self.target_case[int(case)]
            self.threat_gen_prob = self.threat_case[int(case)]
        elif(type == "1"):
            self.target_gen_prob = [0.2, 0.2, 0.2, 0.2, 0.2, 0.8, 0.8, 0.8, 0.8, 0.8]
            self.threat_gen_prob = [0.8, 0.8, 0.8, 0.8, 0.8, 0.2, 0.2, 0.2, 0.2, 0.2]
     
    def generateEnv(self):
        for i in range(self.max_length):
            if(random.random() < self.target_gen_prob[i]):
                self.target.append(1)
            else:
                self.target.append(0)
            if(random.random() < self.threat_gen_prob[i]):
                self.threat.append(1)
            else:
                self.threat.append(0)

    def getFutureEnvState(self, t, h): # return t,...,t+h
        target_list = self.target[t:t+h+1]
        threat_list = self.threat[t:t+h+1]
        while(h + 1 - len(target_list) > 0):
            target_list.append(target_list[-1])
            threat_list.append(threat_list[-1])
        return target_list, threat_list

    
    def getEnvState(self, t): 
        return self.target[t],self.threat[t]
    
    def getEnvStateProb(self, t): 
        return self.target_gen_prob[t],self.threat_gen_prob[t]

    def showEnv(self):
        print("target: " + str(self.target))
        print("threaat: " + str(self.threat))

    