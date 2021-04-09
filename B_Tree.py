import sys
import csv
import time
import random

sys.setrecursionlimit(10**8)
m = 5 #Max degree (order)

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

    def delete(self, key):
        self.node = self.delete_element(key, self.node)

    def delete_element(self, key, t):
        if t == None:
            return
        else:
            idx = None
            for i in range(len(t.key)):
                if t.key[i] == key:
                    idx = i
                    break
                
            #Delete leaf
            if idx != None and t.isLeaf:
                t = self.delete_Leaf(key, t)

            #Delete non leaf with more than minimum number of key
            elif idx != None and (t.child[idx+1].isLeaf == False or t.child[idx].isLeaf == False or len(t.child[idx].key) >= int(m/2) or idx != None and len(t.child[idx+1].key) >= int(m/2) or len(t.key) >= int(m/2) or t.parent == None):
                tmp = t.key[idx] #Target key
                left = t.child[idx]
                t.key[idx] = self.predecessor(tmp, left) 
                self.delete_element(tmp, left) 
            #Delete non leaf with minimum number of key
            elif idx != None:
                merge_node = Node()
                for i in range(len(t.child)):
                    for j in range(len(t.child[i].key)):
                        merge_node.key.append(t.child[i].key[j])
                t.key.pop(idx)
                self.delete_reconstruction(t, merge_node)
            #Search child node
            else:
                idx = 0
                for i in range(len(t.key)):
                    if key < t.key[i]:
                        idx = i
                        break
                    else:
                        idx = i+1
                self.delete_element(key, t.child[idx])
        
        return t

    #Reconstruct tree
    def delete_reconstruction(self, t, merge):
        if t.parent == None:
            return

        idx = self.get_index(t)
        tmp = t.parent
        tmp.child.pop(idx)

        #Max degree : 3
        if m == 3:
            if idx == 0:
                #merge with right sibling
                tmp.child[idx].key.insert(idx, tmp.key[idx])
                tmp.key.pop(idx)

                if merge != None:
                    tmp.child[idx].child.insert(idx, merge)
                    merge.parent = tmp.child[idx]

                merge = tmp.child[idx]

            else:
                #merge with left sibling
                tmp.child[idx-1].key.append(tmp.key[idx-1])
                tmp.key.pop(idx-1)

                if merge != None:
                    tmp.child[idx-1].child.append(merge)
                    merge.parent = tmp.child[idx-1]

                merge = tmp.child[idx-1]
                
        #Max degree : 5, 7 number
        else:
            if idx == 0:
                #merge with right sibling
                tmp.child[idx].key.insert(idx, tmp.key[idx])

                for i in range(len(t.key) - 1, -1, -1):
                    tmp.child[idx].key.insert(idx, t.key[i])
                    
                tmp.key.pop(idx)

                if merge != None:
                    for i in range(len(t.child) - 1, - 1, -1):   
                        tmp.child[idx].child.insert(idx, t.child[i])
                        t.child[i].parent = tmp.child[idx]

                merge = tmp.child[idx]


            else:
                #merge with left sibling
                tmp.child[idx-1].key.append(tmp.key[idx-1])
                for i in range(len(t.key)):
                    tmp.child[idx-1].key.append(t.key[i])
                    
                tmp.key.pop(idx-1) 
            
                if merge != None:
                    for i in range(len(t.child)):   
                        tmp.child[idx-1].child.append(t.child[i])
                        t.child[i].parent = tmp.child[idx-1]

                merge = tmp.child[idx-1]

        #Overflow
        if len(merge.key) >= m:
            return self.split(merge)

        #Reconstruct tree repeat
        elif len(tmp.key) < int(m/2):
            if tmp.parent != None and len(tmp.parent.key) == 0:
                tmp.key = tmp.child[0].key
                tmp.child = tmp.child[0].child
            return self.delete_reconstruction(tmp, merge)
   
    def delete_Leaf(self, key, t):
        if t.parent == None:
            return
        
        idx = self.get_index(t)
        left = None
        right = None

        #Sibling information
        if idx:
            if idx == 0:
                right = t.parent.child[idx + 1]
            elif idx == len(t.parent.child) - 1:
                left = t.parent.child[idx - 1]
            else:
                left = t.parent.child[idx - 1]
                right = t.parent.child[idx + 1]

        #Simple delete
        if int(m/2) < len(t.key):
            for i in range(len(t.key)):
                if key == t.key[i]:
                    t.key.pop(i)
                    break

        #Left sibling > minimum number of key
        elif left != None and len(t.parent.child[idx - 1].key) > int(m/2):
            #Right rotation
            for i in range(len(t.key)):
                if key == t.key[i]:
                    t.key.pop(i)
                    break
            left = t.parent.child[idx - 1]
            t.key.append(t.parent.key[idx - 1])
            t.key.sort()
            t.parent.key[idx - 1] = left.key[len(left.key) - 1]
            left.key.pop(len(left.key) - 1)

        #Right sibling > minimum number of key
        elif right != None and len(t.parent.child[idx + 1].key) > int(m/2):
            #Left rotation
            for i in range(len(t.key)):
                if key == t.key[i]:
                    t.key.pop(i)
                    break
            right = t.parent.child[idx + 1]
            t.key.append(t.parent.key[idx])
            t.key.sort()
            t.parent.key[idx] = right.key[0]
            right.key.pop(0)

        #Parent > minimum number of key
        elif len(t.parent.key) > int(m/2):
            #Delete key
            for i in range(len(t.key)):
                if key == t.key[i]:
                    t.key.pop(i)
                    break
                    
            #Merge
            if idx == 0:
                t.parent.child[idx+1].key.insert(idx, (t.parent.key[idx]))
                for i in range(len(t.key) - 1, -1, -1):
                    t.parent.child[idx+1].key.insert(idx, t.key[i])
                t.parent.key.pop(idx)
                t.parent.child.pop(idx)                            
                            
            else:
                left = t.parent.child[idx - 1]
                left.key.append(t.parent.key[idx - 1])
                for i in range(len(t.key)):
                    left.key.append(t.key[i])
                t.parent.key.pop(idx - 1)
                t.parent.child.pop(idx)

        #Parent, Left, Right < minimum number of key
        #Reconstruction
        else:
            for i in range(len(t.key)):
                if key == t.key[i]:
                    t.key.pop(i)
                    break
            self.delete_reconstruction(t, None)

        return t

    #Get left sibling's max key
    def predecessor(self, target, t):
        if t.isLeaf:
            tmp = t.key.pop(-1)
            t.key.append(target)
            return tmp
        else:
            return self.predecessor(target, t.child[-1])
        
    #get parent index about current node
    def get_index(self, t):
        if t.parent:
            return t.parent.child.index(t)
        else:
            return None
        
    #Inorder traverse for search
    def search_traverse(self, t):
        #Search
        for i in range(len(t.key)):
            if t.child:
                self.search_traverse(t.child[i])
            res.append(t.key[i])
        if t.child:
            self.search_traverse(t.child[i+1])

    #Check for search
    def search_check(self, key, t):
        idx = 0
        for i in range(len(t.key)):
            if key <= t.key[i]:
                idx = i
                break
            else:
                idx = i + 1

        if idx < len(t.key) and key == t.key[idx]:
            res.append(t.key[idx])
        elif t.isLeaf:
            res.append([key[0], "N/A"])
        else:
            self.search_check(key, t.child[idx])



    
