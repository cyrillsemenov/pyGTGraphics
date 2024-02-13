from base_node import Arg, Node
from color import Color
from composition import (
    Composition,
    DataFlags,
    Ellipse,
    Image,
    Layer,
    QRCode,
    Rectangle,
    RightTriangle,
)
from object_attributes import (
    Bitmap,
    Bounding,
    Brush,
    Crop,
    Effect,
    Geometry,
    GradientStop,
    Mask,
    Transform,
)
from point import Dimensions, Feather, Location, Margin, Padding, Range, Rotate
from storyboard import (
    AnimationBounce,
    AnimationCenterAxis,
    AnimationDirection,
    AnimationExpand,
    AnimationFade,
    AnimationFillOffset,
    AnimationFly,
    AnimationHidden,
    AnimationImageSequenceLoop,
    AnimationInterpolation,
    AnimationNone,
    AnimationReveal,
    AnimationRotate,
    AnimationRotateContinuous,
    AnimationStrokeOffset,
    AnimationZoom,
    AnimationZoomFade,
    Storyboard,
)

root = Composition(1920, 1080)
layer1 = root.add_layer("Layer one")
rect1 = layer1.add_rectangle("Rect 1", Dimensions(100, 100), Location(150, 150))
# FIXME: Fill and stroke
rect1.with_fill(Brush.solid(Color.red))
ellipse1 = layer1.add_ellipse("Ellipse 1", Location(100, 100), Dimensions(100, 100))
# FIXME: Fill and stroke
rect1.with_fill(Brush.solid(Color.blue))
animations_in = Storyboard.transition_in()
animations_in.add_bounce(rect1, 1, 2)
animations_in.add_fade(ellipse1, 1, 2)

import xml.etree.ElementTree as ET

er = root.to_xml()
animations_in.to_xml(er)
print(ET.tostring(er, xml_declaration=False, encoding="unicode"))
r"""
<Composition Width="1920" Height="1080">
    <Layer Name="Layer one" Location="0,0,0" Dimensions="1920,1080,0">
        <Layer.Composition>
            <Composition Width="1920" Height="1080">
                <Rectangle Name="Rect 1" Location="150,150,0" Dimensions="100,100,0" />
                <Ellipse Name="Ellipse 1" Location="100,100,0" Dimensions="100,100,0" />
            </Composition>
        </Layer.Composition>
    </Layer>
<Storyboard Type="TransitionIn">
    <Storyboard.Animations>
        <Bounce Object="Rect 1" Duration="1" Delay="2" />
        <Fade Object="Ellipse 1" Duration="1" Delay="2" />
    </Storyboard.Animations>
</Storyboard>
</Composition>
"""
