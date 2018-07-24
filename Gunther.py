import random
import numpy as np
import rech as utils
import subprocess
import json
import properties as p
class GuntherGA:

    def __init__(self):
        self.speedup = [] #lire fichier speedup [val,val,...]
        self.latencies = [] #lire fchier latence [val,val,...]
        self.config = [] #lire fichier config [[c,c,c,..],[c,c,c,..],..]
        self.fitness_result = [] #evaluate fitness
        self.cpt = 1
        self.l = []
        self.cross_rate = 0.7
        self.mutate_rate = 0.1

    def merge_conf_spd(self):
        i = 0
        for c in self.config:
            c['spd'] = self.speedup[i]
            i = i+1

    def read_sl(self,filename):
        c = []
        with open(filename, 'r') as fp:
            c = json.load(fp)
        fp.close()
        # with open(filename) as fp:
        #     line = fp.readline()
        #     while line:
        #         line = line.strip()
        #         c.append(line)
        #         line = fp.readline()
        if filename == '/home/yassine/gunther/speedupG.txt':
            self.speedup = c
        else:
            self.latencies = c

    def read_gunther(self,filename):
        with open(filename, 'r') as fp:
            self.config = json.load(fp)
        fp.close()

    def fitnessP(self,spd):
        return 1/spd

    def fitnessC(self,c):
        utils.update_param(c)
        metrics = utils.exec_ycsb(self.cpt)
        self.cpt = self.cpt + 1
        return metrics

    def select(self,p):
        self.l = self.fitness_result
        self.l.sort(reverse=True)
        avg = np.average(self.fitness_result)
        if self.l[0] > avg:
            parent1 = self.l[1]
        if self.l[1] > avg:
            parent2 = self.l[2]

        for c in p:
            if parent1 == (c['spd']**-1):
                parent1=c
            if parent2 == (c['spd']**-1):
                parent2=c

        return parent1, parent2

    def update(self,child1,child2):
        k = len(self.l)
        if self.fitnessC(child1) > self.l[k]:
            self.l[k] = child1
        if self.fitnessC(child2) > self.l[k+1]:
            self.l[k+1] = child2

    def crossover(self,p1, p2):
        if np.random.rand() < self.cross_rate:
            size = min(len(p1), len(p2))
            cxpoint1 = random.randint(1, size)
            cxpoint2 = random.randint(1, size-1)
            tmp0 = p1[:cxpoint1]
            tmp2 = p2[cxpoint1:]
            tmp1 = p1[:cxpoint2]
            tmp3 = p2[cxpoint2:]
            p1 = tmp0+tmp2
            p2 = tmp1+tmp3

        return p1, p2

    def mutate(self,child1,child2):
        if np.random.rand() < self.mutate_rate:
            pf = p.ParametersFound
            for key, valuep in pf.items():
                tmp = utils.generate_random_parameters(valuep)
                tmp2 = utils.generate_random_parameters(valuep)
                while 'hfile_block_cache_size' == key and tmp >= 0.40:
                    tmp = utils.generate_random_parameters(valuep)

                while 'hfile_block_cache_size' == key and tmp2 >= 0.40:
                    tmp2 = utils.generate_random_parameters(valuep)


                if utils.multi.get(key):
                    tmp = (tmp * utils.multi[key])
                    tmp2 = (tmp2 * utils.multi[key])

                child1[key] = tmp
                child2[key] = tmp2

        return child1, child2

    def traditional_GA(self,p,n):
        M = len(p)

        for c in p:
            self.fitness_result.append(self.fitnessP(c['spd']))

        S_best = max(self.fitness_result)
        C_best = p[self.fitness_result.index(S_best)]

        for j in range(0,n): #GENERATION NEXT POP
            for i in range(0,M/2):
                parent1, parent2 = self.select(p)
                child1,child2 = self.crossover(parent1,parent2)
                child1,child2 = self.mutate(child1,child2)
                child1 = self.fitnessC(child1)
                child2 = self.fitnessC(child2)
                p.append(self.update(child1,child2))
                S_best = max(self.fitness_result)
                C_best = p[self.fitness_result.index(S_best)]

        return C_best




if __name__ == '__main__':

    ga = GuntherGA()
    ga.read_sl('/home/yassine/gunther/speedupG.txt')
    # ga.read_sl('/home/yassine/gunther/latenciesG.txt')
    #
    ga.read_gunther('/home/yassine/gunther/confGunther.txt')
    ga.merge_conf_spd()
    # print(ga.latencies)
    # print(ga.speedup)
    # print(ga.config)
    # print(ga.config[1])

    ga.traditional_GA(ga.config,5)

