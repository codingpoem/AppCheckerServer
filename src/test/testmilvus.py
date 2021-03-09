import os

from milvus import Milvus, IndexType, MetricType, Status



if __name__ == "__main__":
    milvus = Milvus(host="10.91.250.23", port="19530")
    if not milvus.has_collection("screencaps")[1]:
        print("has not collectiion")
        exit(1)

    print("start")
    milvus.drop_collection("screencaps")
