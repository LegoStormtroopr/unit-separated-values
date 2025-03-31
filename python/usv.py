from pyparsing import Word, alphas
import sys

data = """
# Fisher's Iris data set

The Iris flower data set or Fisher's Iris data set is a multivariate data set 
used and made famous by the British statistician and biologist Ronald Fisher 
in his 1936 paper The use of multiple measurements in taxonomic problems as an 
example of linear discriminant analysis.

---


Dataset orderSepal lengthSepal widthPetal lengthPetal widthSpecies
15.13.51.40.2I. setosa
24.93.01.40.2I. setosa

1505.93.05.11.8I. virginica
"""


sdata = """
# Fisher's Iris data set


Dataset orderSepal lengthSepal widthPetal lengthPetal widthSpecies
15.13.51.40.2I. setosa
24.93.01.40.2I. setosa

1505.93.05.11.8I. virginica
"""

def usv_format():
    import pyparsing as pp
    from pyparsing import Word, Literal, alphas8bit, OneOrMore, ZeroOrMore, Optional, unicode, Group, Regex

    unicodeEverything = u''.join(chr(c) for c in range(sys.maxunicode))

    # TEXTDATA =  Word(alphas) # %x20-21 / %x23-2B / %x2D-7E

    SOH = Literal("\x01") # Start of Header
    DLE = Literal("\x10") # Data Link Escape
    ETB = Literal("\x17") # End of Transmission
    GS  = Literal("\x1D") # Group Separator
    RS  = Literal("\x1E") # Record separator
    US  = Literal("\x1F") # Unit separator

    reservedchars = (GS, RS, US, ETB, DLE, SOH)

    CR = Literal("\x0D")
    LF = Literal("\x0A")
    CRLF = (CR + LF) # as per section 6.1 of RFC 2234
 
    eGS = (DLE + GS) # Escaped Group Separator
    eRS = (DLE + RS) # Escaped Record Separator
    eUS = (DLE + US) # Escaped Unit Separator

    TEXTDATA =  Word(unicode.printables+" ", exclude_chars=reservedchars)
    # TEXTDATA =  Regex(r"[^\x01\x10\x17\x1d\x1e\x1f]*?")

    unit = (TEXTDATA) # | eGS | eRS | eUS)

    record = Group(OneOrMore((US | unit)))

    groupannotation = TEXTDATA
    groupdata = Group(OneOrMore(RS + record))
    groupterminators = ETB

    group = Group(GS + Optional(groupannotation).set_results_name('preamble') + groupdata.set_results_name('data') + Optional(groupterminators))

    file = Group(ZeroOrMore(
        TEXTDATA.set_results_name('preamble') ^ group.set_results_name('group')
    )).set_results_name('file')

    return file


parser = usv_format()
from pprint import pprint
pprint(parser.parse_string(sdata).as_dict())

greet = Word(alphas) + "," + Word(alphas) + "!"
hello = "Hello, World!"
print(hello, "->", greet.parse_string(hello))
