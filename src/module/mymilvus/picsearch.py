from src.module.mymilvus.mymilvus import get_milvusclient
from src.module.mymilvus.myvgg import vgg_extract_feat

milvus = get_milvusclient()


def picsearch(collect, pic_path):
    print(pic_path)
    if  not milvus.has_collection("milvus"):
        print("query milvus collection defeat")
        return None

    vectors = []
    # feat = vgg_extract_feat(pic_path, model, graph, sess)
    feat = vgg_extract_feat(pic_path)
    vectors.append(feat)
    search_param = {'nprobe': 16}
    # status, res = milvus.search(collection_name=collect, query_records=vectors, top_k=10, params=search_param)
    # print(status)
    # print(res)


def picToMilvus(pic_dir, milvus_client):
    pass



if __name__ == "__main__":
    picsearch("milvus", "/tmp/pic2/2008_007028.jpg")
