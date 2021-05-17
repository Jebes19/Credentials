# Private script to store the location of the credentials file as well as the location of the key file.
# Generates keys from the code

import os
import sys
import fkey
from shutil import copyfile
from cryptography.fernet import Fernet

def new_key():
    # Writes a new key file to the working directory
    newKey = Fernet.generate_key()
    with open(resource_path('') + newKey.decode() + '.txt', 'wb') as f:
        f.write(Fernet.generate_key()+Fernet.generate_key())


def key(code):
    i = 0
    chars = len(code)
    what = sum(bytes(code, 'utf-8'))
    which = what % 10
    where = what % (44-chars)
    for file in os.listdir(keyLocation):
        fileName, ext = os.path.splitext(file)
        if len(fileName) == 44:
            if i == which:
                val = bytes(fileName[:where]+code+fileName[where+chars:], 'utf-8')
            i += 1
    if i == 10:
        return val
    else:
        print('keys corrupted')


def decrypt(code, data):
    return Fernet(key(code)).decrypt(data)


def encrypt(code, data):
    return Fernet(key(code)).encrypt(data)


def backup():
    try:
        copyfile(baseFile, backupFile)
        print('Info.txt backed up')
    except FileNotFoundError:
        print('No info.txt file in folder')

try:
    # PyInstaller creates a temp folder and then runs script in _MEIPASS
    base_path = sys._MEIPASS
    module_folder = os.getcwd()
except Exception:
    base_path = module_folder = os.path.dirname(fkey.__file__)

keyLocation = base_path+r'\images' #needs to be maintained as the fkey location
images = keyLocation

with open(module_folder+r'\config.txt', 'r') as file:
    info_folder = file.read()

baseFile = info_folder + r'\info.txt'
backupFile = info_folder + r'\info.bak'
decodedFile = info_folder + r'\info_PLAIN_TEXT.txt'


# Clean up decoded file from a previous run when fkey is imported.
# The file is a long term liability in case the user forgets to delete it or doesn't know it was written.
# Print plain text needs to be moved a GUI printout which isn't saved to the drive
if os.path.isfile(decodedFile):
    os.remove(decodedFile)
