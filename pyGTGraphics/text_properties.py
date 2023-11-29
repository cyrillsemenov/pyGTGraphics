from dataclasses import dataclass
from numbers import Number
from typing import Optional, Any


class TextProperties(dict):
    _aliases = {
        "data_flags": "DataFlags",
        "font_family": "FontFamily",
        "font_size": "FontSize",
        "font_weight": "FontWeight",
        "text_align": "TextAlign",
        "vertical_align": "VerticalAlign",
        "word_wrapping": "WordWrapping",
        "ignore_overhang": "IgnoreOverhang",
        "line_spacing": "LineSpacing",
        "auto_size": "AutoSize",
    }

    def __init__(self,
                 font_family: str,
                 font_size: Number,
                 text_align: str = "left",
                 font_weight: Optional[str] = None,
                 vertical_align: Optional[str] = None,
                 word_wrapping: Optional[str] = None,
                 ignore_overhang: Optional[bool] = None,
                 line_spacing: Optional[int] = None,
                 auto_size: Optional[str] = None,
                 *args, **kwargs
                 ) -> None:
        super().__init__()
        self.font_family = font_family
        self.font_size = font_size
        self.font_weight = font_weight
        self.text_align = text_align
        self.vertical_align = vertical_align
        self.word_wrapping = word_wrapping
        self.ignore_overhang = ignore_overhang
        self.line_spacing = line_spacing
        self.auto_size = auto_size
        self.data_flags = None

    def with_attribute(self, **kwargs):
        attr = self.dict()
        attr.update(kwargs)
        result = TextProperties(**attr)
        return result

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key: str, value: Number) -> None:
        setattr(self, key, value)

    def keys(self):
        return [k for k in self._aliases.keys() if self[k] is not None]

    def items(self):
        return ((key, self[key]) for key in self.keys())

    def dict(self):
        return {key: self[key] for key in self.keys()}

    def to_xml(self):
        return {self._aliases[k]: str(self[k]) for k in self.keys()}

    def __iter__(self):
        return iter(self.keys())

    @dataclass(frozen=True)
    class TextAlignment:
        LEFT: str = "Left"
        CENTER: str = "Center"
        RIGHT: str = "Right"

    @dataclass(frozen=True)
    class VerticalAlignment:
        TOP: str = "Top"
        CENTER: str = "Center"
        BOTTOM: str = "Bottom"

    @dataclass(frozen=True)
    class WordWrapping:
        NOWRAP: str = "NoWrap"
        WRAP: str = "Wrap"

    @dataclass(frozen=True)
    class AutoSize:
        FIXED: str = "Fixed"
        WIDTH: str = "Width"
        HEIGHT: str = "Height"
        WIDTH_AND_HEIGHT: str = "WidthAndHeight"
        SHRINK: str = "Shrink"


if __name__ == "__main__":
    a = TextProperties(font_family="Font", font_size=0)
    print(list(a.items()))
    a.font_family = "Family"
    a.text = "A"
    print(dict(**a))
    print(dict(**a.with_attribute(font_size=29)))