def main_display():
    while(1):
        print("---------------------------------------------")
        print("|                                           |")
        print("|                                           |")
        print("|                 <B Tree>                  |")
        print("|                                           |")
        print("|                                           |")
        print("|                                           |")
        print("---------------------------------------------\n")
        print("1. Insertion")
        print("2. Deletion")
        print("3. Quit\n")
        print("Input : ", end = '')
        x = int(input())
        if x == 1:
            a = B_Tree()
            main_insert(a)
        elif x == 2:
            main_delete(a)
        elif x == 3:
            return
        else:
            print("\nError : Wrong input! Try again\n")

def main_insert(a):
    print("\n--------------<Insert section>---------------\n")
    print("Input csv file name (Ex. input, input2)")
    print("-> ", end='')
    insert_file_name = input()

    try:
        global data
        #Read csv
        f = open(insert_file_name + ".csv", 'r', encoding='utf-8')
        file = csv.reader(f, delimiter = '\t')
        data = list(file)
        for i in range(len(data)):
            data[i][0] = int(data[i][0])
    except:
        print("\nError : Wrong file name!\n")
        return
        
    start = time.time() #Time check

    #Insert
    for i in range(len(data)):
        a.insert(data[i])

    global res
    res = []
    
    #Search
    #a.search_traverse(a.node)
    for i in range(len(data)):
        a.search_check(data[i], a.node)
        
    #Write csv
    with open(insert_file_name + "_result.csv", 'w', newline='') as f:
        csvwriter = csv.writer(f, delimiter = '\t')
        for i in res:
            csvwriter.writerow(i)

    print("\n" + insert_file_name + ".csv Done! -> time : {} \n\n".format(time.time() - start))
            
    #Insertion compare
    try:
        fffff = open(insert_file_name + "_result.csv", 'r', encoding='utf-8')
        fffffile = csv.reader(fffff, delimiter = '\t')
        new_insert_data = list(fffffile)
        for i in range(len(new_insert_data)):
            new_insert_data[i][0] = int(new_insert_data[i][0])
    except:
        print("\nError : Wrong file name!\n")
        return

    cnt = 0
    for i in range(len(data)):
        if new_insert_data[i] != data[i]:
            cnt += 1

    print("\nIn insertion, number of wrong data : {}\n\n".format(cnt))



