# Private script to store the location of the credentials file as well as the location of the key file.

import os, sys

def path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")+'\\images'

    return os.path.join(base_path, relative_path)

def key(pin):
    chars = len(pin)
    for file in os.listdir(keyLocation):
        baseFile, ext = os.path.splitext(file)
        if len(baseFile) == 44:
            start = sum(bytes(pin,'utf-8'))%(44-chars)
            return bytes(baseFile[:start]+pin+baseFile[start+chars:], 'utf-8')


keyLocation = path('')
fileLocation = os.getcwd()+r'\info.txt'
decodedFile = os.getcwd()+r'\info_decoded.txt'

if os.path.isfile(decodedFile):
    os.remove(decodedFile)
