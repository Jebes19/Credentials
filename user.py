# Scans the info.txt for a match to the user entered value for 'search'.
# The search is returned as a generator so that the GUI can cycle through the matches.
# script also includes file handling of info.txt

from cryptography.fernet import Fernet
import shutil, fkey

# Encypted Credentials File
CredentialsFile = fkey.fileLocation


# Reading and writing the encrypted file
def read_file(pin):
    if pin is None:
        pin = input('Pin: ')
    with open(CredentialsFile, 'rb') as f:
        allCreds = Fernet(fkey.key(pin)).decrypt(f.read()).decode().split('\n')
        global credsList
        credsList = [cred.split(',') for cred in allCreds]
    return "Pin Accepted"


# Encrypt and overwrite the current CredsList after it has been modified.
def write_file(pin, backup='', decoded=''):
    if backup != 'N':
        shutil.copyfile(CredentialsFile, CredentialsFile.replace('txt', 'bak'))
    if decoded == 'decoded':
        eCreds = '\n'.join([',\t\t'.join(list) for list in credsList])
        fileType = 'w'
        file = CredentialsFile.replace('.txt', '_decoded.txt')
    else:
        eCreds = Fernet(fkey.key(pin)).encrypt(bytes('\n'.join([','.join(entry) for entry in credsList]), 'utf-8'))
        fileType = 'wb'
        file = CredentialsFile
    with open(file, fileType) as f:
        f.write(eCreds)
    return 'File Written'


# Change the encryption key of the file.
def changePin(pin1, pin2):
    if pin1 != pin2:
        return "Pins don't match"
    write_file(pin1)
    return 'Pin changed'


# Read a new unencrypted Credentials file and encrypt it as the new file.
def newFile(file, pin):
    with open(file, 'r') as f:
        preList = [cred.replace('\t', '').split(',') for cred in f.read().split(
            '\n')]  # Reads the file of credentials, removing tabs before splitting each line into a csv.
        global credsList
        credsList = [group + [''] * (4 - len(group)) for group in
                     preList]  # Expand any entries with less than 4 items to include blank lines
        for site in credsList:
            if len(list(logIn(site[0]))) > 2:
                return '{} duplicated in file'.format(site[0])
        write_file(pin, backup='N')
    return '{} read and encoded'.format(CredentialsFile)


# Print out the entire encrypted credentials file to review
# Currently not used by InfoGUI
def printCreds(pin=None):
    read_file(pin)
    print('\n')
    for line in credsList:
        print(line)
    return 'Creds List printed'


# Methods for dealing with a single set of credentials.
# Searches the credentials list and returns a single set of credentials which can be read or manipulated.


def Credentials(function, site, pin, newCreds=None, index=-1, delete=None):
    creds = logIn(site)
    if function == 'login':
        return creds
    if function == 'add':
        return addCred(newCreds, pin)
    if function == 'update':
        return updateCred(index, newCreds, pin)
    if function == 'delete':
        return delCred(index, delete, pin)


def logIn(search):
    for i, line in enumerate(credsList):
        if search.lower() in line[0].lower():  # reformats the line to ignore case when looking for a match
            yield line + ['Credentials Found', i]
    yield ['', '', '', '', 'End of list, no more matches', -1]


def updateCred(index, newCreds, pin):
    if newCreds == None:
        newCreds = [input('Site: '), input('Username: '), input('Password: '), input('Comments: ')]
    credsList[index] = [newCreds[i] for i, line in enumerate(credsList[index])]
    write_file(pin)
    return newCreds + ['Credentials updated']


def addCred(newCreds, pin):
    if newCreds == None:
        newCreds = [input('Site: '), input('Username: '), input('Password: '), input('Comments: ')]
    if newCreds in credsList:
        return newCreds + ['{} duplicated in file'.format(newCreds[0]), -1]
    credsList.append(newCreds)
    write_file(pin)
    print(newCreds[0] + ' added')
    return newCreds + ['Credentials added', len(credsList) - 1]


def delCred(index, delete, pin):
    if delete == 'DELETE':
        creds = credsList[index]
        credsList.pop(index)
        write_file(pin)
        print(creds, ' deleted')
        return ['', '', '', '', 'Credentials deleted', -1]


if __name__ == "__main__":
    read_file(None)
    write_file('', 'decoded')
