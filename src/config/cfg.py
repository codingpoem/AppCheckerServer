import os

#local config
# WORKPATH = "/Users/zdn/work/AppChecker/code/AppCheckerServer"
WORKPATH = "/home/zdn/work/AppChecker/code/AppCheckerServer"

# AAPT = os.path.join(WORKPATH, "bin/mac_arm64/aapt2")
AAPT = os.path.join(WORKPATH, "bin/ubuntu_x86/aapt2")
ADB = os.getenv("adb", "/home/zdn/Android/Sdk/platform-tools/adb")

#mongodb config
DBIP = "127.0.0.1"
DBPORT = 27017
DBNAME = "acpro"