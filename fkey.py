# Private script to store the location of the credentials file as well as the location of the key file.

import os

keyLocation = r'C:\Users\usstwilk\Documents\Useful docs\info'
infoLocation = r'C:\Users\usstwilk\Documents\Useful docs\info\info.txt'

def key():
    for file in os.listdir(keyLocation):
        baseFile, ext = os.path.splitext(file)
        if len(baseFile) == 44:
            return baseFile

