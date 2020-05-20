import string
from pyparsing import Word, Literal, opAssoc, infixNotation

atom_ = Word(string.ascii_uppercase)
#typedec_ = Word('(' + '_')
under = Literal("\\")
over = Literal("/")
#arrowexp_ = over + typedec_ 

typeexp_ = infixNotation(atom_, [(over, 2, opAssoc.RIGHT), (under, 2, opAssoc.RIGHT), ('(', 2, opAssoc.RIGHT), (')', 2, opAssoc.LEFT)],)

def strToPol(str_):
    return unfoldExp(typeexp_.parseString(str_).asList()[0])

def unfoldExp(expL):
    if isinstance(expL, str):
        return expL
    else:
        return ' '.join([unfoldExp(expL[1]), unfoldExp(expL[0]), unfoldExp(expL[2])])

example = "N \\ (S / NP)"
result = strToPol(example) # dit geeft '\ N / S NP'
print(result)
