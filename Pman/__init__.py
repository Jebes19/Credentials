from tkinter import *
from tkinter import ttk, filedialog
from tkinter import messagebox
import os
import shutil
import configparser


class config():

    def __init__(self, main):
        # Initialize the main window
        main.title("Password Manager First Time setup")
        main.columnconfigure(0, weight=1, minsize=400)
        main.rowconfigure(0, weight=1)

        # Initialize variables
        self.info_location = StringVar()
        self.info_location.set(r'C:\Users\usstwilk\PycharmProjects\Credentials\pman\__init__.py')
        self.build_page()

        #ttk.Label(self.mainframe, text='Location to store encrypted file').grid(row=0, column=0, columnspan=2)
        ttk.Label(self.mainframe, textvariable=self.info_location).grid(row=0, column=0)

        #ttk.Button(self.mainframe, text='Set location', command=None).grid(row=1, column=1)
        for child in self.mainframe.winfo_children():
            child.grid_configure(padx=50, pady=5)


    def config_file(self):
        config = configparser.ConfigParser()

        user_config_dir = os.path.expanduser("~") + "/.config/Pman"
        user_config = user_config_dir + "/user_config.ini"

        if not os.path.isfile(user_config):
            os.makedirs(user_config_dir, exist_ok=True)
            config.add_section('section')
            config['section']['setting_1'] = "hello"
            config['section']['setting_2'] = "goodbye"
            with open("default_config.ini", 'w') as f:
                config.write(f)
                shutil.copyfile("default_config.ini", user_config)
        else:
            print('File found')

        config.read(user_config)

        print(config['section']['setting_1'])
        print(config['section']['setting_2'])

    def build_page(self):
        self.mainframe = ttk.Frame(root, padding="3 3 12 12")
        self.mainframe.pack()
        self.mainframe.columnconfigure(0, weight=1, minsize=20)
        self.mainframe.columnconfigure(1, weight=1, minsize=180)
        self.mainframe.columnconfigure(2, weight=1, minsize=180)
        self.mainframe.columnconfigure(3, weight=1, minsize=20)
        self.mainframe.rowconfigure(10, weight=1, minsize=20)

    def set_info_location(self):
        res = messagebox.askquestion('askquestion', 'Do you like cats?')
        if res == 'yes':
            messagebox.showinfo('Response', 'You like Cats')
        elif res == 'no':
            messagebox.showinfo('Response', 'You must be a dog fan.')
        else:
            messagebox.showwarning('error', 'Something went wrong!')



root = Tk()
config(root)
root.mainloop()

