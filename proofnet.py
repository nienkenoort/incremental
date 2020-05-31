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


class Axioma:
    def __init__(self, root, tree):
        '''kijken welke axioma's moeten ontstaan vanuit vertex met polarity'''
        self.tree = tree
        self.root = root

    def find_leaf(self, root):
        #als er geen node meer is die onleed kan worden, dan moeten we axioma verbindingen maken die elke vertex langs gaat
        if(root.isLeaf == True):
            #if the current vertex is also a leaf, then we need to create an axiom with another vertex
            self.find_vertex(root)
        else:
            #if the current vertex is not a leaf and it has children, go to that child
            self.find_leaf(root.left)
            self.find_leaf(root.right)

    def find_vertex(self, root):
        '''vind een knoop waarmee de input vertex een axioma verbinding mee kan vormen
        First look in the tree in which the current node appears as well. If an axiom connection cannot be made, continue to the closest neighbour trees.'''
        #kijk eerst naar het andere kind van de parent
        #als de huidige knoop het rechterkind is, kijk naar links. Anders kijk naar rechts
        if(root.parent.left != root):
            if(root.parent.left.isLeaf == True):
                if(root.data == root.parent.left.data and root.polarity != root.parent.left.polarity):
                    print("hier kan een mogelijke axioma verbinding ontstaan")
                    createAxioma(root, root.parent.left)
                else:
                    root.visited = True
                    mostRightLeaf = self.find_mostRightLeaf(root, root.parent.left)
                    self.toFalse(root)
                    if(mostRightLeaf != None):
                        createAxioma(root, mostRightLeaf)
            else:
                #hier ga je kijken naar de linkerbuur, en is de root dus de rechterbuur van de parent. 
                # Dus de leaves die het dichtst bij de huidige root zitten, zitten rechts van de linkerbuur van de parent.
                #Dus kijk eerst naar rechts van root.parent.left
                root.visited = True
                mostRightLeaf = self.find_mostRightLeaf(root, root.parent.left)
                #hier moet je alle visits weer op false zetten
                if(mostRightLeaf != None):
                    createAxioma(root, mostRightLeaf)
                print("hier moet ik de hele linkerboom langs gaan om te kijken naar alle leaves --> recursief zodat je telkens dezelfde methode kan gebruiken bij een complex type?")
                #kijk telkens per leaf of hij verbonden kan worden met de root
        else: #if root.parent.right != root
            if(root.parent.right.isLeaf == True):
                if(root.data == root.parent.right.data and root.polarity != root.parent.right.polarity):
                    print("hier kan weer een mogelijke axioma verbinding ontstaan")
                    createAxioma(root, root.parent.right)
                else:
                    root.visited = True
                    print("uitvoeren most left")
                    mostLeftLeaf = self.find_mostLeftLeaf(root, root.parent.right)
                    self.toFalse(root)
                    if(mostLeftLeaf != None):
                        createAxioma(root, mostLeftLeaf)
            else:
                root.visited = True
                print("uitvoeren most left")
                mostLeftLeaf = self.find_mostLeftLeaf(root, root.parent.right)
                self.toFalse(root)
                if(mostLeftLeaf != None):
                        createAxioma(root, mostLeftLeaf)
                print("hier moet je de hele rechterboom langs gaan voor een mogelijke verbinding.")
        #hierna kijk via linkedlist naar de andere bomen in het bewijsnet om een connectie te maken.
    
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
                print("connect both vertices")
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
                        return self.find_mostLeftLeaf(vertexOut, vertexIn.parent.parent.left)
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
                else:
                    return self.find_mostRightLeaf(vertexOut, vertexIn.right) 
    
    def find_mostLeftLeaf(self, vertexOut, vertexIn):
        '''If the vertex we want to connect is closest to the left side of the neighbour tree.'''
        #root of the tree in which we want to search now it vertexIn.
        if(vertexIn.visited == True):
            #probleem want vertexIn.parent kan ook None zijn 
            if(vertexIn.parent != None):
                print(vertexIn.parent.data , "parent")
                return self.find_mostLeftLeaf(vertexOut, vertexIn.parent) 
            else:
                #if the parents of the current vertex are visited already, we assume that we have visited all vertices
                return None
        elif(vertexIn.isLeaf == True):
            if(vertexIn.data == vertexOut.data and vertexIn.polarity != vertexOut.polarity):
                print("connect both vertices")
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
                print(vertexIn.left.data , "vertex left")
                if(vertexIn.left.visited == True):
                    return self.find_mostLeftLeaf(vertexOut, vertexIn.right)
                elif(vertexIn.right.visited == True):
                    return self.find_mostLeftLeaf(vertexOut, vertexIn.left) 
                else:
                    return None

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
                    if(root.parent != None):
                        self.toFalse(root.parent)
            elif(root.parent.right.visited == True):
                #leaves will always get a visited value of false, if we have passed them
                root.visited = False
                self.toFalse(root.parent.right)
            elif(root.parent.left.visited == True):
                root.visited = False
                self.toFalse(root.parent.left)
            else:
                root.visited = False
                self.toFalse(root.parent)
        else:
            if(root.parent != None):
                self.toFalse(root.parent)

        
    
    def createAxioma(self, root, vertex):
        #kijk voor alle leaves of ze al een verbinding hebben en maak anders een verbinding
        '''het creeren van axioma verbinding tussen vertex en andere knoop.
        ALTIJD VERBINDING MAKEN VAN MET EEN TYPE VAN EEN ANDER WOORD. 
        Begin bij S(output), ga naar een S(input). Als deze S een left tag heeft, kijk naar het woord dat een right tag heeft en vind hierbij een type.
        Als het woord een right tag heeft, ga naar de left tag en vind hierbij een type.
        Doe opnieuw, totdat elke paren van typen verbonden zijn.
        Als er typen over blijven die nog geen verbinding hebben, sla deze op.'''
        print("een axioma verbinding is gemaakt")
    
    def checkForCycle(self, root):
        '''Check if there are any cycles that do not go through an i-link by adding the new axiom'''
    
    def removeAxioma(self, type1, type2):
        '''verwijderen axioma tussen type1 en type2'''

