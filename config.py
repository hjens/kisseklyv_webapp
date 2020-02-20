import os

class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
    BACKEND_URL = "http://192.168.1.193:8000"