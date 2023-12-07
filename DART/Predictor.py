import numpy as np
import random
from DS import *

class Predictor:
    def __init__(self, horizon, error_prob):
        #self.time_limit = time_limit
        self.h = horizon
        self.err_p = error_prob
        self.target_prediction = []
        self.threat_prediction = []
        for i in range(self.h):
            self.target_prediction.append([])
            self.threat_prediction.append([])

    def storePrediction(self, target_prob_list, threat_prob_list):
        self.target_prediction = self.target_prediction[1:]
        self.target_prediction.append([])
        self.threat_prediction = self.threat_prediction[1:]
        self.threat_prediction.append([])
        for i in range(self.h):
            #print(j)
            #print(prediction[j])
            self.target_prediction[i].append(target_prob_list[i])
            self.threat_prediction[i].append(threat_prob_list[i])
            #print(prediction)


    def getEnvPred(self, target_list, threat_list):
        target_prob_list = []
        threat_prob_list = []
        length = len(target_list)
        thres = 0.8
        sigma = 0.01
        sigma_co = 1.1
        for i in range(length):
            if(target_list[i] == 1):
                if(random.random() > self.err_p):
                    mu = random.uniform(thres,1)
                else:
                    mu = random.uniform(0,1-thres)
                sigma *= sigma_co
                p = np.random.normal(mu, sigma)
                p = min(1, p)
                p = max(0, p)
                target_prob_list.append(p)
            else:
                if(random.random() > self.err_p):
                    mu = random.uniform(0,1-thres)
                else:
                    mu = random.uniform(thres,1)
                sigma *= sigma_co
                p = np.random.normal(mu, sigma)
                p = min(1, p)
                p = max(0, p)
                target_prob_list.append(p)
            if(threat_list[i] == 1):
                if(random.random() > self.err_p):
                    mu = random.uniform(thres,1)
                else:
                    mu = random.uniform(0,1-thres)
                sigma *= sigma_co
                p = np.random.normal(mu, sigma)
                p = min(1, p)
                p = max(0, p)
                threat_prob_list.append(p)
            else:
                if(random.random() > self.err_p):
                    mu = random.uniform(0,1-thres)
                else:
                    mu = random.uniform(thres,1)
                sigma *= sigma_co
                p = np.random.normal(mu, sigma)
                p = min(1, p)
                p = max(0, p)
                threat_prob_list.append(p)

        while(self.h - len(target_prob_list) > 0):
            target_prob_list.append(target_prob_list[-1])   
            threat_prob_list.append(threat_prob_list[-1])
        return target_prob_list, threat_prob_list
    
    def getEnvPred2(self, target_list, threat_list):
        target_prob_list = []
        threat_prob_list = []
        length = len(target_list)
        thres = 0.8
        sigma = 0.01
        sigma_co = 1.2
        for i in range(length):
            thres = thres * 0.97
            if(target_list[i] == 1):
                if(random.random() > self.err_p):
                    mu = thres
                else:
                    mu = 1-thres
                sigma *= sigma_co
                p = np.random.normal(mu, sigma)
                p = min(1, p)
                p = max(0, p)
                target_prob_list.append(p)
            else:
                if(random.random() > self.err_p):
                    mu = 1-thres
                else:
                    mu = thres
                sigma *= sigma_co
                p = np.random.normal(mu, sigma)
                p = min(1, p)
                p = max(0, p)
                target_prob_list.append(p)
            if(threat_list[i] == 1):
                if(random.random() > self.err_p):
                    mu = thres
                else:
                    mu = 1-thres
                sigma *= sigma_co
                p = np.random.normal(mu, sigma)
                p = min(1, p)
                p = max(0, p)
                threat_prob_list.append(p)
            else:
                if(random.random() > self.err_p):
                    mu = 1-thres
                else:
                    mu = thres
                sigma *= sigma_co
                p = np.random.normal(mu, sigma)
                p = min(1, p)
                p = max(0, p)
                threat_prob_list.append(p)

        while(self.h - len(target_prob_list) > 0):
            target_prob_list.append(target_prob_list[-1])   
            threat_prob_list.append(threat_prob_list[-1])
        return target_prob_list, threat_prob_list
    
    def DSPredictionFusion(self):
        fused_target_prob_list = []
        fused_threat_prob_list = []
        for i in range(self.h):
            fused_target_prob_list.append(DSFusionDiscount2(self.target_prediction[i]))
            fused_threat_prob_list.append(DSFusionDiscount2(self.threat_prediction[i]))

        return fused_target_prob_list, fused_threat_prob_list
'''
def KFFusion(x):
    length = len(x)
    var = []
    for i in range(length):
        var.append(0.0025 * pow(1.1, i))
    var.reverse()
    alpha = []
    sum_var = 0
    for i in range(length):
        sum_var += 1 / (var[i] * var[i])
    for i in range(length):
        alpha.append((1 / (var[i] * var[i])) / sum_var)
    x_est = 0
    for i in range(length):
        x_est += alpha[i] * x[i]
    return x_est
'''

