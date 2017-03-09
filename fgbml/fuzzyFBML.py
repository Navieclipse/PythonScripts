# -*- coding: utf-8 -*-
import math
import numpy as np
import pandas as pd

class FuzzyClassifier(object):
    
    """ Fuzzy classifier
    Parameters
    ------------
    divNum : int
        The number of fuzzy membership divide
    rules : {array-like}, shape = [n_features]
        fuzzy rule set
    ------------
    """ 
    # set parameter
    def __init__(self, divNum=5):
        self.divNum = divNum
        self.Sk = []
        self.Lk = []
        for div in range(1, self.divNum+1):
            for i in range(1, div+1):
                self.Lk.append(div)
                self.Sk.append(i)
        
    def setRule(self, fileName, data, Cnum):
        rules = np.loadtxt(fileName, comments='#')
        self.rules = pd.DataFrame(rules)
        cfs, conclutions = self.calcRuleAfter(data, self.rules, Cnum)
        self.rules['cf'] = cfs
        self.rules['conclution'] = conclutions
        
    #Coming Soon
    def makeRules(self, X, y, nIter):
        """Make fuzzy rules
        Parameters
        ----------
        X: {array-like}, shape = [n_samples, n_features]
            Training vectors, where n_samples is the number of samples and
            n_features is the number of features.
        y : array-like, shape = [n_samples]
            Target values.
        nIter: int
            terminal condition
            
        Returns
        -------
        self : object
            rules (pandas)
        """
        for _ in range(nIter):
            print("Coming soon")
        
    def getRules(self):
        return self.rules
        
    #### Fuzzy operation
    def membership(self, num, x):
        rule = int(num)
        uuu = 1.0
        if rule != 0:
            a = float(self.Sk[rule]-1)/float(self.Lk[rule]-1)
            b = 1.0/float(self.Lk[rule]-1)
            uuu = 1.0 - ( math.fabs(x-a) / b )
            if uuu < 0.0:
                uuu = 0.0
        return uuu
    
    def adap(self, datap, rule, dim):
        ans = 1.0
        for i in range(dim):
            ans = ans * self.membership(rule[i], datap[i])
        return ans
        
    def trustCalc(self, ansCla, Cnum, adap):
        allSum = 0.0
        partSum = 0.0
        dataNum = len(ansCla)
        
        for i in range(dataNum):
            if ansCla[i] == Cnum:
                partSum += adap[i]
            allSum += adap[i]
        if allSum == 0.0:
            return 0.0
        else:
            return (partSum / allSum)
    
    def conclutionCalc(self, trust, Cnum):
        maxNum = 0.0
        flag = True
        conCla = 0
        for i in range(Cnum):
            if maxNum < trust[i]:
                conCla = i
                maxNum = trust[i]
                flag = False
            elif maxNum == trust[i]:
                flag = True
        if flag:
            conCla = -1
        
        return conCla
        
    def cfCalc(self, conCla, trust, Cnum):
        if conCla == -1 or trust[conCla] <= 0.5:
            return 0.0
        else:
            add = 0.0
            for i in range(Cnum):
                add += trust[i]
            return (trust[conCla] * 2 - add) 
    
    def calcRuleAfter(self, data, rule, Cnum):
        dataSize = data.shape[0]
        dimention = data.shape[1] - 1
        
        conclutions, cfs = [], []
        for ruleI in range(len(rule)):
            adaptation = []
            for dataI in range(dataSize):
                adaptation.append( self.adap(data.ix[dataI,:], rule.ix[ruleI,:], dimention) )
            
            trust = []
            for classI in range(Cnum):
                trust.append( self.trustCalc( list(data.ix[:,dimention]), classI, adaptation) )
            
            conclutions.append( self.conclutionCalc(trust, Cnum) )
            cfs.append( self.cfCalc(conclutions[ruleI], trust, Cnum ))
            
        return cfs, conclutions
       
    ### predict        
    def predict(self, data):
        dataSize = data.shape[0]
        ruleSize = self.rules.shape[0]
        dim = data.shape[1] - 1
        
        predicts = []
        for dataI in range(dataSize):
            ans = 0
            maax = 0
            kati = 0
            noSign = True
            for ruleI in range(ruleSize):
                seki = self.rules['cf'][ruleI] * self.adap(data.ix[dataI,:], self.rules.ix[ruleI,:], dim)
                if maax < seki:
                    maax = seki
                    kati = ruleI
                    noSign = True
                elif maax == seki and self.rules['conclution'][ruleI] != self.rules['conclution'][kati]:
                    noSign = False
    
            if noSign and maax > 0.0:
                ans = self.rules['conclution'][kati]
            else:
                ans = -1
            predicts.append(ans)
     
        return predicts
            