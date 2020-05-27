import re
from input_parser import read
import lexicon_parser
import type_parser

class Vertex:
    def __init__(self, data, polarity):
        self.data = data #hier is opgeslagen wat de waarde van de knoop is
        self.left = None
        self.right = None
        self.polarity = polarity #dit is de polariteit van de knoop

class Tree:
    def createVertex(self, data, polarity):
        '''wanneer er een splitsing is door een connectief, moeten deze gesplitste typen ook weer vertices worden. Deze moeten worden opgeslagen.'''
        return Vertex(data, polarity)

    def insertVertex(self, vertex, data, place, polarity):
        if vertex == None:
            #print("noen")
            #if root is still empty, create a node
            return self.createVertex(data, polarity)
        #print("yeet", vertex.data)
        if place == "left":
            vertex.left = self.insertVertex(vertex.left, data, "left", polarity)
        elif place == "right":
            vertex.right = self.insertVertex(vertex.right, data, "right", polarity)
        else: #if it is a root element
            vertex = self.insertVertex(vertex, data, "root", polarity)
        return vertex, polarity
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
    def __init__(self, vertex, polarity):
        '''kijken welke axioma's moeten ontstaan vanuit vertex met polarity'''
        self.vertex = vertex
        self.polarity = polarity

    def find_vertex(self, root):
        '''vind een knoop waarmee de input vertex een axioma verbinding mee kan vormen'''
        #ga hele boom na en kijk welke knoop geen linker en rechter buur heeft. 
        if root != None:
            if root.left != None and root.right != None:
                #als left en right niet None zijn, dan wil je naar de kinderen kijken
                self.find_vertex(root.left)
                self.find_vertex(root.right)
            else:
                #als de huidige root geen kinderen heeft, dan kan hij gebruikt worden voor het maken van een axiomaverbinding
                if self.polarity != root.polarity and root.data == vertex.data:
                    #als polarity anders is en type is hetzelfde, dan kan je een verbinding maken
                    createAxioma(root)

        return root
        #kijk voor deze knoop wat zijn polarity is (vertex.polarity)
        #kijk voor deze knoop wat de inhoud van de knoop is (vertex.data)
    
    def createAxioma(self, root):
        '''het creeren van axioma verbinding tussen vertex en andere knoop.
        ALTIJD VERBINDING MAKEN VAN MET EEN TYPE VAN EEN ANDER WOORD. 
        Begin bij S(output), ga naar een S(input). Als deze S een left tag heeft, kijk naar het woord dat een right tag heeft en vind hierbij een type.
        Als het woord een right tag heeft, ga naar de left tag en vind hierbij een type.
        Doe opnieuw, totdat elke paren van typen verbonden zijn.
        Als er typen over blijven die nog geen verbinding hebben, sla deze op.'''
    
    def removeAxioma(self, type1, type2):
        '''verwijderen axioma tussen type1 en type2'''

