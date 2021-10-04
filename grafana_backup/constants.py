import os


if os.name == "nt":
    homedir = os.environ["HOMEPATH"]
else:
    homedir = os.environ["HOME"]

PKG_NAME = "grafana-backup"
PKG_VERSION = "1.1.9"
JSON_CONFIG_PATH = "{0}/.grafana-backup.json".format(homedir)
