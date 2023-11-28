from pyGTGraphics.project import Project
from pyGTGraphics.properties import TextProperties, Colour, AutoSizeOptions
from pyGTGraphics.storyboard import Storyboard, RevealAnimation
from pyGTGraphics.objects import Rectangle, TextBlock

TEXT_PROPS = TextProperties("Century Gothic", 90)
WHITE = Colour.from_hex("#E7E7ED")
BLACK = Colour.from_hex("#232325")
RED = Colour.from_hex("#FF2300")

if __name__ == "__main__":
    with Project(1920, 1080, "basic_example.gtzip") as proj:
        layer1 = proj.create_layer("Layer 1")
        assert layer1 == proj.document.layers["Layer 1"]

        rect1 = layer1.create_rectangle("Rect 1", 0, 0, 1000, 100)
        rect1.set_fill(RED)
        text1 = layer1.create_textblock(
            "Text 1",
            60, 800, 1860, 100,
            "HERE WE ARE",
            TEXT_PROPS.with_attribute(auto_size=AutoSizeOptions.WIDTH_AND_HEIGHT, font_weight="Bold")
        )
        text1.set_fill(WHITE)
        rect1.set_bounding(text1, 15)
        layer1.children.append(rect1)
        assert proj.document.layers["Layer 1"].children[-1] == rect1
        layer1.children.append(text1)
        assert proj.document.layers["Layer 1"].children[-1] == text1

        layer2 = proj.create_layer("Layer 2")
        rect2 = layer2.create_rectangle("Rect 2", 60, 900, 1860, 100)
        rect2.set_fill(WHITE.with_alpha(0.8))
        text2 = layer2.create_textblock(
            "Text2", 46, 872 + 16, 930 - 16, 117 - 16,
            "Lorem ipsum dolor sit amet consectetur adipisicing elit. "
            "Voluptatum facilis nobis earum eos ipsa consectetur incidunt "
            "vitae beatae soluta nihil doloremque, est esse debitis.",
            TEXT_PROPS.with_attribute(font_size=30)
        )
        rect2.set_bounding(text2, 15)
        text2.set_fill(BLACK)
        layer2.children.append(rect2)
        layer2.children.append(text2)

        storyboard_ = Storyboard()
        storyboard_.append(RevealAnimation(rect1, 0, 2))
        storyboard_.append(RevealAnimation(text1, 1, 2))
        proj.document.storyboards.append(storyboard_)
