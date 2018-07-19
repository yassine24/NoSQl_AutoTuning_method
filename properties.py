Parameters = {
"hbase.hregion.memstore.flush.size":(4,32), #16, #trouve dans regionserver role
"hbase.rs.cacheblocksonwrite":(3,6),
"hbase.hstore.compactionThreshold":(4,20),#trouve dans regionserver role
"hbase.storescanner.parallel.seek.threads":(4,20),

"hbase.hstore.blockingStoreFiles":(5,12), #trouve

"hbase.storescanner.parallel.seek.enable":(False,True),

"hbase.regionserver.maxlogs":(16,48), #trouve regionserver role
"hbase.regionserver.handler.count":(20,80), #trouve regionserver

"hbase.client.max.perregion.tasks" : (1,5),
"hbase.client.max.perserver.tasks" : (4,20),


"hbase.ipc.server.callqueue.handler.factor":(0.0,1.0),
"hbase.ipc.server.callqueue.scan.ratio" : (0.0,1.0),


"io.storefile.bloom.block.size":(1,10),#64kb

"ycsb.client.threads" : (24,72),

"regionserver.global.memstore.upperLimit" : (0.10,0.60),#trouve regionserver
"regionserver.global.memstore.lowerLimit": (0.10,0.60), #trouve regionserver

"hfile.index.block.max.size":(1,10),#64kb
"hfile.block.cache.size":(0.10,0.60), #trouve regionserver
"hfile.block.bloom.cacheonwrite":(True,False),
"hfile.block.index.cacheonwrite":(False,True),
"hbase.regionserver.java.heapsize":(8,20)#512mb

}

