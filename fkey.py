# Private script to store the location of the credentials file as well as the location of the key file.
# Generates keys from the pin

import os
import sys
from shutil import copyfile
from cryptography.fernet import Fernet


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS+'\\images'
    except Exception:
        base_path = os.path.abspath(".")+'\\images'
    return os.path.join(base_path, relative_path)


def new_key():
    # Writes a new key file to the working directory
    newKey = Fernet.generate_key()
    with open(resource_path('') + newKey.decode() + '.txt', 'wb') as f:
        f.write(Fernet.generate_key()+Fernet.generate_key())


def key(pin):
    i = 0
    chars = len(pin)
    what = sum(bytes(pin, 'utf-8'))
    which = what % 10
    where = what % (44-chars)
    for file in os.listdir(keyLocation):
        fileName, ext = os.path.splitext(file)
        if len(fileName) == 44:
            if i == which:
                val = bytes(fileName[:where]+pin+fileName[where+chars:], 'utf-8')
            i += 1
    if i == 10:
        return val
    else:
        print('keys corrupted')


def decrypt(pin, data):
    return Fernet(key(pin)).decrypt(data)


def encrypt(pin, data):
    return Fernet(key(pin)).encrypt(data)


def backup():
    if not os.path.isfile(backupFile):
        try:
            copyfile(baseFile, backupFile)
        except FileNotFoundError:
            pass

with open(r'config.txt','r') as f:
    info_folder = f.read()

keyLocation = resource_path('')
baseFile = info_folder + r'\info.txt'
backupFile = info_folder + r'\info.bak'
decodedFile = info_folder + r'\info_PLAIN_TEXT.txt'

# Clean up decoded file from a previous run when fkey is imported.
# The file is a long term liability in case the user forgets to delete it or doesn't know it was written.
if os.path.isfile(decodedFile):
    os.remove(decodedFile)
