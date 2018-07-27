from cm_api.api_client import ApiResource
import properties as p
import random as r
import numpy as np
import subprocess
import json
import re

cm_host = "insilicodb.ulb.ac.be"

api = ApiResource(cm_host, username="ylakbeich", password="yassine")
multi = {"hbase_hregion_memstore_flush_size":16777216,
         "hfile_index_block_max_size":65536,
         "hbase_regionserver_java_heapsize":536870912
         }

param = {
    "hbase_hregion_memstore_flush_size": 0,
    "hbase_hstore_compactionThreshold": 0,
    "hbase_hstore_blockingStoreFiles": 0,
    "hbase_regionserver_maxlogs": 0,
    "hbase_regionserver_handler_count": 0,
    "hbase_regionserver_global_memstore_upperLimit": 0,
    "hbase_regionserver_global_memstore_lowerLimit": 0,
    "hfile_block_cache_size": 0,
    "hbase_regionserver_java_heapsize": 0
}


def get_cluster():
    # Get a list of all clusters
    cdh5 = None
    for c in api.get_all_clusters():
    #  print c.name
      if c.version == "CDH5":
        cdh5 = c

    return cdh5


def get_service(cdh5,service_type="HBASE"):
    for s in cdh5.get_all_services():
     # print s
      if s.type == service_type:
        hbase = s

    return hbase


def generate_random_parameters(value):
    if type(value[0]) == float:
        tmp = round(r.uniform(value[0],value[1]),2)
    elif type(value[0]) == int:
        tmp = int(round(r.uniform(value[0],value[1]),0))
    elif type(value[0]) == bool:
        tmp = r.choice(value)

    return tmp


def generate_param():
    P = p.ParametersFound
    param = {}
    for key, valuep in P.items():
        tmp = generate_random_parameters(valuep)

        while 'hfile_block_cache_size' == key and tmp > 0.40:
            tmp = generate_random_parameters(valuep)

        if multi.get(key):
            tmp = (tmp * multi[key])
        param[key] = tmp
    return param


def update_param(param):
    cdh5 = get_cluster()
    hbase = get_service(cdh5)

    nn = None
    for r in hbase.get_all_roles():
        if r.type == 'REGIONSERVER':
            nn = r

    nn.update_config(param)
    # !!!!!!! restart all or not ?
    cmd = cdh5.restart(restart_only_stale_services=True, redeploy_client_configuration=True)
    return cmd.wait(70)



def rec(s):
   return re.findall("\d+\.*\d+", s)

def extract_metrics(filename):
    latency = []
    filepath = filename
    with open(filepath) as fp:
        line = fp.readline()
        cnt = 1
        while line:
            if cnt == 2:
                t = rec(line)
                throughput = float(t[0])

            if '95thPercentileLatency(us), ' in line.strip() and 'CLEANUP' not in line.strip() :
                l = rec(line)
                latency.append(float(l[1]))

            line = fp.readline()
            cnt += 1

    avglatency = np.average(latency)
    return throughput, avglatency



def exec_ycsb(i,wkld):
    ycsb_load = "bin/ycsb load hbase12 -P workloads/workload"+wkld+" -cp /HBASE-HOME-DIR/conf -p table=usertable -p columnfamily=family"
    ycsb_run = "bin/ycsb run hbase12 -P workloads/workload"+wkld+" -cp /HBASE-HOME-DIR/conf -p table=usertable -p columnfamily=family > ../metrics/metricWkld-"+wkld+"-"+str(i)+".txt"

    subprocess.call(ycsb_load, shell=True, cwd='../YCSB')
    subprocess.call(ycsb_run, shell=True, cwd='../YCSB')

    metrics = extract_metrics("metricWkld-"+wkld+'-'+str(i)+".txt")
    return metrics



def create_config_file(filname,begin, end):
    conf = []
    for i in range(begin,end):
        p = generate_param()
        conf.append(p)
    f = open(filname, 'w+')
    json.dump(conf,f)
    f.close()
    return conf

def write_metric(filename, data):
    with open(filename,"w+") as out :
        json.dump(data,out)
    out.close()

def read_gunther(filename):
    with open(filename,'r') as fp:
        config = json.load(fp)
    fp.close()
    return config


if __name__ == '__main__':
    workload = ['a','b','c','e','f']
    filename = "config.txt"
    create_config_file(filename,0,5)
    cpt = 0
    latencies = []
    speedup = []
    conf = read_gunther(filename)
    for c in conf:
       update_param(c)
       #une boucle pour chaque workload et donner en param la lettre du wklds
       for wk in range(0,5):
           exec_ycsb(cpt,workload[wk])
           cpt = cpt+1
           spd, ltc = extract_metrics("features/feature"+str(cpt)+".txt")
           speedup.append(spd)
           latencies.append(ltc)

    #ATTENTION METTRE APPEND (A+) POUR MODE OPEN FILE... CREER DES FICHIER SPD ET LTC POUR CHAQUE WKLDS.
    #OU AVOIR 5 TABLEAU ET PUIS FAIRE 5 DUMP SINON VA FALLOIR MODIFIER L ECRITURE ET LOUVERTURE DES FICHIERS
       write_metric('speedup.txt',speedup)
       write_metric('latenciesG.txt',latencies)
