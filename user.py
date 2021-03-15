# Scans the info.txt for a match to the user entered value for 'search'. If there is only one match, the site, user and password are returned as a tuple.
# Otherwise a warning is issued as a tuple with the warning string in position 0 and the error flag (None) in position 3
# Change the add to look at the site and see if it is already in the list
from cryptography.fernet import Fernet
import shutil, fkey

#encypted Credentials File
CredentialsFile = r"C:\Users\usstwilk\Documents\Useful docs\info\info.txt"
pin : str

#Reading and writing the encrypted file
def readFile(pin):
    if pin == None:
        pin = input('Pin: ')
    global key
    key = bytes(pin + fkey.key()[len(pin):], 'utf-8')
    with open(CredentialsFile, 'rb') as f:
        global allCreds
        allCreds = Fernet(key).decrypt(f.read()).decode().split('\n')
        global credsList
        credsList = [cred.strip().split(',') for cred in allCreds]
    return "Pin Accepted"

# Encrypt and overwrite the current allCreds list after it has been modified.
def writeFile(key):
    eCreds = Fernet(key).encrypt(bytes('\n'.join(allCreds), 'utf-8'))
    shutil.copyfile(CredentialsFile, CredentialsFile.replace('txt', 'bak'))
    with open(CredentialsFile, 'wb') as f:
        f.write(eCreds)
    return 'File Written'

# Change the encryption key of the file.
def changePin(oldPin = None, newPin = None):
    readFile(oldPin)
    if newPin == None:
        newPin = input('New pin: ')
    key = bytes(newPin + fkey.key()[len(newPin):], 'utf-8')
    writeFile(key)
    return 'Pin changed'

# Read a new unecrypted Credentials file and encrypt it as the new file. 
def newFile(file = CredentialsFile, pin=None):
    if pin == None:
        pin = input('Pin to encode new file: ')
    key = bytes(pin + fkey.key()[len(pin):], 'utf-8')
    with open(file, 'r') as f:
        global allCreds
        allCreds = f.read().split('\n')
        global credsList
        credsList = [cred.strip().split(',') for cred in allCreds]
        writeFile(key)
    return '{} read and encoded'.format(CredentialsFile)

# Print out the entire encrypted credentials file to review
def printCreds(pin=None):
    readFile(pin)
    print('\n')
    for line in credsList:
        print(line)
    return 'Creds List printed'

# Methods for dealing with a single set of credentials.  
# Searches the credentials list and returns a single set of credentials which can be read or manipulated.

def Credentials(function, pin = None, search = None, newCreds = None, delete=None):
    readFile(pin)
    if search == None:
        search = input('Search Credentials: ')
    creds = logIn(search)
    if creds[3] == None:
        if function == 'add':
            return addCred(newCreds)
        return creds
    if function == 'login':
        return creds
    if function == 'update':
        return updateCred(creds, newCreds)
    if function == 'delete':
        return delCred(creds,delete)

def logIn(search):
    if search == '':
        return (None,None,None,None)
    login = (search+' has no matches','','',None)
    count = 0
    for line in credsList:
        if search.lower() in line[0].lower():       #reformats the line and
            count += 1
            login = line
    if count == 0:
        for line in credsList:
            if search.lower() in line[3].lower():
                count += 1
                login = line
    if count > 1:
        return (search+' has too many matches','',None,None)
    return login

def updateCred(creds, newCreds):
    if newCreds == None:
        print('\n\nCurrent credentials\nSite:', creds[0], '\nUser:', creds[1], '\nPassword:', creds[2], '\nComments:', creds[3])
        print('\nEnter new credentials. Leave line blank to keep previous entry\n')
        newCreds = [input('Site: '), input('Username: '), input('Password: '), input('Comments: ')]
        for i, entry in enumerate(newCreds):
            if entry == '':
                newCreds[i] = creds[i]
        newCreds = tuple(newCreds)
    allCreds.append(','.join(newCreds))
    delCred(creds, 'DELETE')
    return (newCreds[0]+' updated','','','')

def addCred(newCreds):
    if newCreds == None:
        newCreds = [input('Site: '), input('Username: '), input('Password: '), input('Comments: ')]
    if newCreds[0]=='':
        return 'No Site entered'
    allCreds.append(','.join(newCreds))
    writeFile(key)
    print(newCreds[0]+' added')
    return (newCreds[0]+' added','','','')

def delCred(creds, delete):
    if delete == None:
        delete = input('Delete entry? '+creds[0]+'\nConfirm with DELETE : ')
    if delete == 'DELETE':
        allCreds.pop(credsList.index(creds))
        writeFile(key)
        print(creds,' deleted')
        return (creds[0]+' deleted','','','')

if __name__ == "__main__":
    Credentials.readFile(None)
