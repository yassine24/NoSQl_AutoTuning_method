from cm_api.api_client import ApiResource


cm_host = "insilicodb.ulb.ac.be"

api = ApiResource(cm_host, username="ylakbeich", password="yassine")
#print(api.get_all_clusters())

all_hosts = api.get_all_hosts(view='full')
#print(all_hosts)

all_hostnames = set([ h.hostname for h in all_hosts])
#print(all_hostnames)

h = all_hosts[0]
#print(h)

#print(h.roleRefs)


role = api.get_cluster('cluster')
#t = role.get_service('hbase').get_role('hbase-MASTER-4e61083dbd483f97174ec27ec055c1d3').get_config(view='full')
t = role.get_service('hdfs') #.get_role('hbase-MASTER-4e61083dbd483f97174ec27ec055c1d3').get_config(view='full')

t = t.get_role('hdfs-NAMENODE-4e61083dbd483f97174ec27ec055c1d3').get_config(view='full')
for key, value in t.iteritems():
    print(key)

