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

import shutil
import zipfile

logging.basicConfig(stream=sys.stdout, format="%(levelname)s: %(asctime)s: %(message)s", level=logging.INFO, datefmt='%a %d %b %Y %H:%M:%S')
log = logging.getLogger(__name__)
apk_path = "/Users/zdn/work/AppChecker/code/ACPro/acpro/tests/apks"

log_file = "local_res_result.csv"

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

class LocalImgExtractor:
    def __init__(self, device_serial):
        self._device_serial = device_serial


    def get_localimg(self, apk_file, local_folder):
        img_extension = [".bmp", ".dib", ".jpeg", ".jpg", ".jpe", ".jp2", ".png", ".webp", ".pbm", ".pgm", ".ppm",
                         ".pxm", ".pnm", ".pfm", ".sr", ".tiff", ".tif", ".exr", ".hdr", ".pic"]

        'A faster method'
        zf = zipfile.ZipFile(apk_file, 'r')
        for f in zf.namelist():
            if os.path.splitext(os.path.basename(f))[-1] in img_extension:
                with open(os.path.join(local_folder, os.path.basename(f)), "wb") as fwh:
                    print(os.path.join(local_folder, os.path.basename(f)))
                    fwh.write(zf.read(f))

        '''
        log.info("decoding..")

        shutil.rmtree("./tmp", ignore_errors = True)

        proc = subprocess.Popen(
            "java -jar ./apktool_2.4.0.jar d '{}' -f -o '{}'".format(apk_file, "./tmp"),
            shell=True, stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        r = (proc.communicate()[0]).decode()

        log.info("searching..")
        for dirpath, dirnames, ifilenames in os.walk("./tmp"):
            for fs in ifilenames:
                file_in_check = os.path.join(dirpath, fs)
                if not os.path.isfile(file_in_check):
                    continue

                try:
                    if os.path.splitext(os.path.basename(file_in_check))[-1] in img_extension:
                        shutil.move(file_in_check, local_folder)
                except:
                    continue
        log.info("cleaning..")
        shutil.rmtree("./tmp", ignore_errors = True)

        '''

        log_writer(os.path.splitext(os.path.basename(apk_file))[-2])
        log.info("local res of {} is stored to {}".format(apk_file, local_folder))
        return True

def main():

    # snapshot_folder = os.path.join(Config.Config["working_folder"], Config.Config["snapshot_folder"])
    snapshot_folder = "./snapshot"
    if not os.path.exists(snapshot_folder):
        os.makedirs(snapshot_folder, exist_ok=True)

    s = LocalImgExtractor("")

    done = log_reader()
    for dirpath, dirnames, ifilenames in os.walk(apk_path):
        for fs in ifilenames:

            file_in_check = os.path.join(dirpath, fs)
            if not os.path.isfile(file_in_check):
                continue

            if os.path.splitext(os.path.basename(file_in_check))[-2] in done: continue

            specific_folder = os.path.join(snapshot_folder, os.path.splitext(os.path.basename(file_in_check))[-2], "localimg")
            if not os.path.exists(specific_folder):
                try:
                    os.makedirs(specific_folder, exist_ok=True)
                except:
                    continue
            log.info("processing file: {}.".format(file_in_check))
            try:
                r = s.get_localimg(file_in_check, specific_folder)
            except:
                continue
            if r == True:
                log.info("processing file: {} success.".format(file_in_check))
            else:
                log.info("processing file: {} failed.".format(file_in_check))

    log.info("finished")


if __name__ == "__main__":
    sys.exit(main())
