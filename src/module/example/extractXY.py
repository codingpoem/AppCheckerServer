#coding=utf-8
import sys
import re
import os
import subprocess
import logging
import time
import zipfile

from apkutils import APK
from configparser import ConfigParser
from src.config.database import Database
from src.config.tools import getSHA1
from src.config.cfg import WORKPATH, DBIP, DBPORT, DBNAME, AAPT, ADB

logging.basicConfig(stream=sys.stdout, format="%(levelname)s: %(asctime)s: %(message)s", level=logging.DEBUG, datefmt='%a %d %b %Y %H:%M:%S')
log = logging.getLogger(__name__)

apk_path = "/home/zdn/work/AppChecker/data/xingyuan"
apk_static_path = os.path.join(WORKPATH, "data/apk_static")

globalDB = Database(DBIP, DBPORT, DBNAME)

def extractScreenshots(apk):

    screenshots_dir = os.path.join(apk_static_path, getSHA1(apk), "screenshots")
    if not os.path.exists(screenshots_dir):
        os.makedirs(screenshots_dir)
    log.info("1, install")
    proc = subprocess.Popen("{} install -r '{}'".format(ADB, apk), shell=True, stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    r = (proc.communicate()[1]).decode()
    log.info("install: {}".format(r))
    if r.find("failed") != -1:
        log.error("install failed.")
        return False
    log.info("2, find lunch activity")
    proc = subprocess.Popen("{} d badging '{}'".format(AAPT, apk), shell=True, stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    r = (proc.communicate()[0]).decode()
    try:
        lunch_activity = re.findall("launchable-activity: name='(.*?)'", r)[0]
    except:
        log.error("no lunch information.")
        return False

    package = re.findall("package: name='(.*?)'", r)[0]
    if lunch_activity == "" or package == "":
        log.error("no lunch information.")
        return False
    log.info("3, start lunch activity")
    proc = subprocess.Popen("{} shell am start -n {}/{}".format(ADB, package, lunch_activity), shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    r = (proc.communicate()[1]).decode()
    log.info("start: {}".format((proc.communicate()[0]).decode()))
    log.info("start: {}".format((proc.communicate()[1]).decode()))

    if "Error" in r:
        log.error("lunch failed.")
        return False

    log.info("4, screencap")
    for i in range(15):
        proc = subprocess.Popen("{} shell screencap -p '/sdcard/{}.png'".format(ADB, i), shell=True, stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        r = (proc.communicate()[1]).decode()
        log.info("screencap: {}".format(r))
        if r != "":
            log.error("screencap failed.")
            return False
        proc = subprocess.Popen("{} pull '/sdcard/{}.png' '{}'".format(ADB, i, screenshots_dir), shell=True,
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        r = (proc.communicate()[0]).decode()
        if "error" in r:
            log.error("adb pull failed.")
        proc = subprocess.Popen("{} shell rm '/sdcard/{}.png'".format(ADB, i), shell=True, stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        r = (proc.communicate()[0]).decode()
        log.info("rm: {}".format(r))
        time.sleep(0.5)


    log.info("5, uninstall")
    proc = subprocess.Popen("{} uninstall '{}'".format(ADB, package), shell=True, stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    r = (proc.communicate()[0]).decode()
    log.info("uninstall: {}".format(r))
    if "Failure" in r:
        log.error("adb uninstall failed.")
        return False


def extractLocalImg(apk):

    img_extension = [".bmp", ".dib", ".jpeg", ".jpg", ".jpe", ".jp2", ".png", ".webp", ".pbm", ".pgm", ".ppm",
                     ".pxm", ".pnm", ".pfm", ".sr", ".tiff", ".tif", ".exr", ".hdr", ".pic"]

    localImg_dir = os.path.join(apk_static_path, getSHA1(apk), "localimage")
    if not os.path.exists(localImg_dir):
        os.makedirs(localImg_dir)
    'A faster method'
    zf = zipfile.ZipFile(apk, 'r')
    for f in zf.namelist():
        if os.path.splitext(os.path.basename(f))[-1] in img_extension:
            pic_path = os.path.join(localImg_dir, os.path.basename(f))
            with open(pic_path, "wb") as fwh:
                fwh.write(zf.read(f))


def retireve_info(file_in_check):

    proc = subprocess.Popen("{} d badging '{}'".format(AAPT, file_in_check), shell=True, stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    r = (proc.communicate()[0]).decode()

    items = re.compile("package: name='(.*?)' versionCode='(.*?)' versionName='(.*?)'").findall(r)
    try:
        pkg, vercode, vername = items[0]
    except:
        pkg = vercode = vername = ''

    try:
        appname = re.compile("application-label:'(.*?)'").findall(r)[0]
    except:
        appname = ''

    try:
        dn,cert = APK(file_in_check).get_certs('sha1')[0]
    except:
        dn, cert = '', ''

    cert = cert.lower()

    #info = [os.path.basename(apk), sha1, pkg, vername, appname, size]
    # log_writer(sha1, pkg, cert, dn, vername, appname)

    # db_data = {"sha1": None, "pkg": None, "cert": None, "dn": None, "vername": None, "appname": None}
    apktime = file_in_check.split('/')[-2]
    # print(apktime)
    db_data = {"sha1": getSHA1(file_in_check), "pkg": pkg, "cert": cert, "dn": dn, "vername": vername, "appname": appname, "apktime":apktime}
    globalDB.insert_one("apk_info", db_data)

def processApk(file_in_check):
    if not re.compile("\.apk$").findall(file_in_check):
        return "file file_in_check is not apk"

    if globalDB.db["apk_info"].find_one({"sha1":getSHA1(file_in_check)}):
        return "file_in_check has in database"

    pass
    retireve_info(file_in_check)
    extractLocalImg(file_in_check)
    extractScreenshots(file_in_check)


def main():
    # done = log_reader()
    for dirpath, dirnames, ifilenames in os.walk(apk_path):
        for fs in ifilenames:
            file_in_check = os.path.join(dirpath, fs)
            if not os.path.isfile(file_in_check):
                continue
            # if os.path.splitext(os.path.basename(file_in_check))[-2] in done: continue
            log.info("Processing: {}".format(file_in_check))
            processApk(file_in_check)


if __name__ == "__main__":
    for root, dirs, files in os.walk(apk_path):
        for f in files:
            if re.match("^[^\.].*\.apk$", f):
                # print(os.path.join(root,f))
                processApk(os.path.join(root,f))
