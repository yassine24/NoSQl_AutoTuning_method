Parameters = {
"hbase.hregion.memstore.flush.size":(4,32), #16, #trouvé dans regionserver role
"hbase.rs.cacheblocksonwrite":(3,6),
"hbase.hstore.compactionThreshold":(4,20),#trouvé dans regionserver role
"hbase.storescanner.parallel.seek.threads":(4,20),

"hbase.hstore.blockingStoreFiles":(5,12), #trouvé

"hbase.storescanner.parallel.seek.enable":(False,True),

"hbase.regionserver.maxlogs":(16,48), #trouvé regionserver role
"hbase.regionserver.hlog.blocksize":(4,32),#16
"hbase.regionserver.handler.count":(20,80),

"hbase.client.max.perregion.tasks" : (1,5),
"hbase.client.max.perserver.tasks" : (4,20),


"hbase.ipc.server.callqueue.handler.factor":(0.0,1.0),
"hbase.ipc.server.callqueue.read.ratio" : (0.0,1.0),
"hbase.ipc.server.callqueue.scan.ratio" : (0.0,1.0),


"io.storefile.bloom.block.size":(1,10),#64kb

"ycsb.client.threads" : (24,72),

"regionserver.global.memstore.upperLimit" : (0.10,0.60),#trouvé regionserver
"regionserver.global.memstore.lowerLimit": (0.10,0.60), #trouvé regionserver

"hfile.index.block.max.size":(1,10),#64kb
"hfile.block.cache.size":(0.10,0.60),
"hfile.block.bloom.cacheonwrite":(True,False),
"hfile.block.index.cacheonwrite":(False,True)


}

JMV_HEAP_SIZE = ("java virtual machine heap size",(8,20))#512mb
