from PIL import Image, ImageDraw, ImageFont
from dataclasses import dataclass, field
from typing import List


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
        data = self.parse(raw)
        img = Image.new("RGB", (data.width, data.height), color=color)
        draw = ImageDraw.Draw(img)

        for i in data.items:
            if i.type == "text":
                draw.text((i.x, i.y), i.data, fill=(0, 0, 0))
            if i.type == "line":
                draw.text((i.x, i.y) + (i.x + i.data[0], i.y + i.data[1]))

        return img

    def parse(self, raw):
        state = None
        result = None
        for line in raw.split("\n"):
            if line.startswith("N"):
                state = "N"
                result = LabelEPL(0, 100)
                continue
            if state != None and line.startswith("q"):
                result.width = int(line[1:])
                continue
            if state != None and line.startswith("A"):
                tmp = line[1:].split(",")
                result.items.append(Item("text", int(tmp[0]), int(tmp[1]), tmp[7]))
                if int(tmp[1]) + 30 > result.height:
                    result.height = int(tmp[1]) + 30
                continue
            if state != None and line.startswith("P"):
                return result
