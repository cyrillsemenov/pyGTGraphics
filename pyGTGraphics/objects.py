"""
Description: This module defines layout building blocks
Author: Cyrill Semenov
Date Created: 2023/11/08
Date Modified: 2023/11/09
Version: 1.0
License: MIT License
"""
import xml.etree.ElementTree as ET
from typing import Optional, Union

from .properties import TextProperties, Colour
from .storyboard import Storyboard


class Root:
    """
    Represents the root element of a composition which includes layers and storyboards.

    Attributes:
        width (int): The width of the composition.
        height (int): The height of the composition.
        layers (dict): A dictionary to store layers by their names.
        storyboards (list): A list to store storyboard elements.
    """

    def __init__(self, width: int, height: int) -> None:
        """
        Initialize a Root object with a given width and height.

        Args:
            width (int): The width of the composition.
            height (int): The height of the composition.
        """
        self.width: int = width
        self.height: int = height
        self.layers: dict[str, Layer] = dict()
        self.storyboards: list[Storyboard] = []

    def create_layer(self, name: str, x: Optional[int] = None, y: Optional[int] = None,
                     width: Optional[int] = None, height: Optional[int] = None) -> 'Layer':
        """
        Create a new layer and add it to the composition with specified dimensions and position.

        If width or height are not provided, the new layer will extend from the specified x or y coordinate
        to the edge of the composition's width or height.

        Args:
            name (str): The name of the layer.
            x (Optional[int]): The x-coordinate of the layer's top-left corner. Defaults to 0 if not provided.
            y (Optional[int]): The y-coordinate of the layer's top-left corner. Defaults to 0 if not provided.
            width (Optional[int]): The width of the layer. Defaults to the remaining width of the composition
                                   from the x-coordinate if not provided.
            height (Optional[int]): The height of the layer. Defaults to the remaining height of the composition
                                    from the y-coordinate if not provided.

        Returns:
            Layer: The created layer object with the specified name, position, and dimensions.
        """
        _x, _y = x or 0, y or 0
        _w, _h = width or (self.width - _x), height or (self.height - _y)
        new_layer = Layer(name, _x, _y, _w, _h)
        self.layers[name] = new_layer
        return new_layer

    def to_xml(self) -> ET.ElementTree:
        """
        Convert the Root object into an XML structure.

        Returns:
            ElementTree: The ElementTree object representing the entire composition.
        """
        comp_element: ET.Element = ET.Element('Composition', Width=str(self.width), Height=str(self.height))
        for element in self.layers.values():
            element.to_xml(comp_element)
        for storyboard in self.storyboards:
            storyboard.to_xml(comp_element)

        return ET.ElementTree(comp_element)


class BaseGTObject:
    def __init__(self, name: str, x: int, y: int, width: int, height: int):
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.fill = Colour.from_hex("#00000000")
        self.stroke = Colour.from_hex("#00000000")

    def set_fill(self, colour: Union[str, Colour]):
        self.fill = colour

    def set_stroke(self, colour: Union[str, Colour]):
        self.stroke = colour

    def to_xml(self, parent):
        raise NotImplementedError(f"Function `to_xml()` should be implemented for {self.__class__.__name__} class!")


class Layer(BaseGTObject):
    def __init__(self, name: str, x: int, y: int, width: int, height: int):
        super().__init__(name, x, y, width, height)
        self.locked = False
        self.children = []

    def to_xml(self, parent):
        element = ET.SubElement(
            parent, 'Layer',
            Name=self.name,
            Dimensions=f"%i,%i,%i" % (self.width, self.height, 0),
            Locked=str(self.locked)
        )
        composition = ET.SubElement(element, 'Layer.Composition')
        inner_composition = ET.SubElement(composition, 'Composition', Width=str(self.width),
                                          Height=str(self.height))
        for el in self.children:
            el.to_xml(inner_composition)


class TextBlock(BaseGTObject):
    def __init__(self, name: str, x: int, y: int, width: int, height: int, text: str, properties: TextProperties):
        super().__init__(name, x, y, width, height)
        self.text = text
        self.properties = properties

    def to_xml(self, parent):
        element = ET.SubElement(parent, 'TextBlock', **self.properties.dict(text_block=self))

        fill = ET.SubElement(element, 'TextBlock.Fill')
        ET.SubElement(fill, "Brush", Color=str(self.fill))
        stroke = ET.SubElement(element, 'TextBlock.Stroke')
        ET.SubElement(stroke, "Brush", Color=str(self.stroke))


class Rectangle(BaseGTObject):
    _tag = 'Rectangle'
    _bound = None
    _padding = "%i,%i,%i,%i"

    def set_bounding(self, obj, padding=None):
        self._bound = obj.name
        if isinstance(padding, int):
            padding = (padding,)
        pad_dimensions = len(padding) if padding else 0
        if pad_dimensions == 1:
            self._padding %= (padding[0], padding[0], padding[0], padding[0])
        elif pad_dimensions < 4:
            self._padding %= (padding[0], padding[1], padding[0], padding[1])
        elif pad_dimensions == 4:
            self._padding %= padding
        else:
            self._padding %= (0, 0, 0, 0)

    def to_xml(self, parent):
        element = ET.SubElement(parent, self._tag,
                                Name=self.name,
                                Dimensions=f"%i,%i,%i" % (self.width, self.height, 0),
                                Location="%i,%i,%i" % (self.x, self.y, 0))
        if self._bound:
            bounding = ET.SubElement(element, 'Rectangle.Bounding')
            ET.SubElement(bounding, "Bounding", Object=self._bound, Padding=self._padding)
        fill = ET.SubElement(element, 'Rectangle.Fill')
        ET.SubElement(fill, "Brush", Color=str(self.fill))
        stroke = ET.SubElement(element, 'Rectangle.Stroke')
        ET.SubElement(stroke, "Brush", Color=str(self.stroke))


class Ellipse(Rectangle):
    _tag = 'Ellipse'


class Triangle(Rectangle):
    _tag = 'Triangle'


class Image(BaseGTObject):
    def __init__(self, name: str, x: int, y: int, width: int, height: int):
        super().__init__(name, x, y, width, height)
        raise NotImplementedError("Image in not implemented yet!")

    def to_xml(self, parent):
        pass


class Text3D(BaseGTObject):
    def __init__(self, name: str, x: int, y: int, width: int, height: int):
        super().__init__(name, x, y, width, height)
        raise NotImplementedError("Text3D in not implemented yet!")

    def to_xml(self, parent):
        pass


class Ticker(BaseGTObject):
    def __init__(self, name: str, x: int, y: int, width: int, height: int):
        super().__init__(name, x, y, width, height)
        raise NotImplementedError("Ticker in not implemented yet!")

    def to_xml(self, parent):
        pass

