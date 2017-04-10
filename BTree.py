#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

class BTree:
    
    class Node:
        
        def __init__(self):
            self.sons = []
            self.keys = []

        def __repr__(self):
            return 'Node' + str(self.keys) + str(self.sons)
        
        def _lower_bound(self, key):
            b = 0
            e = len(self.sons) - 1
            while b < e:
                mid = (b + e + 1) // 2
                if mid == 0: # mid is never 0 actually
                    pass
                elif self.keys[mid - 1] <= key:
                    b = mid
                else:
                    e = mid - 1
            return b

    def __init__(self, t):
        self.root = self.Node()
        self.t = t
    
    
    def _preorder(self, cur):
        if cur == None: return
        yield cur
        for son in cur.sons:
            yield from self._preorder(son)
    
    
    def preorder(self):
        yield from self._preorder(self.root)
        
                
                
    def _split(self, node, parnode, pos):
        
        # root case
        if parnode is None:
            self.root = self.Node()
            left = self.Node()
            right = self.Node()
            left.keys = node.keys[:self.t - 1]
            right.keys = node.keys[self.t:]
            left.sons = node.sons[:self.t]
            right.sons = node.sons[self.t:]
            self.root.keys = [ node.keys[self.t - 1] ]
            self.root.sons = [left, right]
            return self.root
        else:
            left = self.Node()
            right = self.Node()
            left.keys = node.keys[:self.t - 1]
            right.keys = node.keys[self.t:]
            left.sons = node.sons[:self.t]
            right.sons = node.sons[self.t:]
            parnode.keys = parnode.keys[:pos] + [ node.keys[self.t - 1] ] + parnode.keys[pos:]
            parnode.sons = parnode.sons[:pos] + [left, right] + parnode.sons[pos + 1:]
            
        
        
    def _insert(self, key, node, parnode):
        if node is None: return None

        # node is full, and must be root
        if len(node.keys) == 2 * self.t - 1:
            assert node == self.root
            node = self._split(node, parnode, -1)
            assert len(node.keys) == 1
            
            # to the right
            if node.keys[0] <= key:
                self._insert(key, node.sons[1], node)
            else:
                self._insert(key, node.sons[0], node)
            
            return
        
        # only possible for root at the beginning
        if len(node.sons) == 0:
            assert node == self.root
            node.sons.append(None)
            node.keys.append(key)
            node.sons.append(None)
        
            return
        
        
        pos = node._lower_bound(key)

        
        # we are in a leaf
        if node.sons[pos] is None:
            node.keys = node.keys[:pos] + [key] + node.keys[pos:]
            node.sons.append(None)
        else:
            
            # son is full, doing split from here
            if node.sons[pos] is not None and len(node.sons[pos].keys) == 2 * self.t - 1:
                self._split(node.sons[pos], node, pos)
                # go to right
                if node.keys[pos] <= key:
                    self._insert(key, node.sons[pos + 1], node)
                else:
                    self._insert(key, node.sons[pos], node)
            else:
                self._insert(key, node.sons[pos], node)

    
    
    def insert(self, key):
        self._insert(key, self.root, None)
    
    
    def _find(self, key, node):
        if node is None or len(node.sons) == 0:
            return None
        
        
        pos = node._lower_bound(key)

        
        if pos >= 1 and node.keys[pos - 1] == key:
            return node.keys[pos - 1]
        else:
            return self._find(key, node.sons[pos])
         
         
    def find(self, key):
        return self._find(key, self.root)
        
        
    
    def _find_predecessor(self, key, node):
        if node.sons[0] == None:
            return node.keys[-1]
        else:
            return self._find_predecessor(key, node.sons[-1])
    
    def _find_succesor(self, key, node):
        if node.sons[0] == None:
            return node.keys[0]
        else:
            return self._find_succesor(key, node.sons[0])
    
    def _delete_key_leaf(self, key, node, pos):
        
        # condition for correctness of algorithm
        assert node == self.root or len(node.sons) >= self.t
        
        assert node.keys[pos] == key
        
        node.keys = node.keys[:pos] + node.keys[pos + 1:]
        node.sons.pop()
        
        
    def _merge_children_around_key(self, key, node, pos):
        
        assert pos >= 0 and pos < len(node.sons) - 1
        
        y = self.Node()
        y.sons = node.sons[pos].sons + node.sons[pos + 1].sons
        y.keys = node.sons[pos].keys + [node.keys[pos]] + node.sons[pos + 1].keys
        
        node.keys = node.keys[:pos] + node.keys[pos + 1:]
        node.sons = node.sons[:pos] + [y] + node.sons[pos + 2:]
        
        
    def _move_node_from_left_child(self, node, pos):
        
        
        
        assert pos > 0 and len(node.sons[pos - 1].keys) >= self.t
        
        
        node.sons[pos].keys = [node.keys[pos - 1] ] + node.sons[pos].keys
        node.sons[pos].sons = [ node.sons[pos - 1].sons[-1] ] + node.sons[pos].sons
        
        node.keys[pos - 1] = node.sons[pos - 1].keys[-1]
        
        node.sons[pos - 1].sons = node.sons[pos - 1].sons[:-1]
        node.sons[pos - 1].keys = node.sons[pos - 1].keys[:-1]
        

    
    def _move_node_from_right_child(self, node, pos):
        
        
        assert pos < len(node.sons) - 1 and len(node.sons[pos + 1].keys) >= self.t
        
        
        node.sons[pos].keys = node.sons[pos].keys + [node.keys[pos] ]
        node.sons[pos].sons =  node.sons[pos].sons + [ node.sons[pos + 1].sons[0] ] 
        
        node.keys[pos] = node.sons[pos + 1].keys[0]
        
        node.sons[pos + 1].sons = node.sons[pos + 1].sons[1:]
        node.sons[pos + 1].keys = node.sons[pos + 1].keys[1:]
        
        
        
    def _fix_empty_root(self, node):
        if node == self.root and len(node.sons) == 1:
            self.root = node.sons[0]
            return self.root
        else:
            return node
    
    
    def _delete(self, key, node):
        if node is None or len(node.sons) == 0: return
        
        
        pos = node._lower_bound(key)
        
        
        # the key to delete is here
        if pos > 0 and node.keys[pos - 1] == key:
            
            # this node is a leaf
            if node.sons[pos] is None:
                self._delete_key_leaf(key, node, pos - 1)
            # left child node has enough keys
            elif len(node.sons[pos - 1].keys) >= self.t:
                kp = self._find_predecessor(key, node.sons[pos - 1])
                node.keys[pos - 1] = kp
                self._delete(kp, node.sons[pos - 1])
            # right child node has enough keys
            elif len(node.sons[pos].keys) >= self.t:
                kp = self._find_succesor(key, node.sons[pos])
                node.keys[pos - 1] = kp
                self._delete(kp, node.sons[pos])
            # both children have minimal number of keys, must combine them
            else:
                self._merge_children_around_key(key, node, pos - 1)
                
                # here I should take care of missing root
                node = self._fix_empty_root(node)
                
                self._delete(key, node)
        else:
            
            # we are on a leave and haven't found the key, we have nothing to do
            if node.sons[pos] is None:
                pass
            # the amount of keys in the child is enough, simply recurse
            elif len(node.sons[pos].keys) >= self.t:
                self._delete(key, node.sons[pos])
            # we must push a key to the child
            else:
                # left sibbling has enough keys
                if pos > 0 and len(node.sons[pos - 1].keys) >= self.t:
                    self._move_node_from_left_child(node, pos)
                    self._delete(key, node.sons[pos])
                # right sibbling has enough keys
                elif pos < len(node.sons) - 1 and len(node.sons[pos + 1].keys) >= self.t:
                    self._move_node_from_right_child(node, pos)
                    self._delete(key, node.sons[pos])
                # must merge with one of sibblings
                else:
                    
                    if pos > 0:
                        self._merge_children_around_key(key, node, pos - 1)
                        
                        # here I should take care of missing root
                        node = self._fix_empty_root(node)
                        
                        self._delete(key, node)
                    elif pos < len(node.sons) - 1:
                        self._merge_children_around_key(key, node, pos)
                        
                        # here I should take care of missing root
                        node = self._fix_empty_root(node)
                        
                        self._delete(key, node)
                    # this shouldn't be possible
                    else:
                        assert False
                
                
                

        
    def delete(self, key):
        self._delete(key, self.root)
        
        
    
    
    def _find_all(self, key, node, ans):
        if node is None or len(node.sons) == 0: return
        b = 0
        e = len(node.sons) - 1
        while b < e:
            mid = (b + e + 1) // 2
            if mid == 0: # mid is never 0 actually
                pass
            elif node.keys[mid - 1] < key:
                b = mid
            else:
                e = mid - 1
        
        left = b
        
        
        b = 0
        e = len(node.sons) - 1
        while b < e:
            mid = (b + e + 1) // 2
            if mid == 0: # mid is never 0 actually
                pass
            elif node.keys[mid - 1] > key:
                e = mid - 1
            else:
                b = mid
        right = b
        
        # print(left, right, len(node.sons))
        for i in range(left, right + 1):
            self._find_all(key, node.sons[i], ans)
            
            if i < right:
                assert node.keys[i] == key
                ans.append(node.keys[i])
        
    
    def find_all(self, key):
        ans = []
        self._find_all(key, self.root, ans)
        return ans 
    
        

