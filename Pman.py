# InterfaceGUI to interact with user.py
from tkinter import *
from tkinter import ttk, filedialog

import cryptography

import user, webbrowser
version = '1.2.0'


# noinspection PyAttributeOutsideInit,PyUnusedLocal
class CredentialsGUI:

    # Methods to create the GUI, and recreate it when moving to different pages.
    def __init__(self, main):
        # build out standard window
        self.build_page()

        # Initialize the main window
        main.title("Password Manager")
        main.columnconfigure(0, weight=1, minsize=400)
        main.rowconfigure(0, weight=1)

        # Initialize all the variables
        self.currentPin = StringVar()
        self.site = StringVar(name='Site copied to clipboard')
        self.user = StringVar(name='User copied to clipboard')
        self.password = StringVar(name='Password copied to clipboard')
        self.comments = StringVar()
        self.search = StringVar()
        self.pin1 = StringVar()
        self.pin2 = StringVar()
        self.allMatches = iter(())
        self.last = None
        self.index = None       # Index of the current search

        # Import images
        self.copy_image = PhotoImage(file=user.fkey.path('copy.png'), height=30, width=30)
        self.settings_image = PhotoImage(file=user.fkey.path('settings.png'), height=30, width=30)
        self.open_image = PhotoImage(file=user.fkey.path('open.png'), height=30, width=30)
        self.password_image = PhotoImage(file=user.fkey.path('eye2.png'), height=30, width=30)
        self.newFile_image = PhotoImage(file=user.fkey.path('NewFile.png'), height=30, width=30)

        # Version label
        ttk.Label(self.mainframe, text="Password Manager by Taylor Wilkin, Version "+version)\
            .grid(column=1, row=10, columnspan=3, sticky=N)

        # Pin Entry label and pin submission label.
        ttk.Label(self.mainframe, text="PIN for Credentials file")\
            .grid(column=1, row=0, columnspan=2, sticky=N)

        self.status_label = ttk.Label(self.mainframe, text='')
        self.status_label.grid(column=2, row=1, columnspan=2, sticky=E)

        # Pin button and entry
        self.pin_button = ttk.Button(self.mainframe, text='PIN',
                                     command=self.submit_pin)
        self.pin_button.grid(column=1, row=1, sticky=E)
        self.pin_entry = ttk.Entry(self.mainframe, width=15, textvariable=self.currentPin, show='*')
        self.pin_entry.grid(column=2, row=1, sticky=W)
        self.pin_entry.bind("<Return>", lambda event: self.submit_pin())
        self.pin_entry.bind("<Button-1>", lambda event: self.currentPin.set(''))
        self.pin_entry.focus()

        # New File Button
        ttk.Button(self.mainframe, text="New File", image=self.newFile_image, takefocus=0,
                   command=self.popup_load_new_file) \
            .grid(column=0, row=0, rowspan=2, sticky=W)

        self.padding()

    def main_entries_page(self):
        self.mainframe.destroy()
        self.build_page()

        # Search Entry
        self.search_entry = ttk.Entry(self.mainframe, width=30, textvariable=self.search)
        self.search_entry.grid(column=2, row=0, sticky=W)
        self.search_entry.bind("<Return>", self.get_login)
        self.search_entry.bind("<Button-1>", lambda event: self.search.set(''))
        # Search Button
        ttk.Button(self.mainframe, text='Search',
                   command=self.get_login) \
            .grid(column=1, row=0, sticky=E)
        # Options Button
        ttk.Button(self.mainframe, text="Options", image=self.settings_image, takefocus=0,
                   command=self.options_page) \
            .grid(column=0, row=0, sticky=W)
        # Status labels
        ttk.Label(self.mainframe, text="Status") \
           .grid(column=1, row=1, sticky=E)
        self.status_label = ttk.Label(self.mainframe, text='Ready to Search')
        self.status_label.grid(column=2, row=1, sticky=W)
        # Site label, button, entry and site open button
        ttk.Label(self.mainframe, text="Site") \
            .grid(column=1, row=1, columnspan=2, sticky=(W, S))
        ttk.Button(self.mainframe, image=self.copy_image, takefocus=0,
                   command=lambda: self.to_clip(self.site)) \
            .grid(column=3, row=2, sticky=W)
        ttk.Button(self.mainframe, image=self.open_image, takefocus=0,
                   command=lambda: webbrowser.open(self.site.get(), new=2),) \
            .grid(column=0, row=2, sticky=E)
        site_entry = ttk.Entry(self.mainframe, textvariable=self.site)
        site_entry.grid(column=1, row=2, columnspan=2, sticky=(W, E))
        # Username label, button, and entry
        ttk.Label(self.mainframe, text="Username") \
            .grid(column=1, row=3, sticky=(W, S))
        ttk.Entry(self.mainframe, textvariable=self.user) \
            .grid(column=1, row=4, columnspan=2, sticky=(W, E))
        ttk.Button(self.mainframe, image=self.copy_image, takefocus=0,
                   command=lambda: self.to_clip(self.user)) \
            .grid(column=3, row=4, sticky=W)
        # Password label, button, entry, and show password button
        ttk.Label(self.mainframe, text="Password") \
            .grid(column=1, row=5, sticky=(W, S))
        ttk.Button(self.mainframe, image=self.copy_image, takefocus=0,
                   command=lambda: self.to_clip(self.password)) \
            .grid(column=3, row=6, sticky=W)
        self.password_entry = ttk.Entry(self.mainframe, textvariable=self.password, show="*")
        self.password_entry.grid(column=1, row=6, columnspan=2, sticky=(W, E))
        self.show_password = ttk.Button(self.mainframe, takefocus=0, image=self.password_image,
                                        command=self.password_show)
        self.show_password.grid(column=0, row=6, sticky=W)
        # Comments label and entry
        ttk.Label(self.mainframe, text="Comments") \
            .grid(column=1, columnspan=2, row=7, sticky=(W, S))
        ttk.Entry(self.mainframe, textvariable=self.comments) \
            .grid(column=1, row=8, columnspan=2, sticky=(W, E))
        # Add, Update and Delete buttons
        delete_button = ttk.Button(self.mainframe, text="Delete",
                                   command=None)
        delete_button.grid(column=1, row=9, sticky=W)
        delete_button.bind('<Double-Button-1>', lambda event: self.change_entry('delete', self.site))
        delete_button.bind('<Button-1>', lambda event: self.update_status('Double click "Delete" to confirm'))
        ttk.Button(self.mainframe, text="Update",
                   command=lambda: self.change_entry('update', self.site)) \
            .grid(column=2, row=9, sticky=W)
        ttk.Button(self.mainframe, text="Add",
                   command=lambda: self.change_entry('add', self.site)) \
            .grid(column=2, row=9, sticky=E)

        self.padding()

        self.search_entry.focus()

    def options_page(self):
        self.mainframe.destroy()
        self.build_page()

        # Options Button, now returns to the Main Entries window.
        ttk.Button(self.mainframe, text="Options", image=self.settings_image,
                   command=self.main_entries_page) \
            .grid(column=0, row=0, sticky=W)

        # Status labels
        ttk.Label(self.mainframe, text="Status") \
           .grid(column=1, row=0, sticky=W)
        self.status_label = ttk.Label(self.mainframe, text='Ready to Search', wraplength=300)
        self.status_label.grid(column=1, row=0, columnspan=2, sticky=E)

        # Functional buttons
        # Load file buttons
        ttk.Button(self.mainframe, text='Load New File', width=50,
                   command=self.popup_load_new_file) \
            .grid(column=1, row=2, columnspan=2, rowspan=1, sticky='ns')
        ttk.Button(self.mainframe, text='Load Backup File', width=50,
                   command=self.load_backup) \
            .grid(column=1, row=1, columnspan=2, rowspan=1, sticky='ns')
        # Write all credentials
        ttk.Button(self.mainframe, text='Print plain text of all Credentials', width=50,
                   command=lambda: user.write_file(self.currentPin.get(), 'N', 'decoded')) \
            .grid(column=1, row=3, columnspan=2, rowspan=2, sticky='ns')
        # Change pin
        ttk.Button(self.mainframe, text='Change Pin',
                   command=self.change_pin, width=50) \
            .grid(column=1, row=5, columnspan=2, rowspan=2, sticky='ns')

        # Change pin labels and entries
        ttk.Label(self.mainframe, text="New Pin") \
            .grid(column=0, row=7, sticky=W)
        pin1_entry = ttk.Entry(self.mainframe, textvariable=self.pin1)
        pin1_entry.grid(column=0, row=7, columnspan=2, sticky=E)
        pin1_entry.bind("<Button-1>", lambda event: self.pin1.set(''))

        ttk.Label(self.mainframe, text="Pins must match") \
            .grid(column=2, row=8, sticky=W)
        pin2_entry = ttk.Entry(self.mainframe, textvariable=self.pin2)
        pin2_entry.grid(column=2, row=7, columnspan=2, sticky=W)
        pin2_entry.bind("<Button-1>", lambda event: self.pin2.set(''))

        self.mainframe.rowconfigure(1, weight=1, minsize=50)
        self.mainframe.rowconfigure(2, weight=1, minsize=50)
        self.mainframe.rowconfigure(3, weight=1, minsize=50)
        self.mainframe.rowconfigure(4, weight=1, minsize=50)
        self.mainframe.rowconfigure(5, weight=1, minsize=50)
        self.mainframe.rowconfigure(6, weight=1, minsize=50)

        self.padding()

    def build_page(self):
        self.mainframe = ttk.Frame(root, padding="3 3 12 12")
        self.mainframe.pack()
        self.mainframe.columnconfigure(0, weight=1, minsize=20)
        self.mainframe.columnconfigure(1, weight=1, minsize=180)
        self.mainframe.columnconfigure(2, weight=1, minsize=180)
        self.mainframe.columnconfigure(3, weight=1, minsize=20)
        self.mainframe.rowconfigure(10, weight=1, minsize=20)

    def popup_load_new_file(self):
        top = self.top = Toplevel(root)
        Label(top, text="PIN to encode File").pack(padx=10, pady=5)
        entry = Entry(top, justify='center')
        entry.pack(padx=10, pady=5)
        Button(top, text='Ok', command=lambda: self.load_new_file(entry.get())).pack(padx=10, pady=5)
        entry.bind("<Return>", lambda event: self.load_new_file(entry.get()))
        entry.focus()

    def padding(self):
        for child in self.mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

    # Methods to interact with the various entry boxes and buttons.

    def update_status(self, text):
        # temporary method until it can be refactored
        self.status_label['text'] = text

    def submit_pin(self):
        # Primarily checks the pin against the file but also reloads the credsList used by all the User methods
        try:
            user.read_file(self.currentPin.get())
        except cryptography.fernet.InvalidToken:
            self.status_label['text'] = 'Invalid PIN'
            return
        except FileNotFoundError:
            self.status_label['text'] = 'No File found'
            return
        self.main_entries_page()

    def get_login(self, *event):
        # Takes Search input and checks for a matched login. Returns a generator to retrieve all matches
        self.update_entries(['', '', '', '', self.status_label['text']])    # Clears entries but not Status box
        searchEntry = self.search.get()
        if searchEntry == '':
            return
        if self.last != searchEntry:        # New searches won't match the last search nor will end of list
            self.allMatches = user.Credentials('login', searchEntry, self.currentPin.get())
        try:
            next_entry = next(self.allMatches)
        except StopIteration:               # End of list of no matches
            if self.last != searchEntry:
                next_entry = ['', '', '', '', 'No matches found', -1]
            else:
                next_entry = ['', '', '', '', 'End of matches', -1]
            searchEntry = ''                # Forces next search to start over
        self.last = searchEntry             # If try succeeds, self.last will match search entry
        self.update_entries(next_entry)     # Successful search returns the list of strings           # Prep for next search in case it is identical and trigger the next entry
        self.index = next_entry[5]         # Set the i value for the currently displayed search results

    def xxxget_login(self, *event):
        # Takes Search input and checks for a matched login. Returns a generator to retrieve all matches
        self.update_entries(['', '', '', '', self.status_label['text']])    # Clears entries but not Status box
        searchEntry = self.search.get()
        if searchEntry == '':
            return
        if self.last != searchEntry:        # New searches won't match the last search
            self.allMatches = iter(())      # Empty generator object
        try:
            next_entry = next(self.allMatches)
        except StopIteration:               # If no more matches or upon first search
            self.allMatches = user.Credentials('login', searchEntry, self.currentPin.get())
            try:                            # Will reset the search to the top of the list unless there are no matches
                next_entry = next(self.allMatches)
            except StopIteration:
                next_entry = ['', '', '', '', 'No matches found', -1]
        self.update_entries(next_entry)    # Successful search returns the list of strings
        self.last = searchEntry             # Prep for next search in case it is identical and trigger the next entry
        self.index = next_entry[5]         # Set the i value for the currently displayed search results

    def update_entries(self, credentials):
        # Update entries with new values which can be empty to clear the boxes or will be the return from a search.
        self.site.set(credentials[0])
        self.user.set(credentials[1])
        self.password.set(credentials[2])
        self.comments.set(credentials[3])
        self.update_status(credentials[4])

    def change_entry(self, function, site):
        # Use the existing entry values to add, edit or delete the credentials to or from the list.
        site = site.get()
        if site == '':
            return None
        new = [self.site.get(), self.user.get(), self.password.get(), self.comments.get()]
        changed = user.Credentials(function, site, self.currentPin.get(), new, self.index, 'DELETE')
        self.update_entries(changed)    # Updates entries from the return from previous call

    def password_show(self):
        self.password_entry['show'] = ''
        self.password_image['file'] = user.fkey.path('eye_closed.png')
        self.show_password['command'] = self.password_hide

    def password_hide(self):
        self.password_entry['show'] = '*'
        self.password_image['file'] = user.fkey.path('eye1.png')
        self.show_password['command'] = self.password_show

    def to_clip(self, button):
        root.clipboard_clear()
        root.clipboard_append(button.get())
        self.update_status(button)

    def load_new_file(self, entry):
        user.newFile(filedialog.askopenfile(initialdir="/").name, entry)
        self.currentPin.set(entry)        # Reset the global pin to use the new pin for files
        self.top.destroy()
        self.submit_pin()           # Reloads the file from the new pin
        self.search.set('*all*')    # Start the search box with *all* after adding a new file

    def load_backup(self):
        user.read_file(self.currentPin.get(), user.fkey.backupFile)
        self.submit_pin()
        self.update_entries(['', '', '', '', 'Backup File loaded', -1])
        self.search.set('*all*')

    def change_pin(self):
        pin1 = self.pin1.get()
        pin2 = self.pin2.get()
        try:
            user.changePin(pin1, pin2)
        except cryptography.fernet.InvalidToken:
            self.update_status('Invalid PIN')
            return
        self.currentPin.set(pin1)
        self.pin1.set('')
        self.pin2.set('')
        self.update_status('Pin Changed')


root = Tk()
CredentialsGUI(root)
root.mainloop()
