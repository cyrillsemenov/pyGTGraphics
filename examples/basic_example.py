from pyGTGraphics.project import Project
from pyGTGraphics.properties import Colour
from pyGTGraphics.storyboard import Storyboard, RevealAnimation
from pyGTGraphics.text_properties import TextProperties

TEXT_PROPS = TextProperties(font_family="Century Gothic", font_size=90)
WHITE = Colour.from_hex("#E7E7ED")
BLACK = Colour.from_hex("#232325")
RED = Colour.from_hex("#FF2300")

if __name__ == "__main__":
    with Project(1920, 1080, "basic_example.gtzip") as proj:
        layer1 = proj.create_layer("Layer 1")
        assert layer1 == proj.document.layers["Layer 1"]
        proj.layout.pad(60)
        proj.layout.take_from_top(1000)
        rect1 = layer1.create_rectangle("Rect 1", **proj.layout)
        rect1.set_fill(RED)

        text1 = layer1.create_textblock(
            "Text 1",
            text="HERE WE ARE",
            **proj.layout.take_from_top(100),
            **TEXT_PROPS.with_attribute(auto_size=TextProperties.AutoSize.WIDTH_AND_HEIGHT, font_weight="Bold")
        )

        text1.set_fill(WHITE)
        rect1.set_bounding(text1, 15)
        layer1.children.append(rect1)
        assert proj.document.layers["Layer 1"].children[-1] == rect1
        layer1.children.append(text1)
        assert proj.document.layers["Layer 1"].children[-1] == text1

        layer2 = proj.create_layer("Layer 2")
        rect2 = layer2.create_rectangle("Rect 2", **proj.layout)
        rect2.set_fill(WHITE.with_alpha(0.8))
        text2 = layer2.create_textblock(
            "Text2",
            text="Lorem ipsum dolor sit amet consectetur adipisicing elit. "
            "Voluptatum facilis nobis earum eos ipsa consectetur incidunt "
            "vitae beatae soluta nihil doloremque, est esse debitis.",
            **proj.layout.take_from_top(100).pad(16),
            **TEXT_PROPS.with_attribute(font_size=30)
        )
        rect2.set_bounding(text2, 15)
        text2.set_fill(BLACK)
        layer2.children.append(rect2)
        layer2.children.append(text2)

        storyboard_ = Storyboard()
        storyboard_.append(RevealAnimation(rect1, 0, 2))
        storyboard_.append(RevealAnimation(text1, 1, 2))
        proj.document.storyboards.append(storyboard_)
