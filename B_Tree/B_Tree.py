import sys
import csv
import time
import random

sys.setrecursionlimit(10**8)
m = 3 #Max degree (order)

class Node:
    def __init__(self):
        self.parent = None
        self.child = [] 
        self.key= [] 
        self.isLeaf = True

class B_Tree:
    def __init__(self):
        self.node = None
    
    def insert(self, key):
        self.node = self.insert_element(key, self.node)
            
    def insert_element(self, key, t):
        if t == None:
            t = Node()
            t.key.append(key)
        else:
            #Leaf node
            if t.isLeaf:
                t.key.append(key)
                t.key.sort()
                #Check overflow
                if len(t.key) == m:
                    t = self.split(t)
            #Not leaf node
            else:
                #Find index
                idx = 0
                for i in range(len(t.key)):
                    if key < t.key[i]:
                        idx = i
                        break
                    else:
                        idx = i+1
                self.insert_element(key, t.child[idx])
                #Check overflow
                if len(t.key) == m:
                    t = self.split(t)

        return t

    def split(self, t):
        idx = int(m/2)
        #Root node
        if t.parent == None:
            t.parent = Node()

            #Parent Node
            tmp = t.parent
            tmp.key.append(t.key[idx])
            tmp.isLeaf = False

            #Make new node
            left = Node()
            right = Node()

            #Insert key
            for i in range(idx):
                left.key.append(t.key[i])
            for i in range(idx+1, len(t.key)):
                right.key.append(t.key[i])
                
            #Check child
            if t.child:
                left.isLeaf = False
                right.isLeaf = False
                for i in range(idx+1):
                    left.child.append(t.child[i])
                    t.child[i].parent = left
                for i in range(idx+1, len(t.child)):
                    right.child.append(t.child[i])
                    t.child[i].parent = right
                
            #Connect node
            left.parent = tmp
            right.parent = tmp
            
            tmp.child.append(left)
            tmp.child.append(right)
        
            return tmp
        
        else:
            #Parent node
            tmp = t.parent
            tmp.key.append(t.key[idx])
            tmp.key.sort()
            tmp.isLeaf = False
            
            #Make new node
            left = Node()
            right = Node()

            #Insert key
            for i in range(idx):
                left.key.append(t.key[i])
            for i in range(idx+1, len(t.key)):
                right.key.append(t.key[i])
                
            #Child check
            if t.child:
                left.isLeaf = False
                right.isLeaf = False
                for i in range(idx+1):
                    left.child.append(t.child[i])
                    t.child[i].parent = left
                for i in range(idx+1, len(t.child)):
                    right.child.append(t.child[i])
                    t.child[i].parent = right

            #Connect node
            left.parent = tmp
            right.parent = tmp

            k = tmp.child.index(t)
            tmp.child.pop(k)
            tmp.child.insert(k, left)
            tmp.child.insert(k + 1, right)
            
            return tmp
    
    def search(self, t):
        #Search
        for i in range(len(t.key)):
            if t.child:
                self.search(t.child[i])
            res.append(t.key[i])
        if t.child:
            self.search(t.child[i+1])

if __name__ == "__main__":
    start = time.time() #Time check

    #Read csv
    f = open('input.csv', 'r', encoding='utf-8')
    file = csv.reader(f, delimiter = '\t')
    data = list(file)
    for i in range(len(data)):
        data[i][0] = int(data[i][0])

    a = B_Tree()

    #Insert
    for i in range(len(data)):
        a.insert(data[i])
    
    res = []
    #Search
    a.search(a.node)

    #Write csv
    with open('input_result.csv', 'w', newline='') as f:
        csvwriter = csv.writer(f, delimiter = '\t')
        for i in res:
            csvwriter.writerow(i)
            
    print("input.csv Done! -> time : ", time.time() - start)

    print("\n---------------------------------------------------\n")

    start = time.time() #Time check

    #Read csv
    f = open('input2.csv', 'r', encoding='utf-8')
    file = csv.reader(f, delimiter = '\t')
    data = list(file)
    for i in range(len(data)):
        data[i][0] = int(data[i][0])

    a = B_Tree()
        
    #Insert    
    for i in range(len(data)):
        a.insert(data[i])
    
    res = []
    #Search
    a.search(a.node)

    #Write csv
    with open('input2_result.csv', 'w', newline='') as f:
        csvwriter = csv.writer(f, delimiter = '\t')
        for i in res:
            csvwriter.writerow(i)
            
    print("input2.csv Done! -> time : ", time.time() - start)
