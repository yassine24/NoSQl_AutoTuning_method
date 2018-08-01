import random
import numpy as np
import utils as utils
import json
import properties as p


class GuntherGA:

    def __init__(self):
        self.speedup = []  # lire fichier speedup [val,val,...]
        self.latencies = []  # lire fchier latence [val,val,...]
        self.config = []  # lire fichier config [[c,c,c,..],[c,c,c,..],..]
        self.fitness_result = {}  # evaluate fitness
        self.cpt = 0
        self.l = []
        self.cross_rate = 0.7
        self.mutate_rate = 0.1
        self.N_DEC = 20

    def merge_conf_spd(self):
        i = 0
        for c in self.config:
            c['spd'] = self.speedup[i]
            i = i + 1

    def read_sl(self, filename):
        with open(filename, 'r') as fp:
            c = json.load(fp)
        fp.close()
        if filename == '/home/yassine/gunther/speedupG.txt':
            self.speedup = c
        else:
            self.latencies = c

    def read_gunther(self, filename):
        with open(filename, 'r') as fp:
            self.config = json.load(fp)
        fp.close()

    def fitnessP(self, spd):
        return 1 / spd

    def fitnessC(self, c):
        del c['spd']
        utils.update_param(c)
        metrics = utils.exec_ycsb(self.cpt)
        self.cpt = self.cpt + 1
        c['spd'] = metrics[0]
        return c

    def select(self):
        k = self.fitness_result.keys()
        k.sort(reverse=True)
        parent1 = self.fitness_result[k[0]]
        parent2 = self.fitness_result[k[1]]
        return parent1, parent2

    def update(self, child1, child2):
        k = self.fitness_result.keys()
        k.sort()
        spd1 = (1 / child1['spd'])
        if spd1 > k[0]:
            del self.fitness_result[k[0]]
            self.fitness_result[spd1] = child1

        spd2 = (1 / child2['spd'])
        if spd2 > k[1]:
            del self.fitness_result[k[1]]
            self.fitness_result[spd2] = child2


    def swap(self, p1, p2):
        tmp0 = {}
        tmp1 = {}
        size = min(len(p1), len(p2))
        pt1 = random.randint(0, size)
        pt2 = random.randint(0, size)

        cpt = 0
        for key in p1:
            if cpt <= pt1:
                tmp0[key] = p1[key]

            if cpt > pt1:
                tmp0[key] = p2[key]

            if cpt <= pt2:
                tmp1[key] = p1[key]

            if cpt > pt2:
                tmp1[key] = p2[key]
            cpt = cpt + 1
        return tmp0, tmp1

    def crossover(self, p1, p2):
        if np.random.rand() < self.cross_rate:
            p1, p2 = self.swap(p1, p2)
            print('je suis passer dans crossover-----------------')
        return p1, p2

    def mutate(self, child1, child2):
        if np.random.rand() < self.mutate_rate:
            print('je suis passer dans mutate-----------------')
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

    def traditional_GA(self, p, n):
        M = len(p)

        for c in p:
            self.fitness_result[self.fitnessP(c['spd'])] = c

        C_best = self.fitness_result[max(self.fitness_result.keys())]

        for j in range(0, n):  # GENERATION NEXT POP
            print('N GEN %d' % j)
            for i in range(0, M / 2):
                parent1, parent2 = self.select()
                child1, child2 = self.crossover(parent1, parent2)
                child1, child2 = self.mutate(child1, child2)
                print("done mutate and cross")
                child1 = self.fitnessC(child1)
                child2 = self.fitnessC(child2)
                self.update(child1, child2)
                C_best = self.fitness_result[max(self.fitness_result.keys())]

            print("GEN : %d  %s" % (j, C_best))

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
    b = ga.config
    c = ga.traditional_GA(b, 2)
    print(c)
