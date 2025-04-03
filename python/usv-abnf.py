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


This is the data
Dataset orderSepal lengthSepal widthPetal lengthPetal widthSpecies
15.13.51.40.2I. setosa
24.93.01.40.2I. setosa
1505.93.05.11.8I. virginica



"""

def usv_format():
    from abnf.grammars.misc import load_grammar_rulelist

    @load_grammar_rulelist()
    class USV(abnf.Rule):
        first_match_alternation = False
        grammar="""
; This is the authoritative source for the USV specification.

file = *(textsection / group)
textsection = TEXTDATA

group = GS [ groupannotation ] groupdata [ groupterminators ]
groupannotation = TEXTDATA
groupdata =  *CRLF 1*(record)
groupterminators = ETB

record = RS *CRLF 1*(unit)
unit = US TEXTDATA

eGS = DLE GS ; Escaped Group Separator
eRS = DLE RS ; Escaped Record Separator
eUS = DLE US ; Escaped Unit Separator

TEXTDATA =  *(%x0A-0B / %x20-21 / %x23-2B / %x2D-7E)

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
    # class FromFileRule(abnf.Rule):
    #     pass
        
    # USV = FromFileRule.from_file('../usv.abnf')
    # print(USV)
    # import pdb; pdb.set_trace()

    return USV("file")


parser = usv_format()
from pprint import pprint
node = parser.parse_all(sdata)
# pprint(str(node))

# import pdb; pdb.set_trace()
import asyncio


class USVGroup():    
    pass

class USVReader:
    def __init__(self, node):
        self.data = asyncio.run(self.process_node(node))

        self.groups = [
            obj
            for obj in self.data
            if 'data' in obj.keys()
        ]

    async def process_node(self, node):
        if node.name == "file":
            return [
                await self.process_node(child)
                for child in node.children
            ]
        elif node.name == "textsection":
            return {"text": "".join([
                await self.process_node(child)
                for child in node.children
            ])}
        elif node.name == "group":
            group = {}
            for child in node.children:
                if child.name == "groupannotation":
                    group['annotation'] = await self.process_node(child)
                elif child.name == "groupdata":
                    group['data'] =  [
                        await self.process_node(grandchild)
                        for grandchild in child.children
                    ]
            return group
        elif node.name == "record":
            return [
                await self.process_node(child)
                for child in node.children
                if child.name == "unit"
            ]
        elif node.name == "unit":
            for child in node.children:
                if child.name == "TEXTDATA":
                    return await self.process_node(child)
        elif node.name == "groupannotation":
            # Get first text element
            return await self.process_node(node.children[0])
        elif node.name == "TEXTDATA":
            return "".join([
                character.value for character in node.children
            ])
        else:
            return None

thing = USVReader(node)
pprint(thing.data)
pprint(thing.groups)
thing.groups[0].append([1,2,3])
pprint(thing.data)
