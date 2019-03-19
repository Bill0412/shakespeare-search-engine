import btree
import pathlib
from term import Term




class Index(btree.BTree):

    def __init__(self):
        self.root_path = 'data/index'
        # if no index yet generated:
        if not pathlib.Path('data/index').is_file():
            super(Index, self).__init__(degree=3, root_file_path=self.root_path)
        else:  # load the root from file
            self.disk_read()
            self.lru_list = []


# block tests
def test_disk_write():
    index = Index()
    index.insert(Term('hi'))
    index.insert(Term('ai'))
    index.insert(Term('wow'))

    index.insert(Term('hhh'))
    index.insert(Term('before split'))
    index.insert(Term('split'))
    print('index.lru_list: ', index.lru_list)
    index.root.display()
    index.root.disk_write()
    index.root.child[0].disk_write()
    index.root.child[1].disk_write()
    index.disk_write()


def test_disk_read():
    # test_disk_write()
    index = Index()
    index.insert(Term('json again'))
    index.insert(Term('json again'))
    index.insert(Term('json again'))

    index.root.disk_write()
    index.root.child[1].disk_write()
    index.root.child[2].disk_write()
    index.disk_write()


# TODO:
#  1. Index info file update
def test_index_info_read():
    index = Index()
    print(index.lru_size)
    index.disk_write()


# test_disk_write()

test_disk_read()
# test_index_info_read()