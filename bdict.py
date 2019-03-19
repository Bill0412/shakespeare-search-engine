# This is a bidirectional dictionary
import json
import pathlib

class BDict:
    def __init__(self, file_name='data/link_label'):
        # if the file is not found
        self.file_name = file_name
        if not pathlib.Path(file_name).is_file():
            self.dict1 = dict()
            self.dict2 = dict()
        else:
            # if is found, read from the file
            self.disk_read()

    def insert(self, element1, element2):
        self.dict1[element1] = element2
        self.dict2[element2] = element1

    # returns value of the key
    # returns None if the key does not exist
    def search(self, which_dict, key):

        if which_dict == 1:
            d = self.dict1
        elif which_dict == 2:
            d = self.dict2
        else:
            return None

        if key not in d:
            return None
        else:
            return d[key]

    def __jsonfy(self):
        d = dict()
        d['dict1'] = self.dict1
        d['dict2'] = self.dict2
        return d

    def __unjsonfy(self, d):
        self.dict1 = d['dict1']
        self.dict2 = d['dict2']
        return self

    def disk_write(self):
        with open(self.file_name, 'w') as out:
            json.dump(self.__jsonfy(), out)
            out.close()

    def disk_read(self):
        with open(self.file_name, 'r') as infile:
            self.__unjsonfy(json.load(infile))
            infile.close()


# block tests
def test_disk_write():
    bdict = BDict()
    bdict.insert(1, '1.html')
    bdict.insert(2, '2.html')
    bdict.disk_write()

def test_disk_read():
    bdict = BDict()
    print(bdict.dict1)
    print(bdict.dict2)


# test_disk_write()

# test_disk_read()

