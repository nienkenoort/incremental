import string
from pyparsing import Word, Literal, opAssoc, infixNotation

class TypeParser:
       def __init__(self):
              self.typestring = Word(string.ascii_uppercase)
              self.under = Literal("\\")
              self.over = Literal("/")
              self.tensor = Literal("*")
       
       def createList(self, inputtype):
              typeexpr = infixNotation(self.typestring, [(self.over, 2, opAssoc.RIGHT), (self.under, 2, opAssoc.RIGHT), (self.tensor, 2, opAssoc.RIGHT)],)
              typelist = typeexpr.parseString(inputtype).asList()[0]
              return typelist

def main():
    obj = TypeParser()
    inputtype = "(N \\ S) / NP"
    typelist = obj.createList(inputtype)
    #print(typelist)

if __name__ == '__main__':
    main()
