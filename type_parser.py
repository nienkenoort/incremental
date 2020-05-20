import string
from pyparsing import Word, Literal, opAssoc, infixNotation

typestring = Word(string.ascii_uppercase)
under = Literal("\\")
over = Literal("/")
tensor = Literal("*")

typeexpr = infixNotation(typestring, [(over, 2, opAssoc.RIGHT), (under, 2, opAssoc.RIGHT), (tensor, 2, opAssoc.RIGHT)],)

inputtype = "(N \\ S) / NP"
typelist = typeexpr.parseString(inputtype).asList()[0]

for element in typelist:
    if element == '/':
        print("roep de over methode aan")
    elif element == '\\':
        print("roep under methode aan")
    elif element == '*':
        print("roep de tensor methode aan")
