from input_parser import read
import lexicon_parser
import type_parser

class Vertex:
    def __init__(self, data, polarity, parent, iLink):
        self.data = data #hier is opgeslagen wat de waarde van de knoop is
        self.left = None
        self.right = None
        self.polarity = polarity #dit is de polariteit van de knoop
        self.isLeaf = False
        self.parent = parent
        self.iLink = iLink
        self.visited = False
        self.axiom = None
        self.axiomRemoved = [] #so that we will not try to make the same axioms that cannot be made over and over again.
        self.label = None #used for labelling all of the leaves, so we can check if any of the axiom connections cross each other.
        self.potentialAxiom = [] #used for keeping track of all the possible vertices that can connect with the current vertex.

class Tree:
    def createVertex(self, data, polarity, parent, iLink):
        '''wanneer er een splitsing is door een connectief, moeten deze gesplitste typen ook weer vertices worden. Deze moeten worden opgeslagen.'''
        return Vertex(data, polarity, parent, iLink)

    def insertVertex(self, vertex, data, place, polarity, parent, iLink):
        if vertex == None:
            #if root is still empty, create a node
            return self.createVertex(data, polarity, parent, iLink)

        if place == "left":
            vertex.left = self.insertVertex(vertex.left, data, "left", polarity, parent, iLink)
        elif place == "right":
            vertex.right = self.insertVertex(vertex.right, data, "right", polarity, parent, iLink)
        else: #if it is a root element
            vertex = self.insertVertex(vertex, data, "root", polarity, parent, iLink)
        return vertex, polarity, parent, iLink
#MOET NOG EVEN REMOVE FIXEN
    def removeVertex(self, vertex, data):
        '''stel een verkeerde splitsing, dan moet de oude vertex verwijderd worden samen met al zijn kinderen.'''
        #if the vertex that we want to delete does not exist in the current tree
        if vertex is None:
            return None
        #print(vertex.data)
        #zoek door boom naar vertex die verwijderd moet worden
        #als data gelijk is aan de data van de huidige knoop waar we naar kijken
        if data == vertex.data:
            #if root element is the vertex we want to delete, remove it plus its children
            del vertex

        else: #je wil beide kanten op gaan kijken wat verwijderd moet worden > recursieve aanroep??
            if vertex.left != None:
                self.removeVertex(vertex.left, data)
                #print(vertex.left.data)
            if vertex.right != None:
                self.removeVertex(vertex.right, data)
                #print(vertex.right.data)

            return vertex
    
    def traverseInorder(self, root):
        """
        traverse function will print all the node in the tree.
        """
        if root is not None:
            self.traverseInorder(root.left)
            print (root.data)
            self.traverseInorder(root.right)

# class PossibleAxiomCombo:
#     def __init__(self):
#         self.allAxioms = []
    
#     def save(self, axiomCombo):
#         self.allAxioms.append(axiomCombo)

