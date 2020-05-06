'''tellen aantal axioma's'''
class AxiomaCount:
    '''misschien get tuple weglaten en de tuples per axioma telling uitkiezen'''
    def __init__(self):
        # we willen per tuple kijken wat de count is, dus count moet in init worden gedefinieerd
        self.count = 0 '''is count van een bepaalde tuple met twee woorden om de difficulty van die twee woorden vast te leggen'''
    def get_tuple(self, sentencearray):
        '''ga langs de sentence array en pak alle twee woorden die naast elkaar staan eruit als tuple. Return deze.
        Pak ook alle andere mogelijke sets van woorden.'''
        
    def between_tuples(self, tuple):
        '''tel alle axioma verbindingen die tussen deze twee woorden lopen. Opgeslagen in createAxioma van proofnet.py. Tel deze op bij count'''
        self.count = self.count + 1
    def between_neighbors(self, tuple):
        '''Met de tuples die niet naast elkaar staan, maar om de oorspronkelijke tuple heen, tel deze op bij count'''
    def between_tupleFirst_neighbor(self, tuple, sentencearray):
        '''pak het eerste element van de tuple, maak tuple met alles rechts van tweede element tuple en tel hiertussen de axioma verbindingen. Tel op bij count'''
    def between_typleSecond_neigbor(self, tuple, sentencearray):
        '''pak het tweede element van de tuple, maak tuple met alles links van het eerste element van de tuple en tel hiertussen de axioma verbindingen. Tel op bij count.'''