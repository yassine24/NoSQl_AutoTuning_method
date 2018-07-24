Parameters = {
    "hbase.hregion.memstore.flush.size": (4, 32),  # 16, #trouve dans regionserver role
    "hbase.rs.cacheblocksonwrite": (3, 6),
    "hbase.hstore.compactionThreshold": (4, 20),  # trouve dans regionserver role
    "hbase.storescanner.parallel.seek.threads": (4, 20),

    "hbase.hstore.blockingStoreFiles": (5, 12),  # trouve

    "hbase.storescanner.parallel.seek.enable": (False, True),

    "hbase.regionserver.maxlogs": (16, 48),  # trouve regionserver role
    "hbase.regionserver.handler.count": (20, 80),  # trouve regionserver

    "hbase.client.max.perregion.tasks": (1, 5),
    "hbase.client.max.perserver.tasks": (4, 20),

    "hbase.ipc.server.callqueue.handler.factor": (0.0, 1.0),
    "hbase.ipc.server.callqueue.scan.ratio": (0.0, 1.0),

    "io.storefile.bloom.block.size": (1, 10),  # 64kb

    "ycsb.client.threads": (24, 72),

    "regionserver.global.memstore.upperLimit": (0.10, 0.60),  # trouve regionserver
    "regionserver.global.memstore.lowerLimit": (0.10, 0.60),  # trouve regionserver

    "hfile.index.block.max.size": (1, 10),  # 64kb
    "hfile.block.cache.size": (0.10, 0.60),  # trouve regionserver
    "hfile.block.bloom.cacheonwrite": (True, False),
    "hfile.block.index.cacheonwrite": (True, False),
    "hbase.regionserver.java.heapsize": (8, 20)  # 512mb

}

ParametersFound = {
    "hbase_hregion_memstore_flush_size": (4, 32),  # 16, #trouve dans regionserver role
    "hbase_hstore_compactionThreshold": (4, 20),  # trouve dans regionserver role
    "hbase_hstore_blockingStoreFiles": (5, 12),  # trouve
    "hbase_regionserver_maxlogs": (16, 48),  # trouve regionserver role
    "hbase_regionserver_handler_count": (20, 80),  # trouve regionserver
    "hbase_regionserver_global_memstore_upperLimit": (0.10, 0.60),  # trouve regionserver
    "hbase_regionserver_global_memstore_lowerLimit": (0.10, 0.60),  # trouve regionserver
    "hfile_block_cache_size": (0.10, 0.60),  # trouve regionserver
    "hbase_regionserver_java_heapsize": (8, 20)  # 512mb
}

ParamNames = [
    "hbase_hregion_memstore_flush_size",  # 16, #trouve dans regionserver role
    "hbase_hstore_compactionThreshold",  # trouve dans regionserver role
    "hbase_hstore_blockingStoreFiles",  # trouve
    "hbase_regionserver_maxlogs",  # trouve regionserver role
    "hbase_regionserver_handler_count",  # trouve regionserver
    "hbase_regionserver_global_memstore_upperLimit",  # trouve regionserver
    "hbase_regionserver_global_memstore_lowerLimit", # trouve regionserver
    "hfile_block_cache_size",  # trouve regionserver
    "hbase_regionserver_java_heapsize" # 512mb
]