def EucSimilarIndex(p1, p2):
    p1_common = p1[1:]
    p2_common = p2[:-1]
    
    err = 0
    for i in range(len(p1_common)):
        err += (p1_common[i] - p2_common[i]) * (p1_common[i] - p2_common[i])

    return 1 / (1 + np.sqrt(err))

def EucSimilarIndex2(p1, p2):
    p1_common = p1[1:]
    p1_common.append(p1_common[-1])
    p2_common = p2
    
    err = 0
    for i in range(len(p1_common)):
        err += (p1_common[i] - p2_common[i]) * (p1_common[i] - p2_common[i])

    return 1 / (1 + np.sqrt(err))

def CosSimilarIndex(p1, p2):
    p1_common = p1[1:]
    p2_common = p2[:-1]
    
    tmp0 = 0
    tmp1 = 0
    tmp2 = 0
    for i in range(len(p1_common)):
        tmp0 += p1_common[i] * p2_common[i]
        tmp1 += p1_common[i] * p1_common[i]
        tmp2 += p2_common[i] * p2_common[i]

    return tmp0 / (np.sqrt(tmp1) * np.sqrt(tmp2))

def CosSimilarIndex1(p1, p2):
    p1_common = p1[1:]
    p1_common.append(p1_common[-1])
    p2_common = p2[:]
    l = len(p1_common)
    for i in range(l):
        p1_common.append(1 - p1_common[i])
        p2_common.append(1 - p2_common[i])
    
    tmp0 = 0
    tmp1 = 0
    tmp2 = 0

    #print(p1_common)
    #print(p2_common)
    
    for i in range(len(p1_common)):
        tmp0 += p1_common[i] * p2_common[i]
        tmp1 += p1_common[i] * p1_common[i]
        tmp2 += p2_common[i] * p2_common[i]

    return tmp0 / (np.sqrt(tmp1) * np.sqrt(tmp2))

def CosSimilarIndex2(p1, p2):
    p1_common = p1[2:]
    p1_common.append(p1_common[-1])
    p1_common.append(p1_common[-1])
    p2_common = p2[:]
    l = len(p1_common)
    for i in range(l):
        p1_common.append(1 - p1_common[i])
        p2_common.append(1 - p2_common[i])
    
    tmp0 = 0
    tmp1 = 0
    tmp2 = 0
    #print(p1_common)
    #print(p2_common)
    
    for i in range(len(p1_common)):
        tmp0 += p1_common[i] * p2_common[i]
        tmp1 += p1_common[i] * p1_common[i]
        tmp2 += p2_common[i] * p2_common[i]

    return tmp0 / (np.sqrt(tmp1) * np.sqrt(tmp2))

