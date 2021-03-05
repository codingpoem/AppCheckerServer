import logging
import time
from src.module.picseach.common.config import DEFAULT_TABLE
from src.module.picseach.common.const import default_cache_dir
from src.module.picseach.common.config import DATA_PATH as database_path
from src.module.picseach.encoder.encode import feature_extract
from src.module.picseach.preprocessor.vggnet import VGGNet
from diskcache import Cache
from src.module.picseach.indexer.index import milvus_client, create_table, insert_vectors, delete_table, search_vectors, create_index, count_table


#query count  of table in milvus
def do_count(table_name):
    if not table_name:
        table_name = DEFAULT_TABLE
    try:
        index_client = milvus_client()
        print("get table rows:",table_name)
        num = count_table(index_client, table_name=table_name)
        return num
    except Exception as e:
        logging.error(e)
        return "Error with {}".format(e)


if __name__ == "__main__":
    print(do_count("screencaps"))