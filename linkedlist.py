#Author: Nienke Noort 
#Student number (Utrecht University): 6200451
#Supervisor: Gijs J. Wijnholds
#The code in the current file was found on https://github.com/joeyajames/Python/blob/master/LinkedLists/DoublyLinkedList1.py and was written by Joe James.

class Node(object):
    """
    A class used to build nodes with their next and previous nodes (thus also saving their neighbours).

    ...

    Attributes
    ----------
    data : str
        the value of the current node
    next : str
        the value of the next neighbouring node (default None)
    prev : str
        the value of the previous neighbouring node (default None)

    Methods
    -------
    get_next()
        Returns the next neighbour of the current node
    get_prev()
        Returns the previous neighbour of the current node
    set_next()
        Change the value of the next neighbour to the value of parameter "n" that was given when creating an object of the class
    set_prev()
        Change the value of the previous neighbour to the value of parameter "p" that was given when creating an object of the class
    get_data()
        Returns the data of the current node
    set_data()
        Change the value of the data of the current node to the value of parameter "d" that was given when creating an object of the class
    """
    def __init__(self, d, n = None, p = None):
        """
        Parameters
        ----------
        d : str
            The value of the current node
        n : str
            The value of the next neighbouring node (default None)
        p : str
            The value of the previous neighbouring node (default None)
        """
        self.data = d
        self.next = n
        self.prev = p
    
    def get_next(self):
        """
        Used to get the value of the next neighbouring node.

        Returns
        -------
        str
            a string containing the value of the next neighbouring node.
        """
        return self.next
    
    def get_prev(self):
        """
        Used to get the value of the previous neighbouring node.

        Returns
        -------
        str
            a string containing the value of the previous neighbouring node.
        """
        return self.prev

    def set_next(self, n): #Set the next pointer
        """
        Used to set the value of the next neighbouring node to the value of parameter "n" that was given when an object of the class was created.

        Parameters
        ----------
        n : str
            The value of the next neighbouring node
        """
        self.next = n
    
    def set_prev(self, p): #Set the previous pointer
        """
        Used to set the value of the previous neighbouring node to the value of parameter "p" that was given when an object of the class was created.

        Parameters
        ----------
        p : str
            The value of the previous neighbouring node
        """
        self.prev = p
    
    def get_data(self):
        """
        Used to get the value of the current node.

        Returns
        -------
        str
            a string containing the value of the current node.
        """
        return self.data
    
    def set_data(self, d):
        """
        Used to set the value of the current node to the value of parameter "d" that was given when an object of the class was created.

        Parameters
        ----------
        d : str
            The value of the current node
        """
        self.data = d

class LinkedList(object):
    """
    A class used to build nodes with their next and previous nodes (thus also saving their neighbours).

    ...

    Attributes
    ----------
    root : str
        the value of node that is added to the list
    size : int
        the value of the size of the list (starts at 0)

    Methods
    -------
    get_size()
        Returns the size of the list
    add()
        Adds a node to the list
    remove()
        Removes a node from the list
    """
    def __init__(self, r = None):
        """
        Parameters
        ----------
        r : str
            The value that the current node that is added will get (default None)
        """
        self.root = r
        self.size = 0 

    def get_size(self):
        """
        Used to get the value of the size of the list.

        Returns
        -------
        int
            an integer that represents the current size of the list.
        """
        return self.size
    
    def add(self, d):
        """
        Used when adding an item to the list. It changes the size of the list and resets the neighbours.

        Parameters
        ----------
        d : str
            The value of the current node
        """
        new = Node(d, self.root) #Add root as new next node
        if self.root:
            self.root.set_prev(new) 
        self.root = new
        self.size += 1
    
    def remove(self, d):
        """
        Used when removing an item to the list. It changes the size of the list and resets the neighbours. 
        It returns false if the data that needed to be removed was not found in the list.

        Parameters
        ----------
        d : str
            The value of the current node
        """
        current_node = self.root
        while current_node: #When we find a node we want to delete, reform the pointers
            if current_node.get_data() == d:
                next_node = current_node.get_next()
                prev_node = current_node.get_prev()

                if next_node: #If next_node exists, so if it is not None
                    next_node.set_prev(prev_node)
                if prev_node: #If prev_node exists
                    prev_node.set_next(next_node)
                else: #If both are None, set the current node as the root node
                    self.root = current_node
                self.size -= 1
                return True #Data is removed
            else: 
                current_node = current_node.get_next() 
        return False #Data not found
        
