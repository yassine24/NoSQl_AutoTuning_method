import random
import numpy as np
import rech as utils
import subprocess


class GuntherGA:

    def __init__(self):
        self.speedup = [] #lire fichier speedup [val,val,...]
        self.latencies = [] #lire fchier latence [val,val,...]
        self.config = [] #lire fichier config [[c,c,c,..],[c,c,c,..],..]
        self.fitness_result = [] #evaluate fitness
        self.cpt = 1
        self.l = []

    def read_sl(self,filename):
        with open(filename) as fp:
            line = fp.readline()
            while line:
                line = line.strip()
                self.speedup.append(float(line))
                line = fp.readline()

    def read_gunther(self,filename):
        with open(filename) as fp:
            line = fp.readline()
            while line:
                line = (line.strip()).split(',')
                line.remove('')
                for i in range(0,len(line)):
                    line[i] = float(line[i])
                self.config.append(line)
                line = fp.readline()

    def fitnessP(self,c):
        return 1/self.speedup[c]

    def fitnessC(self,c):
        utils.update_param(c)
        metrics = utils.exec_ycsb(self.cpt)
        self.cpt = self.cpt + 1
        return metrics

    def select(self,p):
        self.l = p.sort(reverse=True)
        self.fitness_result.sort(reverse=True)
        avg = np.average(self.fitness_result)
        if self.fitness_result[1] > avg:
            parent1 = self.l[1]
        if self.fitness_result[2] > avg:
            parent2 = self.l[2]

        return parent1, parent2

    def update(self,child1,child2):
        k = len(self.l)
        if self.fitnessC(child1) > self.l[k]:
            self.l[k] = child1
        if self.fitnessC(child2) > self.l[k+1]:
            self.l[k+1] = child2

   #a refaore !!!!
    def crossover(self,ind1, ind2):
        size = min(len(ind1), len(ind2))
        cxpoint1 = random.randint(1, size)
        cxpoint2 = random.randint(1, size - 1)
        if cxpoint2 >= cxpoint1:
            cxpoint2 += 1
        else: # Swap the two cx points
            cxpoint1, cxpoint2 = cxpoint2, cxpoint1

        ind1[cxpoint1:cxpoint2], ind2[cxpoint1:cxpoint2] \
            = ind2[cxpoint1:cxpoint2], ind1[cxpoint1:cxpoint2]

        return ind1, ind2


    def traditional_GA(self,p,n):
        M = len(p)
        l = []
        for c in p:
            self.fitness_result.append(self.fitness(c))

        C_best = max(self.fitness_result)

        for j in range(0,n): #GENERATION NEXT POP
            for i in range(0,M/2):
                parent1, parent2 = self.select(p)
                child1,child2 = self.crossover(parent1,parent2)
                child1,child2 = self.mutate(child1,child2)
                child1 = self.fitness(child1)
                child2 = self.fitness(child2)
                p = self.update(child1,child2)
                C_best = max(self.fitness_result)

        return C_best




if __name__ == '__main__':

    ga = GuntherGA()
    ga.read_sl('speedup.txt')
    ga.read_sl('latencies.txt')

    ga.read_gunther('confGunther0.txt')
    print(ga.config)

    ga.traditional_GA(ga.config,5)