class Axioma:
    def __init__(self, root, tree, passedTrees, connected, tempList):
        '''kijken welke axioma's moeten ontstaan vanuit vertex met polarity'''
        self.tree = tree
        self.root = root
        self.passedTrees = passedTrees
        self.cycleFound = False
        self.iLinkPassed = False
        self.doCross = False
        self.connected = connected #a list with lists containing all possible axiom combinations by saving all axiom tuples where (output, input)
        self.tempList = tempList
        #self.notConnected = [] #save all vertices that are not connected

    def find_leaf(self, root):
        #als er geen node meer is die onleed kan worden, dan moeten we axioma verbindingen maken die elke vertex langs gaat
        if(root.isLeaf == True and root.axiom == None):
            #if the current vertex is also a leaf, then we need to create an axiom with another vertex
            #self.find_vertex(root)
            self.findOtherTree(root)
            #return self.connected
            return (self.tempList)
            #return self.notConnected
        else:
            #if the current vertex is not a leaf and it has children, go to that child
            if(root.left != None and root.right != None):
                self.find_leaf(root.left)
                self.find_leaf(root.right)
    
    def find_leafOtherTree(self, root, rootOtherTree):
        #if the current vertex is also a leaf, then we need to create an axiom with another vertex
        if(rootOtherTree.left != None and rootOtherTree.right != None):
            #you always look at the trees on the left of the current tree, so we want to connect the most right leaves first.
            #set root to visited?? Of hoeft dat niet omdat we in een andere boom aan het werken zijn aha
            mostRightLeaf = self.find_mostRightLeaf(root, rootOtherTree)
            self.toFalse(root)
            self.toFalse(rootOtherTree)
            if(mostRightLeaf != None):
                if(root.axiom == None):                            
                    #root.potentialAxiom.append(mostRightLeaf)
                    # if(root in self.notConnected):
                    #     self.notConnected.remove(root)
                    # if(mostRightLeaf in self.notConnected):
                    #     self.notConnected.remove(mostRightLeaf)
                    self.createAxioma(root, mostRightLeaf)
                    #if the just made axiom was removed, we need to create another axiom
                    if(root.axiom != mostRightLeaf):
                        if((len(root.potentialAxiom) > 0) and root.axiom == None):
                            #in this case we did add possible axioms to the list
                            connect = None
                            for elem in root.potentialAxiom: #nu pak je alleen maar de eerste uit de lijst en kijk je niet verder, dus ook niet als met dat element geen verbinding kan worden gemaakt!!!
                                axiom = elem.axiom
                                if(elem not in root.axiomRemoved):
                                    if(elem.axiom != None):
                                        self.removeAxioma(elem, elem.axiom)
                                        connect = elem
                                        self.createAxioma(root, connect)
                                        if(root.axiom == connect):
                                            break
                                        else:
                                            #if the current node is not connected with the root, then the old axiom needs to be restored
                                            self.removeAxioma(root, elem)
                                            elem.axiomRemoved.remove(axiom)
                                            axiom.axiomRemoved.remove(elem)
                                            self.createAxioma(elem, axiom)
                                    else:
                                        connect = elem
                                        self.createAxioma(root, connect)
                                        if(root.axiom == connect):
                                            break
                                        else:
                                            #if the current node is not connected with the root, then the old axiom needs to be restored
                                            self.removeAxioma(root, elem)
                                            elem.axiomRemoved.remove(axiom)
                                            axiom.axiomRemoved.remove(elem)
                                            self.createAxioma(elem, axiom)
                else:
                    # if(root not in self.notConnected and root.axiom == None):
                    #     print("we added the following to the notcon list ",root.data, root.label, root.axiom)
                    #     self.notConnected.append(root)
                    return None
            else: 
                #als er geen axiomaverbinding gemaakt kan worden in de huidige boom, dan moet je kijken naar andere bomen
                if((len(root.potentialAxiom) > 0) and root.axiom == None):
                    #in this case we did add possible axioms to the list
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
                                    #if the current node is not connected with the root, then the old axiom needs to be restored
                                    self.removeAxioma(root, elem)
                                    elem.axiomRemoved.remove(axiom)
                                    axiom.axiomRemoved.remove(elem)
                                    self.createAxioma(elem, axiom)
                else:
                    #if the node we want to connect with already has an axiom connection, remove that connection
                    for elem in root.potentialAxiom: #nu pak je alleen maar de eerste uit de lijst en kijk je niet verder, dus ook niet als met dat element geen verbinding kan worden gemaakt!!!
                        axiom = elem.axiom
                        if((len(root.potentialAxiom) > 0) and root.axiom == None):
                            if(elem not in root.axiomRemoved):
                                if(elem.axiom != None):
                                    self.removeAxioma(elem, elem.axiom)
                                    connect = elem
                                    self.createAxioma(root, connect)
                                    if(root.axiom == connect):
                                        break
                                    else:
                                        #if the current node is not connected with the root, then the old axiom needs to be restored
                                        self.removeAxioma(root, elem)
                                        elem.axiomRemoved.remove(axiom)
                                        axiom.axiomRemoved.remove(elem)
                                        self.createAxioma(elem, axiom)

                # else:
                #     # if(root not in self.notConnected and root.axiom == None):
                #     #     print("we added the following to the notcon list ",root.data, root.label, root.axiom)
                #     #     self.notConnected.append(root)
                #     return None
        else:
            #if the other tree exists of only a single node, we need to check if that node can be connected
            if(rootOtherTree.data == root.data and rootOtherTree.polarity != root.polarity):
                root.potentialAxiom.append(rootOtherTree)
                if(root.axiom == None):
                    self.createAxioma(root, rootOtherTree)
            else:
                # if(root not in self.notConnected and root.axiom == None):
                #     print("we added the following to the notcon list ",root.data, root.label, root.axiom)
                    # self.notConnected.append(root)
                return None

    def find_vertex(self, root):
        '''vind een knoop waarmee de input vertex een axioma verbinding mee kan vormen
        First look in the closest neighbour trees. If an axiom connection cannot be made, continue to the tree in which the current node appears as well.'''
        #je geeft altijd de root mee, dus als de root geen linker- en rechterkind heeft, dan bestaat de boom uit alleen maar de root en wil je sowieso een axioma 
        # verbinding met een andere boom uitvoeren
        #print(root.data, root.polarity, root.parent.data, "1")
        #self.findOtherTree(root) #even kijken wat handig is
        if(self.root.right != None and self.root.left != None):
            #kijk eerst naar het andere kind van de parent
            #als de huidige knoop het rechterkind is, kijk naar links. Anders kijk naar rechts
            if(root.parent.left != root):
                if(root.parent.left.isLeaf == True):
                    if(root.data == root.parent.left.data and root.polarity != root.parent.left.polarity):
                        #print(root.data , root.polarity , root.parent.left.data , root.parent.left.polarity)
                        self.createAxioma(root, root.parent.left)
                    else:
                        root.visited = True
                        mostRightLeaf = self.find_mostRightLeaf(root, root.parent.left)
                        self.toFalse(root)
                        if(mostRightLeaf != None):
                            self.createAxioma(root, mostRightLeaf)
                        else: 
                            #als er geen axiomaverbinding gemaakt kan worden in de huidige boom, dan moet je kijken naar andere bomen
                            self.findOtherTree(root)
                else:
                    #hier ga je kijken naar de linkerbuur, en is de root dus de rechterbuur van de parent. 
                    # Dus de leaves die het dichtst bij de huidige root zitten, zitten rechts van de linkerbuur van de parent.
                    #Dus kijk eerst naar rechts van root.parent.left
                    root.visited = True
                    mostRightLeaf = self.find_mostRightLeaf(root, root.parent.left)
                    #hier moet je alle visits weer op false zetten
                    if(mostRightLeaf != None):
                        self.createAxioma(root, mostRightLeaf)
                    else: 
                        #als er geen axiomaverbinding gemaakt kan worden in de huidige boom, dan moet je kijken naar andere bomen
                        self.findOtherTree(root)
                    #kijk telkens per leaf of hij verbonden kan worden met de root
            else: #if root.parent.right != root
                if(root.parent.right.isLeaf == True):
                    if(root.data == root.parent.right.data and root.polarity != root.parent.right.polarity):
                        #print(root.data , root.polarity , root.parent.right.data , root.parent.right.polarity)
                        self.createAxioma(root, root.parent.right)
                    else:
                        root.visited = True
                        mostLeftLeaf = self.find_mostLeftLeaf(root, root.parent.right)
                        self.toFalse(root)
                        if(mostLeftLeaf != None):
                            self.createAxioma(root, mostLeftLeaf)
                        else: 
                            #als er geen axiomaverbinding gemaakt kan worden in de huidige boom, dan moet je kijken naar andere bomen
                            self.findOtherTree(root)
                else:
                    root.visited = True
                    mostLeftLeaf = self.find_mostLeftLeaf(root, root.parent.right)
                    self.toFalse(root)
                    if(mostLeftLeaf != None):
                        self.createAxioma(root, mostLeftLeaf)
                    else: 
                        #als er geen axiomaverbinding gemaakt kan worden in de huidige boom, dan moet je kijken naar andere bomen
                        self.findOtherTree(root)
        else: 
            #als er geen verbinding binnen de eigen boom kan worden gemaakt, dan moet dat met een andere boom gebeuren.
            self.findOtherTree(root)

    def findOtherTree(self, root):
        for rootPassed, treePassed in self.passedTrees:
            #check for each tree that we already constructed if there is an axiom connection possible
            if(self.root != rootPassed):
                print("passed",rootPassed.data, self.root.data)
                #if the root of the current tree is not the same as the root of the tree that we want to connect, 
                # then we can try to find leaves to connect in that tree
                self.find_leafOtherTree(root, rootPassed)

    
    def find_mostRightLeaf(self, vertexOut, vertexIn):
        '''If the vertex we want to connect is closest to the right side of the neighbour tree.'''
        #root of the tree in which we want to search now it vertexIn.
        if(vertexIn.visited == True):
            if(vertexIn.parent != None):
                return self.find_mostRightLeaf(vertexOut, vertexIn.parent)
            else:
                return None
        if(vertexIn.isLeaf == True):
            if(vertexIn.data == vertexOut.data and vertexIn.polarity != vertexOut.polarity):
                print("wat voeg je aan je lijst toe?", vertexOut.label, vertexIn.label, len(vertexOut.potentialAxiom))
                vertexOut.potentialAxiom.append(vertexIn) #add to potential list, we will eventually connect with the first element in this list
                vertexIn.visited = True
                if(vertexIn.parent != None):
                    #de rest van de boom doorzoeken voor een verbinding
                    if(vertexIn.parent.left != vertexIn):
                        if(vertexIn.parent.left.visited == False):
                            return self.find_mostRightLeaf(vertexOut, vertexIn.parent.left)
                        else:
                            return vertexIn
                    else: #vertexIn.parent.right != vertexIn
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
                #if we have reached a leaf, but this is not a leaf we can connect, we need to look at the left side
                if(vertexIn == vertexIn.parent.left): #maar wat als je nu N*N hebt? dan is de polariteit en data hetzelfde?
                    #if we have already looked at the left leaf and we cannot connect this one either, we need to go back to the most recent parent of which
                    #we have not covered the left child yet
                    if(vertexIn.parent.parent != vertexIn and vertexIn.parent.visited == True and vertexIn.parent.parent != None):
                        #if the current parent is already visited, we need to look at the right side of the tree
                        return self.find_mostRightLeaf(vertexOut, vertexIn.parent.parent.left)
                    else:
                        #nu is er blijkbaar geen verbinding mogelijk in de huidige tree.
                        return None
                else:
                    return self.find_mostRightLeaf(vertexOut, vertexIn.parent.left)
        else:
            #go further into the tree
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
                    #if both are not visited yet, we choose the most right vertex
                    return self.find_mostRightLeaf(vertexOut, vertexIn.right)
    
    def find_mostLeftLeaf(self, vertexOut, vertexIn):
        '''If the vertex we want to connect is closest to the left side of the neighbour tree.'''
        #root of the tree in which we want to search now it vertexIn.
        if(vertexIn.visited == True):
            #probleem want vertexIn.parent kan ook None zijn 
            if(vertexIn.parent != None):
                return self.find_mostLeftLeaf(vertexOut, vertexIn.parent) 
            else:
                #if the parents of the current vertex are visited already, we assume that we have visited all vertices
                return None
        elif(vertexIn.isLeaf == True):
            if(vertexIn.data == vertexOut.data and vertexIn.polarity != vertexOut.polarity):
                return vertexIn
            else:
                vertexIn.visited = True
                if(vertexIn.parent.left.visited == True and vertexIn.parent.right.visited == True):
                    vertexIn.parent.visited = True
                #if we have reached a leaf, but this is not a leaf we can connect, we need to look at the left side
                if(vertexIn == vertexIn.parent.right): #maar wat als je nu N*N hebt? dan is de polariteit en data hetzelfde?
                    #if we have already looked at the left leaf and we cannot connect this one either, we need to go back to the most recent parent of which
                    #we have not covered the left child yet
                    if(vertexIn.parent.parent != vertexIn and vertexIn.parent.visited == True and vertexIn.parent.parent != None):
                        #if the current parent is already visited, we need to look at the right side of the tree
                        return self.find_mostLeftLeaf(vertexOut, vertexIn.parent.parent.right)
                    else:
                        #nu is er blijkbaar geen verbinding mogelijk in de huidige tree.
                        return None
                else:
                    return self.find_mostLeftLeaf(vertexOut, vertexIn.parent.right)
        else:
            #go further into the tree
            if(vertexIn.left.visited == True and vertexIn.right.visited == True):
                vertexIn.visited = True
                if(vertexIn.parent != None):
                    return self.find_mostLeftLeaf(vertexOut, vertexIn.parent.right)
                else:
                    return None
            else:
                if(vertexIn.left.visited == True):
                    return self.find_mostLeftLeaf(vertexOut, vertexIn.right)
                elif(vertexIn.right.visited == True):
                    return self.find_mostLeftLeaf(vertexOut, vertexIn.left) 
                else:
                    #if both are not visited yet, we choose the most left vertex
                    return self.find_mostLeftLeaf(vertexOut, vertexIn.left)

    def toFalse(self, root):
        '''After trying to find an axiom connection for one leaf, we want to put back all vertex.visited values to false.'''
        if(root.visited == True):
            #if the visited value of the current vertex is True, then make it true and go to the next vertex
            if(root.right != None and root.left != None):
                if(root.right.visited == True):
                    self.toFalse(root.right)
                elif(root.left.visited == True):
                    self.toFalse(root.left)
                else:
                    #if both the left and the right child have a visited value of False, the root will get a value of false as well
                    root.visited = False
                    if(root.axiom != None):
                        if(root.axiom.visited == True):
                            self.toFalse(root.axiom)
                    if(root.parent != None):
                        self.toFalse(root.parent)
            elif(root.parent != None):
                if(root.parent.right.visited == True):
                    #leaves will always get a visited value of false, if we have passed them
                    root.visited = False
                    if(root.axiom != None):
                        if(root.axiom.visited == True):
                            self.toFalse(root.axiom)
                    self.toFalse(root.parent.right)
                elif(root.parent.left.visited == True):
                    root.visited = False
                    if(root.axiom != None):
                        if(root.axiom.visited == True):
                            self.toFalse(root.axiom)
                    self.toFalse(root.parent.left)
                else:
                    root.visited = False
                    if(root.axiom != None):
                        if(root.axiom.visited == True):
                            self.toFalse(root.axiom)
                    if(root.parent != None):
                        self.toFalse(root.parent)
            else:
                root.visited = False
                if(root.axiom != None):
                    if(root.axiom.visited == True):
                        self.toFalse(root.axiom)
                if(root.parent != None):
                    self.toFalse(root.parent)
        else:
            if(root.parent != None):
                self.toFalse(root.parent)
    
    def createAxioma(self, root, vertex):
        print(root.label, root.axiom , vertex.label, vertex.axiom)
        #kijk voor alle leaves of ze al een verbinding hebben en maak anders een verbinding
        '''het creeren van axioma verbinding tussen vertex en andere knoop.
        Begin bij S(output), ga naar een S(input). Als deze S een left tag heeft, kijk naar het woord dat een right tag heeft en vind hierbij een type.
        Als het woord een right tag heeft, ga naar de left tag en vind hierbij een type.
        Doe opnieuw, totdat elke paren van typen verbonden zijn.
        Als er typen over blijven die nog geen verbinding hebben, sla deze op.'''
        #eerst kijken of de verbinding al bestaat, dan pas een nieuwe axioma verbinding maken
        #ook checken of we niet al eerder hebben geprobeerd deze verbinding te maken
        if((root.axiom != vertex or vertex.axiom != root) and (root.axiom == None and vertex.axiom == None) and 
        (vertex not in root.axiomRemoved and root not in vertex.axiomRemoved)):
            #if an axiom connection already exists between these vertices, we do not make another connection
            # if(root in self.notConnected):
            #     print("we have removed the following from the notcon list ", root.data, root.label, root.axiom)
            #     self.notConnected.remove(root)
            # if(vertex in self.notConnected):
            #     print("we have removed the following from the notcon list ",vertex.data, vertex.label, vertex.axiom)
            #     self.notConnected.remove(vertex)
            root.axiom = vertex
            vertex.axiom = root
            print("een axioma verbinding is gemaakt ", root.data ,root.label,  vertex.data, vertex.label )
            #als de verbinding is gemaakt dan wil je kijken of de verbinding uberhaupt mogelijk is
            #dit checken gaat telkens vanuit de output naar input polariteit, dus kijk eerst welke kant de axioma verbinding op loopt
            if(root.polarity == 0):
                self.checkForCycle(root, vertex)
                self.checkForCross(root, vertex)
                self.tempList.append([root, vertex])
            else:
                self.checkForCycle(vertex, root)
                self.checkForCross(vertex, root)
                self.tempList.append([vertex, root])
            
            self.toFalse(root)
            self.toFalse(vertex)

            if((self.cycleFound == True and self.iLinkPassed == False) or self.doCross == True):
                #in this case there is a cycle and we want to get rid of the last axiom made
                self.cycleFound = False
                self.doCross = False
                print("removed",  root.data, root.label ,  vertex.data, vertex.label)
                self.removeAxioma(root, vertex)
                #remove last added item of list
                self.tempList.pop()
                # self.notConnected.append(root)
                # self.notConnected.append(vertex)

            #set iLink back to false for next axiom
            self.iLinkPassed = False
    
    def find_leafCross(self, root, leaves):
        #als er geen node meer is die onleed kan worden, dan moeten we axioma verbindingen maken die elke vertex langs gaat
        if(root.isLeaf == True):
            #if the current vertex is also a leaf, append to the list
            leaves.append(root)
        else:
            #if the current vertex is not a leaf and it has children, go to that child
            if(root.left != None and root.right != None):
                self.find_leafCross(root.left, leaves)
                self.find_leafCross(root.right, leaves)
        return leaves

    def checkForCross(self, rootOutput, rootInput):
        '''Check if any axiom connections cross each other'''
        if((rootOutput.label == (rootInput.label + 1)) or (rootOutput.label == (rootInput.label - 1))):
            #if both axiom leaves appear next to each other, we know for sure that there will not be any crosses
            return self.doCross
        else:
            noAxiom = []
            #if not, we need to check what vertices appear between them and if these vertices can connect with each other
            if(rootOutput.label > rootInput.label):
                #contract 1 from outputlabel, since 4-3=1, even though there are not any leaves between them
                if(((rootOutput.label - 1) - rootInput.label) % 2 != 0):
                    #if there is not an even amount of vertices between them, we know for sure they cannot all connect with another vertex without crossing
                    self.doCross = True
                    return self.doCross
                else:
                    for vertex, tree in self.passedTrees:
                        if(vertex.isLeaf == False):
                            leaves = []
                            leaves = self.find_leafCross(vertex, leaves)
                            for leaf in leaves:
                                if(leaf != rootOutput and leaf != rootInput):
                                    if(leaf.label > rootInput.label and leaf.label < rootOutput.label):
                                        #if the current vertex is between the axiom vertices, we need to check if it has an axiom connection
                                        if(leaf.axiom == None):
                                            #if the leaf has no axiom connection, we will have to check later if such a connection is still possible by looking
                                            #  at all of the elements in the noAxiom list 
                                            noAxiom.append(leaf)
                        else:
                            if(vertex != rootOutput and vertex != rootInput):
                                if(vertex.label > rootInput.label and vertex.label < rootOutput.label):
                                    #if the current vertex is between the axiom vertices, we need to check if it has an axiom connection
                                    if(vertex.axiom == None):
                                        #if the leaf has no axiom connection, we will have to check later if such a connection is still possible by looking
                                        #  at all of the elements in the noAxiom list 
                                        noAxiom.append(vertex)

                    #hier checken of de elementen die geen axioma verbinding hebben mogelijk nog met elkaar vebonden kunnen worden

            elif(rootOutput.label < rootInput.label):
                if(((rootInput.label - 1) - rootOutput.label) % 2 != 0):
                    #if there is not an even amount of vertices between them, we know for sure they cannot all connect with another vertex without crossing
                    self.doCross = True
                    return self.doCross
                else:
                    for vertex, tree in self.passedTrees:
                        if(vertex.isLeaf == False):
                            leaves = []
                            leaves = self.find_leafCross(vertex, leaves)
                            for leaf in leaves:
                                if(leaf != rootOutput and leaf != rootInput):
                                    if(leaf.label < rootInput.label and leaf.label > rootOutput.label):
                                        #if the current vertex is between the axiom vertices, we need to check if it has an axiom connection
                                        if(leaf.axiom == None):
                                            #if the leaf has no axiom connection, we will have to check later if such a connection is still possible by looking
                                            #  at all of the elements in the noAxiom list 
                                            noAxiom.append(leaf)
                        else:
                            if(vertex != rootOutput and vertex != rootInput):
                                if(vertex.label > rootInput.label and vertex.label < rootOutput.label):
                                    #if the current vertex is between the axiom vertices, we need to check if it has an axiom connection
                                    if(vertex.axiom == None):
                                        #if the leaf has no axiom connection, we will have to check later if such a connection is still possible by looking
                                        #  at all of the elements in the noAxiom list 
                                        noAxiom.append(vertex)

            #hier checken of de elementen die geen axioma verbinding hebben mogelijk nog met elkaar verbonden kunnen worden
            for vertex1 in noAxiom:
                for vertex2 in noAxiom:
                    if(vertex1 != vertex2):
                        if(vertex1.data == vertex2.data and vertex1.polarity != vertex2.polarity):
                            #dan kan er nog een axioma ontstaan, mits er geen cykel is
                            if(vertex1.polarity == 0):
                                self.checkForCycle(vertex1, vertex2)
                            else:
                                self.checkForCycle(vertex2, vertex1)
                            if(self.cycleFound == False):
                                #if there is no cycle if this would be a connection, then we can delete the elements from the set
                                if(vertex1 in noAxiom and vertex2 in noAxiom):
                                    noAxiom.remove(vertex1)
                                    noAxiom.remove(vertex2)
            #set cycle back to false
            self.cycleFound = False
            if(len(noAxiom) > 0):
                #if there are leaves that could not connect, set cross to true
                self.doCross = True
            return self.doCross

    def checkForCycle(self, rootOutput, rootInput):
        print(rootOutput.label, rootInput.label, "dit zijn de axiomas die we gaan checken")
        '''Check if there are any cycles that do not go through an i-link by adding the new axiom'''
        #als er een directed path van de output node naar de input node is, voordar de verbinding is gemaakt, dan zal er een cykel ontstaan.
        #begin bij de input node, als je door de verbindingen te volgen bij de output node terecht komt dan is er een cykel aanwezig
        
        if(rootInput.isLeaf == True):
            rootInput.visited = True
        else:
            if(rootInput.left.visited == True and rootInput.right.visited == True):
                rootInput.visited = True
        #first look at the closest neighbour of the input node, go further into the tree if we do not reach the output node
        if(rootInput.iLink == 1):
            self.iLinkPassed = True
            #if we have passed an i-link, we know that the cycle is legit and that we can stop searching???
        if(rootInput == rootOutput):
            #if we have found the vertex that is the same as the output vertex, we know there is a cycle
            print("er is een cykel", rootInput.label, rootOutput.label)
            self.cycleFound = True
            return self.cycleFound
        if(rootInput.parent != None):
            if(rootInput.parent.left != rootInput):
                if(rootInput.parent.left.isLeaf == True):
                    #print(rootInput.parent.left.data, rootInput.parent.left.polarity, rootOutput.data, rootOutput.polarity)
                    if(rootInput.parent.left.iLink == 1):
                        self.iLinkPassed = True
                    if(rootInput.parent.left == rootOutput):
                        print("er is een cykel tussen parent left", rootInput.parent.left.label, rootOutput.label)
                        self.cycleFound = True
                        return self.cycleFound
                    else:
                        if(rootInput.parent.left.axiom != None):
                            goToNode = rootInput.parent.left.axiom
                            if(rootInput.parent.parent != None):
                                if(rootInput.parent.parent.left != rootInput.parent):
                                    return self.checkForCycle(rootOutput, rootInput.parent.parent.left)
                                else:
                                    return self.checkForCycle(rootOutput, rootInput.parent.parent.right)
                            #return self.checkForCycle(rootOutput, rootInput.parent.left)
                        else:
                            return self.checkForCycle(rootOutput, rootInput.parent)
                else:
                    #if the current vertex is not a leaf, we want to go to the leaves
                    print(rootInput.parent.left.left, "wtf waarom kom ik ook hier")
                    if(rootInput.parent.left.left.visited == False):
                        return self.checkForCycle(rootOutput, rootInput.parent.left.left)
                    else:
                        print("een cykel is niet mogelijk, dus de axioma verbinding mag blijven")
                        return self.cycleFound
                    if(rootInput.parent.left.right.visited == False):
                        return self.checkForCycle(rootOutput, rootInput.parent.left.right)
                    else:
                        print("een cykel is niet mogelijk, dus de axioma verbinding mag blijven")
                        return self.cycleFound
            elif(rootInput.parent.right != rootInput):
                if(rootInput.parent.right.isLeaf == True):
                    if(rootInput.parent.right.iLink == 1):
                        self.iLinkPassed = True
                    if(rootInput.parent.right == rootOutput):
                        print("er is een cykel tussen parent right", rootInput.parent.right.label, rootOutput.label)
                        self.cycleFound = True
                        return self.cycleFound
                    else:
                        if(rootInput.parent.right.axiom != None):
                            goToNode = rootInput.parent.right.axiom
                            if(rootInput.parent.parent != None):
                                if(rootInput.parent.parent.left != rootInput.parent):
                                    return self.checkForCycle(rootOutput, rootInput.parent.parent.left)
                                else:
                                    return self.checkForCycle(rootOutput, rootInput.parent.parent.right)
                        else:
                            return self.checkForCycle(rootOutput, rootInput.parent)
                else:
                    #if the current vertex is not a leaf, we want to go to the leaves
                    return self.checkForCycle(rootOutput, rootInput.parent.right.left)
                    if(self.cycleFound == False):
                        return self.checkForCycle(rootOutput, rootInput.parent.right.right)
            else:
                return self.checkForCycle(rootOutput, rootInput.parent)

            #check if the current node we are at is the same as the output node, this would be a cycle
            if(goToNode == rootOutput):
                print("Same")
                return self.checkForCycle(rootOutput, goToNode)
            
            if(goToNode.parent != None):
                if(goToNode.parent.right != goToNode):
                    #kijk of de dichtsbijzijnde buur van de node toevallig de node is die we zoeken voor een cykel
                    if(goToNode.parent.right == rootOutput):
                        self.cycleFound = True #hier nog checken voor axioma!
                        return self.cycleFound
                    else:
                        return self.checkForCycle(rootOutput, goToNode.parent)
                elif(goToNode.parent.left != goToNode):
                    if(goToNode.parent.left == rootOutput):
                        print("er is een cykel gevonden")
                        self.cycleFound = True
                        return self.cycleFound
                    else:
                        return self.checkForCycle(rootOutput, goToNode.parent)
                else:
                    return self.checkForCycle(rootOutput, goToNode.parent)
            else:
                #if the current node has no parent, and we already checked the children (if they have any), then there is no cycle
                print("een cykel is niet mogelijk, dus de axioma verbinding mag blijven")
                return self.cycleFound
        else:
            print("een cykel is niet mogelijk, dus de axioma verbinding mag blijven")
            return self.cycleFound
    
    def removeAxioma(self, type1, type2):
        '''verwijderen axioma tussen type1 en type2'''
        if(type1.axiom == type2 or type2.axiom != type1):
            type1.axiom = None
            type2.axiom = None
            #keep track of the axioms we already tried to make, but had to remove
            type1.axiomRemoved.append(type2)
            type2.axiomRemoved.append(type1)

