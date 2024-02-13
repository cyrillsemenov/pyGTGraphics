"""
'Composition': Height, Width
'Layer': Composition, DataFlags, Dimensions, Location, Locked, Name
    'Layer.Composition' 

'Ellipse': Crop, DataFlags, Dimensions, Effects, Fill, Location, Name, Opacity, Stroke, StrokeThickness, Transform
    'Ellipse.Crop' 
    'Ellipse.Effects' 
    'Ellipse.Fill' 
    'Ellipse.Stroke' 
    'Ellipse.Transform' 
'Image': Bitmap, DataFlags, Dimensions, Effects, Geometry, Location, Name, Opacity, SizeMode, Transform, Visible
    'Image.Bitmap' : Bitmap(Node)
    'Image.Effects' : List[Node]
    'Image.Geometry' 
    'Image.Transform' 
'QRCode': Dimensions, Location, Name, Text
'Rectangle': Bounding, Crop, DataFlags, Dimensions, Effects, Fill, Geometry, Location, Mask, Name, Opacity, Radius, Stroke, StrokeThickness, Style, Transform, Visible
    'Rectangle.Bounding' 
    'Rectangle.Crop' : Node
    'Rectangle.Effects' : List[Node]
    'Rectangle.Fill' : Brush(Node)
    'Rectangle.Geometry' : Geometry(Node)
    'Rectangle.Mask' : Mask(Node)
    'Rectangle.Stroke' : Brush(Node)
    'Rectangle.Transform' : Transform(Node)
'RightTriangle': Crop, Dimensions, Effects, Fill, Location, Name, Stroke, Transform
    'RightTriangle.Crop' : Node
    'RightTriangle.Effects' : List[Node]
    'RightTriangle.Fill' 
    'RightTriangle.Stroke' 
    'RightTriangle.Transform' 
'TextBlock': AutoSize, Crop, DataFlags, Dimensions, Effects, Fill, FontFamily, FontSize, FontWeight, Location, Mask, Name, Stroke, StrokeThickness, Text, TextAlign, TextDecorations, TextWordWrapping, Transform, VerticalAlign
    'TextBlock.Crop' : Node
    'TextBlock.Effects' : List[Node]
    'TextBlock.Fill' 
    'TextBlock.Mask' 
    'TextBlock.Stroke' 
    'TextBlock.TextDecorations' 
        'TextDecoration': 
    'TextBlock.Transform' 
'Ticker': Dimensions, Direction, Fill, FontFamily, FontSize, FontWeight, Location, Name, Speed, Stroke, Template, TextAlign, TextWordWrapping, Type, VerticalAlign
    'Ticker.Fill' 
    'Ticker.Stroke' 
    'Ticker.Template' 
'Triangle': Crop, Dimensions, Fill, Location, Name, Stroke, StrokeThickness, Transform
    'Triangle.Crop' 
    'Triangle.Fill' 
    'Triangle.Stroke' 
    'Triangle.Transform' 
"""

from enum import Enum
from numbers import Real
from typing import List, Optional, TypeVar, Union

import object_attributes
from base_node import Arg, Node
from point import Dimensions, Location

T = TypeVar("T")


class DataFlags(Enum):
    HIDDEN: str = "Hidden"
    SHOW_VISIBLE: str = "ShowVisible"
    NONE: str = "None"


class Composition(
    Node,
    init_args=[
        Arg("width", type=Real, optional=False),
        Arg("height", type=Real, optional=False),
    ],
):
    def __init__(self, width: Real, height: Real, **kwargs):
        super().__init__(width=width, height=height, **kwargs)

    def add_layer(
        self,
        name: str,
        location: Optional[Location] = None,
        dimensions: Optional[Dimensions] = None,
        data_flags: Optional[str] = None,
        locked: Optional[bool] = None,
        composition: Optional["Composition"] = None,
        **kwargs,
    ) -> "Layer":
        if location is None:
            location = Location(0, 0, 0)
        if dimensions is None:
            dimensions = Dimensions(self.width, self.height, 0)
        self.append(
            Layer(name, location, dimensions, data_flags, locked, composition, **kwargs)
        )
        return self.children[-1]


class NamedNode(
    Node,
    init_args=[
        Arg("name", type=str, optional=False),
    ],
):
    def __init__(self, name: str, **kwargs):
        super().__init__(name=name, **kwargs)


