import os


class ConfigClass(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
