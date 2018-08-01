import json
from sklearn.ensemble import RandomForestRegressor
from sklearn.datasets import make_regression
import numpy as np

def recup_config():
    config = []
    with open('config.txt') as f:
        line = f.readline()
        while line:
            tab = []
            line = line.rstrip()
            tmp = line.split(',')

            for c in tmp:
                if c == 'False':
                    c = 0
                elif c == 'True':
                    c = 1
                elif c != '':
                    c = float(c)

                if c != '':
                    tab.append(c)

            config.append(tab)
            line = f.readline()
    return config


def recup_data(filname):
    data = []
    with open(filname) as f:
        line = f.readline()
        while line:
            data.append(float(line.rstrip()))
            line = f.readline()
    return data


def performances_model(sample,output):
    regr = RandomForestRegressor(max_depth=2, random_state=0)
    regr.fit(sample,output)
    print(regr.feature_importances_)
    n = np.zeros(21)
    print(regr.predict([n]))



if __name__ == '__main__':

    speedup = recup_data('speedup.txt')
    latencies = recup_data('latencies.txt')
    config = recup_config()
    # print(speedup)
    # print(latencies)

    # performances_model(config,speedup)
    performances_model(config,latencies)
    #n_estimators = ntree : we set ntree to 550 and to 400 when we build throughput
    # models for update-heavy and read-heavy, respectively
    #Pour l'instant garder 10 puis nous verrons


    # X, y = make_regression(n_features=4, n_informative=2, random_state=0, shuffle=False)
    # print(X)
    # print('------------------- Y -----------------')
    # print(y)