class ObjectNode(
    NamedNode,
    init_args=[
        Arg("location", type=Location, optional=False),
        Arg("dimensions", type=Dimensions, optional=False),
        Arg("data_flags", type=str),
    ],
):
    def __init__(
        self,
        name: str,
        location: Location,
        dimensions: Dimensions,
        data_flags: Union[str, DataFlags, None] = None,
        **kwargs,
    ):
        if isinstance(data_flags, DataFlags):
            data_flags = data_flags.value()
        super().__init__(
            name=name,
            location=location,
            dimensions=dimensions,
            data_flags=data_flags,
            **kwargs,
        )


class Layer(
    ObjectNode,
    init_args=[
        Arg("locked", type=bool, default=False),
        Arg("composition", type=Composition, optional=True),
    ],
):
    r"""
    >>> layer = Layer("Test layer", Location(0, 0), Dimensions(1920, 1080))
    >>> ellipse = layer.add_ellipse("Test Ellipse", Location(200, 150), Dimensions(100, 100)).with_fill(object_attributes.Brush("Color.red"))
    >>> ellipse is layer.composition.children[-1]
    True
    >>> ellipse.dimensions = Dimensions(120, 120)
    >>> import xml.etree.ElementTree as ET
    >>> ET.tostring(layer.to_xml(), xml_declaration=False, encoding='unicode')
    '<Layer Name="Test layer" Location="0,0,0" Dimensions="1920,1080,0"><Layer.Composition><Composition Width="1920" Height="1080"><Ellipse Name="Test Ellipse" Location="200,150,0" Dimensions="120,120,0" /></Composition></Layer.Composition></Layer>'
    """

    def __init__(
        self,
        name: str,
        location: Location,
        dimensions: Dimensions,
        data_flags: Optional[str] = None,
        locked: Optional[bool] = None,
        composition: Optional[Composition] = None,
        **kwargs,
    ):
        if composition is None:
            composition = Composition(width=dimensions.width, height=dimensions.height)
        super().__init__(
            name=name,
            location=location,
            dimensions=dimensions,
            data_flags=data_flags,
            locked=locked,
            composition=composition,
            **kwargs,
        )

    def append(self, *children: Node):
        for c in children:
            self.composition.children.append(c)

    def add_ellipse(
        self,
        name: str,
        location: Location,
        dimensions: Dimensions,
        effects: Optional[List[object_attributes.Effect]] = None,
        fill: Optional[object_attributes.Brush] = None,
        opacity: Optional[float] = None,
        stroke: Optional[object_attributes.Brush] = None,
        stroke_thickness: Optional[Real] = None,
        transform: Optional[object_attributes.Transform] = None,
        crop: Optional[object_attributes.Crop] = None,
        data_flags: Optional[DataFlags] = None,
    ) -> "Ellipse":
        new_object = Ellipse(name, location, dimensions, data_flags)
        self.append(new_object)
        return new_object

    def add_image(
        self,
        name: str,
        # SizeMode,
        bitmap: str,
        dimensions: Dimensions,
        location: Location,
        effects: Optional[List[object_attributes.Effect]] = None,
        geometry: Optional[object_attributes.Geometry] = None,
        opacity: Optional[float] = None,
        transform: Optional[object_attributes.Transform] = None,
        visible: Optional[bool] = None,
        data_flags: Optional[DataFlags] = None,
    ) -> "Image":
        new_object = Image(name, location, dimensions, data_flags)
        self.append(new_object)
        return new_object

    def add_qr_code(
        self,
        name: str,
        text: str,
        dimensions: Dimensions,
        location: Location,
        data_flags: Optional[DataFlags] = None,
    ) -> "QRCode":
        new_object = QRCode(name, location, dimensions, data_flags)
        self.append(new_object)
        return new_object

    def add_rectangle(
        self,
        name: str,
        # Radius,
        # Style,
        # Visible,
        # Mask,
        dimensions: Dimensions,
        location: Location,
        effects: Optional[List[object_attributes.Effect]] = None,
        fill: Optional[object_attributes.Brush] = None,
        geometry: Optional[object_attributes.Geometry] = None,
        opacity: Optional[float] = None,
        stroke: Optional[object_attributes.Brush] = None,
        stroke_thickness: Optional[Real] = None,
        transform: Optional[object_attributes.Transform] = None,
        bounding: Optional[object_attributes.Bounding] = None,
        crop: Optional[object_attributes.Crop] = None,
        data_flags: Optional[DataFlags] = None,
    ) -> "Rectangle":
        new_object = Rectangle(name, location, dimensions, data_flags)
        self.append(new_object)
        return new_object

    def add_right_triangle(
        self,
        name: str,
        dimensions: Dimensions,
        location: Location,
        effects: Optional[List[object_attributes.Effect]] = None,
        fill: Optional[object_attributes.Brush] = None,
        stroke: Optional[object_attributes.Brush] = None,
        transform: Optional[object_attributes.Transform] = None,
        crop: Optional[object_attributes.Crop] = None,
        data_flags: Optional[DataFlags] = None,
    ) -> "RightTriangle":
        new_object = RightTriangle(name, location, dimensions, data_flags)
        self.append(new_object)
        return new_object

    def add_text_block(
        self,
        name: str,
        text: str,
        # AutoSize,
        # FontFamily,
        # FontSize,
        # FontWeight,
        # TextAlign,
        # TextDecorations,
        # TextWordWrapping,
        # VerticalAlign,
        dimensions: Dimensions,
        location: Location,
        effects: Optional[List[object_attributes.Effect]] = None,
        fill: Optional[object_attributes.Brush] = None,
        stroke: Optional[object_attributes.Brush] = None,
        stroke_thickness: Optional[Real] = None,
        transform: Optional[object_attributes.Transform] = None,
        # Mask,
        crop: Optional[object_attributes.Crop] = None,
        data_flags: Optional[DataFlags] = None,
    ) -> "TextBlock":
        # TextBlock >
        #   TextBlock.Mask
        #   TextBlock.Transform
        #   TextBlock.Effects
        #   TextBlock.Crop
        #   TextBlock.Fill
        #   TextBlock.Stroke
        #   TextBlock.TextDecorations
        new_object = TextBlock(name, location, dimensions, data_flags)
        self.append(new_object)
        return new_object

    def add_ticker(
        self,
        name: str,
        # FontFamily,
        # FontSize,
        # FontWeight,
        # Speed,
        # Template,
        # TextAlign,
        # TextWordWrapping,
        # Type,
        # VerticalAlign,
        dimensions: Dimensions,
        location: Location,
        direction: str,
        fill: Optional[object_attributes.Brush] = None,
        stroke: Optional[object_attributes.Brush] = None,
        data_flags: Optional[DataFlags] = None,
    ) -> "Ticker":
        new_object = Ticker(name, location, dimensions, data_flags)
        self.append(new_object)
        return new_object

    def add_triangle(
        self,
        name: str,
        dimensions: Dimensions,
        location: Location,
        fill: Optional[object_attributes.Brush] = None,
        stroke: Optional[object_attributes.Brush] = None,
        stroke_thickness: Optional[Real] = None,
        transform: Optional[object_attributes.Transform] = None,
        crop: Optional[object_attributes.Crop] = None,
        data_flags: Optional[DataFlags] = None,
    ) -> "Triangle":
        new_object = Triangle(name, location, dimensions, data_flags)
        self.append(new_object)
        return new_object


