from lxml import etree
import random  as r
import properties as p
import numpy as np
import json

multi = {"hbase.hregion.memstore.flush.size":16777216,
         "io.storefile.bloom.block.size":65536,
         "hfile.index.block.max.size":65536,
         "hbase.regionserver.java.heapsize":536870912
         }

def create_file_features(filename,data):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)
        outfile.write('\n')

def generate_random_parameters(value):
    if type(value[0]) == float:
        tmp = round(r.uniform(value[0],value[1]),2)
    elif type(value[0]) == int:
        tmp = int(round(r.uniform(value[0],value[1]),0))
    elif type(value[0]) == bool:
        tmp = r.choice(value)

    return tmp


def xml_parser(i):
    P = p.Parameters
    v = []

    conf = etree.Element("configuration")
    for key,value in P.items():
        tmp = generate_random_parameters(value)
        prop = etree.SubElement(conf, "property")
        name = etree.SubElement(prop, "name")
        value = etree.SubElement(prop, "value")
        name.text = key
        if multi.get(key):
            tmp = (tmp*multi[key])
        value.text = str(tmp)
        v.append(tmp)

    et = etree.ElementTree(conf)
    et.write(("./features/hbase-site.xml"+str(i)), pretty_print=True)
    return v


def extract_metrics():
    avglatency = 0
    latency = []
    filepath = 'features0.txt'
    with open(filepath) as fp:
        line = fp.readline()
        cnt = 1
        while line:
            if cnt == 2:
                throughput = line.strip()[32:]
                throughput = float(throughput)
                # print(throughput)
                # print("Line {}: {}".format(cnt, line.strip()))
            if cnt == 13:
                latency.append(float(line.strip()[28:]))

            if cnt == 522:
                latency.append(float(line.strip()[30:]))
                # print("Line {}: {}".format(cnt, line.strip()))

            line = fp.readline()
            cnt += 1
    avglatency = np.average(latency)
    return throughput, avglatency


def generate_conf(n):
    for i in range(0,n):
        c = xml_parser(i)
    return c

def create_training_set(c,metrics):
    data = {}
    data['metrics'] = []
    latency = list(c)
    throughtput = c
    throughtput.insert(0, metrics[0])
    data['metrics'].append(throughtput)

    latency.insert(0, metrics[1])
    data['metrics'].append(latency)
    create_file_features("training_set.json", data)


if __name__ == '__main__':
    generate_conf(200)
    # metrics = extract_metrics()
    # create_training_set(c,metrics)

    # dans ATH il disent prendre 95 95 percentile latency pour la latence car
    # la latence est diff entre les operation... mais que prendre ? jai pris la moyenne des 2



