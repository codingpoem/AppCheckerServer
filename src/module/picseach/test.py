import os
import os.path as path
import logging
from flask_cors import CORS
from flask import Flask, request, send_file, jsonify
from flask_restful import reqparse
from milvus import Milvus
from werkzeug.utils import secure_filename
from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input as preprocess_input_vgg
from keras.preprocessing import image
import numpy as np
from numpy import linalg as LA
import tensorflow as tf
from tensorflow.python.keras.backend import set_session
from tensorflow.python.keras.models import load_model
from diskcache import Cache
import shutil

from src.module.picseach.common.config import DATA_PATH
from src.module.picseach.common.const import input_shape
from src.module.picseach.search import do_search
from src.module.picseach.train import do_train
from src.module.picseach.delete import do_delete


config = tf.ConfigProto()
config.gpu_options.allow_growth = True
config.gpu_options.per_process_gpu_memory_fraction = 0.5
global sess
sess = tf.Session(config=config)
set_session(sess)

model = None

def load_model():
    global graph
    graph = tf.get_default_graph()

    global model
    model = VGG16(weights='imagenet',
                  input_shape=input_shape,
                  pooling='max',
                  include_top=False)


def do_train_api(file_path,table_name):
    try:
        # thread_runner(1, do_train, table_name, file_path)
        do_train(table_name, file_path)
        filenames = os.listdir(file_path)
        if not os.path.exists(DATA_PATH):
            print("DATA_PATH:" + DATA_PATH)
            os.mkdir(DATA_PATH)
        for filename in filenames:
            shutil.copy(file_path + '/' + filename, DATA_PATH)
        return "Start"
    except Exception as e:
        return "Error with {}".format(e)

def do_delete_api(table_name):
    # args = reqparse.RequestParser(). \
    #     add_argument('Table', type=str). \
    #     parse_args()
    # table_name = args['Table']
    print("delete table.")
    status = do_delete(table_name)
    try:
        shutil.rmtree(DATA_PATH)
    except:
        print("cannot remove", DATA_PATH)
    return "{}".format(status)

def do_search_api(pic):
    res_id,res_distance  = do_search("screencaps", pic, 10, model, graph, sess)
    print(res_id)
    print(res_distance)
    if isinstance(res_id, str):
        return res_id
    imgs_path = [request.url_root +"data/" + x for x in res_id]
    res = dict(zip(imgs_path, res_distance))
    res = sorted(res.items(), key=lambda item: item[1])
    print(res)
    # return jsonify(res), 200



if __name__ =="__main__":
    load_model()

    ### picture  vector search by milvus
    pic = "/home/zdn/work/AppChecker/code/AppCheckerServer/data/statistics/screencaps/ffd709f5da6705c57978f3584b260b58e5d0c0d8_11.png"
    ret = do_search_api(pic)
    print(ret)


    ###upload picture data set to milvus collection and bak to tmp dir
    # do_train_api("/home/zdn/work/AppChecker/code/AppCheckerServer/data/statistics/screencaps", "screencaps")

    ###clear milvus collection and picture tmp dir
    # do_delete_api("screencaps")

