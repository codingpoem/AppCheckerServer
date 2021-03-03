#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Created on Tue Dec 22 21:08:56 2020
@author: yujun
'''

import sys
import importlib
import logging
import argparse
import os
import subprocess
import platform
import re
import hashlib
import time
import csv

logging.basicConfig(stream=sys.stdout, format="%(levelname)s: %(asctime)s: %(message)s", level=logging.INFO, datefmt='%a %d %b %Y %H:%M:%S')
log = logging.getLogger(__name__)
log_file = "snapshot_result.csv"
apk_path = "/Users/zdn/work/AppChecker/code/ACPro/acpro/tests/apks"
aapt2 = "../../bin/aapt2"



def log_writer(sha1):
    if not os.path.exists(log_file):
        with open(log_file, 'w', newline='') as f:
            f_csv = csv.writer(f)
            f_csv.writerow(['sha1'])
            f_csv.writerow([sha1])
    else:
        with open(log_file, 'a', newline='') as f:
            f_csv = csv.writer(f)
            f_csv.writerow([sha1])

def log_reader():
    if not os.path.exists(log_file):
        return []
    else:
        retMe = []
        with open(log_file) as f:
            f_csv = csv.reader(f)
            _ = next(f_csv)
            for row in f_csv:
                retMe.append(row[0])
        return retMe

def gethash(file):
    with open(file, "rb") as frh:
        sha1obj = hashlib.sha1()
        sha1obj.update(frh.read())
        return sha1obj.hexdigest()

class SnapShotExtractor:
    def __init__(self, device_serial):
        self._device_serial = device_serial

    @property
    def _aapt(self):
        return "aapt2-linux"

    def get_screen_shot(self, apk_file, local_folder):

        log.info("install")
        proc = subprocess.Popen("adb install -r '{}'".format(apk_file), shell=True, stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        r = (proc.communicate()[1]).decode()
        log.info("install: {}".format(r))
        if r.find("failed") != -1:
            log.error("install failed.")
            return False

        # lunch
        proc = subprocess.Popen("./{} d badging '{}'".format(aapt2, apk_file), shell=True, stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        r = (proc.communicate()[0]).decode()
        print(r)
        try:
            lunch_activity = re.findall("launchable-activity: name='(.*?)'", r)[0]
            print(lunch_activity)
        except:
            log.error("no lunch information.")
            return False

        package = re.findall("package: name='(.*?)'", r)[0]
        if lunch_activity == "" or package == "":
            log.error("no lunch information.")
            return False

        log.info("start")
        proc = subprocess.Popen("adb shell am start -n {}/{}".format(package, lunch_activity), shell=True, stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        r = (proc.communicate()[1]).decode()
        log.info("start: {}".format((proc.communicate()[0]).decode()))
        log.info("start: {}".format((proc.communicate()[1]).decode()))

        if "Error" in r:
            log.error("lunch failed.")
            return False

        # # take screen shot
        # snap_shot_file = "/sdcard/Splash-{}.png".format(snap_shot_file_name)
        # proc = subprocess.Popen("adb shell screencap -p {}".format(snap_shot_file), shell=True, stdin=subprocess.PIPE,
        #                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # r = (proc.communicate()[1]).decode()
        # if r != "":
        #     log.error("screencap failed.")
        #     return False
        #
        # time.sleep(2)
        #

        # wait for a while
        # time.sleep(15)

        # take screen shot
        for i in range(15):
            log.info("screencap")
            proc = subprocess.Popen("adb shell screencap -p '/sdcard/{}.png'".format(i), shell=True, stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            r = (proc.communicate()[1]).decode()
            log.info("screencap: {}".format(r))
            if r != "":
                log.error("screencap failed.")
                return False
            time.sleep(0.5)

        for i in range(15):
            # retrieve screenshot
            proc = subprocess.Popen("adb pull '/sdcard/{}.png' '{}'".format(i, local_folder), shell=True, stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            r = (proc.communicate()[0]).decode()
            if "error" in r:
                log.error("adb pull failed.")
                return False

        # uninstall
        log.info("uninstall")
        proc = subprocess.Popen("adb uninstall '{}'".format(package), shell=True, stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        r = (proc.communicate()[0]).decode()
        log.info("uninstall: {}".format(r))
        if "Failure" in r:
            log.error("adb uninstall failed.")
            return False

        # clean
        log.info("rm")
        for i in range(15):
            proc = subprocess.Popen("adb shell rm '/sdcard/{}.png'".format(i), shell=True, stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            r = (proc.communicate()[0]).decode()
            log.info("rm: {}".format(r))

        log_writer(os.path.splitext(os.path.basename(apk_file))[-2])
        log.info("snapshot of {} is stored to {}".format(apk_file, local_folder))
        return True

def main():

    # snapshot_folder = os.path.join(Config.Config["working_folder"], Config.Config["snapshot_folder"])
    snapshot_folder = "./snapshot"
    if not os.path.exists(snapshot_folder):
        os.makedirs(snapshot_folder, exist_ok=True)

    # ensure adb exist
    proc = subprocess.Popen("adb --version", shell=True, stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    r = (proc.communicate()[1]).decode()
    if r.find("not found") != -1:
        log.error("adb command not found.")
        sys.exit(1)

    # if args.device_serial:
    #     s = SnapShotExtractor(args.device_serial)
    # else:
    s = SnapShotExtractor("")

    done = log_reader()
    for dirpath, dirnames, ifilenames in os.walk(apk_path):
        for fs in ifilenames:
            file_in_check = os.path.join(dirpath, fs)
            if not os.path.isfile(file_in_check):
                continue

            if os.path.splitext(os.path.basename(file_in_check))[-2] in done: continue

            specific_folder = os.path.join(snapshot_folder, os.path.splitext(os.path.basename(file_in_check))[-2])
            if not os.path.exists(specific_folder):
                os.makedirs(specific_folder, exist_ok=True)

            log.info("processing file: {}.".format(file_in_check))
            r = s.get_screen_shot(file_in_check, specific_folder)
            if r == True:
                log.info("processing file: {} success.".format(file_in_check))
            else:
                log.info("processing file: {} failed.".format(file_in_check))

    log.info("finished")


if __name__ == "__main__":
    sys.exit(main())
