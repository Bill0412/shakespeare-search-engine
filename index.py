import btree
import pathlib
import json


class Term:
    def __init__(self, term):
        self.term = term
        self.times = 0
        self.occur = dict()

    def jsonfy(self):
        d = dict()
        d['term'] = self.term
        d['times'] = self.times
        d['occur'] = self.occur
        return d

    def unjsonfy(self, d):
        self.term = d['term']
        self.times = d['times']
        self.occur = d['occur']

    # define operations for the keys(terms),
    # should only compare the word(term) field
    def __lt__(self, other):
        return self.term < other.term

    def __le__(self, other):
        return self.term <= other.term

    def __gt__(self, other):
        return self.term > other.term

    def __ge__(self, other):
        return self.term >= other.term

    def __eq__(self, other):
        return self.term == other.term

    def insert(self, doc, ith):
        if self.dict.has_key(doc):
            self.dict[doc].append(ith)
        else:
            self.dict[doc] = [ith]




class Index(btree.BTree):

    def __init__(self):
        self.root_path = 'data/index'
        # if no index yet generated:
        if not pathlib.Path('data/index').is_file():
            super(Index, self).__init__(degree=3, root_file_path='data/index')
        else:  # load the root from file
            self.disk_read()





index = Index()
index.insert(Term('hi'))
index.root.display()
index.root.disk_write()

# index =