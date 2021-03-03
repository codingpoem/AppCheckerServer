import requests

def test_upload_apk():
    localfile1 = "/Users/zdn/work/AppChecker/code/ACPro/acpro/tests/apks/30e32b3f5bfdceb74e05f80d68c443a80ba4aef6.apk"
    localfile2 = "/Users/zdn/work/AppChecker/code/ACPro/acpro/tests/apks/f0af4c508ba13ef893fe32d23413c6e6c0193e05.apk"
    localfile3 = "/Users/zdn/work/AppChecker/code/ACPro/acpro/tests/apks/c51a1a062ed71b630aa565fa584eac40b050b453.apk"
    localfile4= "/Users/zdn/work/AppChecker/code/ACPro/acpro/tests/apks/bf6aa3725b5d59bd48b1a2a0beaf8a98fe660f07.apk"


    files = { "file":open(localfile2, "rb")}
    data = {}
    ##此处是重点！我们操作文件上传的时候，接口请求参数直接存到upload_data变量里面，在请求的时候，直接作为数据传递过去
    upload_res = requests.post("http://127.0.0.1:5000/upload_apk", files=files, data=data)
    print(upload_res, upload_res.content)



if __name__ == "__main__":

    # reponse = requests.get("http://127.0.0.1:5000")
    # print(reponse, reponse.content)

    test_upload_apk()