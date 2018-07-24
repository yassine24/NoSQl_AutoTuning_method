from cm_api.api_client import ApiResource
import properties as p
import random  as r
import subprocess
import json


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
        # print r
        if r.type == 'REGIONSERVER':
            nn = r

    nn.update_config(param)

    cmd = cdh5.restart(restart_only_stale_services=True, redeploy_client_configuration=True)
    return cmd.wait(70)



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


def exec_ycsb(i):
    ycsb_load = "bin/ycsb load hbase12 -P workloads/workloadb -cp /HBASE-HOME-DIR/conf -p table=usertable -p columnfamily=family"
    ycsb_run = "bin/ycsb run hbase12 -P workloads/workloadb -cp /HBASE-HOME-DIR/conf -p table=usertable -p columnfamily=family > ../gunther/child"+str(i)+".txt"

    subprocess.call(ycsb_load, shell=True, cwd='YCSB')
    subprocess.call(ycsb_run, shell=True, cwd='YCSB')
    metrics = extract_metrics("child"+str(i)+".txt")
    return metrics


def create_file_features(filename,data):
    with open(filename, 'w+') as outfile:
        outfile.write(data + '\n')


def create_config_file(begin, end):
    conf = []
    for i in range(begin,end):
        p = generate_param()
        conf.append(p)
    filname = "confGunther.txt"
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
    filname = "confGunther0.txt"
    create_config_file(0,5)
    cpt = 0
    latencies = []
    speedup = []
    conf = read_gunther(filname)
    for c in conf:
       update_param(c)
       exec_ycsb(cpt)
       cpt = cpt+1
       spd, ltc = extract_metrics("../gunther/child"+str(cpt)+".txt")
       speedup.append(spd)
       latencies.append(ltc)

    write_metric('speedupG.txt',speedup)
    write_metric('latenciesG.txt',latencies)
