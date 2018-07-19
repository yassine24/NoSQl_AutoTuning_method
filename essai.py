import json
from sklearn.ensemble import RandomForestRegressor
from sklearn.datasets import make_regression
import numpy as np
if __name__ == '__main__':

    config = []
    with open('config.txt') as f:
        line = f.readline()
        while line:
            config.append(line.split(','))
            line = f.readline()
    print(config)

    speedup = []
    with open('speedup.txt') as f:
        line = f.readline()
        while line:
            speedup.append(line.rstrip())
            line = f.readline()
    print(speedup)

    latencies = []
    with open('latencies.txt') as f:
        line = f.readline()
        while line:
            latencies.append(line.rstrip())
            line = f.readline()
    print(latencies)




    #n_estimators = ntree : we set ntree to 550 and to 400 when we build throughput
    # models for update-heavy and read-heavy, respectively
    #Pour l'instant garder 10 puis nous verrons


    # X, y = make_regression(n_features=4, n_informative=2, random_state=0, shuffle=False)
    # print(X)
    # print('------------------- Y -----------------')
    # print(y)