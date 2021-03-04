import hashlib


def getSHA1(file):
    with open(file, "rb") as frh:
        sha1obj = hashlib.sha1()
        sha1obj.update(frh.read())
        return sha1obj.hexdigest()