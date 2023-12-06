# (0,0,3,0,0,false,false,false,false,0,false,0,true,false,false,false,false,1,0):DecAlt_start
class Strategy:
    def __init__(self):
        self.action_lists = {}
        self.start_file = "./str.txt"
        self.t = 1

    def loadStart(self, file="./str.txt"):
        self.t = 0
        self.action_lists = {}
        with open(file) as strfile:
            actions = strfile.readlines()
    
        for action in actions:
            a = action.split(":")
            a[0] = a[0][1:-1]
            a[1] = a[1].strip()
            state_list = a[0].split(",")
            state = ""
            for i in range(5):
                state += state_list[i] + ','
            if(a[1] != "null" and a[1] != "tick" and a[1] != "tick2" and a[1] != "tack" and a[1].find("complete") == -1):
                if(self.action_lists.get(state) != None):
                    self.action_lists[state].add(a[1])
                else:
                    self.action_lists[state] = {a[1]}

    def getTactic(self, state):
        return self.action_lists.get(state)
                
    def showAll(self):
        length = len(self.action_lists)
        print(length)
        for key,value in self.action_lists.items():
            print(key)
            for a in value:
                print(a)

if __name__ == "__main__":
    strategy = Strategy()
    strategy.loadStart()
    strategy.showAll()

    