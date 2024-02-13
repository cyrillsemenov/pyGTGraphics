"""
    'Ellipse.Crop' 
    'Rectangle.Crop' : Node
    'RightTriangle.Crop' : Node
    'TextBlock.Crop' : Node
    'Triangle.Crop' 

    'Ellipse.Effects' 
    'Image.Effects' : List[Node]
    'Rectangle.Effects' : List[Node]
    'RightTriangle.Effects' : List[Node]
    'TextBlock.Effects' : List[Node]

    'Ellipse.Fill' 
    'Rectangle.Fill' : Brush(Node)
    'RightTriangle.Fill' 
    'TextBlock.Fill' 
    'Ticker.Fill' 
    'Triangle.Fill' 

    'Ellipse.Stroke' 
    'Rectangle.Stroke' : Brush(Node)
    'RightTriangle.Stroke' 
    'TextBlock.Stroke' 
    'Ticker.Stroke' 
    'Triangle.Stroke' 

    'Ellipse.Transform' 
    'Image.Transform' 
    'Rectangle.Transform' : Transform(Node)
    'RightTriangle.Transform' 
    'TextBlock.Transform' 
    'Triangle.Transform' 

    'Image.Bitmap' : Bitmap(Node)

    'Image.Geometry' 
    'Rectangle.Geometry' : Geometry(Node)

    'Rectangle.Bounding' 

    'Rectangle.Mask' : Mask(Node)
    'TextBlock.Mask' 

    'TextBlock.TextDecorations' 
        'TextDecoration': 
    'Ticker.Template' 
"""

from enum import Enum
from numbers import Real
from typing import Optional, Tuple, Union

from base_node import Arg, Node, Reference
from color import Color
from point import Feather, Padding, Range, Rotate


class Crop(
    Node,
    init_args=[
        Arg("range", type=Range),
        Arg("feather", type=Feather),
    ],
):
    pass


class GradientStop(
    Node,
    init_args=[
        Arg("color", type=Color),
        Arg("position", type=Real),
    ],
):
    """
    Represents a stop in a gradient.

    >>> gradient_stop = GradientStop(color=Color.red, position=0.5)
    >>> gradient_stop_xml = gradient_stop.to_xml()
    >>> import xml.etree.ElementTree as ET
    >>> ET.tostring(gradient_stop_xml, xml_declaration=False, encoding="unicode")
    '<GradientStop Color="#0000FFFF" Position="0.5" />'
    """

    def __init__(self, color: Color, position: Optional[Real] = None, **kwargs):
        super().__init__(color=color, position=position, **kwargs)


