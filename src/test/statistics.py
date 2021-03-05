import os
import re
import shutil

def mvPNG(r, f):
    dest_dir = "/home/zdn/work/AppChecker/code/AppCheckerServer/data/statistics/screencaps"
    src_file = os.path.join(r,f)
    dest_file = os.path.join(dest_dir, r.split('/')[-2]+'_'+f)
    print(src_file, dest_file)
    shutil.copyfile(src_file, dest_file)



if __name__ == "__main__":
    p = "/home/zdn/work/AppChecker/code/AppCheckerServer/data/apk_static"
    for r,ds,fs in os.walk(p):
        # for d in ds:
        #     print(d)
        for f in fs:
            if re.compile("screenshots$").findall(r):
                print(r, f)
                mvPNG(r, f)
            # print(os.path.join(r,f))

