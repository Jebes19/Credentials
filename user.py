# Encrypts, decrypts and handles a file containing logins for a match to the user entered value for 'search'.
# The search is returned as a generator so that the GUI can cycle through the matches.

from cryptography.fernet import Fernet
import fkey


# Reading and writing the encrypted file
def read_file(pin, file=fkey.baseFile):
    if pin is None:
        pin = input('Pin: ')
    with open(file, 'rb') as f:
        allCreds = Fernet(fkey.key(pin)).decrypt(f.read()).decode().split('\n')
    global credsList
    credsList = [cred.split(',') for cred in allCreds]
    return "Pin Accepted"


# Encrypt and overwrite the current CredsList after it has been modified.
def write_file(pin, backup=False, decoded=''):
    if len(pin) not in range(1,44):
        return 'Pin of invalid length'
    if backup is True:
        fkey.backup()
    if decoded == 'decoded':        # Write a decoded file and drop the final end of list item
        eCreds = '\n'.join([',\t\t'.join(entry) for entry in credsList[:-1]])
        fileType = 'w'
        file = fkey.decodedFile
    else:
        eCreds = Fernet(fkey.key(pin)).encrypt(bytes('\n'.join([','.join(entry) for entry in credsList]), 'utf-8'))
        fileType = 'wb'
        file = fkey.baseFile
    with open(file, fileType) as f:
        f.write(eCreds)
    return 'File Written'


# Change the encryption key of the file.
def change_pin(pin1, pin2):
    if pin1 != pin2:
        return "Pins don't match"
    if len(pin1) not in range(1,44):
        return 'Pin of invalid length'
    write_file(pin1, backup=True)
    return 'Pin changed'


def new_file(file, pin):
    # Read a new unencrypted Credentials csv type file and encrypt it as the working file.
    with open(file, 'r') as f:
        preList = [cred.replace('\t', '')             # Remove tabs from lines
                       .split(',')[:4]                # Split on commas and limit size to 4 items max
                   for cred in f.read().split('\n')]    # Read lines and removes newlines
        global credsList
        credsList = [group + [''] * (4 - len(group)) for group in preList]  # Expand size 4 items min
        for site in credsList:      # Checks for duplicates
            if len(list(log_in(site[0]))) > 1:
                return '{} duplicated in file'.format(site[0])
        write_file(pin, backup=True)
    return '{} read and encoded'.format(fkey.baseFile)


# Print out the entire encrypted credentials file to review
# Currently not used by InfoGUI
def print_creds(pin=None):
    read_file(pin)
    print('\n')
    for line in credsList:
        print(line)
    return 'Creds List printed'


# Methods for dealing with a single set of credentials.
# Searches the credentials list and returns a single set of credentials which can be read or manipulated.


def credentials(function, site, pin, new=None, index=-1, delete=None):
    creds = log_in(site)
    if function == 'login':
        return creds
    if function == 'add':
        return add_entry(new, pin)
    if function == 'update':
        return update_entry(index, new, pin)
    if function == 'delete':
        return del_entry(index, delete, pin)


def log_in(search):
    for i, line in enumerate(credsList):
        if search == '*all*':
            yield line + ['Search again for next entry', i]
        if search.lower() in line[0].lower():       # ignore case
            yield line + ['Credentials Found', i]


def update_entry(index, new, pin):
    # Takes the entries as newCreds and location as index. Overwrites all the values at that index
    credsList[index] = [new[i] for i, line in enumerate(credsList[index])]  # Line variable ignored
    write_file(pin, backup=False)
    return new + ['Credentials updated']


def add_entry(new, pin):
    if new is None:
        new = [input('Site: '), input('Username: '), input('Password: '), input('Comments: ')]
    if new in credsList:
        return new + ['{} duplicated in file'.format(new[0]), -1]
    credsList.append(new)
    write_file(pin, backup=False)
    print(new[0] + ' added')
    return new + ['Credentials added', len(credsList) - 1]


def del_entry(index, delete, pin):
    if delete == 'DELETE':
        creds = credsList[index]
        credsList.pop(index)
        write_file(pin, backup=True)
        print(creds, ' deleted')
        return ['', '', '', '', 'Credentials deleted', -1]


if __name__ == "__main__":
    read_file(None)
    write_file('', decoded='decoded')
