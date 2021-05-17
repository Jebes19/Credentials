from tkinter import *
from tkinter import ttk, filedialog
import os
import configparser
import pman_GUI

config = configparser.ConfigParser()

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

# Define config folder in user/.config/Pman and file in folder as /user_config.ini
user_config_dir = os.path.expanduser("~") + "/.config/Pman"
user_config = user_config_dir + "/user_config.ini"
config.read(user_config)

# If file does not exist, then launch the first time setup GUI to create the file.
if not os.path.isfile(user_config):
    os.makedirs(user_config_dir, exist_ok=True)
    root = Tk()
    Config(root)
    root.mainloop()
else:
    print('Config File found')


