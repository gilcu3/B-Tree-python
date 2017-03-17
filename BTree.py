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
        
        
        b = 0
        e = len(node.sons) - 1
        while b < e:
            mid = (b + e + 1) // 2
            if mid == 0: # mid is never 0 actually
                pass
            elif node.keys[mid - 1] <= key:
                b = mid
            else:
                e = mid - 1
        
        # we are in a leaf
        if node.sons[b] is None:
            node.keys = node.keys[:b] + [key] + node.keys[b:]
            node.sons.append(None)
        else:
            
            # son is full, doing split from here
            if node.sons[b] is not None and len(node.sons[b].keys) == 2 * self.t - 1:
                self._split(node.sons[b], node, b)
                # go to right
                if node.keys[b] <= key:
                    self._insert(key, node.sons[b + 1], node)
                else:
                    self._insert(key, node.sons[b], node)
            else:
                self._insert(key, node.sons[b], node)

    
    
    def insert(self, key):
        self._insert(key, self.root, None)
    
    
    def _find(self, key, node):
        if node is None:
            return None
        
        
        b = 0
        e = len(node.sons) - 1
        while b < e:
            mid = (b + e + 1) // 2
            if mid == 0: # mid is never 0 actually
                pass
            elif node.keys[mid - 1] <= key:
                b = mid
            else:
                e = mid - 1
        
        if b >= 1 and node.keys[b - 1] == key:
            return node
        
        return self._find(key, node.sons[b])
         
         
    def find(self, key):
        return self._find(key, self.root)
        
    def _delete(self, key, node):
        if node is None: return
        pass
        
    def delete(self, key):
        self._delete(key, self.root)
        

from random import shuffle
def main(args):
    '''
    Testing BTree Implementation
    '''
    T = BTree(6)
    rng = list(range(9000))
    shuffle(rng)
    for i in rng:
        T.insert(i)
        #print(T.root, '\n')
    
    for i in range(9):
        print(T.find(i), '\n')
    return 0

if __name__ == '__main__':
    import sys
    sys.setrecursionlimit(10 ** 4)
    sys.exit(main(sys.argv))
