import xml.etree.ElementTree as ET
from typing import Optional

from .properties import AnimationProperties, AnimationDirection, AnimationInterpolation


class Animation:
    _tag = "None"

    def __init__(
            self, target, duration: float = 1.0, delay: Optional[float] = None,
            interpolation: Optional[str] = None, direction: Optional[str] = None,
            center_axis: str = "X", **kwargs
    ):
        self.properties = AnimationProperties(duration, delay, interpolation, direction)
        self.target = target

    def to_xml(self, parent):
        return ET.SubElement(parent, self._tag, **self.properties.dict(target=self.target))


class RevealAnimation(Animation):
    _tag = "Reveal"


class FadeAnimation(Animation):
    _tag = "Fade"


class Storyboard(list):
    def __init__(self, reverse: bool = False):
        super().__init__()
        self.reversed = reverse

    def append(self, layer):
        if not isinstance(layer, Animation):
            raise TypeError("Composition can only contain Animation instances")
        super().append(layer)

    def to_xml(self, parent):
        storyboard = ET.SubElement(
            parent, "Storyboard",
            Type="TransitionOut" if self.reversed else "TransitionIn"
        )
        storyboard_inner = ET.SubElement(storyboard, "Storyboard.Animations")
        for a in self:
            a.to_xml(storyboard_inner)