if __name__ == "__main__":
    # prediction[i]: prediction for time i
    # prediction[i][j]: prediction for time i at time j
    
    horizon = 5
    time_limit = 100
    predictor = Predictor(horizon, 0.15)

    avg_true_num = 0
    ds_true_num = 0
    total_num = 0
    ds_acc_score = [[] for i in range(horizon)]
    ds2_acc_score = [[] for i in range(horizon)]
    avg_acc_score = [[] for i in range(horizon)]
    last_acc_score = [[] for i in range(horizon)]
    
    avg_prediction_for_t = [] 
    ds_prediction_for_t = [] 
    ds2_prediction_for_t = [] 
    

    latest_prediction_at_t = []
    ds_prediction_at_t = [] 
    ds2_prediction_at_t = [] 
    for i in range(time_limit + horizon):
        avg_prediction_for_t.append([])
        ds_prediction_for_t.append([])
        ds2_prediction_for_t.append([])

    target_list = []
    threat_list = []
    for i in range(time_limit + horizon):
        if(random.random() > 0.5):
            target_list.append(1)
        else:
            target_list.append(0)
        if(random.random() > 0.5):
            threat_list.append(1)
        else:
            threat_list.append(0)

    for i in range(time_limit):
        #print("time: " + str(i))    
        
        target_prediction_at_t, threat_prediction_at_t = predictor.getEnvPred2(target_list[i:i+horizon], threat_list[i:i+horizon])
        predictor.storePrediction(target_prediction_at_t, threat_prediction_at_t)
        fused_target_prediction_at_t,fused_threat_prediction_at_t = predictor.DSPredictionFusion()
        ds2_prediction_at_t.append(fused_target_prediction_at_t)
        latest_prediction_at_t.append(target_prediction_at_t)

        #print(true_list[i:i+horizon])
        #print(prediction)
        for j in range(horizon):
            last_p_1 = predictor.target_prediction[j][-1]
            avg_p_1 = np.mean(predictor.target_prediction[j])
            #kf_p_1 = KFFusion(prediction[i])
            #ds_p_1 = DSFusionDiscount(predictor.target_prediction[j])
            ds2_p_1 = DSFusionDiscount2(predictor.target_prediction[j])
            
            #avg_prediction_for_t[i+j].append(avg_p_1)
            #ds_prediction_for_t[i+j].append(ds_p_1)
            ds2_prediction_for_t[i+j].append(ds2_p_1)
            #print("predict time " + str(i+j) + ": " + str(avg_p_1))
            #print("predict time " + str(i+j) + ": " + str(ds_p_1))
            #print("predict time " + str(i+j) + ": " + str(ds2_p_1))
            #if(target_list[i+j] == round(avg_p_1)):
            #    avg_true_num += 1
            #if(target_list[i+j] == round(ds_p_1)):
            #    ds_true_num += 1
            #total_num += 1
            
            #print("time: " + str(i+j))
            #print(target_list[i+j])
            #print(ds2_p_1)
            #print(last_p_1)
            #print(avg_p_1)
            #print(target_prediction_at_t)
            #print(predictor.target_prediction[i+j])
            avg_acc_score[j].append(1 - abs(target_list[i+j] - avg_p_1))
            #ds_acc_score[j].append(1 - abs(target_list[i+j] - ds_p_1))
            ds2_acc_score[j].append(1 - abs(target_list[i+j] - ds2_p_1))
            last_acc_score[j].append(1 - abs(target_list[i+j] - last_p_1))
            '''
            if(1 - abs(target_list[i+j] - ds2_p_1) < 0.5):
                print("outliar:")
                print(target_list[i+j])
                print(ds2_p_1)
                print(last_p_1)
                print(predictor.target_prediction[j])
            '''
            
    #print("avg: true num:" + str(avg_true_num) + ", accurancy: " + str(avg_true_num / total_num))
    #print("ds: true num:" + str(ds_true_num) + ", accurancy: " + str(ds_true_num / total_num))
    #for i in range(time_limit+ horizon):
    #    print("for time " + str(i))
    #    print(avg_prediction_for_t[i])
    #    print(ds_prediction_for_t[i])
    #    print(ds2_prediction_for_t[i])
    
    
    for i in range(horizon):
        print("\n")
        print("time ahead" + str(i+1) + " avg accurancy score mean: " + str(np.mean(avg_acc_score[i])))
        #print("time ahead" + str(i+1) + " ds accurancy score: " + str(np.mean(ds_acc_score[i])))
        print("time ahead" + str(i+1) + " ds2 accurancy score mean: " + str(np.mean(ds2_acc_score[i])))
        print("time ahead" + str(i+1) + " last accurancy score mean: " + str(np.mean(last_acc_score[i])))
        print("time ahead" + str(i+1) + " avg accurancy score median: " + str(np.median(avg_acc_score[i])))
        print("time ahead" + str(i+1) + " ds2 accurancy score median: " + str(np.median(ds2_acc_score[i])))
        print("time ahead" + str(i+1) + " last accurancy score median: " + str(np.median(last_acc_score[i])))
        print("time ahead" + str(i+1) + " avg accurancy score std: " + str(np.std(avg_acc_score[i])))
        print("time ahead" + str(i+1) + " ds2 accurancy score std: " + str(np.std(ds2_acc_score[i])))
        print("time ahead" + str(i+1) + " last accurancy score std: " + str(np.std(last_acc_score[i])))
        print("time ahead" + str(i+1) + " avg accurancy score min: " + str(np.min(avg_acc_score[i])))
        print("time ahead" + str(i+1) + " ds2 accurancy score min: " + str(np.min(ds2_acc_score[i])))
        print("time ahead" + str(i+1) + " last accurancy score min: " + str(np.min(last_acc_score[i])))
    
    #print(similarIndex([0.1,0.5,0.6,0.7],[0.55,0.58,0.72,0.33]))
    '''
    l = len(ds2_prediction_at_t)
    num1 = 0
    num2 = 0
    num1_latest = 0
    num2_latest = 0
    for i in range(l):
        if(i < l - 2):
            #print("Eucindx: " + str(EucSimilarIndex(ds2_prediction_at_t[i],ds2_prediction_at_t[i+1])))
            #print("Eucindx2: " + str(EucSimilarIndex2(ds2_prediction_at_t[i],ds2_prediction_at_t[i+1])))
            #print("cosindx: " + str(CosSimilarIndex(ds2_prediction_at_t[i],ds2_prediction_at_t[i+1])))
            print("ds csi1:")
            CSI1 = CosSimilarIndex1(ds2_prediction_at_t[i],ds2_prediction_at_t[i+1])
            print("latest csi1:")
            CSI_latest_1 = CosSimilarIndex1(latest_prediction_at_t[i], latest_prediction_at_t[i+1])
            print("ds csi2:")
            CSI2 = CosSimilarIndex2(ds2_prediction_at_t[i],ds2_prediction_at_t[i+2])
            print("latest csi2:")
            CSI_latest_2 = CosSimilarIndex2(latest_prediction_at_t[i], latest_prediction_at_t[i+2])
            #print("cosindx2: " + str(CSI2))
            if(CSI1 < 0.9):
                num1 += 1
            if(CSI2 < 0.9):
                num2 += 1
            if(CSI_latest_1 < 0.9):
                num1_latest += 1
            if(CSI_latest_2 < 0.9):
                num2_latest += 1
    print(num1)
    print(num2)
    print(num1_latest)
    print(num2_latest)
    '''