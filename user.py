# Scans the info.txt for a match to the user entered value for 'search'. The search is returned as a gnerator so that the GUI can cycle through the matches.
# script also includes file handling of info.txt

from cryptography.fernet import Fernet
import shutil, fkey

#encypted Credentials File
CredentialsFile = fkey.infoLocation

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
    global key
    key = bytes(pin + fkey.key()[len(pin):], 'utf-8')
    with open(file, 'r') as f:
        preList = [cred.split(',') for cred in f.read().split('\n')]
        global credsList
        credsList = [group+['']*(4-len(group)) for group in preList]        # Expand any entries with less than 4 items
        for site in credsList:
            if len(list(logIn(site[0]))) > 2:
                return '{} duplicated in file'.format(site[0])
        writeFile()
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


def Credentials(function, site, newCreds=None, index=-1, delete=None):
    creds = logIn(site)
    if function == 'login':
        return creds
    if function == 'add':
        return addCred(newCreds)
    if function == 'update':
        return updateCred(index, newCreds)
    if function == 'delete':
        return delCred(index,delete)

def logIn(search):
    for i,line in enumerate(credsList):
        if search.lower() in line[0].lower():       #reformats the line to ignore case when looking for a match
            yield line+['Credentials Found',i]
    yield ['','','','','End of list, no more matches',-1]

def updateCred(index, newCreds):
    if newCreds == None:
        newCreds = [input('Site: '), input('Username: '), input('Password: '), input('Comments: ')]
    credsList[index] = [newCreds[i] for i,line in enumerate(credsList[index])]
    writeFile()
    return newCreds+['Credentials updated']

def addCred(newCreds):
    if newCreds == None:
        newCreds = [input('Site: '), input('Username: '), input('Password: '), input('Comments: ')]
    if newCreds in credsList:
        return newCreds+['{} duplicated in file'.format(newCreds[0]),-1]
    credsList.append(newCreds)
    writeFile()
    print(newCreds[0]+' added')
    return newCreds+['Credentials added',len(credsList)-1]

def delCred(index, delete):
    if delete == 'DELETE':
        creds = credsList[index]
        credsList.pop(index)
        writeFile()
        print(creds,' deleted')
        return ['','','','','Credentials deleted',-1]


if __name__ == "__main__":
    readFile(None)
