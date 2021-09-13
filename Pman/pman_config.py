import os
import configparser
config = configparser.ConfigParser()


class Config:

    def __init__(self, main):
        # Initialize the main window
        main.title("Password Manager First Time setup")
        main.geometry('600x175')
        self.mainframe = ttk.Frame(root, padding="8 8 20 20")

        # String displayed as the location of the info.txt
        self.info_location = StringVar()

        # Initialize config file variables
        try:
            self.info_location.set(config['locations']['info_location'])
        except KeyError:
            config.add_locations('locations')
            config['locations']['info_location'] = ""
        self.info_location.set("... Credentials File directory is not currently set ... !!!")

        # Build the main GUI frame
        self.mainframe.grid()
        self.mainframe.columnconfigure(0, weight=1, minsize=150)
        self.mainframe.columnconfigure(1, weight=1, minsize=150)
        self.mainframe.columnconfigure(2, weight=1, minsize=150)
        self.mainframe.columnconfigure(3, weight=1, minsize=150)

        # Add the Buttons and entries
        ttk.Label(self.mainframe, text='Location to store encrypted file')\
            .grid(row=0, column=1, columnspan=2)
        ttk.Label(self.mainframe, textvariable=self.info_location)\
            .grid(row=1, column=0, sticky=E, columnspan=3)
        ttk.Button(self.mainframe, text='Set location', command=self.load_new_file)\
            .grid(row=1, column=3, sticky=W)
        ttk.Button(self.mainframe, text='Save and close', command=self.set_config)\
            .grid(row=3, column=2, sticky=W)
        for child in self.mainframe.winfo_children():
            child.grid(padx=15, pady=15)

    def load_new_file(self):
        config_directory = filedialog.askdirectory(initialdir="/")
        if config_directory != "":
            config['locations']['info_location'] = config_directory
            self.info_location.set(config_directory)

    def set_config(self):
        if self.info_location.get() != "... Credentials File directory is not currently set ... !!!":
            with open(user_config, 'w') as f:
                config.write(f)
            root.destroy()
        else:
            on_closing()


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit without setting a file location?"):
        sys.exit(1)


# Look for the config file in the user's config directory
user_config_dir = os.path.expanduser("~") + r"\.config\Pman"
user_config = user_config_dir + r"\user_config.ini"

# If config file can't be read or is corrupt, then launch the first time setup GUI to create the file.
try:
    config.read(user_config)
    info_location = config['locations']['info_location']
except KeyError:    # Info location can't be read from config.ini
    config.add_section('locations')
    config['locations']['info_location'] = ""

    # Build directory if not already existing
    os.makedirs(user_config_dir, exist_ok=True)

    # Start Gui to create the config file
    from tkinter import *
    from tkinter import ttk
    from tkinter import filedialog
    from tkinter import messagebox
    root = Tk()
    Config(root)
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
else:
    print('Config File found at '+info_location)
