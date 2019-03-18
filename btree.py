class Node:
    def __init__(self, is_leaf):
        self.is_leaf = is_leaf
        self.n_keys = 0
        self.keys = []
        self.child = []

    def display(self):
        print('is_leaf: ', self.is_leaf)
        print('keys: ', self.keys[0:self.n_keys])
        print('child: ', self.child)
        print("n_keys: ", self.n_keys)
        print("len(keys): ", len(self.keys))
        print('\n')


class BTree:
    def __init__(self, degree):
        self.root = Node(True) # root: a leaf node
        self.degree = degree  # degree = 2, 2-3-4 tree
        # DISK-WRITE(self.root)

    def __search(self, node, search_key):
        # find the bigger or equal key on the tree
        i = 0
        while i < node.n_keys and search_key > self.keys[i]:
            i += 1

        # when search_key >= self.keys[i]
        # if this is a leaf node
        if i < node.n_keys and search_key == self.keys[i]:
            return node, i
        elif node.is_leaf:
            return None
        else:
            # DISK-READ(node.child[i])
            return self.__search(node.child[i], search_key)

    def __split_child(self, node, ith_child):
        left_child = node.child[ith_child]
        right_child = Node(left_child.is_leaf)  # right sub of the tree, newly created
        right_child.n_keys = self.degree - 1
        for j in range(0, self.degree - 1):
            right_child.keys.append(left_child.keys[j + self.degree])
        if not left_child.is_leaf:
            for j in range(0, self.degree):
                right_child.child.append(left_child.child[j + self.degree])
        left_child.n_keys = self.degree - 1  # dummy deletion

        # shift relative right ones in node one place right

        if ith_child == node.n_keys:  # if it is the end child
            # if there's no dummy space
            if len(node.keys) == node.n_keys:
                node.child.append(right_child)
                node.keys.append(left_child.keys[self.degree - 1])  # use the first dummy node, i.e. the new root
            else:
                node.child[node.n_keys + 1] = right_child
                node.keys[node.n_keys] = left_child.keys[self.degree - 1]
            node.n_keys += 1
            return

        # if no dummy space
        if len(node.keys) == node.n_keys:
            node.child.append(node.child[node.n_keys])
        else:  # dummy space remaining
            node.child[node.n_keys + 1] = node.child[node.n_keys]

        for j in range(node.n_keys - 1, ith_child, -1):
            node.child[j + 1] = node.child[j]
        node.child[ith_child + 1] = right_child

        # shift keys one place right
        # if no dummy space
        if len(node.keys) == node.n_keys:
            node.keys.append(node.chid[node.n_keys - 1])
        else:
            node.keys[node.n_keys] = node.chid[node.n_keys - 1]
        for j in range(node.n_keys - 1, ith_child - 1, -1):
            node.keys[j + 1] = node.keys[j]
        node.keys[ith_child] = left_child.keys[self.degree - 1]
        node.n_keys += 1
        # DISK-WRITE(node)
        # DISK-WRITE(left_child)
        # DISK-WRITE(right_child)

    def __insert_nonfull(self, node, key):
        # base case, if it is empty root
        if node.n_keys == 0:
            node.keys.append(key)
            node.n_keys += 1
            return

        i = node.n_keys - 1  # the last node

        # base case, insert directly
        if node.is_leaf:
            # if key is the biggest, insert at the right side directly
            if key > node.keys[node.n_keys - 1]:
                # if no dummy space
                if len(node.keys) == node.n_keys:
                    node.keys.append(key)
                else:
                    node.keys[node.n_keys] = key
                node.n_keys += 1
                return
            else:
                if len(node.keys) == node.n_keys:  # no dummy space
                    node.keys.append(node.keys[node.n_keys - 1])  # 0 .. n_keys after appending
                else:
                    node.keys[node.n_keys] = node.keys[node.n_keys - 1]

                if i == 0:
                    node.keys[0] = key
                    node.n_keys += 1
                    return

                while i >= 1 and key < node.keys[i]:
                    node.keys[i] = node.keys[i - 1]
                    i -= 1

                node.keys[i + 1] = key  # replace the 'i-1' above

                node.n_keys += 1
            # DISK-WRITE(node)
        else:
            # key >= ith key, go to the (i+1)th child
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1
            # DISK-READ(node.child[i + 1])
            if node.child[i].n_keys == (2 * self.degree - 1):
                self.__split_child(node, i)
                if key > node.keys[i]:
                    i += 1
            # print("ith-child: ", i)
            self.__insert_nonfull(node.child[i], key)

    def search(self, search_key):
        self.__search(self.root, search_key)

    def insert(self, key):
        root = self.root
        if self.root.n_keys == 2 * self.degree - 1:
            self.root = Node(False)
            self.root.child.append(root)
            self.__split_child(self.root, 0)
            self.__insert_nonfull(self.root, key)
        else:
            self.__insert_nonfull(root, key)


# TODO:
#  (DONE) 1. solve dummy deletion and later append conflict
#  - compare list length with the length in the record
#  2. Tests on higher degree B Tree


# ## block test
# btree = BTree(2)
# btree.insert(1)
# btree.insert(6)
# # insert between
# btree.insert(4)
#
# # should split child
# btree.insert(7)
#
# # another split right side
# btree.insert(9)
# btree.insert(5)
# #
#
# btree.insert(8)
# btree.insert(10)
# btree.insert(11)
# btree.insert(12)
# #print("inserting 2:")
# #btree.insert(2)
#
# btree.root.display()
# for c in btree.root.child:
#     c.display()





