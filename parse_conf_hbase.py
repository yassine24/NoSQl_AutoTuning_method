import xml.etree.ElementTree as ET
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


def read_xml_to_array(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    myArray = []
    for i in range(0, 21):
        # para_name = root[i][0].text
        para_value = root[i][1].text
        if para_value != 'False' and para_value != 'True':
            para_value = float(para_value)
        myArray.append(para_value)

    return myArray


def xml_parser(i):
    P = p.Parameters
    v = []
    s = ''
    filename = "./features/hbase-site" + str(i) + ".xml"
    with open(filename, 'w+') as outfile:
        for key,valuep in P.items():
            tmp = generate_random_parameters(valuep)

            prop = etree.Element("property")
            name = etree.SubElement(prop, "name")
            value = etree.SubElement(prop, "value")
            name.text = key
            while 'hfile.block.cache.size' == key and tmp > 0.40:
               tmp = generate_random_parameters(valuep)

            if 'hfile.block.cache.size' == key:
                print(tmp)

            if multi.get(key):
                tmp = (tmp*multi[key])
            value.text = str(tmp)
            v.append(tmp)
            et = etree.ElementTree(prop)
            s = ET.tostring(prop)
            outfile.write(s+"\n")
    return v


def extract_metrics(filename):
    latency = []
    filepath = filename
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


def generate_conf(start,n):
    for i in range(start,n):
        c = xml_parser(i)
    return c


def create_training_set(c,i):
    metrics = extract_metrics("features"+str(i)+".txt")
    latency = list(c)
    throughtput = c
    throughtput.insert(0, metrics[0])
    latency.insert(0, metrics[1])
    return throughtput, latency


if __name__ == '__main__':
    #generer les conf randomly
    c = generate_conf(6,50)

    # data = {}
    # data['metrics'] = []
    # for i in range(0,1):
    #     c = read_xml_to_array("features/hbase-site"+str(i)+".xml")
    #     throughtput, latency = create_training_set(c,i)
    #     data['metrics'].append(throughtput)
    #     data['metrics'].append(latency)
    #
    # create_file_features('training_set.json',data)

    # dans ATH il disent prendre 95 95 percentile latency pour la latence car
    # la latence est diff entre les operation... mais que prendre ? jai pris la moyenne des 2

