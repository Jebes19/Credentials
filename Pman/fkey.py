# Private script to store the location of the credentials file as well as the location of the key file.
# Generates keys from the code

import base64
import os
import sys
import configparser
from shutil import copyfile

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def new_key():
    # Writes a new key file to the working directory
    # This should probably be incorporated with the setup function
    newKey = Fernet.generate_key()
    with open(base_path + newKey.decode() + '.txt', 'wb') as f:
        f.write(Fernet.generate_key()+Fernet.generate_key())

def key(password):
    # Takes the password given and returns the hash
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salter(password),
        iterations=100000,
        )
    key = base64.urlsafe_b64encode(kdf.derive(bytes(password,'utf-8')))
    return(key)

def salter(hash):
    # Takes a code and returns a string of bytes 44 characters long which is used as the key for the info file
    i = 0
    chars = len(hash)
    what = sum(bytes(hash, 'utf-8'))
    which = what % 10
    where = what % (44-chars)
    for file in os.listdir(keyLocation):
        fileName, ext = os.path.splitext(file)
        if len(fileName) == 44:
            if i == which:
                val = bytes(fileName[:where]+hash+fileName[where+chars:], 'utf-8')
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

# Locate and use the user's configuration
user_config_file_location = os.path.expanduser("~") + r"\.config\Pman\user_config.ini"
this_config = configparser.ConfigParser()
this_config.read(user_config_file_location)

# Try and except to determine if the script is running as .exe or as a python script.
try:
    # PyInstaller creates a temp folder and then runs script in _MEIPASS
    base_path = sys._MEIPASS
    module_folder = os.path.abspath(os.pardir)
except Exception:
    print("No exe detected, running script in python")
    base_path = module_folder = os.path.dirname(__file__)

keyLocation = base_path+r'\images' # keyLocation needs to be maintained as the fkey location
images = keyLocation

info_folder = this_config['locations']['info_location']
baseFile = info_folder + r'\info.txt'
backupFile = info_folder + r'\info.bak'
decodedFile = info_folder + r'\info_PLAIN_TEXT.txt'

# Clean up decoded file from a previous run when fkey is imported.
# The file is a long term liability in case the user forgets to delete it or doesn't know it was written.
# Print plain text needs to be moved a GUI printout which isn't saved to the drive
if os.path.isfile(decodedFile):
    os.remove(decodedFile)
