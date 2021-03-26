# Private script to store the location of the credentials file as well as the location of the key file.
# Generates keys from the pin

import os
import sys
import shutil


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
        fileName, ext = os.path.splitext(file)
        if len(fileName) == 44:
            start = sum(bytes(pin, 'utf-8')) % (44-chars)
            return bytes(fileName[:start]+pin+fileName[start+chars:], 'utf-8')


keyLocation = path('')
baseFile = os.getcwd() + r'\info.txt'
backupFile = os.getcwd()+r'\info.bak'
decodedFile = os.getcwd()+r'\info_decoded.txt'

if os.path.isfile(decodedFile):
    os.remove(decodedFile)

if not os.path.isfile(backupFile):
    try:
        shutil.copyfile(baseFile, backupFile)
    except FileNotFoundError:
        pass
