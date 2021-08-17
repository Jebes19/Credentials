# Encrypts, decrypts and handles a file containing logins for a match to the user entered value for 'search'.
# The search is returned as a generator so that the GUI can cycle through the matches.

from pman import fkey

class InfoFile:

    def __init__(self, code, file=fkey.baseFile):
        # Instantiate a new read of the file of credentials.
        with open(file, 'rb') as f:
            allCreds = fkey.decrypt(code, f.read()).decode().split('\n')
            self.infoList = [cred.split(',') for cred in allCreds]
            self.code = code
        print("Credentials Loaded")

        # Change the encryption key of the file.
    def change_code(self, code1, code2):
        if code1 != code2:
            return "Codes don't match"
        if len(code1) not in range(1, 44):
            return 'Code of invalid length'
        self.code = code1
        write_file(code1, self.infoList, backup=False)
        print('Code changed')

    # Print out the entire encrypted credentials file to review
    # Currently not used by InfoGUI
    def print_creds(self):
        print('\n')
        for line in self.infoList:
            print(line)
        return 'Creds List printed'

    def update_entry(self, new: []):
        # Takes the entries as newCreds and location as index. Overwrites all the values at that index
        index = new[5]
        self.infoList[index] = new[:4]
        write_file(self.code, self.infoList, backup=False)
        new[4] = 'Credentials updated'
        return new

    def delete_entry(self, index: int):
        creds = self.infoList[index][0]
        self.infoList.pop(index)
        write_file(self.code, self.infoList, backup=True)
        print(creds, 'deleted')
        return ['', '', '', '', 'Credentials deleted', len(self.infoList)]

    def add_entry(self, new: []):
        if new is None:
            new = [input('Site: '), input('Username: '), input('Password: '), input('Comments: ')]
        if new in self.infoList:
            return new + ['{} duplicated in file'.format(new[0]), len(self.infoList)]
        self.infoList.append(new[:4])
        write_file(self.code, self.infoList, backup=False)
        print(new[0] + ' added')
        return new + ['Credentials added', len(self.infoList) - 1]


def search_results(infolist: list, search: str):
    # takes an infoList, searches it and returns a generator object to cycle through matches one at a time.
    for i, line in enumerate(infolist):
        if search.lower() in line[0].lower():
            yield line+['Search again for next match', i]


def new_file(code, file):
    with open(file, 'r') as f:
        preList = [cred.replace('\t', '')               # Remove tabs from lines
                   .split(',')[:4]                  # Split on commas and limit size to 4 items max
                   for cred in f.read().split('\n')]    # Read lines and removes newlines
        infoList = [group + [''] * (4 - len(group)) for group in preList]  # Expand size 4 items min
        write_file(code, infoList, backup=True)
        print('{} read and encoded'.format(fkey.baseFile))


def write_file(code, infolist: list, backup=False, decoded=''):
    if len(code) not in range(1, 44):
        return 'Code of invalid length'
    if backup is True:
        fkey.backup()
    if decoded == 'decoded':        # Write a decoded file
        eCreds = '\n'.join([',\t\t'.join(entry) for entry in infolist])
        fileType = 'w'
        file = fkey.decodedFile
    else:
        eCreds = fkey.encrypt(code, bytes('\n'.join([','.join(entry) for entry in infolist]), 'utf-8'))
        fileType = 'wb'
        file = fkey.baseFile
    with open(file, fileType) as f:
        f.write(eCreds)
    print('File Written')


if __name__ == "__main__":
    x = InfoFile('77', r'C:\Users\usstwilk\Documents\Useful docs\info\Copy.txt')
    y = search_results(x.infoList, 'jira')
    pass
