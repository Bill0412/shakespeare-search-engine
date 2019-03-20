from index import Index
from term import Term
import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import ssl
import string
import json


try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('punkt')
nltk.download('stopwords')
index = Index()
# only one term supported
def query(search_term):

    word_tokens = word_tokenize(search_term)

    stop_words = set(stopwords.words('english'))

    punctuation_filtered = [word for word in word_tokens if word[0] not in string.punctuation]

    ps = PorterStemmer()

    # filter stop_words & word stemming
    filtered_words = [ps.stem(word).strip('.') for word in punctuation_filtered if word not in stop_words]

    if not filtered_words:
        filtered_words = search_term

    if not filtered_words:
        return None

    result = []
    for term in filtered_words:
        r = index.search(Term(term))
        if r:
            node, ith_child = r
        result += node.keys[ith_child].get_links()

    # add full.html
    base_uri = 'http://shakesepare.mit.edu/'
    pre_len = len(base_uri)
    full2 = []
    with open('data/full', 'r') as infile:
        full = json.load(infile)['full']

        for r in result:
            sub_dir = r[pre_len:]
            sub_dir = sub_dir[0:sub_dir.find('/')]
            if sub_dir in full:
                full_link = base_uri + sub_dir + '/full.html'
                full2.append(full_link)
    result += full2
    # sort by occurrence
    result.sort(key=lambda x: x[1], reverse=True)
    return [r[0] for r in result]

print(query('love'))