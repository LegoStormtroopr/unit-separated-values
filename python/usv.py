import abnf
import sys
import asyncio
import typing
from dataclasses import dataclass

GS  = "\x1D" # Group Separator
RS  = "\x1E" # Record separator
US  = "\x1F" # Unit separator
ETB  = "\x17" # Unit separator
GS_DISPLAY  = "\u241D" # Group Separator Display Character
RS_DISPLAY  = "\u241E" # Record separator Display Character
US_DISPLAY  = "\u241F" # Unit separator Display Character


def usv_format():
    class USVRule(abnf.Rule):
        first_match_alternation = False
        
    USVRule.from_file('./usv.abnf')
    return USVRule("file")


@dataclass
class Group:    
    annotation: str = ""
    records: list[list] = list

    def __str__(self):
        def record_str(record):
            return f"".join([f"{US}"+str(unit) for unit in record])

        output = f"{GS}"
        output += self.annotation
        output += "".join(
            [f"{RS}\n" + record_str(record) for record in self.records]
        )
        output += f"{ETB}"
        return output

    def to_csv(self):
        def record_str(record):
            return f",".join([f'"{unit}"' for unit in record])

        output = "".join(
            [record_str(record)+"\n" for record in self.records]
        )
        return output

    def to_display(self):
        def record_str(record):
            return f"".join([f"{US_DISPLAY}"+str(unit) for unit in record])

        output = self.annotation
        output += f"{RS_DISPLAY}"
        output += "".join(
            [f"{RS_DISPLAY}\n" + record_str(record) for record in self.records]
        )
        return output

    def __eq__(self, other):
        return (
            (self.annotation == other.annotation) &
            (self.records == other.records)
        )

@dataclass
class Annotation:    
    text: str

    def __str__(self):
        return self.text

    def __eq__(self, other):
        return self.text == other.text

class BetterParseError(abnf.parser.ParseError):
    def __init__(self, parser: abnf.parser.Parser, start: int, text: str, *args: typing.Any):
        super().__init__(parser, start, *args)
        self.text = text

    def __str__(self):
        pos = self.start
        lines = self.text.split("\n")
        line = None
        for i, line in enumerate(lines):
            print(pos, len(line))
            if pos < len(line):
                break
            else:
                pos -= len(line)

        txt = f"{self.parser!s}: {self.start}" 
        txt += f"\nError occurred on line {i+1} at position {pos}: "
        txt += f"\n{line}"
        txt += "\n" + " "*pos + "^"
        return txt


class USVReader:
    data: list = [] 

    def parse(self, text):
        try:
            return usv_format().parse_all(text)
        except abnf.parser.ParseError as e:
            raise BetterParseError(e.parser, e.start, text, *e.args)

    def __init__(self, text, strict=False):

        if strict:
            node = self.parse(text)
            self.data = asyncio.run(self.process_node(node))
        else:
            self.data = self.streaming_parse(text)

        self.groups = [
            obj
            for obj in self.data
            if isinstance(obj, Group)
        ]
    
    def streaming_parse(self, text):
        import re
        x = re.match(
            f"^([^{GS}{ETB}]*|{GS}.*{ETB}?)*$",
            text
        )
        for i in text:
            if i == GS:
                print("new group")
            if i == RS:
                print("new record")
            if i == RS:
                print("new unit")
        print(text)
        print(x.groups(31))
        return []

    async def process_node(self, node):
        if node.name == "file":
            return [
                await self.process_node(child)
                for child in node.children
            ]
        elif node.name == "annotation":
            return Annotation(text="".join([
                await self.process_node(child)
                for child in node.children
            ]))
        elif node.name == "group":
            group = {}
            for child in node.children:
                if child.name == "groupannotation":
                    group['annotation'] = await self.process_node(child)
                elif child.name == "groupdata":
                    group['records'] =  [
                        await self.process_node(grandchild)
                        for grandchild in child.children
                    ]
            return Group(**group)
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

    def __str__(self):
        return "".join([str(obj) for obj in self.data])

    def insert(self, pos, obj):
        # Insert an appropriate child object at position pos
        assert isinstance(obj, (Group, Annotation))
        self.data.insert(pos, obj)

    def normalised_data(self):
        # Useful for testing as concurrent annotations on parsing will be seen as one.
        
        children = []
        last_child = None
        for child in self.data:
            if last_child and  isinstance(last_child, Annotation) and isinstance(child, Annotation):
                last_child.text += child.text
            else:
                children.append(child)
            last_child = child
        return children

    def __eq__(self, other):
        return all(
            us == them
            for us, them in zip(self.normalised_data(), other.normalised_data())
        )

    @classmethod
    def from_file(cls, filename):
        with open(filename) as f:
            src = f.read()
        return cls(src)