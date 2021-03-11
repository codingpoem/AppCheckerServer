
import time
import threading
from src.config.database import Database

dbIP = "127.0.0.1"
dbPort = 27017
dbName = "acpro"
globalDB = Database(dbIP, dbPort, dbName)

def task(str):
    print("str start")
    time.sleep(5)
    print("str end")


def getData(page, limit):


    return_data = {"code":0, "msg":"", "count":0, "data":[]}
    ct = globalDB.db["apk_info"].count_documents({})

    print(type(ct), ct)
    # result = globalDB.db["apk_info"].find().skip((page-1)*limit).limit(limit)
    # for i in result:
    #     # i.pop("_id")
    #     # print(type(i), i)
    #     # print(type(i["_id"]), i["_id"])
    #     # i["_id"] = str(i["_id"])
    #     # print(type(i["_id"]), i["_id"])
    #
    #     return_data["data"].append(i)


if __name__ == "__main__" :
    # th = threading.Thread(target=task, args=("tt",))
    # th.start()
    # print("this is main thread")

    # getData(2,5)
    # getData(2,10)
    # getData(3,10)

    mlist =  ["aa","bb","cc","dd","ee"]
    print(mlist)
    # mlist = filter(lambda x:x!="aa", mlist)
    mlist =  [x for x in mlist if x!="aa"]
    print(mlist)









