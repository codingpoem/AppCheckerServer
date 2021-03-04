from configparser import ConfigParser

from src.config.database import Database
from src.config.cfg import WORKPATH, DBIP, DBPORT, DBNAME

##db
globalDB = Database(DBIP, DBPORT, DBNAME)


def getPageData(page, limit):
    rdata = {"code":0, "msg":"", "count":0, "data":[]}
    rdata["count"] = globalDB.db["apk_info"].count_documents({})
    result = globalDB.db["apk_info"].find().skip((page-1)*limit).limit(limit)
    for i in result:
        i.pop("_id")
        # i["_id"] = str(i["_id"])
        rdata["data"].append(i)
    return rdata
