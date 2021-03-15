import os
def key():
    for file in os.listdir(r'C:\Users\usstwilk\Documents\Useful docs\info'):
        baseFile, ext = os.path.splitext(file)
        if len(baseFile) == 44:
            return baseFile

