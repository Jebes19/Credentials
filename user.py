# Scans the info.txt for a match to the user entered value for 'search'.
# The search is returned as a generator so that the GUI can cycle through the matches.
# script also includes file handling of info.txt

from cryptography.fernet import Fernet
import shutil, fkey


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
def write_file(pin, backup='', decoded=''):
    if backup != 'N':
        shutil.copyfile(fkey.baseFile, fkey.backupFile)
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
    write_file(pin1)
    return 'Pin changed'


def new_file(file, pin):
    # Read a new unencrypted Credentials csv type file and encrypt it as the working file.
    with open(file, 'r') as f:
        preList = [cred.replace('\t', '')             # Remove tabs from lines
                       .split(',')[:4]                # Split on commas and limit size to 4 items
                   for cred in f.readlines()]  ##### Check if this can become readlines

        global credsList
        credsList = [group + [''] * (4 - len(group)) for group in preList]
            # Expand any entries with less than 4 items to include blank lines
        for site in credsList:      # Checks if the exact same entry is already in the file
            if len(list(log_in(site[0]))) > 2:
                return '{} duplicated in file'.format(site[0])
        write_file(pin, backup='N')
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
        if search=='*all*':
            yield line + ['Search again for next entry',i]
        if search.lower() in line[0].lower():       # ignore case
            yield line + ['Credentials Found', i]

def update_entry(index, newCreds, pin):
    # Takes the entries as newCreds and location as index. Overwrites all the values at that index
    credsList[index] = [newCreds[i] for i, line in enumerate(credsList[index])] # Line ignored and overwritten
    write_file(pin)
    return newCreds + ['Credentials updated']


def add_entry(newCreds, pin):
    if newCreds == None:
        newCreds = [input('Site: '), input('Username: '), input('Password: '), input('Comments: ')]
    if newCreds in credsList:
        return newCreds + ['{} duplicated in file'.format(newCreds[0]), -1]
    credsList.append(newCreds)
    write_file(pin)
    print(newCreds[0] + ' added')
    return newCreds + ['Credentials added', len(credsList) - 1]


def del_entry(index, delete, pin):
    if delete == 'DELETE':
        creds = credsList[index]
        credsList.pop(index)
        write_file(pin)
        print(creds, ' deleted')
        return ['', '', '', '', 'Credentials deleted', -1]


if __name__ == "__main__":
    read_file(None)
    write_file('', 'decoded')