class BuildStartTree:
    '''build the prooftree of the input sentence, first build tree per word in linked list'''
    def __init__(self, linkedList):
        self.linkedList = linkedList

    def find_leaf(self, root):
            #als er geen node meer is die onleed kan worden, dan moeten we axioma verbindingen maken die elke vertex langs gaat
            while root.left != None and root.right != None:
                #zolang root kinderen heeft, ga naar kind
                print(root.left.data)
                self.find_leaf(root.left)
                self.find_leaf(root.right)
            #print(root.data)
            return root
        
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
            tree = Tree()
            root = tree.insertVertex(root, node.data, "root", 1)
            stringtype = node.data[1]
            type_polarity = node.data[2]
            #check the connective of the root and call that connective class
            parser_obj = type_parser.TypeParser()
            typelist = parser_obj.createList(stringtype)
            #typelist = [ 'N', '\\', ['N', '/', 'N']]
            #root = tree.insertVertex(root, typelist, "root", 1)
            #type_polarity = 1
            #if there is a connective in the string on which we need to split
            self.build(root, tree, typelist, type_polarity)
            #print("pauze")
            tree.traverseInorder(root)
            node = node.next
            #doe dit alleen als de huidige root anders is dan vorige root
            #axiom_root = self.find_leaf(root)
            #axioma_object = Axioma(axiom_root, axiom_root.polarity)

    def build(self, root, tree, typelist, type_polarity):
        if(len(typelist) > 1): #as long as we can split and build the tree
            if(typelist[1] == "/"):
                over_obj = Over(type_polarity)
                #example typelist of N\N is [N,\,N]
                pol = over_obj.get_polarity()
                left_pol = pol[0]
                right_pol = pol[1]
            elif(typelist[1] == "\\"):
                under_obj = Under(type_polarity)
                pol = under_obj.get_polarity()
                left_pol = pol[0]
                right_pol = pol[1]
            elif (typelist[1] == "*"):
                product_obj = Product(type_polarity)
                pol = product_obj.get_polarity()
                left_pol = pol[0]
                right_pol = pol[1]

            #add values of seperated root to tree, including their polarity
            if typelist[0] != None and left_pol != None:
                tree.insertVertex(root, typelist[0], "left", left_pol)
            if typelist[2] != None and right_pol != None:
                tree.insertVertex(root, typelist[2], "right", right_pol)
                
            #check if we need to split the types any further
            if(len(typelist[0]) > 1 ):
                self.build(root.left, tree, typelist[0], left_pol)
            if(len(typelist[2]) > 1):
                self.build(root.right, tree, typelist[2], right_pol)

class Over:
    def __init__(self, polarity):
        '''je wil weten of de root een output polarity heeft of een input polarity. Bij een ingevulde zin hebben de woorden een input polarity, maar de S heeft een output polarity.'''
        self.polarity = polarity

    def get_polarity(self):
        '''de polariteit van de linker moet input zijn (gevuld rondje), de polariteit van de rechter moet output zijn (leeg rondje). BIJ EEN INPUT POLARITY ROOT.'''
        if self.polarity == 1:
            left_pol = 1
            right_pol = 0
        else:
            left_pol = 0
            right_pol = 1  
        return left_pol, right_pol

class Under:
    def __init__(self, polarity):
        self.polarity = polarity

    def get_polarity(self):
        '''de polariteit van de linker moet output zijn (leeg rondje), de polariteit van de rechter moet input zijn (gevuld rondje). BIJ EEN INPUT POLARITY ROOT.'''
        if self.polarity == 1:
            left_polarity = 0
            right_polarity = 1
        else:
            left_polarity = 1
            right_polarity = 0
        return left_polarity, right_polarity

class Product:
    def __init__(self, polarity):
        self.polarity = polarity

    def get_polarity(self):
        '''de polariteit van beide dat ze input moeten zijn (gevuld rondje). BIJ EEN INPUT POLARITY ROOT.'''
        if self.polarity == 1:
            left_polarity = 1
            right_polarity = 1
        else:
            left_polarity = 0
            right_polarity = 0
        return left_polarity, right_polarity


def main():
    '''parsen string input + print output'''
    '''
    root = None
    tree = Tree()
    root = tree.insertVertex(root, "henlo", "left") #insert a root of 10. In my case insert a word 
    tree.insertVertex(root, "amigo", "right")
    tree.insertVertex(root, "linkseamigo", "left")
    tree.traverseInorder(root)
    print("pauze")
    tree.removeVertex(root, "amigo") #de node is nu wel verwijderd, maar is nog steeds de rechter node van de root
    tree.traverseInorder(root)'''
    #---------------------------------------
    read_sentence = read
    linkedlist = read_sentence.lijst
    obj = BuildStartTree(linkedlist)
    read_root = obj.readRoot()
    #-------------------------------------
    vertex_obj = Vertex("hoi", 1)
    ax_obj = Axioma(vertex_obj, vertex_obj.polarity)
    create = ax_obj.find_vertex(vertex_obj)

if __name__ == '__main__':
    main()
