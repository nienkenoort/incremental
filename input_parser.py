#Author: Nienke Noort 
#Student number (Utrecht University): 6200451
#Supervisor: Gijs J. Wijnholds

from input_parser import Read
import lexicon_parser
import type_parser

class Vertex:
    """
    A class that gets a string as parameter and creates a Linked List of that string. The Linked List will include 
    each word of the string with their corresponding type and polarity. It will do so by using the other parameter: a string 
    that saves the resulting type of the sentence.
    
    ...

    Attributes
    ----------
    data : list
        the type of vertex which is saved as a list.
    left : Vertex
        the left child of the current vertex.
    right : Vertex
        the right child of the current vertex.
    polarity : int
        the polarity of the vertex. An input polarity is saved as 1, an output polarity is saved as 0.
    isLeaf : bool
        is True if the vertex is a leaf (thus has no left and right child), is False otherwise.
    parent : Vertex
        the parent vertex of the current vertex.
    iLink : int
        is 1 if there is an i-link between the vertex and its parent, is 2 if this is an ii-link.
    visited : bool
        is true if the vertex was visited before, otherwise is false.
    axiom : Vertex
        the vertex that is connected with the current vertex through an axiomconnection.
    axiomRemoved : list
        exists of all vertices which were connected with the current vertex, but that connection was not correct / was removed.
    label : int
        the label of the vertex is an integer. Each vertex gets a unique label so that the order of the leaves is preserved.
    potentialAxiom : list
        a list containing all vertices that can possibly connect with the current vertex.
    """
    def __init__(self, data, polarity, parent, iLink):
        """
        Parameters
        ----------
        data : list
            The type of vertex which is saved as a list.
        left : Vertex
            The left child of the current vertex.
        right : Vertex
            The right child of the current vertex.
        polarity : int
            The polarity of the vertex. An input polarity is saved as 1, an output polarity is saved as 0.
        isLeaf : bool
            This bool is True if the vertex is a leaf (thus has no left and right child), is False otherwise.
        parent : Vertex
            The parent vertex of the current vertex.
        iLink : int
            This integer is 1 if there is an i-link between the vertex and its parent, is 2 if this is an ii-link.
        visited : bool
            This bool is true if the vertex was visited before, otherwise is false.
        axiom : Vertex
            The vertex that is connected with the current vertex through an axiomconnection.
        axiomRemoved : list
            A list which exists of all vertices which were connected with the current vertex, but that connection was not correct / was removed.
            Is used so that the program will not try to make the same axioms that cannot be made over and over again.
        label : int
            The label of the vertex is an integer. Each vertex gets a unique label so that the order of the leaves is preserved.
            Is used for labelling all of the leaves, so we can check if any of the axiom connections cross each other.
        potentialAxiom : list
            A list containing all vertices that can possibly connect with the current vertex.
        """
        self.data = data
        self.left = None
        self.right = None
        self.polarity = polarity
        self.isLeaf = False
        self.parent = parent
        self.iLink = iLink
        self.visited = False
        self.axiom = None
        self.axiomRemoved = []
        self.label = None
        self.potentialAxiom = []

class Tree:
    """
    A class that creates a tree by adding vertices one by one. The root vertex is added first, after that the children are added.
    
    ...

    Methods
    -------
    createVertex(data, polarity, parent, iLink)
        Creates a vertex of the data by calling the Vertex class.
    insertVertex(vertex, data, place, polarity, parent, iLink)
        Creates a vertex of the data if the vertex does not exist. It adds the created vertex to the tree.
    removeVertex(vertex)
        Removes all nodes from the tree in which the parameter vertex appears.
    """
    def createVertex(self, data, polarity, parent, iLink):
        """
        Uses the values that were given as parameters to save a vertex. These values are features of the current vertex. 
        It uses the Vertex class to do so.

        Returns
        -------
        Vertex
            a vertex containing the start values of all attributes of the Vertex class.
        """
        return Vertex(data, polarity, parent, iLink)

    def insertVertex(self, vertex, data, place, polarity, parent, iLink):
        """
        Uses the values that were given as parameters to insert a vertex to the tree. These values are features of the current vertex. 
        It is a recursive method so that it can insert all children to the root.

        Returns
        -------
        vertex
            a vertex containing the start values of all attributes of the Vertex class.
        polarity
            the polarity of the inserted vertex. This can be 0 (output) or 1 (input).
        parent
            a vertex that was inserted before the current vertex, which makes it the parent of the current vertex.
        iLink
            the value of the link between the current node and the parent. This is 1 (i-link) or 2 (ii-link).
        """
        if vertex == None:
            return self.createVertex(data, polarity, parent, iLink) #If root is still empty, create a node

        if place == "left":
            vertex.left = self.insertVertex(vertex.left, data, "left", polarity, parent, iLink)
        elif place == "right":
            vertex.right = self.insertVertex(vertex.right, data, "right", polarity, parent, iLink)
        else:
            vertex = self.insertVertex(vertex, data, "root", polarity, parent, iLink) #If the current vertex is a root element, insert the root
        return vertex, polarity, parent, iLink
    
    def removeVertex(self, vertex):
        """
        Removes all of the vertices that are in the same tree as the parameter vertex. Calls itself recursively
        so that it can delete the children first, and the parents after.

        Returns
        -------
        None
        """
        if vertex is None: #If the vertex that we want to delete does not exist in the current tree, return None
            return None
        if(vertex.left == None and vertex.right == None):
            del vertex

        else:
            if vertex.left != None:
                self.removeVertex(vertex.left)
            if vertex.right != None:
                self.removeVertex(vertex.right)
            if(vertex != None and vertex.left == None and vertex.right == None):
                if(vertex.parent != None):
                    self.removeVertex(vertex.parent)
                else:
                    self.removeVertex(vertex)              

