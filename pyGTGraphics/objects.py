"""
Description: This module defines layout building blocks
Author: Cyrill Semenov
Date Created: 2023/11/08
Date Modified: 2023/11/09
Version: 1.0
License: MIT License
"""
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from inspect import signature, Parameter
from numbers import Number
from typing import Optional, SupportsIndex, Union, Any, List, Type

from pyGTGraphics.properties import TextProperties, Colour
from pyGTGraphics.storyboard import Storyboard

PAD_STR = "%i,%i,%i,%i"


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


class Layer:
    def __init__(self, name: str, x: int, y: int, width: int, height: int):
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.locked = False
        self.children = []

    @classmethod
    def __generate_stub__(cls):

        with open('objects.pyi', "w") as file:
            def write_class_stub(subclass, file):
                # Write the stub for the create_* method
                args = ["self"]
                non_default = []
                default_param = []
                end = ["*args", "**kwargs"]
                for arg in subclass._args:
                    attr = arg.attribute
                    typehint = arg.type.__name__ if arg.type else 'Any'
                    default = f"= {arg.default}" if arg.default is not None else ""
                    if default:
                        default_param.append(f"{attr}: '{typehint}' {default}")
                    else:
                        non_default.append(f"{attr}: '{typehint}'")
                args = ', '.join(args + non_default + default_param + end)
                file.write(
                    f"    def create_{subclass.__name__.lower()}({args}) -> '{subclass.__name__}': ...\n")

                # Recursively write stubs for the subclasses of this subclass
                for subsubclass in subclass.__subclasses__():
                    write_class_stub(subsubclass, file)

            file.write(f"class {cls.__name__}:\n")
            for subclass in BaseGTObject.__subclasses__():
                write_class_stub(subclass, file)
        #
        # with open('objects.pyi', "w") as file:
        #     file.write(f"class {cls.__name__}:\n")
        #     for subclass in BaseGTObject.__subclasses__():
        #         args = ["self"]
        #         non_default = []
        #         default_param = []
        #         end = ["*args", "**kwargs"]
        #         for arg in subclass._args:
        #             attr = arg.attribute
        #             typehint = arg.type.__name__ if arg.type else 'Any'
        #             default = f"= {arg.default}" if arg.default or arg.optional else ""
        #             if default:
        #                 default_param.append(f"{attr}: '{typehint}' {default}")
        #             else:
        #                 non_default.append(f"{attr}: '{typehint}'")
        #         args = ', '.join(args + non_default + default_param + end)
        #         file.write(f"    def create_{subclass.__name__.lower()}({args}) -> '{subclass.__name__}': ...\n")

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

    def insert_children(
            self,
            type_of_object: Type['BaseGTObject'],
            index: SupportsIndex = -1, **kwargs
    ) -> Type['BaseGTObject']:
        self.children.insert(index, type_of_object(**kwargs))
        return self.children[index]

    def create_textblock(
            self,
            name: str, x: Number, y: Number, width: Number, height: Number,
            text: str, properties: TextProperties,
            *args, **kwargs
    ) -> 'TextBlock': ...

    def create_rectangle(
            self,
            name: str, x: Number, y: Number, width: Number, height: Number,
            bound: Any, padding: Any,
            *args, **kwargs
    ) -> 'Rectangle': ...

    def create_ellipse(
            self,
            name: str, x: Number, y: Number, width: Number, height: Number,
            bound: Any, padding: Any,
            *args, **kwargs
    ) -> 'Ellipse': ...

    def create_triangle(
            self,
            name: str, x: Number, y: Number, width: Number, height: Number,
            bound: Any, padding: Any,
            *args, **kwargs
    ) -> 'Triangle': ...

    def create_image(self, name: str, x: Number, y: Number, width: Number, height: Number, *args, **kwarg) -> 'Image':
        ...

    def create_text3d(self, name: str, x: Number, y: Number, width: Number, height: Number, *args, **kwarg) -> 'Text3D':
        ...

    def create_ticker(self, name: str, x: Number, y: Number, width: Number, height: Number, *args, **kwarg) -> 'Ticker':
        ...


@dataclass
class Arg:
    attribute: str
    type: Optional[type] = None
    default: Any = None
    optional: bool = True


