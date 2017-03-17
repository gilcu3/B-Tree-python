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
        
        
    
    def _find_predecessor(self, key, node):
        pass
    
    def _find_succesor(self, key, node):
        pass
    
    def _delete_key_leaf(self, key, node, pos):
        pass
        
    def _merge_children_deleted_key(self, key, node, pos):
        pass
        
    def _move_node_from_left_child(self, node, pos):
        pass
    
    def _move_node_from_right_child(self, node, pos):
        pass
    
    def _merge_node_with_left_sibbling(self, node, pos):
        pass
    
    def _merge_node_with_right_sibbling(self, node, pos):
        pass
    
    
    def _delete(self, key, node):
        if node is None: return
        
        
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
        
        
        # the key to delete is here
        if mid > 0 and node.keys[mid - 1] == key:
            
            # this node is a leaf
            if node.sons[mid] is None:
                self._delete_key_leaf(key, node, mid - 1)
            # left child node has enough keys
            elif len(node.sons[mid - 1].keys) >= self.t:
                kp = _find_predecessor(key, node.sons[mid - 1])
                node.keys[mid - 1] = kp
                self._delete(kp, node.sons[mid - 1])
            # right child node has enough keys
            elif len(node.sons[mid].keys) >= self.t:
                kp = _find_succesor(key, node.sons[mid])
                node.keys[mid] = kp
                self._delete(kp, node.sons[mid])
            # both children have minimal number of keys, must combine them
            else:
                self._merge_children_deleted_key(key, node, mid - 1)
        else:
            
            # we are on a leave and haven't found the key, we have nothing to do
            if node.sons[mid] is None:
                pass
            # the amount of keys in the child is enough, simply recurse
            elif len(node.sons[mid].keys) >= self.t:
                self._delete(key, node.sons[mid])
            # we must push a key to the child
            else:
                # left sibbling has enough keys
                if mid > 0 and len(node.sons[mid - 1].keys) >= self.t:
                    self._move_node_from_left_child(node, mid)
                    self._delete(key, node.sons[mid])
                # right sibbling has enough keys
                elif mid < len(node.sons) - 1 and len(node.sons[mid + 1].keys) >= self.t:
                    self._move_node_from_right_child(node, mid)
                    self._delete(key, node.sons[mid])
                # must merge with one of sibblings
                else:
                    
                    if mid > 0:
                        self._merge_node_with_left_sibbling(node, mid)
                        self._delete(key, node.sons[mid - 1])
                    elif mid < len(node.sons) - 1:
                        self._merge_node_with_right_sibbling(node, mid)
                        self._delete(key, node.sons[mid])
                    # this shouldn't be possible
                    else:
                        assert 1 == 0
                
                
                

        
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
    #sys.setrecursionlimit(10 ** 4)
    sys.exit(main(sys.argv))
