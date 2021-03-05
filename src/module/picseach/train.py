import logging
import time
import os
from src.module.picseach.common.config import DEFAULT_TABLE
from src.module.picseach.common.const import default_cache_dir
from src.module.picseach.common.config import DATA_PATH as database_path
from src.module.picseach.encoder.encode import feature_extract, feature_extract_one
from src.module.picseach.preprocessor.vggnet import VGGNet
from diskcache import Cache
from src.module.picseach.indexer.index import milvus_client, create_table, insert_vectors, delete_table, search_vectors, create_index, has_table

# DEFAULT_TABLE = os.getenv("DEFAULT_TABLE", "screencaps")
# default_cache_dir="/home/zdn/work/AppChecker/code/AppCheckerServer/src/module/picseach/tmp"

#insert vectors into milvus
def do_train(table_name, database_path):
    if not table_name:
        table_name = DEFAULT_TABLE
    cache = Cache(default_cache_dir)
    try:
        vectors, names = feature_extract(database_path, VGGNet())
        index_client = milvus_client()
        # delete_table(index_client, table_name=table_name)
        # time.sleep(1)
        status, ok = has_table(index_client, table_name)
        if not ok:
            print("create table.")
            create_table(index_client, table_name=table_name)
        print("insert into:", table_name)
        status, ids = insert_vectors(index_client, table_name, vectors)
        create_index(index_client, table_name)
        for i in range(len(names)):
            # cache[names[i]] = ids[i]
            cache[ids[i]] = names[i]
        print("Train finished")
        return "Train finished"
    except Exception as e:
        logging.error(e)
        return "Error with {}".format(e)

def do_train_one(table, pic):
    if not table:
        table = DEFAULT_TABLE
    cache = Cache(default_cache_dir)
    try:
        vector, name = feature_extract_one(pic, VGGNet())
        index_client = milvus_client()

        status, ok = has_table(index_client, table)
        if not ok:
            print("create table.")
            create_table(index_client, table_name=table)



    except Exception as e:
        logging.error(e)
        return "Error with {}".format(e)


if  __name__ == "__main__":
    do_train(DEFAULT_TABLE, database_path)
    # do_train(DEFAULT_TABLE, "/home/zdn/work/AppChecker/code/AppCheckerServer/data/statistics/screencaps_test")


