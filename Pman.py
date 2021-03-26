# InterfaceGUI to interact with user.py

from tkinter import *
from tkinter import ttk, filedialog
import cryptography
import user
import webbrowser

VERSION = '1.2.4'


# noinspection PyAttributeOutsideInit,PyUnresolvedReferences
class GUI:

    # Methods to create the GUI, and recreate it when moving to different pages.
    def __init__(self, main):

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
        self.status = StringVar('')
        self.allMatches = iter(())
        self.last = None
        self.index = None

        # Import images
        self.copy_image = PhotoImage(file=user.fkey.path('copy.png'), height=30, width=30)
        self.settings_image = PhotoImage(file=user.fkey.path('settings.png'), height=30, width=30)
        self.open_image = PhotoImage(file=user.fkey.path('open.png'), height=30, width=30)
        self.password_image = PhotoImage(file=user.fkey.path('eye2.png'), height=30, width=30)
        self.newFile_image = PhotoImage(file=user.fkey.path('NewFile.png'), height=30, width=30)

        # Import standard window configuration
        self.build_page()
        self.status_label.grid(column=2, row=1, columnspan=2, sticky=E)

        # Version label
        ttk.Label(self.mainframe, text="Password Manager by Taylor Wilkin, Version " + VERSION)\
            .grid(column=1, row=10, columnspan=3, sticky=N)

        # Pin Entry label.
        ttk.Label(self.mainframe, text="PIN for Credentials file")\
            .grid(column=1, row=0, columnspan=2, sticky=N)

        # Pin button and entry
        self.pin_button = ttk.Button(self.mainframe, text='PIN', command=self.submit_pin)
        self.pin_button.grid(column=1, row=1, sticky=E)
        self.pin_entry = ttk.Entry(self.mainframe, width=15, textvariable=self.currentPin, show='*')
        self.pin_entry.grid(column=2, row=1, sticky=W)
        self.pin_entry.bind("<Return>", lambda event: self.submit_pin())
        self.pin_entry.bind("<Button-1>", lambda event: self.currentPin.set(''))
        self.pin_entry.focus()

        # New File Button
        ttk.Button(self.mainframe, text="New File", image=self.newFile_image, takefocus=0,
                   command=self.popup_select_new_file) \
            .grid(column=0, row=0, rowspan=2, sticky=W)

        self.padding()

    def main_entries_page(self):
        self.mainframe.destroy()
        self.build_page()

        # Search Entry
        search_entry = ttk.Entry(self.mainframe, width=30, textvariable=self.search)
        search_entry.grid(column=2, row=0, sticky=W)
        search_entry.bind("<Return>", lambda event: self.get_login(self.search.get()))
        search_entry.bind("<Button-1>", lambda event: self.search.set(''))
        search_entry.focus()
        # Search Button
        ttk.Button(self.mainframe, text='Search',
                   command=lambda: self.get_login(self.search.get())) \
            .grid(column=1, row=0, sticky=E)
        # Options Button
        ttk.Button(self.mainframe, text="Options", image=self.settings_image, takefocus=0,
                   command=self.options_page) \
            .grid(column=0, row=0, sticky=W)
        # Status labels
        ttk.Label(self.mainframe, text="Status") \
           .grid(column=1, row=1, sticky=E)
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
        ttk.Entry(self.mainframe, textvariable=self.site) \
            .grid(column=1, row=2, columnspan=2, sticky=(W, E))
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
                                   command=lambda: self.status.set('Double click "Delete" to confirm'))
        delete_button.grid(column=1, row=9, sticky=W)
        delete_button.bind('<Double-Button-1>', lambda event: self.change_entry('delete', self.site))
        ttk.Button(self.mainframe, text="Update",
                   command=lambda: self.change_entry('update', self.site)) \
            .grid(column=2, row=9, sticky=W)
        ttk.Button(self.mainframe, text="Add",
                   command=lambda: self.change_entry('add', self.site)) \
            .grid(column=2, row=9, sticky=E)

        self.padding()

    def options_page(self):
        self.mainframe.destroy()
        self.build_page()

        # Build out rows to fixed size
        self.mainframe.rowconfigure(1, weight=1, minsize=50)
        self.mainframe.rowconfigure(2, weight=1, minsize=50)
        self.mainframe.rowconfigure(3, weight=1, minsize=50)
        self.mainframe.rowconfigure(4, weight=1, minsize=50)
        self.mainframe.rowconfigure(5, weight=1, minsize=50)
        self.mainframe.rowconfigure(6, weight=1, minsize=50)

        # Options Button, now returns to the Main Entries window.
        ttk.Button(self.mainframe, text="Options", image=self.settings_image,
                   command=self.main_entries_page) \
            .grid(column=0, row=0, sticky=W)

        # Status labels
        ttk.Label(self.mainframe, text="Status") \
           .grid(column=1, row=0, sticky=W)
        self.status_label.grid(column=1, row=0, columnspan=2, sticky=E)

        # Load file buttons
        ttk.Button(self.mainframe, text='Load New File', width=50,
                   command=self.popup_select_new_file) \
            .grid(column=1, row=2, columnspan=2, rowspan=1, sticky=NS)
        ttk.Button(self.mainframe, text='Load Backup File', width=50,
                   command=self.load_backup) \
            .grid(column=1, row=1, columnspan=2, rowspan=1, sticky=NS)
        # Write all credentials
        ttk.Button(self.mainframe, text='Print plain text of all Credentials', width=50,
                   command=lambda: user.write_file(self.currentPin.get(), 'N', 'decoded')) \
            .grid(column=1, row=3, columnspan=2, rowspan=2, sticky=NS)
        # Change pin
        ttk.Button(self.mainframe, text='Change Pin',
                   command=self.change_pin, width=50) \
            .grid(column=1, row=5, columnspan=2, rowspan=2, sticky=NS)

        # Change pin labels and entries
        ttk.Label(self.mainframe, text="New Pin") \
            .grid(column=0, row=7, sticky=W)
        ttk.Label(self.mainframe, text="Pins must match") \
            .grid(column=2, row=8, sticky=W)
        ttk.Entry(self.mainframe, textvariable=self.pin1) \
            .grid(column=0, row=7, columnspan=2, sticky=E)
        ttk.Entry(self.mainframe, textvariable=self.pin2) \
            .grid(column=2, row=7, columnspan=2, sticky=W)

        self.padding()

    def build_page(self):
        # Builds the elements common to all the main pages
        self.mainframe = ttk.Frame(root, padding="3 3 12 12")
        self.mainframe.pack()
        self.mainframe.columnconfigure(0, weight=1, minsize=20)
        self.mainframe.columnconfigure(1, weight=1, minsize=180)
        self.mainframe.columnconfigure(2, weight=1, minsize=180)
        self.mainframe.columnconfigure(3, weight=1, minsize=20)
        self.mainframe.rowconfigure(10, weight=1, minsize=20)
        self.status_label = ttk.Label(self.mainframe, textvariable=self.status)

    def padding(self):
        for child in self.mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def popup_select_new_file(self):
        top = self.top = Toplevel(root)
        Label(top, text="PIN to encode File").pack(padx=10, pady=5)
        entry = Entry(top, justify='center')
        entry.pack(padx=10, pady=5)
        entry.bind("<Return>", lambda event: self.load_new_file(entry.get()))
        entry.focus()
        Button(top, text='Ok', command=lambda: self.load_new_file(entry.get())).pack(padx=10, pady=5)

    # Methods to interact with the various entry boxes and buttons.

    def submit_pin(self):
        # Primarily checks the pin against the file but also reloads the credsList used by all the User methods
        try:
            user.read_file(self.currentPin.get())
        except cryptography.fernet.InvalidToken:
            self.status.set('Invalid PIN')
            return
        except FileNotFoundError:
            self.status.set('No File found')
            return
        self.status.set('Ready to Search')
        self.main_entries_page()

    def get_login(self, search):
        # Takes search input and checks for a matched login. Returns a generator to retrieve all matches
        self.update_entries(['', '', '', '', self.status.get()])    # Clears entries but not Status box
        if search == '':
            return
        if self.last != search:        # New searches won't match the "last" search nor will end of list
            self.allMatches = user.credentials('login', search, self.currentPin.get())
        try:
            next_entry = next(self.allMatches)
        except StopIteration:               # End of list if no matches or no more matches
            if self.last != search:
                next_entry = ['', '', '', '', 'No matches found', -1]
            else:
                next_entry = ['', '', '', '', 'End of matches', -1]
            search = ''                # Forces next search to start over
        self.last = search             # If try succeeds, self.last will match search entry
        self.update_entries(next_entry)     # Successful search returns the list of strings
        self.index = next_entry[5]          # Stores list index for the currently displayed search results

    def update_entries(self, credentials):
        # Update entries with new values which can be empty to clear the boxes or will be the return from a search.
        self.site.set(credentials[0])
        self.user.set(credentials[1])
        self.password.set(credentials[2])
        self.comments.set(credentials[3])
        self.status.set(credentials[4])

    def change_entry(self, function, site):
        # Use the existing entry values to add, edit or delete the credentials to or from the list.
        site = site.get()
        if site == '':
            return None
        new = [self.site.get(), self.user.get(), self.password.get(), self.comments.get()]
        changed = user.credentials(function, site, self.currentPin.get(), new, self.index, 'DELETE')
        self.update_entries(changed)    # Updates entries from the return of the previous call

    def password_show(self):
        # Show password, change image of button and remap command to password_hide
        self.password_entry['show'] = ''
        self.password_image['file'] = user.fkey.path('eye_closed.png')
        self.show_password['command'] = self.password_hide

    def password_hide(self):
        # Hide password, change image of button and remap command to password_show
        self.password_entry['show'] = '*'
        self.password_image['file'] = user.fkey.path('eye1.png')
        self.show_password['command'] = self.password_show

    def to_clip(self, button):
        # Copy contents of the corresponding entry to clipboard and tell the user it is done
        root.clipboard_clear()
        root.clipboard_append(button.get())
        self.status.set(button)

    def load_new_file(self, entry):
        # Load all new credentials from a csv formatted file
        user.new_file(filedialog.askopenfile(initialdir="/").name, entry)
        self.currentPin.set(entry)      # Reset the global pin to use the new pin for files
        self.top.destroy()
        self.submit_pin()               # Reloads the file from the new pin
        self.search.set('*all*')        # Start the search box with *all* after adding a new file

    def load_backup(self):
        # Reload the backup in case of a mistake in the file.
        user.read_file(self.currentPin.get(), user.fkey.backupFile)
        self.submit_pin()
        self.update_entries(['', '', '', '', 'Backup File loaded', -1])
        self.search.set('*all*')

    def change_pin(self):
        # Compare pins entered and then encrypting the credsList with the new key
        pin1 = self.pin1.get()
        pin2 = self.pin2.get()
        try:
            self.status.set(user.change_pin(pin1, pin2))     # Changes pin if matched and valid pins
        except cryptography.fernet.InvalidToken:
            self.status.set('Invalid PIN')
            return
        self.currentPin.set(pin1)
        self.pin1.set('')
        self.pin2.set('')


root = Tk()
GUI(root)
root.mainloop()
