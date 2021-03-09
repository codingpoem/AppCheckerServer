import os

MILVUS_HOST = os.getenv("MILVUS_HOST", "10.91.250.23")
MILVUS_PORT = os.getenv("MILVUS_PORT", "19530")
VECTOR_DIMENSION = os.getenv("VECTOR_DIMENSION", 512)
# DATA_PATH = os.getenv("DATA_PATH", "../data/jpegimages")
DATA_PATH = os.getenv("DATA_PATH", "/home/zdn/work/AppChecker/code/AppCheckerServer/src/module/picseach/data/jpegimages")
# DEFAULT_TABLE = os.getenv("DEFAULT_TABLE", "milvus")
# DATA_PATH = os.getenv("DATA_PATH", "/home/zdn/work/AppChecker/code/AppCheckerServer/data/statistics/screencaps")
DEFAULT_TABLE = os.getenv("DEFAULT_TABLE", "screencaps")

# UPLOAD_PATH = "/tmp/search-images"