class Brush(
    Node,
    init_args=[
        Arg("color", type=Color),
        Arg("type", type=str),
        Arg("start_point", type=str),
        Arg("end_point", type=str),
        Arg("stops", type=list, default=[]),
        Arg("bitmap", type=Node),
    ],
):
    r"""
    >>> gradient = Brush(type=Brush.types.LINEAR_GRADIENT.value)
    >>> gradient.type
    'LinearGradient'
    >>> gradient.stops.append(GradientStop(Color.red))
    >>> gradient.stops[-1].color
    #0000FFFF
    >>> gradient.stops.append(GradientStop(color=Color.blue, position=1))
    >>> gradient.stops[-1].color
    #FF0000FF
    >>> gradient.stops[-1].position
    1
    >>> import xml.etree.ElementTree as ET
    >>> ET.tostring(gradient.to_xml(), xml_declaration=False, encoding='unicode')
    '<Brush Type="LinearGradient"><Brush.Stops><GradientStop Color="#0000FFFF" /><GradientStop Color="#FF0000FF" Position="1" /></Brush.Stops></Brush>'
    """

    class types(Enum):
        SOLID: str = "Solid"
        LINEAR_GRADIENT: str = "LinearGradient"
        RADIAL_GRADIENT: str = "LinearGradient"
        TRANSPARENT: str = "Transparent"
        BITMAP: str = "Bitmap"

    def __init__(self, type: Union[str, "Brush.types", None] = None, **kwargs):
        if isinstance(type, Enum):
            type = type.value
        super().__init__(type=type, **kwargs)

    @classmethod
    def solid(cls, color: Color) -> "Brush":
        # <Rectangle.Fill>
        #   <Brush Color="#FFFFFFFF" />
        # </Rectangle.Fill>
        # <Rectangle.Stroke>
        #   <Brush Color="#FFFFFFFF" />
        # </Rectangle.Stroke>
        return cls.__init__(type=cls.types.SOLID, color=color)

    @classmethod
    def linear_gradient(
        cls,
        *stops: Union[GradientStop, Tuple[Color, Real]],
        start_point=None,
        end_point=None,
    ):
        # _attrs = [
        #     Arg("Type", type=str),
        #     Arg("Angle", type=Number),
        #     Arg("Wrap", type=str),
        #     Arg("Stops", type=List[GradientStop]),
        #     Arg("StartPoint", type=str),
        #     Arg("EndPoint", type=str),
        # ]
        # <Brush Type="LinearGradient" Color="#FF00B050" StartPoint="0.5000001,0" EndPoint="1,0">
        #   <Brush.Stops>
        #     <GradientStop Color="#FFFF0000" />
        #     <GradientStop Position="0.5" Color="#FF00FF00" />
        #     <GradientStop Position="1" Color="#FF8B00FF" />
        #   </Brush.Stops>
        # </Brush>
        gradient_stops = []
        for s in stops:
            if isinstance(s, GradientStop):
                gradient_stops.append(s)
            else:
                color, position = s
                gradient_stops.append(GradientStop(color, position))
        return cls.__init__(
            type=cls.types.LINEAR_GRADIENT,
            stops=gradient_stops,
            start_point=start_point,
            end_point=end_point,
        )


class Bitmap(
    Node,
    init_args=[
        Arg("source", type=str, optional=False),
    ],
):
    pass


class Bounding(
    Node,
    init_args=[
        Arg("object", type=Reference),
        Arg("padding", type=Padding),
    ],
):
    pass


class Effect(
    Node,
    init_args=[
        Arg("type", type=str, optional=False),
        Arg("angle", type=str),
        Arg("blur_amount", type=int),
        Arg("mode", type=str),
    ],
):
    r"""
    Represents an effect that can be applied to objects.

    Example usage:
    >>> effect = Effect.skew(angle_x=30, angle_y=20)
    >>> effect.type
    'Skew'
    >>> effect.angle
    '30,20'

    >>> shadow_effect = Effect.shadow(blur_amount=15, mode="Outer")
    >>> shadow_effect.type
    'Shadow'
    >>> shadow_effect.blur_amount
    15
    >>> shadow_effect.mode
    'Outer'
    >>> import xml.etree.ElementTree as ET
    >>> ET.tostring(shadow_effect.to_xml(), xml_declaration=False, encoding='unicode')
    '<Effect Type="Shadow" BlurAmount="15" Mode="Outer" />'
    """

    class types(Enum):
        SKEW: str = "Skew"
        SHADOW: str = "Shadow"
        FLIP_X: str = "FlipX"
        FLIP_Y: str = "FlipY"

    def __init__(self, type: Union[str, "Effect.types"], **kwargs):
        if isinstance(type, Enum):
            type = type.value
        super().__init__(type=type, **kwargs)

    @classmethod
    def skew(cls, angle_x: int = 0, angle_y: int = 0):
        return cls(type=cls.types.SKEW, angle=f"{angle_x},{angle_y}")

    @classmethod
    def shadow(cls, blur_amount: int = 0, mode: str = "Shadow"):
        return cls(type=cls.types.SHADOW, blur_amount=blur_amount, mode=mode)

    @classmethod
    def flip_x(cls):
        return cls(type=cls.types.FLIP_X)

    @classmethod
    def flip_y(cls):
        return cls(type=cls.types.FLIP_Y)


class Geometry(
    Node,
    init_args=[
        Arg("type", type=str),
    ],
):
    pass


class Mask(
    Node,
    init_args=[
        Arg("object", type=Reference),
    ],
):

    pass


class Transform(
    Node,
    init_args=[
        Arg("rotate", type=Rotate),
    ],
):
    pass


if __name__ == "__main__":
    import doctest

    print(doctest.testmod())
