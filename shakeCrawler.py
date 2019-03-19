from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import nltk
import ssl
import string

import crawler
from index import Index
from term import Term
from bdict import BDict


try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('punkt')
nltk.download('stopwords')


class ShakeCrawler(crawler.Crawler):
    base_uri = 'shakespeare.mit.edu'

    def __init__(self):
        super(ShakeCrawler, self).__init__(self.base_uri)
        self.index = Index(30)
        self.bdict = BDict()

    # get all the links in the page previously crawled
    # 2 levels crawling

    # index the shakespeare page by levels
    def crawl_all(self):
        # get relative links of the level 0 index
        self.get_relative_links('')

        self.__crawl_news_html()

        # self.__crawl_first3_colums()
        #
        # self.__crawl_poetry()

    # analyze by term
    def analyze_page(self, relative_link, link_index):
        # from html recognize paragraphs
        html = self.crawl_html(relative_link)
        soup = BeautifulSoup(html, 'html.parser')
        page = soup.find('title').getText() + soup.find('p').getText()
       # print(page)

        word_tokens = word_tokenize(page)
        # print(word_tokens)

        stop_words = set(stopwords.words('english'))

        stop_words_filtered = [word for word in word_tokens if word[0] not in string.punctuation]

        ps = PorterStemmer()

        # filter stop_words & word stemming
        filtered_words = [ps.stem(word).strip('.') for word in stop_words_filtered if word not in stop_words]

        # print(filtered_words)
        # for comparison
        # print([word for word in stop_words_filtered if word not in stop_words])

        # insert the term
        # a. if word is not indexed, index the word, the word occurrence
        # b. if indexed, word occurrence
        count = 0
        for word in filtered_words:
            term = Term(word)
            search_info = self.index.search(term)
            if search_info:
                node, ith_key = search_info
            else:
                node, ith_key = self.index.insert(term)

            # update the term node info
            # print('ith_key', ith_key)

            node.keys[ith_key].insert(link_index, count)
            # print('link_index', link_index)
            count += 1







    def __crawl_news_html(self):
        # print()
        pass




# block tests
def test_crawl_html():
    sc = ShakeCrawler()
    print(sc.crawl_html('allswell/allswell.4.1.html'))


def test_crawl_relative_links():
    sc = ShakeCrawler()
    # get the links on the first page
    print(sc.get_relative_links(''))

    # when no link on the page
    print(sc.get_relative_links('allswell/allswell.4.1.html'))

def test_analyze_page():
    sc = ShakeCrawler()
    if not sc.bdict.is_page_crawled(1):
        sc.analyze_page('news.html', sc.bdict.insert_new_link('news.html'))

# test_crawl_relative_links()


test_analyze_page()