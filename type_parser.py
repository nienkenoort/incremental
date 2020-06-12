#Author: Nienke Noort 
#Student number (Utrecht University): 6200451
#Supervisor: Gijs J. Wijnholds

import string
from pyparsing import Word, Literal, opAssoc, infixNotation

class TypeParser:
    """
    A class that takes a string and creates a type of that string. The type will be returned as a list.
    
    ...

    Attributes
    ----------
    typestring : str
        name of the string that will be become the type.
    under : Literal()
        name of the literal that represents the \\ type (imported from the pyparsing package)
    over : Literal()
        name of the literal that represents the / type (imported from the pyparsing package)
    product : Literal()
        name of the literal that represents the * type (imported from the pyparsing package)

    Methods
    -------
    createList(inputtype)
        Creates a list of the inputtype string parameter by using the literals defined as attributes.
    """
    def __init__(self):
        """
        Parameters
        ----------
        None
        """
        self.typestring = Word(string.ascii_uppercase)
        self.under = Literal("\\")
        self.over = Literal("/")
        self.product = Literal("*")
       
    def createList(self, inputtype):
        """
        Gets a string as parameter and creates a list of this string which will be the type.
        
        Parameters
        ----------
        inputtype : str
            The string that will become a list of the type.

        Returns
        -------
        list
            a list of all elements that together form a type.
        """
        typeexpr = infixNotation(self.typestring, [(self.over, 2, opAssoc.RIGHT), (self.under, 2, opAssoc.RIGHT), (self.product, 2, opAssoc.RIGHT)],)
        typelist = typeexpr.parseString(inputtype).asList()[0]
        return typelist

def main():
    obj = TypeParser()
    inputtype = "(N \\ S) / NP"
    typelist = obj.createList(inputtype)

if __name__ == '__main__':
    main()