class BuildStartTree:
    '''build the prooftree of the input sentence, first build tree per word in linked list'''
    def __init__(self, linkedList):
        self.linkedList = linkedList
        
    def readRoot(self):
        '''read what type is in the root, depending on this, call /,\,*'''
        linkedList = self.linkedList
        node = linkedList.root
        while node:
            root = None
            left_vertex = None
            right_vertex = None
            left_pol = None
            right_pol = None
            parent = None
            iLink = None
            tree = Tree()
            root = tree.insertVertex(root, node.data, "root", 1, parent, iLink)
            stringtype = node.data[1]
            type_polarity = node.data[2]
            check the connective of the root and call that connective class
            parser_obj = type_parser.TypeParser()
            #typelist = parser_obj.createList(stringtype)
            #typelist = ['N', '/', [ ['S', '\\', 'N'], '\\', ['N', '\\', 'S']]]
            #typelist = [[ 'N', '\\', ['N', '/', 'N']], '*', 'S' ]
            #root = tree.insertVertex(root, typelist, "root", 1, parent, iLink)
            #type_polarity = 1
            #if there is a connective in the string on which we need to split
            self.build(root, tree, typelist, type_polarity)
            #tree.traverseInorder(root)

            #op dit punt heb je (als je net begonnen bent) 1 boom gemaakt. Nu wil je dus alvast kijken naar welke mogelijke axioma verbindingen er zijn.
            axioma_object = Axioma(root, tree)
            leaf = axioma_object.find_leaf(root)
            node = node.next
            #doe dit alleen als de huidige root anders is dan vorige root
            #axioma_object = Axioma(axiom_root, axiom_root.polarity)

    def build(self, root, tree, typelist, type_polarity):
        if(len(typelist) > 1): #as long as we can split and build the tree
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
            if typelist[0] != None and left_pol != None:
                tree.insertVertex(root, typelist[0], "left", left_pol, root, iLink)
            if typelist[2] != None and right_pol != None:
                tree.insertVertex(root, typelist[2], "right", right_pol, root, iLink)
                
            #check if we need to split the types any further
            if(len(typelist[0]) > 1 ):
                self.build(root.left, tree, typelist[0], left_pol)
            else:
                root.left.isLeaf = True

            if(len(typelist[2]) > 1):
                self.build(root.right, tree, typelist[2], right_pol)
            else:
                root.right.isLeaf = True
        else:
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
    '''parsen string input + print output'''
    #---------------------------------------
    read_sentence = read
    linkedlist = read_sentence.lijst
    obj = BuildStartTree(linkedlist)
    read_root = obj.readRoot()

if __name__ == '__main__':
    main()
