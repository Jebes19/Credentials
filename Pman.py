# InterfaceGUI to interact with user.py
from tkinter import *
from tkinter import ttk, filedialog
import user, webbrowser, os, sys

# Map the images to either the local directory or the temp directory created whe the exe runs.
copy_img = user.fkey.path('copy.png')
settings_img = user.fkey.path('settings.png')
open_img = user.fkey.path('open.png')
eye1_img = user.fkey.path('eye1.png')
eye2_img = user.fkey.path('eye2.png')
newFile_img = user.fkey.path('NewFile.png')
eyeclosed_img = user.fkey.path('eye_closed.png')

class CredentialsGUI:

    # Methods to create the GUI, and recreate it when moving to different pages.
    def __init__(self, root):
        # build out standard window
        self.buildPage()

        # Initialize the main window
        root.title("Pman")
        root.columnconfigure(0, weight=1, minsize=400)
        root.rowconfigure(0, weight=1)

        # Initialize all the variables
        self.pinEntry = StringVar()
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
        self.copy_image = PhotoImage(file=copy_img, height=30, width=30)
        self.settings_image = PhotoImage(file=settings_img, height=30, width=30)
        self.open_image = PhotoImage(file=open_img, height=30, width=30)
        self.password_image = PhotoImage(file=eye2_img, height=30, width=30)
        self.newFile_image = PhotoImage(file=newFile_img, height=30, width=30)

        # Version label
        ttk.Label(self.mainframe, text="Password Manager by Taylor Wilkin, Version 1.0.0")\
            .grid(column=1, row=10, columnspan=3, sticky=N)

        # Pin Entry label and pin submission label.
        ttk.Label(self.mainframe, text="PIN for Credentials file")\
            .grid(column=1, row=0, columnspan=2, sticky=N)

        self.submit_failed_label = ttk.Label(self.mainframe, text="")
        self.submit_failed_label.grid(column=2, row=1, columnspan=2, sticky=E)

        # Pin button and entry
        self.pin_button = ttk.Button(self.mainframe, text='PIN',
                                     command=self.submitPin)
        self.pin_button.grid(column=1, row=1, sticky=E)
        self.pin_entry = ttk.Entry(self.mainframe, width=15, textvariable=self.pinEntry, show='*')
        self.pin_entry.grid(column=2, row=1, sticky=W)
        self.pin_entry.bind("<Return>", lambda event: self.submitPin())
        self.pin_entry.bind("<Button-1>", lambda event: self.clearSearch(entry=self.pinEntry))
        self.pin_entry.focus()

        # New File Button
        ttk.Button(self.mainframe, text="New File", image=self.newFile_image, takefocus=0,
                   command=self.loadNewFilepopup) \
            .grid(column=0, row=0, rowspan=2, sticky=W)

        self.padding()

    def mainEntriesPage(self):
        self.mainframe.destroy()
        self.buildPage()

        # Search Entry
        self.search_entry = ttk.Entry(self.mainframe, width=30, textvariable=self.search)
        self.search_entry.grid(column=2, row=0, sticky=W)
        self.search_entry.bind("<Return>", self.getLogin)
        self.search_entry.bind("<Button-1>", lambda event: self.clearSearch(entry=self.search))
        # Search Button
        ttk.Button(self.mainframe, text='Search',
                   command=self.getLogin) \
            .grid(column=1, row=0, sticky=E)
        # Options Button
        ttk.Button(self.mainframe, text="Options", image=self.settings_image, takefocus=0,
                   command=self.optionsPage) \
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
                   command=lambda: self.toClip(self.site)) \
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
                   command=lambda: self.toClip(self.user)) \
            .grid(column=3, row=4, sticky=W)
        # Password label, button, entry, and show password button
        ttk.Label(self.mainframe, text="Password") \
            .grid(column=1, row=5, sticky=(W, S))
        ttk.Button(self.mainframe, image=self.copy_image, takefocus=0,
                   command=lambda: self.toClip(self.password)) \
            .grid(column=3, row=6, sticky=W)
        self.password_entry = ttk.Entry(self.mainframe, textvariable=self.password, show="*")
        self.password_entry.grid(column=1, row=6, columnspan=2, sticky=(W, E))
        self.show_password = ttk.Button(self.mainframe, takefocus=0, image=self.password_image,
                                        command=self.passwordShow)
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
        delete_button.bind('<Double-Button-1>', lambda event: self.changeCreds('delete', self.site))
        delete_button.bind('<Button-1>',lambda event: self.updateStatus('Double click "Delete" to confirm'))
        ttk.Button(self.mainframe, text="Update",
                   command=lambda: self.changeCreds('update', self.site)) \
            .grid(column=2, row=9, sticky=W)
        ttk.Button(self.mainframe, text="Add",
                   command=lambda: self.changeCreds('add', self.site)) \
            .grid(column=2, row=9, sticky=E)

        self.padding()

        self.search_entry.focus()


    def optionsPage(self):
        self.mainframe.destroy()
        self.buildPage()

        # Options Button, now returns to the Main Entries window.
        ttk.Button(self.mainframe, text="Options", image=self.settings_image,
                   command=self.mainEntriesPage) \
            .grid(column=0, row=0, sticky=W)

        # Status labels
        ttk.Label(self.mainframe, text="Status") \
           .grid(column=1, row=0, sticky=W)
        self.status_label = ttk.Label(self.mainframe, text='Ready to Search', wraplength=300)
        self.status_label.grid(column=1, row=0, columnspan=2, sticky=E)

        # Functional buttons
        # Load file button
        ttk.Button(self.mainframe, text='Load New File', width=50,
                   command=self.loadNewFilepopup) \
            .grid(column=1, row=1, columnspan=2, rowspan=2, sticky='ns')
        # Write all credentials
        ttk.Button(self.mainframe, text='Print plain text of all Credentials', width=50,
                   command=lambda: user.write_file(self.pinEntry.get(), 'N', 'decoded')) \
            .grid(column=1, row=3, columnspan=2, rowspan=2, sticky='ns')
        # Change pin
        ttk.Button(self.mainframe, text='Change Pin',
                   command=self.changePin, width=50) \
            .grid(column=1, row=5, columnspan=2, rowspan=2, sticky='ns')

        # Change pin labels and entries
        ttk.Label(self.mainframe, text="New Pin") \
            .grid(column=0, row=7, sticky=W)
        pin1_entry = ttk.Entry(self.mainframe, textvariable=self.pin1)
        pin1_entry.grid(column=0, row=7, columnspan=2, sticky=E)
        pin1_entry.bind("<Button-1>", lambda event: self.clearSearch(entry=self.pin1))

        ttk.Label(self.mainframe, text="Pins must match") \
            .grid(column=2, row=8, sticky=W)
        pin2_entry = ttk.Entry(self.mainframe, textvariable=self.pin2)
        pin2_entry.grid(column=2, row=7, columnspan=2, sticky=W)
        pin2_entry.bind("<Button-1>", lambda event: self.clearSearch(entry=self.pin2))

        self.mainframe.rowconfigure(1, weight=1, minsize=50)
        self.mainframe.rowconfigure(2, weight=1, minsize=50)
        self.mainframe.rowconfigure(3, weight=1, minsize=50)
        self.mainframe.rowconfigure(4, weight=1, minsize=50)
        self.mainframe.rowconfigure(5, weight=1, minsize=50)
        self.mainframe.rowconfigure(6, weight=1, minsize=50)

        self.padding()

    def buildPage(self):
        self.mainframe = ttk.Frame(root, padding="3 3 12 12")
        self.mainframe.pack()
        self.mainframe.columnconfigure(0, weight=1, minsize=20)
        self.mainframe.columnconfigure(1, weight=1, minsize=180)
        self.mainframe.columnconfigure(2, weight=1, minsize=180)
        self.mainframe.columnconfigure(3, weight=1, minsize=20)
        self.mainframe.rowconfigure(10, weight=1, minsize=20)

    def loadNewFilepopup(self):
        top = self.top = Toplevel(root)
        Label(top, text="PIN to encode File").pack(padx=10, pady=5)
        self.entry = Entry(top)
        self.entry.pack(padx=10, pady=5)
        Button(top, text='Ok', command=self.loadNewFile).pack(padx=10, pady=5)

    def padding(self):
        for child in self.mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

    # Methods to interact with the various entry boxes and buttons.

    def clearSearch(self, *event, entry=None):  # This is called by the left click event on the entry to clear all text from the entry.
        entry.set('')

    def updateStatus(self,text):
        self.status_label['text'] = text

    def submitPin(self):
        try:
            user.read_file(self.pin_entry.get())
        except:
            self.submit_failed_label['text']='Invalid PIN'
            return
        self.mainEntriesPage()

    def getLogin(self, *event):  # Use the input from the search box and look for login information.
        self.updateEntries(['', '', '', '',self.status_label['text']])  # Clears the entries whenever a search is run. Doesn't clear the search bar.
        searchEntry = self.search.get()
        if searchEntry == '':  # If no search text entered, ignores this command after clearing the boxes.
            return
        if self.last != searchEntry:       # If current search doesn't match previous search, reset allMatches to end of generator to force a new search
            self.allMatches = iter(())
        try:
            creds = next(self.allMatches)   # Try to advance the generator
        except StopIteration:               # If no more matches
            self.allMatches = user.Credentials('login', searchEntry, self.pinEntry.get())  # Uses the pin and search box to search the Credentials File for the credentials.
            try:
                creds = next(self.allMatches)
            except StopIteration:
                creds = ['','','','','No matches found',-1]
        self.updateEntries(creds)  # Successful search returns the list of strings.
        self.last = searchEntry   # Prep for next search if it is going to be identical and trigger the next entry
        self.index = creds[5]       # Set the i value for the currently displayed search results

    # Set a flag that the Stopiteration was hit. If it is the first time, rerun the search, if it happens again, that it because there is no matches.

    def updateEntries(self, creds):  # Update the 4 boxes with new values which can be empty to clear the boxes or will be the return value from a search.
        self.site.set(creds[0])
        self.user.set(creds[1])
        self.password.set(creds[2])
        self.comments.set(creds[3])
        self.updateStatus(creds[4])


    def changeCreds(self, function, site):  # Use the existing entry values to add, edit or delete the creds to or from the list.
        site = site.get()
        if site == '':
            return None
        newCreds = [self.site.get(), self.user.get(), self.password.get(), self.comments.get()]
        changed = user.Credentials(function, site, self.pinEntry.get(), newCreds, self.index, 'DELETE')
        self.updateEntries(changed)

    def passwordShow(self):
        self.password_entry['show'] = ''
        self.password_image['file'] = eyeclosed_img
        self.show_password['command'] = self.passwordHide

    def passwordHide(self):
        self.password_entry['show'] = '*'
        self.password_image['file'] = eye1_img
        self.show_password['command'] = self.passwordShow

    def toClip(self, button):
        root.clipboard_clear()  # clear clipboard contents
        root.clipboard_append(button.get())  # append new value to clipboard
        self.updateStatus(button)


    def loadNewFile(self):
        user.newFile(filedialog.askopenfile(initialdir="/").name, self.entry.get())
        self.pinEntry.set(self.entry.get())        # Reset the global pin to use the new pin for files
        self.top.destroy()


    def changePin(self):
        pin1 = self.pin1.get()
        pin2 = self.pin2.get()
        try:
            user.changePin(pin1, pin2)
        except:
            self.updateStatus('Invalid PIN')
            return
        self.pinEntry.set(pin1)
        self.pin1.set('')
        self.pin2.set('')
        self.updateStatus('Pin Changed')


root = Tk()
CredentialsGUI(root)
root.mainloop()
