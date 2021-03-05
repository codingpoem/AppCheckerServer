from bson import json_util
import hashlib
import json
import os
import threading
from configparser import ConfigParser
from flask import Flask, request, send_file, render_template, make_response
from src.config.database import Database
from src.module.dogetData import getPageData
from src.module.extractApkInfo import processApk
from src.config.cfg import WORKPATH, DBIP, DBPORT, DBNAME

# cfg = ConfigParser()
# cfg.read("config/cfg.ini")
# workPath = cfg.get("local", "workpath")
# dbIP = cfg.get('mongoDB', 'IP')
# dbPort = int(cfg.get('mongoDB', 'port'))
# dbName = cfg.get('mongoDB', 'dbName')
globalDB = Database(DBIP, DBPORT, DBNAME)

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

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


@app.route('/getdata', methods=['get'])
def getData():
    page = request.args["page"]
    limit = request.args["limit"]
    if page and limit:
        rd = getPageData(int(page), int(limit))
        print(rd)
        return json_util.dumps(rd)

    return "error"

screencaps_path = "/home/zdn/work/AppChecker/code/AppCheckerServer/data/statistics/screencaps"
@app.route('/pic/<picname>', methods=['get'])
def getPic(picname):
    pic_path = os.path.join(screencaps_path, picname)
    if pic_path.exists(pic_path):
        return  (pic_path)
    return "file not exist"



if __name__ == "__main__":
    app.run(host='127.0.0.1', port=6666)
