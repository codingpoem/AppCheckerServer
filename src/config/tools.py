import hashlib


def gethash(file):
    with open(file, "rb") as frh:
        sha1obj = hashlib.sha1()
        sha1obj.update(frh.read())
        return sha1obj.hexdigest()