def dummy_test0():
    T = BTree(6)
    rng = list(range(9000))
    shuffle(rng)
    for i in rng:
        T.insert(i)
        #print(T.root, '\n')
    
    for i in range(9):
        print(T.find(i), '\n')

def dummy_test1():
    T = BTree(3)
    for i in range(9):
        T.insert(i)
    print(T.root)
    T.delete(5)
    print(T.root)
    T.delete(4)
    print(T.root)
    T.insert(100)
    T.insert(101)
    T.insert(3)
    T.insert(3)
    T.insert(3)
    print(T.root)
    T.delete(1)
    print(T.root)
    
    
def dummy_test2():
    T = BTree(3)
    for _ in range(10):
        T.insert(0)
    T.insert(1)
    T.insert(2)
    T.insert(-1)
    print(T.root)
    ans = T.find_all(0)
    print(len(ans), ans)


import random
import collections
def map_test():
    '''
    It's purpose is to compare againt map implementation
    '''
    seed = random.randint(0, 1000)
    print('random seed %d' % seed)
    # seed = 195
    random.seed(seed)
    num_tests = 10000
    num_ops = 200
    debug = False
    for deg in range(2, 20):
        
        for test in range(num_tests):
            B = BTree(deg)
            M = collections.defaultdict(int)
            if debug: print('Beginning block of tests %d %d' % (deg, test))
            for _ in range(num_ops):
                if debug: print(B.root)
                prob = random.random()
                elem = random.randint(0, 10)
                if prob < 1 / 3: # insert
                    if debug: print('insert %d' % elem)
                    B.insert(elem)
                    M[elem] += 1
                elif prob < 1/3 + 1/3: # find
                    if debug: print('find %d' % elem)
                    r1 = (B.find(elem) != None)
                    r2 = (elem in M and M[elem] > 0)
                    if r1 != r2:
                        print(B.root)
                        print(r1, r2, elem)
                    assert r1 == r2
                elif prob < 1/3 + 1/3 + 1/6: # findall
                    if debug: print('findall %d' % elem)
                    r1 = len(B.find_all(elem))
                    if elem not in M:
                        r2 = 0
                    else:
                        r2 = M[elem]
                    if r1 != r2:
                        print(B.root)
                        print(r1, r2, elem)
                    assert r1 == r2
                else: # delete
                    if debug: print('delete %d' % elem)
                    if elem in M and M[elem] > 0:
                        M[elem] -= 1
                    B.delete(elem)
            if debug: print('Block finished correctly')
def dummy_tests():
    map_test()


def main(args):
    '''
    Testing BTree Implementation
    '''
    
    dummy_tests()
    return 0

if __name__ == '__main__':
    import sys
    #sys.setrecursionlimit(10 ** 4)
    sys.exit(main(sys.argv))
