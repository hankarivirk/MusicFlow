import os

def check_dirs():
    for d in ["downloads", "cache"]:
        if not os.path.exists(d):
            os.makedirs(d, exist_ok=True)