class Axioma:
    """
    A class that creates axiomconnections between two leaves. This class checks if the axiomconnection is possible. 
    After creating an axiomconnection, it checks if the proofnet is still valid (thus if there is no cycle and if there are
    no crossed links). It removes the connection if the proofnet is not valid.
    
    ...

    Attributes
    ----------
    root : Vertex
        the root of the tree in which we want to make axiomconnections.
    passedTrees : list
        a list containing all trees that were already built (thus trees that can form a connection with the current tree).
    cycleFound : bool
        is True if a cycle was found after adding the axiomconnection, otherwise is False.
    iLinkPassed : bool
        is True if an iLink was found after adding the axiomconnection, otherwise is False.
    doCross : bool
        is True if a crossed links were found after adding the axiomconnection, otherwise is False.
    axiomConnections : list
        the axiomconnections made so far are saved in this list.
    notConnected : list
        a list containing all nodes that are not connected and thus still need to form a connection for a complete proofnet.
    incremental : bool
        is true if the user wants to see the incremental process, otherwise is false.
    
    Methods
    -------
    find_leaf(root)
        Finds the leaves of the current tree, so that these leaves can connect with other leaves that are already created.
    find_leafOtherTree(root, rootOtherTree)
        Finds the leaves in other trees than the tree in which the current leaf appears, so that these leaves can connect with the current leaf 
        (that is currently trying to create an axiomconnection).
    findOtherTree(root)
        Goes through the passedTrees list (the list that contains all trees that are created so far) to check for each tree if a connection
        with a leaf from that tree is possible.
    find_mostRightLeaf(vertexOut, vertexIn)
        Tries to find the leaf that is on the right side of the tree. In this case vertexOut is the leaf that is looking for an axiomconnection
        and vertexIn is the root of the tree in which we want to search for a leaf that can connect with vertexOut.
    toFalse(root)
        Sets the visited values of all vertices that are reachable from the parameter root vertex to false.
    createAxioma(root, vertex)
        Creates the actual axiomconnection between the parameter leaves 'root' and 'vertex'.
    find_leafCross(root, leaves)
        Creates a list of all of the leaves that are between the two leaves that were just connected.
    checkForCross(rootOutput, rootInput)
        Checks if the just made axiomconnection causes any other vertices to cross connections if they want to make any.
        The just made connection was between parameters rootOutput and rootInput.
    checkForCycle(rootOutput, rootInput)
        Checks if the just made axiomconnection causes a cycle. This just made connection was between the parameters rootOutput
        and rootInput.
    removeAxioma(type1, type2)
        Removes the axiom connection between the vertices 'type1' and 'type2'.

    """
    def __init__(self, root, passedTrees, axiomConnections, notConnected, incremental):
        """
        Parameters
        ----------
        root : Vertex
            The root of the tree in which we want to make axiomconnections.
        passedTrees : list
            A list containing all trees that were already built (thus trees that can form a connection with the current tree).
        cycleFound : bool
            Is True if a cycle was found after adding the axiomconnection, otherwise is False.
        iLinkPassed : bool
            Is True if an iLink was found after adding the axiomconnection, otherwise is False.
        doCross : bool
            Is True if a crossed links were found after adding the axiomconnection, otherwise is False.
        axiomConnections : list
            The axiomconnections made so far are saved in this list.
        notConnected : list
            A list containing all nodes that are not connected and thus still need to form a connection for a complete proofnet.
        incremental : bool
            Is true if the user wants to see the incremental process, otherwise is false.
        """
        self.root = root
        self.passedTrees = passedTrees
        self.cycleFound = False
        self.iLinkPassed = False
        self.doCross = False
        self.axiomConnections = axiomConnections
        self.notConnected = notConnected
        self.incremental = incremental

    def find_leaf(self, root):
        """
        Takes the root parameter and finds all the leaves that are reachable from this root. 
        These leaves should be connected to leaves that appear in other trees.

        Returns
        -------
        axiomConnections
            a list of all the axiomconnections made so far.
        notConnected
            a list of the leaves that are not connected yet.
        """
        if(root.isLeaf == True and root.axiom == None): #If there is no vertex anymore on which can be split, then a connection needs to be created
            self.findOtherTree(root)
            return self.axiomConnections, self.notConnected
        else:
            #If the current vertex is not a leaf and it has children, go to that child
            if(root.left != None and root.right != None):
                self.find_leaf(root.left)
                self.find_leaf(root.right)
    
    def find_leafOtherTree(self, root, rootOtherTree):
        """
        Finds a leaf in the tree which has the root 'rootOtherTree' (by using the find_mostRightLeaf method) which is able to form a 
        connection with the 'root' parameter.

        Returns
        -------
        None
        """
        if(rootOtherTree.left != None and rootOtherTree.right != None):#If the current vertex is also a leaf, then we need to create an axiom with another vertex
            mostRightLeaf = self.find_mostRightLeaf(root, rootOtherTree)
            self.toFalse(root)
            self.toFalse(rootOtherTree)
            if(mostRightLeaf != None):
                if(root.axiom == None):                            
                    self.createAxioma(root, mostRightLeaf)
                    if(root.axiom != mostRightLeaf):#If the just made axiom was removed, another axiom needs to be created
                        withAxiom = []
                        if((len(root.potentialAxiom) > 0) and root.axiom == None):#In this case, there are other leaves that are also possible to connect with
                            connect = None
                            for elem in root.potentialAxiom:
                                axiom = elem.axiom
                                if(elem not in root.axiomRemoved):
                                    if(elem.axiom == None):
                                        connect = elem
                                        self.createAxioma(root, connect)
                                        if(root.axiom == connect):
                                            break
                                        else:
                                            self.removeAxioma(root, elem) #If the current vertex is not connected with the root, then the old axiom needs to be restored
                                    else:
                                        withAxiom.append(elem) #If the current vertex already has an axiom connection, add this vertex to the withAxiom[] for later use
                            if(root.axiom == None):
                                #If the current vertex still has no axiom connection, go through the list of vertices that already had an axiom connection
                                if(len(withAxiom) > 0):
                                    for elem in withAxiom:
                                        axiom = elem.axiom
                                        self.removeAxioma(elem, elem.axiom)
                                        connect = elem
                                        self.createAxioma(root, connect)
                                        if(root.axiom == connect):
                                            break
                                        else:
                                            #If the current node is not connected with the root, then the old axiom needs to be restored
                                            self.removeAxioma(root, elem)
                                            if(axiom in elem.axiomRemoved):
                                                elem.axiomRemoved.remove(axiom)
                                            if(elem in axiom.axiomRemoved):
                                                axiom.axiomRemoved.remove(elem)
                                            self.createAxioma(elem, axiom)
                                else:
                                    #In this case no connection can be made
                                    if(root.axiom == None):
                                        isInList = False
                                        for element in self.notConnected:
                                            if(element.label == root.label):
                                                isInList = True
                                        if(isInList == False):
                                            self.notConnected.append(root)
                                    return None
                else:
                    #In this case no connection can be made
                    if(root.axiom == None):
                        isInList = False
                        for element in self.notConnected:
                            if(element.label == root.label):
                                isInList = True
                        if(isInList == False):
                            self.notConnected.append(root)
                    return None
            else: 
                #If no connection was created with the current tree, look at old vertices from potentialAxiom to check if a connection is possible
                if((len(root.potentialAxiom) > 0)): #In this case possible axioms were added to the list
                    connect = None
                    withAxiom = []
                    for elem in root.potentialAxiom:
                        axiom = elem.axiom
                        if(elem not in root.axiomRemoved):
                            if(elem.axiom == None):
                                connect = elem
                                if(root.axiom != None):
                                    rootAx = root.axiom
                                    self.removeAxioma(root, rootAx)
                                self.createAxioma(root, connect)
                                if(root.axiom == connect):
                                    break
                                else:
                                    self.removeAxioma(root, elem) #If the current vertex is not connected with the root, then the old axiom needs to be restored
                            else:
                                withAxiom.append(elem) #If the current vertex already has an axiom connection, add this vertex to the withAxiom[] for later use
                    if(root.axiom == None):
                        #If the current vertex still has no axiom connection, go through the list of vertices that already had an axiom connection
                        if(len(withAxiom) > 0):
                            for elem in withAxiom:
                                self.removeAxioma(elem, elem.axiom)
                                connect = elem
                                self.createAxioma(root, connect)
                                if(root.axiom == connect):
                                    break
                                else:
                                    #If the current vertex is not connected with the root, the old axiom needs to be restored
                                    self.removeAxioma(root, elem)
                                    if(axiom in elem.axiomRemoved):
                                        elem.axiomRemoved.remove(axiom)
                                    if(elem in axiom.axiomRemoved):
                                        axiom.axiomRemoved.remove(elem)
                                    self.createAxioma(elem, axiom)
                        else:
                            #In this case no connection can be made
                            if(root.axiom == None):
                                isInList = False
                                for element in self.notConnected:
                                    if(element.label == root.label):
                                        isInList = True
                                if(isInList == False):
                                    self.notConnected.append(root)
                            return None
                else:
                    #In this case no connection can be made
                    if(root.axiom == None):
                        isInList = False
                        for element in self.notConnected:
                            if(element.label == root.label):
                                isInList = True
                        if(isInList == False):
                            self.notConnected.append(root)
                    return None
        else:
            #If the other tree exists of only a single vertex, check if that vertex can be connected
            if(rootOtherTree.data == root.data and rootOtherTree.polarity != root.polarity):
                root.potentialAxiom.append(rootOtherTree)
                if(root.axiom == None):
                    self.createAxioma(root, rootOtherTree)
                    if(root.axiom != rootOtherTree):
                        withAxiom = []
                        if(len(root.potentialAxiom) > 0):
                            #In this case possible axioms were added to the potentialAxioms list
                            connect = None
                            for elem in root.potentialAxiom:
                                axiom = elem.axiom
                                if(elem not in root.axiomRemoved):
                                    if(elem.axiom == None):
                                        connect = elem
                                        self.createAxioma(root, connect)
                                        if(root.axiom == connect):
                                            break
                                        else:
                                            self.removeAxioma(root, elem) #If the current vertex is not connected with the root, the old axiom needs to be restored

                                    else:
                                        withAxiom.append(elem) #If the current vertex already has an axiom connection, add this vertex to the withAxiom[] for later use
                            if(root.axiom == None):
                                #If the current vertex still has no axiom connection, go through the list of vertices that already had an axiom connection
                                if(len(withAxiom) > 0):
                                    for elem in withAxiom:
                                        self.removeAxioma(elem, elem.axiom)
                                        connect = elem
                                        self.createAxioma(root, connect)
                                        if(root.axiom == connect):
                                            break
                                        else:
                                            #If the current vertex is not connected with the root, the old axiom needs to be restored
                                            self.removeAxioma(root, elem)
                                            if(axiom in elem.axiomRemoved):
                                                elem.axiomRemoved.remove(axiom)
                                            if(elem in axiom.axiomRemoved):
                                                axiom.axiomRemoved.remove(elem)
                                            self.createAxioma(elem, axiom)
                                else:
                                    #In this case no connection can be made
                                    if(root.axiom == None):
                                        isInList = False
                                        for element in self.notConnected:
                                            if(element.label == root.label):
                                                isInList = True
                                        if(isInList == False):
                                            self.notConnected.append(root)
                                    return None
            else:
                #In this case no connection can be made
                if(root.axiom == None):
                    isInList = False
                    for element in self.notConnected:
                        if(element.label == root.label):
                            isInList = True
                    if(isInList == False):
                        self.notConnected.append(root)
                return None

    def findOtherTree(self, root):
        """
        Goes through all of the trees that were already created (passedTrees) to (possibly) form an axiomconnection with leaves from that tree.

        Returns
        -------
        None
        """
        for rootPassed in self.passedTrees:
            if(self.root != rootPassed):
                if(self.incremental == True):
                    print("Try to create axiom connections between the following trees: ",rootPassed.data, self.root.data)
                #If the root of the current tree is not the same as the root of the tree that we want to connect, 
                # then we can try to find leaves to connect in that tree (since a connection with another tree is preferred).
                self.find_leafOtherTree(root, rootPassed)

    def find_mostRightLeaf(self, vertexOut, vertexIn):
        """
        This method tries to find the most right leaf in the tree (of which the parameter 'vertexIn' is the root) and tries to 
        create an axiomconnection between this leaf and the leaf that is given as the 'vertexOut' parameter. It adds all other 
        leaves that can form a connection with the 'vertexOut' leaf as well to the potentialAxioms list of that leaf. The method
        searches through the entire tree by calling itself recursively.

        Returns
        -------
        vertexIn
            a that can form an axiomconnection with the 'vertexOut' leaf.
        None
        """
        if(vertexIn.visited == True):
            if(vertexIn.parent != None):
                return self.find_mostRightLeaf(vertexOut, vertexIn.parent)
            else:
                return None
        if(vertexIn.isLeaf == True):
            if(vertexIn.data == vertexOut.data and vertexIn.polarity != vertexOut.polarity):
                vertexOut.potentialAxiom.append(vertexIn) #Add leaves that can connect with vertexOut to potentialAxiom list
                vertexIn.visited = True
                if(vertexIn.parent != None):
                    #Search rest of tree to find a leaf to connect with
                    if(vertexIn.parent.left != vertexIn):
                        if(vertexIn.parent.left.visited == False):
                            return self.find_mostRightLeaf(vertexOut, vertexIn.parent.left)
                        else:
                            return vertexIn
                    else: 
                        if(vertexIn.parent.right.visited == False):
                            return self.find_mostRightLeaf(vertexOut, vertexIn.parent.right)
                        else:
                            return vertexIn
                else:
                    return vertexIn
            else:
                vertexIn.visited = True
                if(vertexIn.parent.left.visited == True and vertexIn.parent.right.visited == True):
                    vertexIn.parent.visited = True
                if(vertexIn == vertexIn.parent.left): #If we have reached a leaf, but this is not a leaf we can connect, we need to look at the left side
                    #If the left leaf is already visited, and we cannot connect this one either, go back to the most recent parent of which
                    #the left child was not yet covered
                    if(vertexIn.parent.parent != vertexIn and vertexIn.parent.visited == True and vertexIn.parent.parent != None):
                        #If the current parent is already visited, look at the right side of the tree
                        return self.find_mostRightLeaf(vertexOut, vertexIn.parent.parent.left)
                    else:
                        #A connection with the current tree is not possible
                        return None
                else:
                    return self.find_mostRightLeaf(vertexOut, vertexIn.parent.left)
        else: #Go further into the tree
            if(vertexIn.left.visited == True and vertexIn.right.visited == True):
                vertexIn.visited = True
                if(vertexIn.parent != None):
                    return self.find_mostRightLeaf(vertexOut, vertexIn.parent.left)
                else:
                    return None
            else:
                if(vertexIn.right.visited == True):
                    return self.find_mostRightLeaf(vertexOut, vertexIn.left)
                elif(vertexIn.left.visited == True):
                    return self.find_mostRightLeaf(vertexOut, vertexIn.right) 
                else:
                    #If both are not visited yet, choose the most right vertex
                    return self.find_mostRightLeaf(vertexOut, vertexIn.right)

    def toFalse(self, root):
        """
        Sets the values of visited of all nodes that are reachable from the 'root' parameter to false. The method calls itself
        recursively so that it is able to search through the entire tree (and possibly other trees through axiomconnections).

        Returns
        -------
        None
        """
        if(root.isLeaf == False):
            if(root.left.visited == True or root.right.visited == True):
                root.visited = True
        if(root.visited == True): #If the visited value of the current vertex is True, then go to the next vertex
            if(root.right != None and root.left != None):
                if(root.right.visited == True):
                    return self.toFalse(root.right)
                elif(root.left.visited == True):
                    return self.toFalse(root.left)
                else: #If both the left and the right child have a visited value of False, the root will get a value of False as well
                    root.visited = False
                    if(root.axiom != None):
                        if(root.axiom.visited == True):
                            return self.toFalse(root.axiom)
                    if(root.parent != None):
                        return self.toFalse(root.parent)
            elif(root.parent != None):
                if(root.parent.right.isLeaf == False):
                    if(root.parent.right.left.visited == True or root.parent.right.right.visited == True):
                        root.parent.right.visited = True
                if(root.parent.left.isLeaf == False):
                    if(root.parent.left.left.visited == True or root.parent.left.right.visited == True):
                        root.parent.left.visited = True
                if(root.parent.right.visited == True):
                    #Leaves will always get a visited value of false, if we have passed them
                    root.visited = False
                    if(root.axiom != None):
                        if(root.axiom.visited == True):
                            return self.toFalse(root.axiom)
                    return self.toFalse(root.parent.right)
                elif(root.parent.left.visited == True):
                    root.visited = False
                    if(root.axiom != None):
                        if(root.axiom.visited == True):
                            return self.toFalse(root.axiom)
                    return self.toFalse(root.parent.left)
                else:
                    root.visited = False
                    if(root.axiom != None):
                        if(root.axiom.visited == True):
                            return self.toFalse(root.axiom)
                    if(root.parent != None):
                        return self.toFalse(root.parent)
            else: #If the vertex has no parent, set its value to False
                root.visited = False
                if(root.axiom != None):
                    if(root.axiom.visited == True):
                        return self.toFalse(root.axiom)
                if(root.parent != None):
                    return self.toFalse(root.parent)
        else: #If the value of the current vertex was already set to False, then go to the parent
            if(root.parent != None):
                return self.toFalse(root.parent)
    
    def createAxioma(self, root, vertex):
        """
        Creates an axiomconnection between the leaves that are given as parameters. This method calls the checkForCycle and checkForCross 
        so that invalid axiomconnections can be removed.

        Returns
        -------
        None
        """
        if((root.axiom != vertex or vertex.axiom != root) and (root.axiom == None and vertex.axiom == None) and 
        (vertex not in root.axiomRemoved and root not in vertex.axiomRemoved)):
            #If an axiom connection already exists between these vertices, we do not make another connection
            root.axiom = vertex
            vertex.axiom = root
            #Remove the vertices that now have an axiomconnection from the notConnected list
            isInListRoot = False
            isInListVertex = False
            for element in self.notConnected:
                if(element.label == root.label):
                    isInListRoot = True
                    new_root = element
                if(element.label == vertex.label):
                    isInListVertex = True
                    new_vertex = element
            if(isInListRoot == True):
                self.notConnected.remove(new_root)
            if(isInListVertex == True):
                self.notConnected.remove(new_vertex)
            if(self.incremental == True):
                print("An axiom connection has been created between the following leaves (data, label) :", root.data ,root.label,  vertex.data, vertex.label )
            #After a connection was created, check if this connection is valid
            if(root.polarity == 0):
                #These methods depend on what vertex has an output polarity and what vertex has an input polarity
                self.checkForCycle(root, vertex)
                self.checkForCross(root, vertex)
                self.axiomConnections.append([root, vertex])
            else:
                self.checkForCycle(vertex, root)
                self.checkForCross(vertex, root)
                self.axiomConnections.append([vertex, root])

            #Set all visited values to False
            self.toFalse(root)
            self.toFalse(vertex)

            if((self.cycleFound == True and self.iLinkPassed == False) or self.doCross == True):
                #In this case there is a cycle thus get rid of the last axiom made
                if(self.incremental == True):
                    print("A cycle or crossed links were caused by the last-made axiom connection (data, label): ",  root.data, root.label ,  vertex.data, vertex.label)
                self.cycleFound = False
                self.doCross = False
                if(self.incremental == True):
                    print("The following axiom connection was removed (data, label): ",  root.data, root.label ,  vertex.data, vertex.label)
                self.removeAxioma(root, vertex)
                #Remove last added item of list
                self.axiomConnections.pop()
                #Add these vertices back to the notConnected list
                self.notConnected.append(root)
                self.notConnected.append(vertex)

            #Set iLink back to false for next axiom
            self.iLinkPassed = False
    
    def find_leafCross(self, root, leaves):
        """
        Creates a list of all leaves that are reachable from the 'root' parameter.

        Returns
        -------
        leaves
            a list containing all leaves that are reachable from the 'root' parameter.
        """
        if(root.isLeaf == True): #If the current vertex is a leaf, append to the list
            leaves.append(root)
        else: #If the current vertex is not a leaf and it has children, go to that child
            if(root.left != None and root.right != None):
                self.find_leafCross(root.left, leaves)
                self.find_leafCross(root.right, leaves)
        return leaves

    def checkForCross(self, rootOutput, rootInput):
        """
        Checks if any crossed connections are possible after adding the axiomconnection between the 
        leaves that are given as parameters.

        Returns
        -------
        doCross
            a bool that has a value of True if crosses are found between (possible) connections, otherwise is False.
        """
        if((rootOutput.label == (rootInput.label + 1)) or (rootOutput.label == (rootInput.label - 1))):
            #If both axiom leaves appear next to each other, there is no case in which there are crossed connections (thus return doCross with a value of False)
            return self.doCross
        else:
            noAxiom = []
            #If not, check what vertices appear between them and if these vertices can connect with each other
            if(rootOutput.label > rootInput.label):
                #Contract 1 from outputlabel, since 4-3=1, even though there are not any leaves between them
                if(((rootOutput.label - 1) - rootInput.label) % 2 != 0):
                    #If there is not an even amount of vertices between them, there is a centainty that they cannot all connect with another vertex without crossing
                    self.doCross = True
                    return self.doCross
                else:
                    for vertex in self.passedTrees:
                        if(vertex.isLeaf == False):
                            leaves = []
                            leaves = self.find_leafCross(vertex, leaves)
                            for leaf in leaves:
                                if(leaf != rootOutput and leaf != rootInput):
                                    if(leaf.label > rootInput.label and leaf.label < rootOutput.label):
                                        #If the current vertex is between the axiom vertices, check if it has an axiomconnection
                                        if(leaf.axiom == None):
                                            #If the leaf has no axiomconnection, check later if such a connection is still possible by looking
                                            #  at all of the elements in the noAxiom list 
                                            noAxiom.append(leaf)
                                        else:
                                            #If the leaf does have a connection, and the connection is not with any leaf that is also between the rootInput and
                                            #  rootOutput, then there are crosses
                                            if(leaf.axiom.label < rootInput.label or leaf.axiom.label > rootOutput.label):
                                                self.doCross = True
                                                return self.doCross
                        else: #If the vertex is a leaf
                            if(vertex != rootOutput and vertex != rootInput):
                                if(vertex.label > rootInput.label and vertex.label < rootOutput.label):
                                    #If the current vertex is between the axiom vertices, check if it has an axiomconnection
                                    if(vertex.axiom == None):
                                        #If the leaf has no axiom connection, check later if such a connection is still possible by looking
                                        #  at all of the elements in the noAxiom list 
                                        noAxiom.append(vertex)
                                    else:
                                        #If the leaf does have a connection, and the connection is not with any leaf that is also between the rootInput and 
                                        # rootOutput, then there are crosses
                                        if(vertex.axiom.label < rootInput.label or vertex.axiom.label > rootOutput.label):
                                            self.doCross = True
                                            return self.doCross
            elif(rootOutput.label < rootInput.label):
                if(((rootInput.label - 1) - rootOutput.label) % 2 != 0):
                    #If there is not an even amount of vertices between them, they cannot all connect with another vertex without crossing
                    self.doCross = True
                    return self.doCross
                else:
                    for vertex in self.passedTrees:
                        if(vertex.isLeaf == False):
                            leaves = []
                            leaves = self.find_leafCross(vertex, leaves)
                            for leaf in leaves:
                                if(leaf != rootOutput and leaf != rootInput):
                                    if(leaf.label < rootInput.label and leaf.label > rootOutput.label):
                                        #If the current vertex is between the axiom vertices, check if it has an axiom connection
                                        if(leaf.axiom == None):
                                            #If the leaf has no axiom connection, check later if such a connection is still possible by looking
                                            #  at all of the elements in the noAxiom list 
                                            noAxiom.append(leaf)
                                        else:
                                            #If the leaf does have a connection, and the connection is not with any leaf that is also between the rootInput and 
                                            # rootOutput, then there are crosses
                                            if(leaf.axiom.label > rootInput.label or leaf.axiom.label < rootOutput.label):
                                                self.doCross = True
                                                return self.doCross
                        else: #If the vertex is a leaf
                            if(vertex != rootOutput and vertex != rootInput):
                                if(vertex.label > rootInput.label and vertex.label < rootOutput.label):
                                    #If the current vertex is between the axiom vertices, check if it has an axiom connection
                                    if(vertex.axiom == None):
                                        #If the leaf has no axiom connection, check later if such a connection is still possible by looking
                                        #  at all of the elements in the noAxiom list 
                                        noAxiom.append(vertex)
                                    else:
                                        #If the leaf does have a connection, and the connection is not with any leaf that is also between the rootInput and 
                                        # rootOutput, then there are crosses
                                        if(leaf.axiom.label < rootInput.label or leaf.axiom.label > rootOutput.label):
                                            self.doCross = True
                                            return self.doCross

            #Check if the elements that do not have an axiomconnection can possibly connect with each other
            for vertex1 in noAxiom:
                for vertex2 in noAxiom:
                    if(vertex1 != vertex2):
                        if(vertex1.data == vertex2.data and vertex1.polarity != vertex2.polarity):
                            #In this case it is still possible that both leaves connect, if there is no cycle
                            if(vertex1.polarity == 0):
                                self.checkForCycle(vertex1, vertex2)
                            else:
                                self.checkForCycle(vertex2, vertex1)
                            self.toFalse(vertex1)
                            self.toFalse(vertex2)
                            if(self.cycleFound == False):
                                #If there is no cycle if this would be a connection, then delete the elements from the set
                                if(vertex1 in noAxiom and vertex2 in noAxiom):
                                    noAxiom.remove(vertex1)
                                    noAxiom.remove(vertex2)
            #Set cycle back to false
            self.cycleFound = False
            if(len(noAxiom) > 0):
                #If there are leaves that could not connect, set cross to true
                self.doCross = True
            return self.doCross

    def checkForCycle(self, rootOutput, rootInput):
        """
        Checks if a cycle was created because of the just made connection between the parameter leaves (rootOutput and rootInput).
        It does so by starting in the rootInput leaf, and checking if it passes the rootOutput leaf. If it passes the rootOutput leaf,
        a cycle was found.
        The method also checks if the cycle goes through any i-links. In this case the cycle is permitted, and iLinkPassed is set to True.

        Returns
        -------
        cycleFound
            a bool that has a value of True if cycles are found between (possible) connections, otherwise is False.
        """
        goToNode = None
        if(rootInput.isLeaf == True):
            rootInput.visited = True
        else:
            if(rootInput.left.visited == True and rootInput.right.visited == True):
                rootInput.visited = True
        if(rootInput.iLink == 1):
            #If an i-link was passed, set iLinkPassed to True
            self.iLinkPassed = True
        if(rootInput == rootOutput):
            #If a vertex was found that is the same as the output vertex, there is a cycle
            self.cycleFound = True
            return self.cycleFound
        if(rootInput.parent != None):
            if(rootInput.parent.left != rootInput):
                if(rootInput.parent.left.isLeaf == True):
                    if(rootInput.parent.left.iLink == 1):
                        #If an i-link was passed, set iLinkPassed to True
                        self.iLinkPassed = True
                    if(rootInput.parent.left == rootOutput):
                        #If a vertex was found that is the same as the output vertex, there is a cycle
                        self.cycleFound = True
                        return self.cycleFound
                    else: #Set visited to True and check the leaves that are connected
                        rootInput.parent.left.visited = True
                        if(rootInput.parent.left.axiom != None):
                            goToNode = rootInput.parent.left.axiom
                            if(rootInput.parent.parent != None): #Go further into the tree
                                if(rootInput.parent.parent.left != rootInput.parent):
                                    if(rootInput.parent.parent.left.visited == False):
                                        return self.checkForCycle(rootOutput, rootInput.parent.parent.left)
                                else:
                                    if(rootInput.parent.parent.right.visited == False):
                                        return self.checkForCycle(rootOutput, rootInput.parent.parent.right)
                        else:#Go further into the tree
                            if(rootInput.parent.visited == False):
                                return self.checkForCycle(rootOutput, rootInput.parent)
                else:
                    #If the current vertex is not a leaf, go to the leaves
                    if(rootInput.parent.left.left.visited == False):
                        return self.checkForCycle(rootOutput, rootInput.parent.left.left)
                    else: #If already visited, everything is covered and no cycle was found
                        return self.cycleFound
                    if(rootInput.parent.left.right.visited == False):
                        return self.checkForCycle(rootOutput, rootInput.parent.left.right)
                    else:#If already visited, everything is covered and no cycle was found
                        return self.cycleFound
            elif(rootInput.parent.right != rootInput):
                if(rootInput.parent.right.isLeaf == True):
                    if(rootInput.parent.right.iLink == 1):
                        #If an i-link was passed, set iLinkPassed to True
                        self.iLinkPassed = True
                    if(rootInput.parent.right == rootOutput):
                        #If a vertex was found that is the same as the output vertex, there is a cycle
                        self.cycleFound = True
                        return self.cycleFound
                    else: #Set visited to True and check the leaves that are connected
                        rootInput.parent.right.visited = True
                        if(rootInput.parent.right.axiom != None):
                            goToNode = rootInput.parent.right.axiom
                            if(rootInput.parent.parent != None): #Go further into the tree
                                if(rootInput.parent.parent.left != rootInput.parent):
                                    if(rootInput.parent.parent.left.visited == False):
                                        return self.checkForCycle(rootOutput, rootInput.parent.parent.left)
                                else:
                                    if(rootInput.parent.parent.right.visited == False):
                                        return self.checkForCycle(rootOutput, rootInput.parent.parent.right)
                        else: #Go further into the tree
                            if(rootInput.parent.visited == False):
                                return self.checkForCycle(rootOutput, rootInput.parent)
                else:
                    #If the current vertex is not a leaf, go to the leaves
                    if(rootInput.parent.right.left.visited == False):
                        return self.checkForCycle(rootOutput, rootInput.parent.right.left)
                    elif(rootInput.parent.right.right.visited == False):
                        return self.checkForCycle(rootOutput, rootInput.parent.right.right)
                    elif(rootInput.parent.right.visited == False):
                        return self.checkForCycle(rootOutput, rootInput.parent.right) 
            else: #Go further into the tree
                if(rootInput.parent.visited == False):
                    return self.checkForCycle(rootOutput, rootInput.parent)

            #Check if the current vertex is the same as the output vertex, this would be a cycle
            if(goToNode != None):
                if(goToNode == rootOutput):
                    if(goToNode.visited == False):
                        return self.checkForCycle(rootOutput, goToNode)
            
                if(goToNode.parent != None):
                    if(goToNode.parent.right != goToNode):
                        #check if the closest neighbour causes a cycle
                        if(goToNode.parent.right == rootOutput):
                            #If a vertex was found that is the same as the output vertex, there is a cycle
                            self.cycleFound = True
                            return self.cycleFound
                        else: #Check the axiom connections
                            if(goToNode.parent.right.axiom != None):
                                if(goToNode.parent.right.axiom.visited == False):
                                    return self.checkForCycle(rootOutput, goToNode.parent.right.axiom) 
                            if(goToNode.parent.visited == False):
                                return self.checkForCycle(rootOutput, goToNode.parent)
                    elif(goToNode.parent.left != goToNode):
                        if(goToNode.parent.left == rootOutput):
                            #If a vertex was found that is the same as the output vertex, there is a cycle
                            self.cycleFound = True
                            return self.cycleFound
                        else: #Check the axiom connections
                            if(goToNode.parent.left.axiom != None):
                                if(goToNode.parent.left.axiom.visited == False):
                                    return self.checkForCycle(rootOutput, goToNode.parent.left.axiom)
                            if(goToNode.parent.visited == False):
                                return self.checkForCycle(rootOutput, goToNode.parent)
                    else: #Go further into the tree
                        if(goToNode.parent.visited == False):
                            return self.checkForCycle(rootOutput, goToNode.parent)
                else:
                    #If the current node has no parent, and the children were already covered (if they have any), then there is no cycle
                    return self.cycleFound
            else:
                #A cycle is not possible
                return self.cycleFound
        else:
            #A cycle is not possible
            return self.cycleFound
    
    def removeAxioma(self, type1, type2):
        """
        Removes the axiomconnection between the leaves that are given as parameters.

        Returns
        -------
        None
        """
        if(self.incremental == True):
            print("The following axiom connection was removed (data, label): ", type1.data, type1.label, type2.data, type2.label)
        if(type1.axiom == type2 or type2.axiom != type1):
            type1.axiom = None
            type2.axiom = None
            #Keep track of the axioms that were already made, but had to be removed
            type1.axiomRemoved.append(type2)
            type2.axiomRemoved.append(type1)

