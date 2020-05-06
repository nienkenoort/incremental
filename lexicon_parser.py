'''eerst een soort test lexicon opbouwen, dit moet een set zijn'''
class Lexicon:
    def __init__(self):
        self.lexicon = dict()
       
    def createLexicon(self):
        lexicon = self.lexicon
        #wanneer ik de lexicon ga importeren kan ik hier wel een loop van maken die de elementen automatisch toevoegt zonder dat ik alles los moet doen
        lexicon["de"] = "N"
        lexicon["rode"] = "N/N"
        lexicon["hoed"] = "N"
        lexicon["en"] = "N\(N/N)"
        lexicon["laars"] = "N"
        return self.lexicon

def main():
    obj = Lexicon()
    obj.createLexicon()
    for key, value in obj.lexicon.items():
        print(key, value)
if __name__ == '__main__':
    main()
        
    