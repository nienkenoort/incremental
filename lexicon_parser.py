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
        #wanneer ik de lexicon ga importeren kan ik hier wel een loop van maken die de elementen automatisch toevoegt zonder dat ik alles los moet doen
        lexicon["de"] = "NP/N"
        lexicon["rode"] = "N/N"
        lexicon["hoed"] = "N"
        lexicon["en"] = "(N\\N)/N"
        lexicon["laars"] = "N"
        return self.lexicon

def main():
    obj = Lexicon()
    obj.createLexicon()

if __name__ == '__main__':
    main()
        
    