def main_delete(a):
    print("\n--------------<Delete section>---------------\n")
    print("Input csv file name (Ex. delete, delete2)")
    print("-> ", end='')
    delete_file_name = input()

    #Read csv
    try:
        ff = open(delete_file_name + ".csv", 'r', encoding='utf-8')
        ffile = csv.reader(ff, delimiter = '\t')
        delete_data = list(ffile)
        for i in range(len(delete_data)):
            delete_data[i][0] = int(delete_data[i][0])
    except:
        print("\nError : Wrong file name!\n")
        return
    
    start = time.time() #Time check
        
    for i in range(len(delete_data)):
        a.delete(delete_data[i])

    global res
    res = []

    for i in range(len(data)):
        a.search_check(data[i], a.node)

    #Write csv
    with open("New_" + delete_file_name + "_result.csv", 'w', newline='') as f:
        csvwriter = csv.writer(f, delimiter = '\t')
        for i in res:
            csvwriter.writerow(i)

    print("\n" + delete_file_name + ".csv Done! -> time : {} \n\n".format(time.time() - start))

    
    #For compare    
    print("Input result csv file name (Ex. delete_result, delete_result2)")
    print("-> ", end='')
    origin_delete_file_name = input()

    #Read original result csv for compare
    try:
        fff = open(origin_delete_file_name + ".csv", 'r', encoding='utf-8')
        fffile = csv.reader(fff, delimiter = '\t')
        origin_delete_data = list(fffile)
        for i in range(len(origin_delete_data)):
            origin_delete_data[i][0] = int(origin_delete_data[i][0])
    except:
        print("\nError : Wrong file name!\n")
        return

    #Read new result csv for compare
    try:
        ffff = open("New_" + delete_file_name + "_result.csv", 'r', encoding='utf-8')
        ffffile = csv.reader(ffff, delimiter = '\t')
        new_delete_data = list(ffffile)
        for i in range(len(new_delete_data)):
            new_delete_data[i][0] = int(new_delete_data[i][0])
    except:
        print("\nError : Wrong file name!\n")
        return

    cnt = 0
    for i in range(len(origin_delete_data)):
        #print(new_delete_data[i])
        #print(origin_delete_data[i])
        if new_delete_data[i] != origin_delete_data[i]:
            cnt += 1

    print("\nIn deletion, number of wrong data : {}\n\n".format(cnt))
         
if __name__ == "__main__":
    main_display()
