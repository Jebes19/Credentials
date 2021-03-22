# Private script to store the location of the credentials file as well as the location of the key file.

import os, sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")+'\\images'

    return os.path.join(base_path, relative_path)

def key():
    for file in os.listdir(keyLocation):
        baseFile, ext = os.path.splitext(file)
        if len(baseFile) == 44:
            return baseFile


keyLocation = resource_path('')
infoLocation = os.getcwd()+r'\info.txt'
try:
    os.remove(infoLocation.replace('.txt','decoded.txt'))
except:
    print('No decoded.txt file')