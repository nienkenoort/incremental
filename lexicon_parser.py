#Author: Nienke Noort 
#Student number (Utrecht University): 6200451
#Supervisor: Gijs J. Wijnholds

class Lexicon:
    """
    A class that forms a dictionary of all of the words with their corresponding types that are necessary for building a proofnet of any random sentence.
    
    ...

    Attributes
    ----------
    lexicon : dict()
        name of the dictionary in which the words and their types are saved.

    Methods
    -------
    createLexicon()
        Adds a type to each word that is in the dictionary.
    """
    def __init__(self):
        """
        Parameters
        ----------
        None
        """
        self.lexicon = dict()
       
    def createLexicon(self):
        """
        Gets an empty dictionary and adds words with their corresponding type to the dictionary.

        Returns
        -------
        dictionary
            a dictionary of all words with their types of which we can choose when creating a proofnet.
        """
        lexicon = self.lexicon
        lexicon["de"] = "NP/N"
        lexicon["rode"] = "N/N"
        lexicon["hoed"] = "N"
        lexicon["en"] = "(N\\N)/N"
        lexicon["laars"] = "N"

        lexicon["the"] = "N/CN"
        lexicon["horse"] = "CN"
        lexicon["raced"] = "N\S"
        lexicon["past"] = "((N\\S)\\(N\\S))/N"
        lexicon["barn"] = "CN"

        lexicon["someone"] = "S/(N\\S)"
        lexicon["loves"] = "(N\\S)/N"
        lexicon["everyone"] = "(S/N)\S"

        lexicon["kid"] = "N"
        lexicon["who"] = "((N\\N)/(S/NP))"
        lexicon["Kelly"] = "NP"
        lexicon["Terry"] = "NP"
        lexicon["Robin"] = "NP"
        lexicon["likes"] = "((NP\\S)/NP)"
        lexicon["believes"] = "((NP\\S)/S)"
        lexicon["knows"] = "((NP\\S)/S)"

        lexicon["iemand"] = "S/(NP\\S)"
        lexicon["verdween"] = "NP\\S"
        lexicon["gisteren"] = "(NP\\S)\\(NP\\S)"

        lexicon["mensen"] = "N"
        lexicon["die"] = "(N\\N)/(NP\\S)"
        lexicon["dieren"] = "NP"
        lexicon["eten"] = "NP\\(NP\\S)"

        lexicon["Alice"] = "NP"
        #lexicon["en"] = "(NP\\NP)/NP"
        lexicon["Bob"] = "NP"
        lexicon["vinden"] = "(NP\\S)/NP"
        lexicon["oplossing"] = "N"

        return self.lexicon

def main():
    obj = Lexicon()
    obj.createLexicon()

if __name__ == '__main__':
    main()
        
    
