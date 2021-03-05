import os
import numpy as np
from src.module.picseach.common.config import DATA_PATH as database_path
from src.module.picseach.common.const import default_cache_dir
from src.module.picseach.encoder.utils import get_imlist
from src.module.picseach.preprocessor.vggnet import VGGNet
from diskcache import Cache

# default_cache_dir="/home/zdn/work/AppChecker/code/AppCheckerServer/src/module/picseach/tmp"
# DATA_PATH = os.getenv("DATA_PATH", "/home/zdn/work/AppChecker/code/AppCheckerServer/data/statistics/screencaps")
# database_path = DATA_PATH

def feature_extract(database_path, model):
    cache = Cache(default_cache_dir)
    feats = []
    names = []
    img_list = get_imlist(database_path)
    model = model
    for i, img_path in enumerate(img_list):
        print(img_path)
        norm_feat = model.vgg_extract_feat(img_path)
        img_name = os.path.split(img_path)[1]
        feats.append(norm_feat)
        names.append(img_name.encode())
        current = i+1
        total = len(img_list)
        cache['current'] = current
        cache['total'] = total
        print ("extracting feature from image No. %d , %d images in total" %(current, total))
#    feats = np.array(feats)
    return feats, names


def feature_extract_one(pic, model):
    cache = Cache(default_cache_dir)
    norm_feat = model.vgg_extract_feat(pic)
    img_name = os.path.split(pic)[1]
    return norm_feat,img_name

