
from configparser import ConfigParser

# https://www.jb51.net/article/188206.htm

if __name__ == "__main__":
    config = ConfigParser()
    config.read("cfg.ini")
    secs = config.sections()
    keys = config.options('mongoDB')
    ip = config.get('mongoDB','IP')
    print(secs)
    print(keys)
    print(ip)

