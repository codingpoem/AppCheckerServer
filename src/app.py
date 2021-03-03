
import hashlib
import os
import threading
from configparser import ConfigParser
from flask import Flask, request, send_file
from src.config.database import Database
from src.module.extractApkInfo import processApk
cfg = ConfigParser()
cfg.read("config/cfg.ini")
dbIP = cfg.get('mongoDB', 'IP')
dbPort = int(cfg.get('mongoDB', 'port'))
dbName = cfg.get('mongoDB', 'dbName')
globalDB = Database(dbIP, dbPort, dbName)

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'


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
            apkbak_path = os.path.join("/Users/zdn/work/AppChecker/code/AppCheckerServer/data/apk_bak",sha1+".apk")
            file.seek(0)
            file.save(apkbak_path)
            print("aaa", apkbak_path)
            sub_thread = threading.Thread(
                target=processApk,
                args=(apkbak_path,)
            )
            sub_thread.start()
            return "process"+file.filename
    else:
        return "file wrong"




if __name__ == "__main__":
    app.run()