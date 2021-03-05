import requests
from bson import json_util

def test_upload_apk():
    localfile1 = "/Users/zdn/work/AppChecker/code/ACPro/acpro/tests/apks/30e32b3f5bfdceb74e05f80d68c443a80ba4aef6.apk"
    localfile2 = "/Users/zdn/work/AppChecker/code/ACPro/acpro/tests/apks/f0af4c508ba13ef893fe32d23413c6e6c0193e05.apk"
    localfile3 = "/Users/zdn/work/AppChecker/code/ACPro/acpro/tests/apks/c51a1a062ed71b630aa565fa584eac40b050b453.apk"
    localfile4= "/Users/zdn/work/AppChecker/code/ACPro/acpro/tests/apks/bf6aa3725b5d59bd48b1a2a0beaf8a98fe660f07.apk"
    files = { "file":open(localfile2, "rb")}
    data = {}
    upload_res = requests.post("http://127.0.0.1:5000/upload_apk", files=files, data=data)
    print(upload_res, upload_res.content)

def test_getdata():
    response = requests.get("http://127.0.0.1:6666/getdata?page=2&limit=5")
    # response = requests.get("https://www.layui.com/demo/table/user/?page=3&limit=3")
    print(response, response.content)
    # for i in json_util.loads(response.content.decode()):
    #     print(i)
# {"id":10006,"username":"user-6","sex":"\xe5\xa5\xb3","city":"\xe5\x9f\x8e\xe5\xb8\x82-6","sign":"\xe7\xad\xbe\xe5\x90\x8d-6","experience":982,"logins":37,"wealth":57768166,"classify":"\xe4\xbd\x9c\xe5\xae\xb6","score":34}


if __name__ == "__main__":
    response = requests.get("http://127.0.0.1:6666")
    print(response, response.content)

    # test_getdata()
    # test_upload_apk()