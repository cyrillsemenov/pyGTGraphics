import os.path
import shutil
import tempfile
from pyGTGraphics.storyboard import Storyboard, RevealAnimation
from pyGTGraphics.objects import Root, Layer, Rectangle
from pyGTGraphics.content import ContentTypes
from pyGTGraphics.resources import Resources

temp_dir = tempfile.TemporaryDirectory()

# document.xml
root = Root(1920, 1080)
layer1 = Layer("Layer 1", 0, 0, 1920, 1080)
rect1 = Rectangle("Rect 1", 10, 10, 100, 100)
rect1.set_fill("#FEEDBEEF")
layer1.children.append(rect1)
root.layers.append(layer1)

storyboard_ = Storyboard()
animation = RevealAnimation(rect1)
storyboard_.append(animation)
root.storyboards.append(storyboard_)

tree = root.to_xml()
tree.write(os.path.join(temp_dir.name, "document.xml"), encoding='utf-16', xml_declaration=True)

# resources.xml
resources = Resources()
resources.to_xml().write(os.path.join(temp_dir.name, "resources.xml"), encoding='utf-8', xml_declaration=False)

# [Content_Types].xml
types = ContentTypes()
types.to_xml().write(os.path.join(temp_dir.name, "[Content_Types].xml"), encoding='utf-8', xml_declaration=True)

# thumbnail.png


shutil.make_archive("basic_example", 'zip', temp_dir.name)
os.rename("basic_example.zip", "basic_example.gtzip")

temp_dir.cleanup()
