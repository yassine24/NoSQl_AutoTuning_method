import xml.etree.ElementTree as ET
from lxml import etree
import random  as r
import properties as p
import numpy as np


multi = {"hbase.hregion.memstore.flush.size":16777216,
         "io.storefile.bloom.block.size":65536,
         "hfile.index.block.max.size":65536,
         "hbase.regionserver.java.heapsize":536870912
         }


def create_file_features(filename,data):
    with open(filename, 'w+') as outfile:
        outfile.write(data + '\n')


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
    for key,valuep in P.items():
        tmp = generate_random_parameters(valuep)

        while 'hfile.block.cache.size' == key and tmp > 0.40:
            tmp = generate_random_parameters(valuep)

        if multi.get(key):
            tmp = (tmp * multi[key])
        value.text = str(tmp)
        v.append(tmp)


        conf = etree.Element('configuration')
        prop = etree.SubElement(conf,"property")
        name = etree.SubElement(prop, "name")
        value = etree.SubElement(prop, "value")
        name.text = key

    et = etree.ElementTree(conf)
    et.write(("hbase_param_file/hbase-site."+ str(i)+"xml"), pretty_print=True)

    return v


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

            if cnt > 13:
                if  'AverageLatency(us)' in line.strip() :
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


def create_file_metrics(begin,end):
    for i in range(begin,end):
        metrics = extract_metrics("features"+str(i)+".txt")
        create_file_features('speedup.txt', str(metrics[0]))
        create_file_features('latencies.txt',str(metrics[1]))


def create_file_array_config(begin,end):
    f = open('config.txt', 'w+')
    for i in range(begin,end):
        c = read_xml_to_array("hbase_param_file/hbase-site" + str(i) + ".xml")
        # json.dump(c , f)
        for v in c:
            f.write(str(v)+",")
        f.write('\n')
    f.close()


if __name__ == '__main__':
    #generer les conf randomly
    # c = generate_conf(1,3)
    create_file_array_config(1,11)
    # create_file_metrics(1,3)

    # dans ATH il disent prendre 95 95 percentile latency pour la latence car
    # la latence est diff entre les operation... mais que prendre ? jai pris la moyenne des 2

