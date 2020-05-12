import re
from input_parser import read
import lexicon_parser

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
            #if root is still empty, create a node
            return self.createVertex(data, polarity)

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
    def __init__(self, type1, type2):
        '''kijken welke axioma's moeten ontstaan tussen type1 en type2'''
    
    def createAxioma(self, type1, type2):
        '''het creeren van axioma verbinding tussen type1 en type2.
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
            #check the connective of the root and call that connective class
            # nu pakt hij een type zoals (N/N)\N niet goed, want hij kijkt eerst naar / terwijl hij naar \ moet kijken
            for index in range(0, len(node.data[1])):
                '''if "(" in node.data[1]:
                    part_of_element = node.data[1][1:4]
                    print(part_of_element)'''
                '''
                split = re.split(r'[()]', node.data[1], 1) #nu blijft de laatste ) staan
                print(split)'''
                #if split != node.data[1]
                if node.data[1][index] == "/":
                    over_obj = Over(node.data[1], node.data[2])
                    parsen = over_obj.parse_root()
                    left_vertex = parsen[0]
                    right_vertex = parsen[1]
                    pol = over_obj.get_polarity()
                    left_pol = pol[0]
                    right_pol = pol[1]
                elif node.data[1][index] == "\\":
                    under_obj = Under(node.data[1], node.data[2])
                    parsen = under_obj.parse_root()
                    left_vertex = parsen[0]
                    right_vertex = parsen[1]
                    pol = under_obj.get_polarity()
                    left_pol = pol[0]
                    right_pol = pol[1]
                elif node.data[1][index] == "*":
                    product_obj = Product(node.data[1], node.data[2])
                    parsen = product_obj.parse_root()
                    left_vertex = parsen[0]
                    right_vertex = parsen[1]
                    pol = product_obj.get_polarity()
                    left_pol = pol[0]
                    right_pol = pol[1]
                #else:
                    #in dit geval is er geen splitsing meer mogelijk, de boom bestaat uit alleen de root
                    #return node
            #add values of seperated root to tree, including their polarity
            if left_vertex != None and left_pol != None:
                tree.insertVertex(root, (left_vertex, left_pol), "left", left_pol)
            if right_vertex != None and right_pol != None:
                tree.insertVertex(root, (right_vertex, right_pol), "right", right_pol)
            #print("pauze")
            #tree.traverseInorder(root)
            node = node.next


class Over:
    def __init__(self, root, polarity):
        '''je wil weten of de root een output polarity heeft of een input polarity. Bij een ingevulde zin hebben de woorden een input polarity, maar de S heeft een output polarity.'''
        self.root = root
        self.polarity = polarity

    def parse_root(self):
        '''je weet al dat je een Over connectief gebruikt, dus hieruit moet volgen wat left en right is. Hierbij createEdge aanroepen om de kanten tussen typen te geven.'''
        #root_tree = Vertex(self.root, self.polarity)
        split = self.root.split("/")
        left = split[0]
        right = split[1]
        return left, right

    def get_polarity(self):
        '''de polariteit van de linker moet input zijn (gevuld rondje), de polariteit van de rechter moet output zijn (leeg rondje). BIJ EEN INPUT POLARITY ROOT.'''
        if self.polarity == 1:
            left_polarity = 1
            right_polarity = 0
        else:
            left_polarity = 0
            right_polarity = 1  
        return left_polarity, right_polarity

class Under:
    def __init__(self, root, polarity):
        self.root = root
        self.polarity = polarity

    def parse_root(self):
        '''je weet al dat je een Under connectief gebruikt, dus hieruit moet volgen wat left en right is. Hierbij createEdge aanroepen om de kanten tussen typen te geven.'''
        split = self.root.split("\\")
        left = split[0]
        right = split[1]
        return left, right

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
    def __init__(self, root, polarity):
        self.root = root
        self.polarity = polarity

    def parse_root(self):
        '''je weet al dat je een Product connectief gebruikt, dus hieruit moet volgen wat left en right is. Hierbij createEdge aanroepen om de kanten tussen typen te geven.'''
        split = self.root.split("*")
        left = split[0]
        right = split[1]
        return left, right
        
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
    read_sentence = read
    linkedlist = read_sentence.lijst
    obj = BuildStartTree(linkedlist)
    read_root = obj.readRoot()

if __name__ == '__main__':
    main()
