import xml.etree.ElementTree as ET


class Animation:
    _tag = "None"

    def __init__(
            self, target, start_time: int = 0, duration: int = 1,
            interpolation: str = "Linear", direction: str = "Left",
            center_axis: str = "X"
    ):
        self.target = target
        self.start_time = start_time
        self.duration = duration
        self.interpolation = interpolation
        self.direction = direction
        self.center_axis = center_axis

    def to_xml(self, parent):
        attributes = {
            "Object": self.target.name,
            "Delay": str(self.start_time),
            "Duration": str(self.duration),
            "Interpolation": self.interpolation,
            "Direction": self.direction,
            "CenterAxis": self.center_axis
        }
        return ET.SubElement(parent, self._tag, **attributes)


class RevealAnimation(Animation):
    _tag = "Reveal"
    #
    # def __init__(self, target, direction, **kwargs):
    #     super().__init__(target, **kwargs)
    #     self.direction = direction
    #
    # def to_xml(self):
    #     element = super().to_xml()
    #     element.attrib["Direction"] = self.direction
    #     return element


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
