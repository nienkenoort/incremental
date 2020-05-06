class Vertex:
    def __init__(self):
        '''wat wil ik in deze class'''

    '''misschien kijken naar wat de inhoud is van de vertices, deze input meegeven aan de connectieven classen'''
    def createVertex(self):
        '''wanneer er een splitsing is door een connectief, moeten deze gesplitste typen ook weer vertices worden. Deze moeten worden opgeslagen.'''

    def removeVertex(self):
        '''stel een verkeerde splitsing, dan moet de oude vertex verwijderd worden.'''

class Edge:
    def __init__(self, type1, type2):
        '''kijken wat de verbindingen zijn tussen twee typen'''

    def createEdge(self, type1, type2):
        '''wanneer er verbindingen gemaakt moeten worden tussen typen'''

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

class Over:
    def __init__(self, root, polarity):
        '''je wil weten of de root een output polarity heeft of een input polarity. Bij een ingevulde zin hebben de woorden een input polarity, maar de S heeft een output polarity.'''

    def parse_root(self, root):
        '''je weet al dat je een Over connectief gebruikt, dus hieruit moet volgen wat left en right is. Hierbij createEdge aanroepen om de kanten tussen typen te geven.'''

    def get_polarity(self, left, right):
        '''de polariteit van de linker moet input zijn (gevuld rondje), de polariteit van de rechter moet output zijn (leeg rondje). BIJ EEN INPUT POLARITY ROOT.'''

class Under:
    def __init__(self, root, polarity):

    def parse_root(self, root):
        '''je weet al dat je een Under connectief gebruikt, dus hieruit moet volgen wat left en right is. Hierbij createEdge aanroepen om de kanten tussen typen te geven.'''

    def get_polarity(self, left, right):
        '''de polariteit van de linker moet output zijn (leeg rondje), de polariteit van de rechter moet input zijn (gevuld rondje). BIJ EEN INPUT POLARITY ROOT.'''

class Product:
    def __init__(self, root):

    def parse_root(self, root):
        '''je weet al dat je een Product connectief gebruikt, dus hieruit moet volgen wat left en right is. Hierbij createEdge aanroepen om de kanten tussen typen te geven.'''

    def get_polarity(self, left, right):
        '''de polariteit van beide dat ze input moeten zijn (gevuld rondje). BIJ EEN INPUT POLARITY ROOT.'''


def main():
    '''parsen string input + print output'''
         
if __name__ == '__main__':
    main()