class ContentNode(ObjectNode):
    def with_crop(self: T, crop: object_attributes.Crop) -> T:
        self.crop = crop
        return self

    def with_transform(self: T, transform: object_attributes.Transform) -> T:
        self.transform = transform
        return self

    def with_bounding(self: T, bounding: object_attributes.Bounding) -> T:
        self.bounding = bounding
        return self

    def with_mask(self: T, mask: object_attributes.Mask) -> T:
        self.mask = mask
        return self

    def with_geometry(self: T, geometry: object_attributes.Geometry) -> T:
        self.geometry = geometry
        return self

    def with_fill(self: T, fill: object_attributes.Brush) -> T:
        self.fill = fill
        return self

    def with_stroke(self: T, stroke: object_attributes.Brush) -> T:
        self.stroke = stroke
        return self

    def add_effects(self: T, *effects: object_attributes.Effect) -> T:
        self.effects.extend(effects)
        return self


class Ellipse(ContentNode):
    pass


class Image(ContentNode):
    pass


class QRCode(ContentNode):
    pass


class Rectangle(ContentNode):
    pass


class RightTriangle(ContentNode):
    pass


class TextBlock(ContentNode):
    # init_args=[
    #     Arg("text", type=str, optional=False),
    #     Arg("font_family", type=str, optional=False),
    #     Arg("font_size", type=Number, optional=False),
    #     Arg("font_weight", type=str),
    #     Arg("text_align", type=str),
    #     Arg("vertical_align", type=str),
    #     Arg("word_wrapping", type=str),
    #     Arg("ignore_overhang", type=bool),
    #     Arg("line_spacing", type=Number),
    #     Arg("auto_size", type=str),
    #     Arg("data_flags", type=str),
    # ],
    pass


class Ticker(ContentNode):
    pass


class Triangle(ContentNode):
    pass


if __name__ == "__main__":
    import doctest

    print(doctest.testmod())
