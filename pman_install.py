# Script just allows pyinstaller to grab the pman package.
import os

if not os.path.isfile(os.path.expanduser("~") + r"\.config\Pman\user_config.ini"):
    print("Config file not found, run pman_config.exe")
    exit()

from pman import pman_GUI

