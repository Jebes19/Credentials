# Private script to store the location of the credentials file as well as the location of the key file.
# Generates keys from the code

import os
import sys
from shutil import copyfile
from cryptography.fernet import Fernet
from tkinter import *
from tkinter import ttk, filedialog
import configparser
config = configparser.ConfigParser()


def new_key():
    # Writes a new key file to the working directory
    newKey = Fernet.generate_key()
    with open(base_path + newKey.decode() + '.txt', 'wb') as f:
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


class Config():

    def __init__(self, main):
        # Initialize the main window
        main.title("Password Manager First Time setup")
        main.geometry('600x200')

        self.info_location = StringVar()

        # Initialize config file variables
        try:
            self.info_location.set(config['section']['info_location'])
        except KeyError:
            config.add_section('section')
            config['section']['info_location'] = "... Not currently set ... !!!"
        self.info_location.set(config['section']['info_location'])

        # Build the main GUI frame
        self.build_page()
        ttk.Label(self.mainframe, text='Location to store encrypted file')\
            .grid(row=0, column=1, columnspan=2)
        ttk.Label(self.mainframe, textvariable=self.info_location)\
            .grid(row=1, column=0, sticky=E, columnspan=3)
        ttk.Button(self.mainframe, text='Set location', command=self.load_new_file)\
            .grid(row=1, column=3, sticky=W)
        ttk.Button(self.mainframe, text='Save', command=self.set_config)\
            .grid(row=3, column=3, sticky=W)
        for child in self.mainframe.winfo_children():
            child.grid(padx=15, pady=5)

    def build_page(self):
        self.mainframe = ttk.Frame(root, padding="8 8 20 20")
        self.mainframe.grid()
        self.mainframe.columnconfigure(0, weight=1, minsize=150)
        self.mainframe.columnconfigure(1, weight=1, minsize=150)
        self.mainframe.columnconfigure(2, weight=1, minsize=150)
        self.mainframe.columnconfigure(3, weight=1, minsize=150)

    def load_new_file(self):
        self.info_location.set(filedialog.askdirectory(initialdir="/"))
        config['section']['info_location'] = self.info_location.get()

    def set_config(self):
        with open(user_config, 'w') as f:
            config.write(f)
        root.destroy()

user_config_dir = os.path.expanduser("~") + "\.config\Pman"
user_config = user_config_dir + r"\user_config.ini"
config.read(user_config)

# If file does not exist, then launch the first time setup GUI to create the file.
if not os.path.isfile(user_config):
    os.makedirs(user_config_dir, exist_ok=True)
    root = Tk()
    Config(root)
    root.mainloop()
else:
    print('File found')

try:
    # PyInstaller creates a temp folder and then runs script in _MEIPASS
    base_path = sys._MEIPASS
    module_folder = os.path.abspath(os.pardir)
except Exception:
    print("No exe detected, running script in python")
    base_path = module_folder = os.path.dirname(__file__)

keyLocation = base_path+r'\images' #needs to be maintained as the fkey location
images = keyLocation

info_folder = config['section']['info_location']

baseFile = info_folder + r'\info.txt'
backupFile = info_folder + r'\info.bak'
decodedFile = info_folder + r'\info_PLAIN_TEXT.txt'

# Clean up decoded file from a previous run when fkey is imported.
# The file is a long term liability in case the user forgets to delete it or doesn't know it was written.
# Print plain text needs to be moved a GUI printout which isn't saved to the drive
if os.path.isfile(decodedFile):
    os.remove(decodedFile)
