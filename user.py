# Encrypts, decrypts and handles a file containing logins for a match to the user entered value for 'search'.
# The search is returned as a generator so that the GUI can cycle through the matches.

import fkey

credsList = []


# Reading and writing the encrypted file
def read_file(pin, file=fkey.baseFile):
    if pin is None:
        pin = input('Pin: ')
    with open(file, 'rb') as f:
        allCreds = fkey.decrypt(pin, f.read()).decode().split('\n')
    if allCreds == ['']:
        print('Empty File')
        return
    global credsList
    credsList = [cred.split(',') for cred in allCreds]
    print("Pin Accepted")


# Encrypt and overwrite the current CredsList after it has been modified.
def write_file(pin, backup=False, decoded='', blank=False):
    all_items = credsList
    if len(pin) not in range(1, 44):
        return 'Pin of invalid length'
    if backup is True:
        fkey.backup()
    if blank is True:
        all_items = [['Site,Username,Password,Comments']]
    if decoded == 'decoded':        # Write a decoded file
        eCreds = '\n'.join([',\t\t'.join(entry) for entry in all_items])
        fileType = 'w'
        file = fkey.decodedFile
    else:
        eCreds = fkey.encrypt(pin, bytes('\n'.join([','.join(entry) for entry in all_items]), 'utf-8'))
        fileType = 'wb'
        file = fkey.baseFile
    with open(file, fileType) as f:
        f.write(eCreds)
    print('File Written')


# Change the encryption key of the file.
def change_pin(pin1, pin2):
    if pin1 != pin2:
        return "Pins don't match"
    if len(pin1) not in range(1, 44):
        return 'Pin of invalid length'
    write_file(pin1, backup=False)
    print('Pin changed')


def new_file(file, pin):
    # Read a new unencrypted Credentials csv type file and encrypt it as the working file.
    with open(file, 'r') as f:
        preList = [cred.replace('\t', '')               # Remove tabs from lines
                       .split(',')[:4]                  # Split on commas and limit size to 4 items max
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
    read_file(pin)
    if function == 'login':
        return log_in(site)
    if function == 'add':
        return add_entry(new, pin)
    if function == 'update':
        return update_entry(index, new, pin)
    if function == 'delete':
        return del_entry(index, delete, pin)


def log_in(search):
    for i, line in enumerate(credsList):
        if search.lower() in line[0].lower():       # ignore case
            yield line + ['Search again for next match', i]


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
    pass
