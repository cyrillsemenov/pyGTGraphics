import os.path
import tempfile
import zipfile

import xml.etree.ElementTree as ET

from pyGTGraphics.storyboard import Storyboard, RevealAnimation
from pyGTGraphics.objects import Root, Layer, Rectangle, TextBlock
from pyGTGraphics.content import ContentTypes
from pyGTGraphics.resources import Resources


def write_xml(element_tree, file_or_filename, encoding=None, declared_encoding=None, xml_declaration=None):
    if not encoding:
        encoding = "utf-8"
    if not declared_encoding:
        declared_encoding = encoding
    with open(file_or_filename, "w", encoding=encoding.lower(), errors="xmlcharrefreplace") as file:
        if xml_declaration:
            file.write("<?xml version='1.0' encoding='%s'?>\n" % (declared_encoding,))
        qnames, namespaces = ET._namespaces(element_tree._root, None)
        ET._serialize_xml(file.write, element_tree._root, qnames, namespaces, short_empty_elements=True)


temp_dir = tempfile.TemporaryDirectory()

# document.xml
root = Root(1920, 1080)
layer1 = Layer("Layer 1", 0, 0, 1920, 1080)
rect1 = Rectangle("Rect 1", 10, 10, 1000, 100)
rect1.set_fill("#FEEDBEEF")
text1 = TextBlock("Q1", 100, 100, 1000, 100, "Question:")
text1.set_fill("#FF0000FF")
rect1.set_bounding(text1, 20)
layer1.children.append(rect1)
layer1.children.append(text1)
root.layers.append(layer1)

storyboard_ = Storyboard()
animation = RevealAnimation(rect1, 0, 2)
animation = RevealAnimation(text1, 1, 2)
storyboard_.append(animation)
root.storyboards.append(storyboard_)

tree = root.to_xml()
ET.indent(tree, "  ")
write_xml(tree, os.path.join(temp_dir.name, "document.xml"), declared_encoding="utf-16", xml_declaration=True)

# resources.xml
resources = Resources()
write_xml(resources.to_xml(), os.path.join(temp_dir.name, "resources.xml"), xml_declaration=False)

# [Content_Types].xml
types = ContentTypes()
write_xml(types.to_xml(), os.path.join(temp_dir.name, "[Content_Types].xml"), xml_declaration=True)

# thumbnail.png


with zipfile.ZipFile("basic_example.gtzip", "w", zipfile.ZIP_STORED, allowZip64=False) as zf:
    for filename in os.listdir(temp_dir.name):
        f = os.path.join(temp_dir.name, filename)
        f = os.path.normpath(f)
        if os.path.isfile(f):
            zf.write(f, filename)

temp_dir.cleanup()
