import xml.etree.ElementTree as ET


class Root:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.layers = []
        self.storyboards = []

    def to_xml(self):
        comp_element = ET.Element('Composition', Width=str(self.width), Height=str(self.height))
        for element in self.layers:
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
        self.fill = "#00000000"
        self.stroke = "#00000000"

    def set_fill(self, colour):
        self.fill = colour

    def set_stroke(self, colour):
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
    def __init__(self, name: str, x: int, y: int, width: int, height: int, text: str, **kwargs):
        super().__init__(name, x, y, width, height)
        self.text = text
        self.font_family = kwargs.get("font_family", "TT Firs Neue")
        self.font_size = kwargs.get("font_size", 34)
        self.font_weight = kwargs.get("font_weight", "Regular")
        self.text_align = kwargs.get("text_align", "Left")
        self.ignore_overhang = kwargs.get("ignore_overhang", True)
        self.line_spacing = kwargs.get("line_spacing", 0)
        self.auto_size = kwargs.get("auto_size", "Width")

        self.fill = "#00000000"
        self.stroke = "#00000000"

    def to_xml(self, parent):
        element = ET.SubElement(
            parent, 'TextBlock',
            Name=self.name,
            Dimensions=f"%i,%i,%i" % (self.width, self.height, 0),
            Location="%i,%i,%i" % (self.x, self.y, 0),
            DataFlags="ShowVisible",
            Text=self.text,
            FontFamily=self.font_family,
            FontSize=str(self.font_size),
            FontWeight=self.font_weight,
            TextAlign=self.text_align,
            IgnoreOverhang=str(self.ignore_overhang),
            LineSpacing=str(self.line_spacing),
            AutoSize=self.auto_size
        )

        fill = ET.SubElement(element, 'TextBlock.Fill')
        ET.SubElement(fill, "Brush", Color=self.fill)
        stroke = ET.SubElement(element, 'TextBlock.Stroke')
        ET.SubElement(stroke, "Brush", Color=self.stroke)


class Rectangle(BaseGTObject):
    _tag = 'Rectangle'

    def to_xml(self, parent):
        element = ET.SubElement(parent, self._tag,
                                Name=self.name,
                                Dimensions=f"%i,%i,%i" % (self.width, self.height, 0),
                                Location="%i,%i,%i" % (self.x, self.y, 0))
        fill = ET.SubElement(element, 'Rectangle.Fill')
        ET.SubElement(fill, "Brush", Color=self.fill)
        stroke = ET.SubElement(element, 'Rectangle.Stroke')
        ET.SubElement(stroke, "Brush", Color=self.stroke)


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
        raise NotImplementedError("Image in not implemented yet!")

    def to_xml(self, parent):
        pass


class Ticker(BaseGTObject):
    def __init__(self, name: str, x: int, y: int, width: int, height: int):
        super().__init__(name, x, y, width, height)
        raise NotImplementedError("Image in not implemented yet!")

    def to_xml(self, parent):
        pass