class BuildStartTree:
    '''build the prooftree of the input sentence, first build tree per word in linked list'''
    def __init__(self, linkedList, incremental):
        self.linkedList = linkedList
        self.labelLeaves = 1
        self.output = []
        self.incremental = incremental
        
    def readRoot(self):
        '''read what type is in the root, depending on this, call /,\,*'''
        linkedList = self.linkedList
        node = linkedList.root
        passedTrees = []
        axiomList = []
        notConnected = []
        while node:
            root = None
            parent = None
            iLink = None
            tree = Tree()
            stringtype = node.data[1]
            type_polarity = node.data[2]
            self.output.append(node.data[0])
            #check the connective of the root and call that connective class
            parser_obj = type_parser.TypeParser()
            typelist = parser_obj.createList(stringtype)
            root = tree.insertVertex(root, typelist, "root", type_polarity, parent, iLink)
            #if there is a connective in the string on which we need to split
            self.build(root, tree, typelist, type_polarity)

            passedTrees.append(root)
            #op dit punt heb je (als je net begonnen bent) 1 boom gemaakt. Nu wil je dus alvast kijken naar welke mogelijke axioma verbindingen er zijn.
            axioma_object = Axioma(root, passedTrees, axiomList, notConnected, self.incremental)
            axiomListAndnotConnected = axioma_object.find_leaf(root)
            if(axiomListAndnotConnected != None):
                if(axiomListAndnotConnected[0] != None and axiomListAndnotConnected[0] != []):
                    axiomList = axiomListAndnotConnected[0]
                if(axiomListAndnotConnected[1] != None and axiomListAndnotConnected[1] != []):
                    notConnected = axiomListAndnotConnected[1]
            node = node.next
        #in the notConnected list are all the nodes that do not have any axiom connections after creating the entire proofnet. 
        #We want to search the Lexicon to create an axiom connection
        if(len(notConnected) > 0):
            for elem in notConnected:
                for elem2 in notConnected:
                    if(elem != elem2):
                        #check of er tussen deze niet al een axioma kan worden gemaakt
                        if(elem.data == elem2.data and elem.polarity != elem2.polarity):
                            axioma_object = Axioma(elem, passedTrees, axiomList, notConnected, self.incremental)
                        if(elem.axiom == elem2):
                            notConnected.remove(elem)
                            notConnected.remove(elem2)
        if(len(notConnected) > 0):
            self.findNewType(notConnected, passedTrees, axiomList, self.incremental)
        #if we have found the missing word, we want to output it to the console
        print("You were looking for the following sentence:")
        outputString = self.toOutput()
        print(outputString)

    def toOutput(self):
        ''' convert the output list to a string and print it'''
        outputString = " "
        for word in self.output:
            if(word == None):
                self.output.remove(word)
        return outputString.join(self.output)

    def build(self, root, tree, typelist, type_polarity):
        connective_incl = False
        for element in typelist:
            if(element == '/' or element == '\\' or element == '*'):
                connective_incl = True
        if(connective_incl == True): #as long as we can split and build the tree
            iLink = None #set i-link type to None
            if(typelist[1] == "/"):
                over_obj = Over(type_polarity, typelist)
                #example typelist of N\N is [N,\,N]
                pol = over_obj.get_polarity_and_iLink()
                left_child = pol[3]
                right_child = pol[4]
                left_pol = pol[0]
                right_pol = pol[1]
                iLink = pol[2]
            elif(typelist[1] == "\\"):
                under_obj = Under(type_polarity, typelist)
                pol = under_obj.get_polarity_and_iLink()
                left_child = pol[3]
                right_child = pol[4]
                left_pol = pol[0]
                right_pol = pol[1]
                iLink = pol[2]
            elif (typelist[1] == "*"):
                product_obj = Product(type_polarity, typelist)
                pol = product_obj.get_polarity_and_iLink()
                left_child = pol[3]
                right_child = pol[4]
                left_pol = pol[0]
                right_pol = pol[1]
                iLink = pol[2]

            #add values of seperated root to tree, including their polarity
            connective_incl_left = False
            connective_incl_right = False
            if left_child != None and left_pol != None:
                for element in left_child:
                    #als de lijst uit alleen maar axioma's bestaat, dan staat er wss een NP type in dat gezien wordt als twee elementen
                    #in dit geval maken we een nieuwe lijst van dat element en geven we die mee
                    if(element == '/' or element == '\\' or element == '*'):
                        connective_incl_left = True
                if(connective_incl_left == False):
                    new_typelist_left = [left_child]
                    tree.insertVertex(root, new_typelist_left, "left", left_pol, root, iLink)
                else:
                    tree.insertVertex(root, left_child, "left", left_pol, root, iLink)
            if right_child != None and right_pol != None:
                for element in right_child:
                    if(element == '/' or element == '\\' or element == '*'):
                        connective_incl_right = True
                if(connective_incl_right == False):
                    new_typelist_right = [right_child]
                    tree.insertVertex(root, new_typelist_right, "right", right_pol, root, iLink)
                else:
                    tree.insertVertex(root, right_child, "right", right_pol, root, iLink)
                
            #check if we need to split the types any further
            if(connective_incl_left == True):
                self.build(root.left, tree, left_child, left_pol)
            else:
                root.left.label = self.labelLeaves
                self.labelLeaves += 1
                root.left.isLeaf = True

            if(connective_incl_right == True):
                self.build(root.right, tree, right_child, right_pol)
            else:
                root.right.label = self.labelLeaves
                self.labelLeaves += 1
                root.right.isLeaf = True
        else:
            #give the leaf a label and count one to the label total, so that the next leaf will get a label that is one higher than the current.
            root.label = self.labelLeaves
            self.labelLeaves += 1
            root.data = [root.data]
            root.isLeaf = True

    def findListSize(self, typelist, typelistLength):
        ''' Get number of elements in a type that has multiple lists'''
        # Iterate over the list
        tempLength = 0
        for elem in typelist:
            # Check if type of element is list
            if type(elem) == list:
                # Again call this function to get the size of this element
                tempLength = typelistLength
                typelistLength += self.findListSize(elem, typelistLength)
            elif(elem != "/" and elem != "\\" and elem != "*"):
                typelistLength += 1    
        typelistLength -= tempLength
        return typelistLength

    def findNewType(self, notConnected, passedTrees, axiomList, incremental):
        #this method is used to find new types for the types from the notConnected list by searching the lexicon.
        #ik ga ervan uit dat kruizen niet meer mogelijk zijn, omdat hier met de opbouw van het bewijsnet rekening mee is gehouden
        #ik ga ervan uit dat de parser maar 1 woord kan aanvullen, dus er moet een type bestaan dat dezelfde grootte heeft als de notCon lijst
        lexicon_obj = lexicon_parser.Lexicon()
        lexicon_obj.createLexicon()
        possibleType = None
        size = len(notConnected)
        hasSingleType = False
        notCon = []
        templLabelLeaves = self.labelLeaves
        for elem in notConnected:
            notCon.append(elem)
        if(size == 1):
            hasSingleType = True
        for leaf in notConnected:
            notPossible = []
            for lexicon_word, lexicon_type in lexicon_obj.lexicon.items():
                if(lexicon_type not in notPossible):
                    if(leaf.data[0] in lexicon_type):
                        newConnected = []
                        for elem in notConnected:
                            newConnected.append(elem)
                        possibleType = lexicon_type
                        parser_obj = type_parser.TypeParser()
                        typelist = parser_obj.createList(lexicon_type)
                        contains_con = False
                        for element in typelist:
                            if(element == "/" or element == "\\" or element == "*"):
                                #set value of bool to true if there appears a connective in the list. If this is not the case, 
                                # then we know that a type such as "NP" is a single type.
                                contains_con = True
                        if(contains_con == False and len(typelist) > 1):
                            #set a type such as "NP" as a single type.
                            new_typelist = [typelist]
                        else:
                            new_typelist = typelist
                        typelistLength = len(new_typelist)
                        if((hasSingleType and typelistLength == 1)  or (hasSingleType == False)):
                            #if there is only a single leaf that still needs an axiom connection, then we want a lexicon type that has a single connection as well
                            typelistLength = 0
                            typelistLength = self.findListSize(new_typelist, typelistLength)
                            if(len(new_typelist) == 1 and hasSingleType):
                                #in this case the typelist contains only a single leaf
                                root = None
                                parent = None
                                iLink = None
                                tree = Tree()
                                #check the connective of the root and call that connective class
                                root = tree.insertVertex(root, typelist, "root", 1, parent, iLink)
                                #if there is a connective in the string on which we need to split
                                self.build(root, tree, typelist, 1)
                                axioma_object = Axioma(root, passedTrees, axiomList, notConnected, incremental)
                                axiomListAndnotConnected = axioma_object.find_leaf(root)
                                if(not axiomListAndnotConnected[1]):
                                    self.output.append(lexicon_word)
                                    break
                            if(len(notConnected) == typelistLength):
                                #only if the amount of leaves in that still need a connection is the same as the amount of leaves in the new type from the lexicon,
                                #we want to go on checking if they match
                                for element in new_typelist:
                                    foundType = False
                                    if(len(element) < 3):
                                        if(element != "/" and element != "\\" and element != "*"):
                                            #in this case, the element is a type
                                            for leaf2 in newConnected:
                                                if(leaf != leaf2):
                                                    if(leaf2.data[0] == element):
                                                        foundType = True
                                                        newConnected.remove(leaf2)
                                        else:
                                            foundType = True
                                    else: #if the current element is a type like [NP/S]
                                        foundType = self.findTypeCombo(element, foundType, newConnected)

                                    if(foundType == False):
                                        #if we were not able to match an element from the typelist with an element from the notConnected list, 
                                        # then we know we are not looking for this type from the lexicon
                                        notPossible.append(lexicon_type)
                                        break
                                if(foundType == True):
                                    #if all types are able to connect, then do so
                                    root = None
                                    parent = None
                                    iLink = None
                                    tree = Tree()
                                    #check the connective of the root and call that connective class
                                    root = tree.insertVertex(root, typelist, "root", 1, parent, iLink)
                                    #if there is a connective in the string on which we need to split
                                    self.build(root, tree, typelist, 1)
                                    axioma_object = Axioma(root, passedTrees, axiomList, notConnected, incremental)
                                    axiomListAndnotConnected = axioma_object.find_leaf(root)
                                    if(axioma_object.notConnected == []):
                                        if(not axioma_object.notConnected):
                                            self.output.append(lexicon_word)
                                            break
                                    else:
                                        self.labelLeaves = templLabelLeaves
                                        notConnected.clear()
                                        for i in notCon:
                                            notConnected.append(i)
                                        notPossible.append(lexicon_type)
                                        tree.removeVertex(root)
                    else:
                        notPossible.append(lexicon_type)

    def findTypeCombo(self, element, foundType, newConnected):
        for el in element:
            if(len(el) < 3):
                if(el != "/" and el != "\\" and el != "*"):
                    #in this case, the element is a type
                    for leaf2 in newConnected:
                        if(el != leaf2):
                            if(leaf2.data[0] == el):
                                foundType = True
                                newConnected.remove(leaf2)
            else:
                return self.findTypeCombo(el, foundType, newConnected)
        return foundType