class BuildStartTree:
    '''build the prooftree of the input sentence, first build tree per word in linked list'''
    def __init__(self, linkedList):
        self.linkedList = linkedList
        self.labelLeaves = 1
        
    def readRoot(self):
        '''read what type is in the root, depending on this, call /,\,*'''
        linkedList = self.linkedList
        node = linkedList.root
        #saveCombo_obj = PossibleAxiomCombo()
        passedTrees = []
        connected = []
        axiomList = []
        possibleConnection = []
        while node:
            root = None
            left_vertex = None
            right_vertex = None
            left_pol = None
            right_pol = None
            parent = None
            iLink = None
            tree = Tree()
            stringtype = node.data[1]
            type_polarity = node.data[2]
            #check the connective of the root and call that connective class
            parser_obj = type_parser.TypeParser()
            typelist = parser_obj.createList(stringtype)
            #print(type_polarity)
            root = tree.insertVertex(root, typelist, "root", type_polarity, parent, iLink)
            #if there is a connective in the string on which we need to split
            self.build(root, tree, typelist, type_polarity)
            #tree.traverseInorder(root)

            passedTrees.append([root, tree])
            #op dit punt heb je (als je net begonnen bent) 1 boom gemaakt. Nu wil je dus alvast kijken naar welke mogelijke axioma verbindingen er zijn.
            axioma_object = Axioma(root, tree, passedTrees, connected, axiomList)
            axioList = axioma_object.find_leaf(root)
            if(axioList != None and axioList != []):
                axiomList = axioList

            # for item in axiomList:
            #     print(item[0].data, item[1].data)
            node = node.next

        #nu ben je alle bomen langs gegaan, kijk naar de knopen die nog geen verbinding hebben
        connected.append(axiomList)
        print(len(connected))

    def build(self, root, tree, typelist, type_polarity):
        connective_incl = False
        for element in typelist:
            if(element == '/' or element == '\\' or element == '*'):
                connective_incl = True
        if(connective_incl == True): #as long as we can split and build the tree
            iLink = None #set i-link type to None
            if(typelist[1] == "/"):
                over_obj = Over(type_polarity)
                #example typelist of N\N is [N,\,N]
                pol = over_obj.get_polarity_and_iLink()
                left_pol = pol[0]
                right_pol = pol[1]
                iLink = pol[2]
            elif(typelist[1] == "\\"):
                under_obj = Under(type_polarity)
                pol = under_obj.get_polarity_and_iLink()
                left_pol = pol[0]
                right_pol = pol[1]
                iLink = pol[2]
            elif (typelist[1] == "*"):
                product_obj = Product(type_polarity)
                pol = product_obj.get_polarity_and_iLink()
                left_pol = pol[0]
                right_pol = pol[1]
                iLink = pol[2]

            #add values of seperated root to tree, including their polarity
            connective_incl_left = False
            connective_incl_right = False
            if typelist[0] != None and left_pol != None:
                for element in typelist[0]:
                    #als de lijst uit alleen maar axioma's bestaat, dan staat er wss een NP type in dat gezien wordt als twee elementen
                    #in dit geval maken we een nieuwe lijst van dat element en geven we die mee
                    if(element == '/' or element == '\\' or element == '*'):
                        connective_incl_left = True
                if(connective_incl_left == False):
                    new_typelist_left = [typelist[0]]
                    tree.insertVertex(root, new_typelist_left, "left", left_pol, root, iLink)
                else:
                    tree.insertVertex(root, typelist[0], "left", left_pol, root, iLink)
            if typelist[2] != None and right_pol != None:
                for element in typelist[2]:
                    if(element == '/' or element == '\\' or element == '*'):
                        connective_incl_right = True
                if(connective_incl_right == False):
                    new_typelist_right = [typelist[2]]
                    tree.insertVertex(root, new_typelist_right, "right", right_pol, root, iLink)
                else:
                    tree.insertVertex(root, typelist[2], "right", right_pol, root, iLink)
                
            #check if we need to split the types any further
            if(connective_incl_left == True):
                self.build(root.left, tree, typelist[0], left_pol)
            else:
                root.left.label = self.labelLeaves
                self.labelLeaves += 1
                root.left.isLeaf = True

            if(connective_incl_right == True):
                self.build(root.right, tree, typelist[2], right_pol)
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

