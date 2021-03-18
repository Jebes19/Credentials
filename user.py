# Scans the info.txt for a match to the user entered value for 'search'. If there is only one match, the site, user and password are returned as a tuple.
# Otherwise a warning is issued as a tuple with the warning string in position 0 and the error flag (None) in position 3
# Change the add to look at the site and see if it is already in the list
from cryptography.fernet import Fernet
import shutil, fkey

#encypted Credentials File
CredentialsFile = r"C:\Users\usstwilk\Documents\Useful docs\info\info.txt"

#Reading and writing the encrypted file
def readFile(pin):
    if pin == None:
        pin = input('Pin: ')
    global key
    key = bytes(pin + fkey.key()[len(pin):], 'utf-8')
    with open(CredentialsFile, 'rb') as f:
        allCreds = Fernet(key).decrypt(f.read()).decode().split('\n')
        global credsList
        credsList = [cred.split(',') for cred in allCreds]
    return "Pin Accepted"

# Encrypt and overwrite the current CredsList after it has been modified.
def writeFile():
    global key
    eCreds = Fernet(key).encrypt(bytes('\n'.join([','.join(list) for list in credsList]), 'utf-8'))
    shutil.copyfile(CredentialsFile, CredentialsFile.replace('txt', 'bak'))
    with open(CredentialsFile, 'wb') as f:
        f.write(eCreds)
    return 'File Written'

# Change the encryption key of the file.
def changePin(pin1, pin2):
    if pin1 != pin2:
        return "Pins don't match"
    global key
    key = bytes(pin1 + fkey.key()[len(pin1):], 'utf-8')
    writeFile()
    return 'Pin changed'

# Read a new unecrypted Credentials file and encrypt it as the new file. 
def newFile(file, pin):
    key = bytes(pin + fkey.key()[len(pin):], 'utf-8')
    with open(file, 'r') as f:
        preList = [cred.split(',') for cred in f.read().split('\n')]
        global credsList
        credsList = [group+['']*(4-len(group)) for group in preList]        # Expand any entries with less than 4 items
        for site in credsList:
            if len(list(logIn(site[0]))) > 2:
                return '{} duplicated in file'.format(site[0])
            pass
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

def Credentials(function, site, newCreds = None, delete=None):
    creds = logIn(site)
    if function == 'login':
        return creds
    creds = list(creds)[0]
    if function == 'add':
        return addCred(newCreds)
    if function == 'update':
        return updateCred(creds, newCreds)
    if function == 'delete':
        return delCred(newCreds,delete)

def logIn(search):
    for line in credsList:
        if search.lower() in line[0].lower():       #reformats the line to ignore case when looking for a match
            yield line+['Credentials Found']
    yield ['','','','','End of list, no more matches']

def updateCred(creds, newCreds):
    if newCreds == None:
        newCreds = [input('Site: '), input('Username: '), input('Password: '), input('Comments: ')]
    credsList.append(newCreds)
    delCred(creds, 'DELETE')
    return newCreds+['Credentials updated']

def addCred(newCreds):
    if newCreds == None:
        newCreds = [input('Site: '), input('Username: '), input('Password: '), input('Comments: ')]
    if newCreds[0]=='':
        return ['','','','','No site Entered']
    credsList.append(newCreds)
    writeFile()
    print(newCreds[0]+' added')
    return newCreds+['Credentials added']

def delCred(creds, delete):
    if delete == None:      # Allows confirmation when using console commands
        delete = input('Delete entry? '+creds[0]+'\nConfirm with DELETE : ')
    if delete == 'DELETE':
        credsList.remove(creds[:4])
        writeFile()
        print(creds,' deleted')
        return creds[:4]+['Credentials deleted']

if __name__ == "__main__":
    readFile(None)
