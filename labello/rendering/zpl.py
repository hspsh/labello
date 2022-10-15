from PIL import Image, ImageDraw, ImageFont
from dataclasses import dataclass, field
from typing import List
import requests


@dataclass
class Item:
    type: str
    x: int
    y: int
    data: "typing.Any"


@dataclass
class LabelEPL:
    width: int
    height: int
    items: List[Item] = field(default_factory=list)


class Renderer:
    def render(self, raw, color=(0xFF, 0xFF, 0xFF)):
        url = 'http://api.labelary.com/v1/printers/8dpmm/labels/2.20x1.65/0/'
        files = {'file' : raw}        
        response = requests.post(url, files = files, stream = True)

        if response.status_code == 200:
            response.raw.decode_content = True
            return response.raw
        else:
            return None


from dataclasses import dataclass, field
import logging
import shlex
from typing import List

logger = logging.getLogger(__name__)


@dataclass
class Line:
    """
    Line is an EPL command line, consisting of a command and rest of line data.

    This is a thin wrapper around EPL's text-based script. For example, the
    following EPL data:

        LO25,600,750,20

    Would get parsed as command 'L' and rest '25,600,750,20'.
    """

    command: str
    rest: str

    @classmethod
    def parse(cls, data: str):
        command, rest = data[0], data[1:]
        return Line(command, rest)

    def parts(self, n: int) -> List[str]:
        """Returns the rest of the line split by comma into n parts."""
        res = self.rest.split(",", maxsplit=n - 1)
        # If any part is double-quote-delimited, unquote it.
        # TODO: is this expected behaviour?
        for i, r in enumerate(res):
            if not r.startswith('"') or not r.endswith('"'):
                continue
            unquoted = shlex.split(r)
            if len(unquoted) != 1:
                raise Exception(f"Failed to unquote part {res}")
            res[i] = unquoted[0]
        return res


@dataclass
class Item:
    type: str
    x: int
    y: int
    data: "typing.Any"


@dataclass
class LabelEPL:
    """LabelEPL is a parsed EPL label, created by a 'N' command."""

    width: int = 0
    height: int = 100
    items: List[Item] = field(default_factory=list)

    def _command_set_width(self, line: Line):
        (width,) = line.parts(1)
        self.width = int(width)

    def _command_append(self, line: Line):
        width, height, _, _, _, _, _, text = line.parts(8)
        width, height = int(width), int(height)
        self.items.append(Item("text", width, height, text))

        if height + 30 > self.height:
            self.height = height + 30

    def feed(self, line: Line):
        """Executes a Line against this LabelEPL (mutating it)."""
        if line.command == "P":
            return True

        handler = {"q": self._command_set_width, "A": self._command_append,}.get(
            line.command
        )
        if handler is None:
            logger.warning(f"Unhandled line in label: {line}")
        else:
            handler(line)
        return False


def parse(raw) -> List[LabelEPL]:
    """
    Takes an EPL script (newline-delimited EPL commands) and parses it as a
    list of EPL Labels.
    """
    res = []
    current = None
    types = {
        "N": LabelEPL,
    }
    for line in raw.split("\n"):
        line = line.strip()
        if not line:
            continue
        line = Line.parse(line)

        if current is None:
            type_ = types.get(line.command)
            if type_ is None:
                raise Exception(f"Unknown type {command}")
            current = type_()
        else:
            if current.feed(line):
                res.append(current)
                current = None
    return res


import unittest


class TestParse(unittest.TestCase):
    def test_example(self):
        example = """
N
q812
S2
A50,0,0,1,1,1,N,"Example 1 0123456789"
A50,50,0,2,1,1,N,"Example 2 0123456789"
A50,100,0,3,1,1,N,"Example 3 0123456789"
A50,150,0,4,1,1,N,"Example 4 0123456789"
A50,200,0,5,1,1,N,"EXAMPLE 5 0123456789"
A50,300,0,3,2,2,R,"Example 6 0123456789"
LO25,600,750,20
B50,800,0,3,3,7,200,B,"998152-001"
P1
"""
        res = parse(example)
        self.assertEqual(
            res,
            [
                LabelEPL(
                    width=812,
                    height=330,
                    items=[
                        Item(type="text", x=50, y=0, data="Example 1 0123456789"),
                        Item(type="text", x=50, y=50, data="Example 2 0123456789"),
                        Item(type="text", x=50, y=100, data="Example 3 0123456789"),
                        Item(type="text", x=50, y=150, data="Example 4 0123456789"),
                        Item(type="text", x=50, y=200, data="EXAMPLE 5 0123456789"),
                        Item(type="text", x=50, y=300, data="Example 6 0123456789"),
                    ],
                )
            ],
        )


if __name__ == "__main__":
    unittest.main()
