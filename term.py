class Term:
    def __init__(self, term=None):
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
        return self

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

