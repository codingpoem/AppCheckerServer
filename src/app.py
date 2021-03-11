from bson import json_util
import hashlib
import json
import os
import threading
import tensorflow as tf

from configparser import ConfigParser

from flask_cors import CORS
from keras.applications import VGG16
from tensorflow.python.keras.backend import set_session
from flask import Flask, request, send_file, render_template, make_response, jsonify
from src.config.database import Database
from src.module.dogetData import getPageData
from src.module.extractApkInfo import processApk
from src.config.cfg import WORKPATH, DBIP, DBPORT, DBNAME
from src.module.picseach.common.config import DATA_PATH

# cfg = ConfigParser()
# cfg.read("config/cfg.ini")
# workPath = cfg.get("local", "workpath")
# dbIP = cfg.get('mongoDB', 'IP')
# dbPort = int(cfg.get('mongoDB', 'port'))
# dbName = cfg.get('mongoDB', 'dbName')
from src.module.picseach.common.const import input_shape
from src.module.picseach.search import do_search

globalDB = Database(DBIP, DBPORT, DBNAME)
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
app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():
    return render_template('index.html')

#upload apk and check
@app.route('/upload_apk', methods=['POST'])
def upload_apk():
    file = request.files.get("file")
    if file:
        sha1obj = hashlib.sha1()
        sha1obj.update(file.read())
        sha1 = sha1obj.hexdigest()
        if globalDB.db["apk_info"].find_one({"sha1": sha1}):
            return "database has existed file"
        else:#bak , process
            apkbak_path = os.path.join(WORKPATH, "/data/apk_bak",sha1+".apk")
            file.seek(0)
            file.save(apkbak_path)
            sub_thread = threading.Thread(
                target=processApk,
                args=(apkbak_path,)
            )
            sub_thread.start()
            return "process"+file.filename
    else:
        return "file wrong"

#return page content to browser
@app.route('/getdata', methods=['get'])
def getData():
    page = request.args["page"]
    limit = request.args["limit"]
    if page and limit:
        rd = getPageData(int(page), int(limit))
        print(rd)
        return json_util.dumps(rd)

    return "error"

# screencaps_path = "/home/zdn/work/AppChecker/code/AppCheckerServer/data/statistics/screencaps"
#retrun local picturn resource to browser
@app.route('/data/<picname>', methods=['get'])
def getPic(picname):
    pic_path = os.path.join(DATA_PATH, picname)
    if os.path.exists(pic_path):
        return  send_file(pic_path)
    return "file not exist"

#search pic,return related  picture
@app.route('/apk/screencaps/search', methods=['get'])
def do_search_api():
    picname = request.args["picname"]
    picpath = os.path.join(DATA_PATH,picname)
    res_id,res_distance  = do_search("screencaps", picpath, 10+15, model, graph, sess)
    print(res_id)
    print(res_distance)
    if isinstance(res_id, str):
        return res_id
    imgs_path = [request.url_root +"data/" + x for x in res_id]
    res = dict(zip(imgs_path, res_distance))
    res = sorted(res.items(), key=lambda item: item[1])
    # print("before")
    # for x in res:
    #     print(x)
    res = [ x for x in res if x[0].find(picname.split("_")[0]) == -1 ]
    res = res[0:10]
    # print("after")
    # for x in res:
    #     print(x)
    ret = {"data": res}
    return jsonify(ret), 200

#get apk all screencaps
@app.route('/apk/screencaps', methods=['get'])
def get_apk_screencaps():
    sha1 = request.args["sha1"]
    imgs = []
    for r,dirs,files in  os.walk(DATA_PATH):
        for f in files:
            if f.find(sha1) == -1:
                continue
            imgs.append(f)
    imgs_path = [request.url_root +"data/" + x for x in imgs]
    # res = dict(zip(imgs_path, res_distance))
    # res = sorted(res.items(), key=lambda item: item[1])
    res = sorted(imgs_path)
    print(res)
    ret = {"data": res}
    return jsonify(ret), 200

#get apk detail
@app.route('/apk/detail', methods=['get'])
def get_apk_detial():
    return render_template('index.html')


@app.route('/test', methods=['get'])
def test():
    return render_template('test.html')


if __name__ == "__main__":
    load_model()
    app.run(host='0.0.0.0', port=9999)
