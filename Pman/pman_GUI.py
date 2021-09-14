# InterfaceGUI to interact with user.py
from tkinter import *
from tkinter import ttk, filedialog
from threading import Timer
from cryptography.fernet import InvalidToken
from webbrowser import open as web_open
from pman import pman_config
from pman import user
from pman.fkey import images
from tkinter import messagebox
import os
import sys

VERSION = '2.1.11'


# noinspection PyAttributeOutsideInit
class GUI:

    # Methods to create the GUI, and recreate it when moving to different pages.
    def __init__(self, main):

        # Initialize the main window
        main.title("Password Manager")
        main.columnconfigure(0, weight=1, minsize=400)
        main.rowconfigure(0, weight=1)

        # Initialize all the variables
        self.timeOutIntVar = IntVar(value=600)    # 10 minute timeout
        self.indexVar = IntVar()
        self.activeCodeStrVar = StringVar()
        self.siteStrVar = StringVar(name='Site copied to clipboard')
        self.userStrVar = StringVar(name='User copied to clipboard')
        self.passwordStrVar = StringVar(name='Password copied to clipboard')
        self.URL_commentsStrVar = StringVar(name='URL')
        self.searchStrVar = StringVar()
        self.code1StrVar = StringVar()
        self.code2StrVar = StringVar()
        self.statusStrVar = StringVar('')
        self.infoFile = None
        self.lastVar = None

        # Import images
        self.copy_image = PhotoImage(file=images+r'\copy.png', height=30, width=30)
        self.settings_image = PhotoImage(file=images+r'\settings.png', height=30, width=30)
        self.open_image = PhotoImage(file=images+r'\open.png', height=30, width=30)
        self.password_image = PhotoImage(file=images+r'\eye2.png', height=30, width=30)
        self.new_file_image = PhotoImage(file=images+r'\new_file.png', height=30, width=30)
        self.load_file_image = PhotoImage(file=images+r'\load_from_file.png', height=30, width=30)
        self.main_menu_image = PhotoImage(file=images+r'\main_menu.png', height=30, width=30)

        # Import standard window configuration
        self.build_page()
        self.status_label.grid(column=2, row=1, columnspan=2, sticky=E)

        # Version label
        ttk.Label(self.mainframe, text="Password Manager by Taylor Wilkin, Version " + VERSION)\
            .grid(column=1, row=10, columnspan=3, sticky=N)

        # Code Entry label.
        ttk.Label(self.mainframe, text="Code for Credentials file")\
            .grid(column=1, row=0, columnspan=2, sticky=N)

        # Code button and entry
        self.code_button = ttk.Button(self.mainframe, text='Code', command=self.load_file)
        self.code_button.grid(column=1, row=1, sticky=E)
        self.code_entry = ttk.Entry(self.mainframe, width=15, textvariable=self.activeCodeStrVar, show='*')
        self.code_entry.grid(column=2, row=1, sticky=W)
        self.code_entry.bind("<Return>", lambda event: self.load_file())
        self.code_entry.bind("<Button-1>", lambda event: self.activeCodeStrVar.set(''))
        self.code_entry.focus()

        # New File Button
        ttk.Button(self.mainframe, text="New File", image=self.load_file_image, takefocus=0,
                   command=self.popup_select_new_file) \
            .grid(column=0, row=0, rowspan=2, sticky=W)

        # New file label.
        ttk.Label(self.mainframe, text="Start New")\
            .grid(column=0, row=10, sticky=W)

        self.padding()

    def main_entries_page(self):
        self.mainframe.destroy()
        self.build_page()

        # Search Entry
        search_entry = ttk.Entry(self.mainframe, width=30, textvariable=self.searchStrVar)
        search_entry.grid(column=2, row=0, sticky=W)
        search_entry.bind("<Return>", lambda event: self.get_next_login(self.searchStrVar.get()))
        search_entry.bind("<Button-1>", lambda event: self.searchStrVar.set(''))
        search_entry.focus()
        # Search Button
        ttk.Button(self.mainframe, text='Search',
                   command=lambda: self.get_next_login(self.searchStrVar.get())) \
            .grid(column=1, row=0, sticky=E)
        # Options Button
        ttk.Button(self.mainframe, text="Options", image=self.settings_image, takefocus=0,
                   command=self.options_page) \
            .grid(column=0, row=0, sticky=W)
        # Status labels
        ttk.Label(self.mainframe, text="Status") \
           .grid(column=1, row=1, sticky=E)
        self.status_label.grid(column=2, row=1, sticky=W)
        # Site label, button, and entry
        ttk.Label(self.mainframe, text="Site", ) \
            .grid(column=1, row=1, columnspan=2, sticky=(W, S))
        ttk.Button(self.mainframe, image=self.copy_image, takefocus=0,
                   command=lambda: self.to_clip(self.siteStrVar)) \
            .grid(column=3, row=2, sticky=W)
        ttk.Entry(self.mainframe, textvariable=self.siteStrVar) \
            .grid(column=1, row=2, columnspan=2, sticky=(W, E))
        # Username label, button, and entry
        ttk.Label(self.mainframe, text="Username") \
            .grid(column=1, row=3, sticky=(W, S))
        ttk.Entry(self.mainframe, textvariable=self.userStrVar) \
            .grid(column=1, row=4, columnspan=2, sticky=(W, E))
        ttk.Button(self.mainframe, image=self.copy_image, takefocus=0,
                   command=lambda: self.to_clip(self.userStrVar)) \
            .grid(column=3, row=4, sticky=W)
        # Password label, button, entry, and show password button
        ttk.Label(self.mainframe, text="Password") \
            .grid(column=1, row=5, sticky=(W, S))
        ttk.Button(self.mainframe, image=self.copy_image, takefocus=0,
                   command=lambda: self.to_clip(self.passwordStrVar)) \
            .grid(column=3, row=6, sticky=W)
        self.password_entry = ttk.Entry(self.mainframe, textvariable=self.passwordStrVar, show="*")
        self.password_entry.grid(column=1, row=6, columnspan=2, sticky=(W, E))
        self.show_password = ttk.Button(self.mainframe, takefocus=0, image=self.password_image,
                                        command=self.password_show)
        self.show_password.grid(column=0, row=6, sticky=W)
        # Comments label, entry, and open site button
        ttk.Label(self.mainframe, text="URL or Comments") \
            .grid(column=1, columnspan=2, row=7, sticky=(W, S))
        ttk.Entry(self.mainframe, textvariable=self.URL_commentsStrVar) \
            .grid(column=1, row=8, columnspan=2, sticky=(W, E))
        self.open_site = ttk.Button(self.mainframe, image=self.open_image, takefocus=0, state='disabled',
                                    command=lambda: web_open(self.URL_commentsStrVar.get(), new=2))
        self.open_site.grid(column=0, row=8, sticky=E)

        # Add, Update and Delete buttons
        self.delete_button = ttk.Button(self.mainframe, text="Delete", state="disabled",
                            command=self.delete_button_set)
        self.delete_button.grid(column=1, row=9, sticky=W)
        self.update_button = ttk.Button(self.mainframe, text="Update", state='disabled',
                                        command=lambda: self.update_or_add_entry())
        self.update_button.grid(column=2, row=9, sticky=W)
        self.add_button = ttk.Button(self.mainframe, text="Add",
                                     command=lambda: self.add_new_credentials())
        self.add_button.grid(column=2, row=9, sticky=E)

        # Variable Traces to change button states when variables change
        # Add trace to URLComments variable to check for an valid website and update button status.
        self.URL_commentsStrVar.trace_add('write', lambda a, b, c: self.url_button_status())
        # Add traces to entry variables to enable update and add buttons
        self.siteStrVar.trace_add('write', lambda a, b, c: self.update_button_status())
        self.userStrVar.trace_add('write', lambda a, b, c: self.update_button_status())
        self.passwordStrVar.trace_add('write', lambda a, b, c: self.update_button_status())
        self.URL_commentsStrVar.trace_add('write', lambda a, b, c: self.update_button_status())
        # Add Trace to index to enable delete button if index > 0
        self.indexVar.trace_add('write', lambda a, b, c: self.delete_button_status())

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
        ttk.Button(self.mainframe, text="Options", image=self.main_menu_image,
                   command=self.main_entries_page) \
            .grid(column=0, row=0, sticky=W)

        # Status labels

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
                   command=lambda: [user.write_file(self.activeCodeStrVar.get(),
                                    self.infoFile.infoList,
                                    decoded='decoded'),
                                    web_open(user.fkey.info_folder,
                                    new=2)]) \
            .grid(column=1, row=3, columnspan=2, rowspan=2, sticky=NS)
        # Change code
        ttk.Button(self.mainframe, text='Change Code',
                   command=self.code_change, width=50) \
            .grid(column=1, row=5, columnspan=2, rowspan=2, sticky=NS)

        # Change code labels and entries
        ttk.Label(self.mainframe, text="New Code") \
            .grid(column=0, row=7, sticky=W)
        ttk.Entry(self.mainframe, textvariable=self.code1StrVar) \
            .grid(column=0, row=7, columnspan=2, sticky=E)
        ttk.Entry(self.mainframe, textvariable=self.code2StrVar) \
            .grid(column=2, row=7, columnspan=2, sticky=W)

        # Timeout checkbox
        self.timeout_button = ttk.Checkbutton(self.mainframe,
                                              text="1 hour timeout",
                                              variable=self.timeOutIntVar,
                                              offvalue=600,
                                              onvalue=3600)
        self.timeout_button.grid(column=1, row=0, sticky=W)

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
        self.status_label = ttk.Label(self.mainframe, textvariable=self.statusStrVar)
        self.mainframe.bind("<FocusOut>", lambda e: self.focus_from_app())
        self.mainframe.bind("<FocusIn>", lambda e: self.focus_on_app())

    def padding(self):
        for child in self.mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def popup_select_new_file(self):
        top = self.top = Toplevel(root)
        ttk.Label(top, text="Code to encrypt New File").grid(row=0, column=0, columnspan=3)
        entry = Entry(top, justify='center')
        entry.grid(row=1, column=0, columnspan=3)
        entry.focus()
        ttk.Button(top, text='Blank File', image=self.new_file_image, takefocus=0,
                   command=lambda: self.load_new_file(entry.get(), blank=True)).grid(row=3, column=0)
        ttk.Button(top, text='Load File', image=self.load_file_image,
                   command=lambda: self.load_new_file(entry.get())).grid(row=3, column=2)
        ttk.Label(top, text='Start with a new File').grid(row=2, column=0)
        ttk.Label(top, text='Load an existing File').grid(row=2, column=2)
        for child in top.winfo_children():
            child.grid_configure(padx=15, pady=10)

    # Methods to interact with the various entry boxes and buttons.

    def load_file(self):
        # Loads the list of credentials and stores the results to be manipulated
        try:
            self.infoFile = user.InfoFile(self.activeCodeStrVar.get())
            self.statusStrVar.set('Ready to Search')
            self.main_entries_page()
        except InvalidToken:
            self.statusStrVar.set('Invalid Code')
            return
        except FileNotFoundError:
            self.statusStrVar.set('No File found')
            return

    def get_next_login(self, search):
        # Takes search input and checks for matched logins. Returns a generator to retrieve all matches
        if self.lastVar != search:        # New searches won't match the "last" search nor will end of list
            self.allMatches = user.search_results(self.infoFile.infoList, search)
        try:
            next_entry = next(self.allMatches)
        except StopIteration:               # End of list if no matches or no more matches
            if self.lastVar != search:
                next_entry = ['', '', '', '', 'No matches found', len(self.infoFile.infoList)]
            else:
                next_entry = ['', '', '', '', 'End of matches', len(self.infoFile.infoList)]
            search = None                # Forces next search to start over
        self.lastVar = search             # If try succeeds, self.last will match search entry
        self.update_entry_boxes(next_entry)     # Successful search returns the list of strings
        self.indexVar.set(next_entry[5])         # Stores list index for the currently displayed search results

    def update_entry_boxes(self, credentials):
        # Update visible entry boxes on gui
        # Updates can be to '' to clear the boxes or will otherwise be the return from a search.
        # Also, update-entries sets update and add buttons to disabled
        self.siteStrVar.set(credentials[0])
        self.userStrVar.set(credentials[1])
        self.passwordStrVar.set(credentials[2])
        self.URL_commentsStrVar.set(credentials[3])
        self.statusStrVar.set(credentials[4])
        self.update_button.config(state='disabled')

    # Delete button Handling
    def delete_entry(self, index):
        # Updates entries from the return of the previous call
        if index == len(self.infoFile.infoList):
            return
        self.update_entry_boxes(self.infoFile.delete_entry(index))
        self.indexVar.set(len(self.infoFile.infoList))      # Set current index to end of the list
        self.delete_button_reset()

    def delete_button_status(self):
        # Called on every update to the index variable to enable the delete button if credentials are loaded
        if self.indexVar.get() < len(self.infoFile.infoList):
            self.delete_button.config(state='normal')
            self.delete_button_reset()
        else:
            self.delete_button.config(state='disabled')

    def delete_button_set(self):
        self.delete_button.bind('<Button-1>',lambda event: self.delete_entry(self.indexVar.get()))
        self.statusStrVar.set('click "Delete" again to confirm')

    def delete_button_reset(self):
        self.delete_button.unbind('<Button-1>')

    # Add Button handling
    def add_new_credentials(self):
        # The add button clears the credentials and starts with blank entries
        self.update_entry_boxes(['', '', '', '', 'Press Update when ready to add'])
        self.indexVar.set(len(self.infoFile.infoList))   # Remove any of the current credentials from the targeted change
        self.add_button.config(state='disabled')

    def update_or_add_entry(self):
        new = [self.siteStrVar.get(),
               self.userStrVar.get(),
               self.passwordStrVar.get(),
               self.URL_commentsStrVar.get(),
               '',
               self.indexVar.get()]
        try:
            self.update_entry_boxes(self.infoFile.update_entry(new))
        except IndexError:
            self.update_entry_boxes(self.infoFile.add_entry(new))
        self.infoFile = user.InfoFile(self.activeCodeStrVar.get())
        self.add_button.config(state='enabled')
        self.update_button.config(state='disabled')

    def password_show(self):
        # Show password, change image of button and remap command to password_hide
        self.password_entry['show'] = ''
        self.password_image['file'] = images+r'\eye_closed.png'
        self.show_password['command'] = self.password_hide

    def password_hide(self):
        # Hide password, change image of button and remap command to password_show
        self.password_entry['show'] = '*'
        self.password_image['file'] = images+r'\eye1.png'
        self.show_password['command'] = self.password_show

    def to_clip(self, button):
        # Copy contents of the corresponding entry to clipboard and tell the user it is done
        root.clipboard_clear()
        root.clipboard_append(button.get())
        self.statusStrVar.set(button)

    def load_new_file(self, code, blank=False):
        # Load all new credentials from a csv formatted file
        if code == '':
            return
        if blank is False:
            user.new_file(code, filedialog.askopenfile(initialdir=user.fkey.info_folder).name)
        else:
            user.write_file(code, [['Site,Username,Password,Comments']])
        self.activeCodeStrVar.set(code)      # Reset the global code to use the new code for files
        self.top.destroy()
        self.load_file()               # Reloads the file from the new code

    def load_backup(self):
        # Reload the backup in case of a mistake in the file.
        print('Backup file found')
        self.infoFile = user.InfoFile(self.activeCodeStrVar.get(), file=user.fkey.backupFile)
        self.main_entries_page()
        self.update_entry_boxes(['', '', '', '', 'Backup File loaded', len(self.infoFile.infoList)])

    # Code changing bugged, doesn't report invalid codes anymore
    def code_change(self):
        # Compare codes entered and then encrypting the credsList with the new key
        code1 = self.code1StrVar.get()
        code2 = self.code2StrVar.get()
        try:
            self.infoFile.change_code(code1, code2)
            self.statusStrVar.set('Code Changed')     # Changes code if matched and valid codes
        except InvalidToken:
            self.statusStrVar.set('Invalid Code')
            return
        self.activeCodeStrVar.set(code1)
        self.code1StrVar.set('')
        self.code2StrVar.set('')

    # Delete, Add and Update button status functions
    def url_button_status(self):
        # Scans the Comment string for 'http' and sets the open site to available if found
        if 'http' in self.URL_commentsStrVar.get():
            self.open_site.config(state='normal')
        else:
            self.open_site.config(state='disabled')

    def update_button_status(self):
        # Is called whenever a key stroke might change a data entry
        self.update_button.config(state='normal')
        self.add_button.config(state='normal')

    # Time out functions
    def focus_on_app(self):
        print('focus_on_app')
        # Cancel timer when focus returns to app
        try:
            self.delay.cancel()
            self.warning_timer.cancel()
        except AttributeError:
            pass

    def focus_from_app(self):
        print('focus_from_app')
        # Start timer whenever focus moves from app
        self.delay = Timer(interval=self.timeOutIntVar.get(), function=self.timed_quit)
        self.warning_timer = Timer(interval=self.timeOutIntVar.get()-30, function=self.warning_before_exit)
        self.delay.start()
        self.warning_timer.start()

    def warning_before_exit(self):
        print('warning_before_exit')
        messagebox.showinfo('Password Manager Timeout', 'Password Manager is about to timeout (or has already)\n'
                                        'Press Ok to continue to use the application\n'
                                        'Note: The timeout can be temporarily increased to 1 hour on the options page')


    def timed_quit(self):
        print('timed_quit')
        # Quit program if timer expires.
        self.mainframe.destroy()
        ttk.Label(root, text='\tPassword Manager Logged out due to inactivity').grid(padx=15, pady=15, sticky=EW)


root = Tk()
GUI(root)
root.mainloop()
