import abnf
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


sdata = """# Fisher's Iris data set


Dataset orderSepal lengthSepal widthPetal lengthPetal widthSpecies
15.13.51.40.2I. setosa
24.93.01.40.2I. setosa
1505.93.05.11.8I. virginica

"""

def usv_format():
    from abnf.grammars.misc import load_grammar_rulelist

    @load_grammar_rulelist()
    class USV(abnf.Rule):
        grammar="""
; This is the authoritative source for the USV specification.

file = *(textsection / group)
textsection = *TEXTDATA

group = GS [ groupannotation ] groupdata [ groupterminators ]
groupannotation = *TEXTDATA
groupdata = 1*(*CRLF RS *CRLF record)
groupterminators = ETB

record = 1*(US unit)
unit = *(TEXTDATA)

eGS = DLE GS ; Escaped Group Separator
eRS = DLE RS ; Escaped Record Separator
eUS = DLE US ; Escaped Unit Separator

TEXTDATA =  %x0A-0B / %x20-21 / %x23-2B / %x2D-7E

SOH = %x01 ; Start of Header
DLE = %x10 ; Data Link Escape
ETB = %x17 ; End of Transmission
GS  = %x1D ; Group Separator
RS  = %x1E ; Record separator
US  = %x1F ; Unit separator

CR = %x0D ;as per section 6.1 of RFC 2234
LF = %x0A ;as per section 6.1 of RFC 2234
CRLF = CR / LF / (CR RF) ;as per section 6.1 of RFC 2234
"""

    return USV("file")

parser = usv_format()
from pprint import pprint
node = parser.parse_all(sdata)
pprint(node)
import pdb; pdb.set_trace()