class BaseGTObject:
    _args: List[Arg] = [
        Arg("name", type=str, optional=False),
        Arg("x", type=Number, optional=False),
        Arg("y", type=Number, optional=False),
        Arg("width", type=Number, optional=False),
        Arg("height", type=Number, optional=False),
    ]

    def __init_subclass__(cls, **_kwargs) -> None:
        super().__init_subclass__()
        cls._tag = _kwargs.get("tag", cls.__name__)
        cls._args = []
        for parent in cls.__mro__[1:-1]:
            if not hasattr(parent, "_args"):
                continue
            cls._args.extend([a for a in getattr(parent, "_args") if a not in cls._args])
        cls._args.extend(_kwargs.get("init_args", []))
        sig = signature(cls.create)
        parameters = list(sig.parameters.values())[2:]  # Skip 'cls' and 'parent'

        # Define the method with the specific parameters
        def layer_method(self, *args, **kwargs):
            for i, arg in enumerate(args):
                argument = cls._args[i]
                kwargs[argument.attribute] = arg
            return cls.create(self, **kwargs)

        # Set the name of the function
        method_name = f"create_{cls.__name__.lower()}"
        layer_method.__name__ = method_name

        # Set the signature of the function
        layer_method.__signature__ = sig.replace(
            parameters=[Parameter('self', Parameter.POSITIONAL_OR_KEYWORD)] + parameters)

        # Attach the method to the Layer class
        setattr(Layer, method_name, layer_method)

    def __init__(self, **kwargs):
        for a in self._args:
            k, v = a.attribute, kwargs.get(a.attribute, a.default)
            if not (a.optional or v is not None):
                raise TypeError(f"{self.__class__.__name__} takes {k} attribute")
            if a.type and not isinstance(v, (a.type,)):
                raise TypeError(
                    f"{self.__class__.__name__}.{k} requires"
                    f"a '{a.type.__name__}' but received a '{type(v).__name__}'"
                )
            setattr(self, k, v)

        self.fill = Colour.from_hex("#00000000")
        self.stroke = Colour.from_hex("#00000000")

    @classmethod
    def create(cls, parent: Layer, index: int = -1, **kwargs):
        return parent.insert_children(cls, index, **kwargs)

    def set_fill(self, colour: Union[str, Colour]):
        self.fill = colour

    def set_stroke(self, colour: Union[str, Colour]):
        self.stroke = colour

    def to_xml(self, parent):
        raise NotImplementedError(f"Function `to_xml()` should be implemented for {self.__class__.__name__} class!")


class TextBlock(BaseGTObject, init_args=[
    Arg("text", type=str, optional=False),
    Arg("properties", type=TextProperties, optional=False)
]):

    def to_xml(self, parent):
        element = ET.SubElement(parent, 'TextBlock', **self.properties.dict(text_block=self))

        fill = ET.SubElement(element, 'TextBlock.Fill')
        ET.SubElement(fill, "Brush", Color=str(self.fill))
        stroke = ET.SubElement(element, 'TextBlock.Stroke')
        ET.SubElement(stroke, "Brush", Color=str(self.stroke))


# Arg("bound"), Arg("padding")
class Shape(BaseGTObject, init_args=[Arg("bound"), Arg("padding")]):
    def set_bounding(self, obj, padding=None):
        self.bound = obj.name
        if isinstance(padding, int):
            padding = (padding,)
        pad_dimensions = len(padding) if padding else 0
        if pad_dimensions == 1:
            self.padding = PAD_STR % (padding[0], padding[0], padding[0], padding[0])
        elif pad_dimensions < 4:
            self.padding = PAD_STR % (padding[0], padding[1], padding[0], padding[1])
        elif pad_dimensions == 4:
            self.padding = PAD_STR % padding
        else:
            self.padding = PAD_STR % (0, 0, 0, 0)

    def to_xml(self, parent):
        element = ET.SubElement(parent, self._tag,
                                Name=self.name,
                                Dimensions=f"%i,%i,%i" % (self.width, self.height, 0),
                                Location="%i,%i,%i" % (self.x, self.y, 0))
        if self.bound and self.padding:
            bounding = ET.SubElement(element, f'{self._tag}.Bounding')
            ET.SubElement(bounding, "Bounding", Object=self.bound, Padding=self.padding)
        fill = ET.SubElement(element, f'{self._tag}.Fill')
        ET.SubElement(fill, "Brush", Color=str(self.fill))
        stroke = ET.SubElement(element, f'{self._tag}.Stroke')
        ET.SubElement(stroke, "Brush", Color=str(self.stroke))


class Rectangle(Shape):
    ...


class Ellipse(Shape):
    ...


class Triangle(Shape):
    ...


class Image(BaseGTObject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        raise NotImplementedError("Image in not implemented yet!")

    def to_xml(self, parent):
        pass


class Text3D(BaseGTObject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        raise NotImplementedError("Text3D in not implemented yet!")

    def to_xml(self, parent):
        pass


class Ticker(BaseGTObject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        raise NotImplementedError("Ticker in not implemented yet!")

    def to_xml(self, parent):
        pass


if __name__ == "__main__":
    Layer.__generate_stub__()
