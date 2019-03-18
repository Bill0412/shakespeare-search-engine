import crawler


class ShakeCrawler(crawler.Crawler):
    base_uri = 'shakespeare.mit.edu'

    def __init__(self):
        super(ShakeCrawler, self).__init__(self.base_uri)

    # get all the links in the page previously crawled



# tests
sc = ShakeCrawler()
print(sc.crawl_page('allswell/allswell.4.1.html'))