class Over:
    def __init__(self, polarity):
        '''je wil weten of de root een output polarity heeft of een input polarity. Bij een ingevulde zin hebben de woorden een input polarity, maar de S heeft een output polarity.'''
        self.polarity = polarity

    def get_polarity_and_iLink(self):
        '''de polariteit van de linker moet input zijn (gevuld rondje/1), de polariteit van de rechter moet output zijn (leeg rondje). BIJ EEN INPUT POLARITY ROOT.
        If the root is input, the transition will get an ii-link. Else it will get an i-link.'''
        if self.polarity == 1:
            left_pol = 1
            right_pol = 0
            iLink = 2
        else:
            left_pol = 0
            right_pol = 1  
            iLink = 1
        return left_pol, right_pol, iLink
    

class Under:
    def __init__(self, polarity):
        self.polarity = polarity

    def get_polarity_and_iLink(self):
        '''de polariteit van de linker moet output zijn (leeg rondje), de polariteit van de rechter moet input zijn (gevuld rondje). BIJ EEN INPUT POLARITY ROOT.'''
        if self.polarity == 1:
            left_polarity = 0
            right_polarity = 1
            iLink = 2
        else:
            left_polarity = 1
            right_polarity = 0
            iLink = 1
        return left_polarity, right_polarity, iLink

class Product:
    def __init__(self, polarity):
        self.polarity = polarity

    def get_polarity_and_iLink(self):
        '''de polariteit van beide dat ze input moeten zijn (gevuld rondje). BIJ EEN INPUT POLARITY ROOT.'''
        if self.polarity == 1:
            left_polarity = 1
            right_polarity = 1
            iLink = 1
        else:
            left_polarity = 0
            right_polarity = 0
            iLink = 2
        return left_polarity, right_polarity, iLink


def main():
    read_sentence = read
    linkedlist = read_sentence.lijst
    obj = BuildStartTree(linkedlist)
    read_root = obj.readRoot()

if __name__ == '__main__':
    main()