class Over:
    def __init__(self, polarity, typelist):
        '''je wil weten of de root een output polarity heeft of een input polarity. Bij een ingevulde zin hebben de woorden een input polarity, maar de S heeft een output polarity.'''
        self.polarity = polarity
        self.typelist = typelist

    def get_polarity_and_iLink(self):
        '''de polariteit van de linker moet input zijn (gevuld rondje/1), de polariteit van de rechter moet output zijn (leeg rondje). BIJ EEN INPUT POLARITY ROOT.
        If the root is input, the transition will get an ii-link. Else it will get an i-link.'''
        if self.polarity == 1:
            left = self.typelist[0]
            right = self.typelist[2]
            iLink = 2
        else:
            left = self.typelist[2]
            right = self.typelist[0] 
            iLink = 1
        left_pol = 1
        right_pol = 0
        return left_pol, right_pol, iLink, left, right
    

class Under:
    def __init__(self, polarity, typelist):
        self.polarity = polarity
        self.typelist = typelist

    def get_polarity_and_iLink(self):
        '''de polariteit van de linker moet output zijn (leeg rondje), de polariteit van de rechter moet input zijn (gevuld rondje). BIJ EEN INPUT POLARITY ROOT.'''
        if self.polarity == 1:
            left = self.typelist[0]
            right = self.typelist[2]
            iLink = 2
        else:
            left = self.typelist[2]
            right = self.typelist[0]
            iLink = 1
        left_polarity = 0
        right_polarity = 1
        return left_polarity, right_polarity, iLink, left, right

class Product:
    def __init__(self, polarity, typelist):
        self.polarity = polarity
        self.typelist = typelist

    def get_polarity_and_iLink(self):
        '''de polariteit van beide dat ze input moeten zijn (gevuld rondje). BIJ EEN INPUT POLARITY ROOT.'''
        if self.polarity == 1:
            left_polarity = 1
            right_polarity = 1
            iLink = 1
            left = self.typelist[0]
            right = self.typelist[2]
        else:
            left_polarity = 0
            right_polarity = 0
            iLink = 2
            left = self.typelist[2]
            right = self.typelist[0]
        return left_polarity, right_polarity, iLink, left, right


def main():
    read_sentence = Read
    incremental = read_sentence.incremental
    linkedlist = read_sentence.lijst
    obj = BuildStartTree(linkedlist, incremental)
    read_root = obj.readRoot()

if __name__ == '__main__':
    main()
