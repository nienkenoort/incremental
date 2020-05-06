class Node(object):
    def __init__(self, d, n = None, p = None):
        self.data = d
        self.next = n
        self.prev = p
    
    def get_next(self):
        return self.next
    
    def get_prev(self):
        return self.prev

    def set_next(self, n): #set the next pointer
        self.next = n
    
    def set_prev(self, p): #set the previous pointer
        self.prev = p
    
    def get_data(self):
        return self.data
    
    def set_data(self, d):
        self.data = d

class LinkedList(object):
    def __init__(self, r = None):
        self.root = r
        self.size = 0 #Y?

    def get_size(self):
        return self.size
    
    def add(self, d):
        new = Node(d, self.root) #add root as new next node
        if self.root:
            self.root.set_prev(new)
        self.root = new
        self.size += 1
    
    def remove(self, d):
        current_node = self.root
        while current_node: #when we find a node we want to delete, reform the pointers
            if current_node.get_data() == d:
                next_node = current_node.get_next()
                prev_node = current_node.get_prev()

                if next_node: #if next_node exists, so if it is not None
                    next_node.set_prev(prev_node)
                if prev_node: #if prev_node exists
                    prev_node.set_next(next_node)
                else: #if both are None, set the current node as the root node
                    self.root = current_node
                self.size -= 1
                return True #data is removed
            else: 
                current_node = current_node.get_next() 
        return False #data not found
        