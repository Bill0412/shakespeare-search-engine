import crawler


class ShakeCrawler(crawler.Crawler):
    base_uri = 'shakespeare.mit.edu'

    def __init__(self):
        super(ShakeCrawler, self).__init__(self.base_uri)

    # get all the links in the page previously crawled


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


test_crawl_relative_links()

