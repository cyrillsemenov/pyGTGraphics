# GT Graphics Library for vMix

> [!WARNING]  
> This library is in a very early stage of development.
> It does not yet implement many functions and objects.
> Additionally, there are plans to add an import from Figma feature.


The GT Graphics Library is a Python tool 
designed to generate XML structures 
for use with vMix titles (gtzip files). 
It provided an object-oriented approach 
to define layers, shapes, text blocks, and animations.

## Features

- Object-oriented interface for creating **vMix** title compositions.
- Support for layers, rectangles, text blocks, and more.
- Animation support for dynamic title sequences.
- Export functionality to generate `gtzip` files compatible with vMix titles.

## Installation

To install the GT Graphics Library, you'll need Python 
installed on your system. The library is structured 
as a standard Python package, so installation is straightforward.
Simply clone the repository or download the package 
and include it in your project.

```bash
git clone https://github.com/yourusername/gt-graphics-library.git
cd gt-graphics-library
```

<strike>
Alternatively, if the package is available on PyPI, you can install it using pip:

```bash
pip install gt-graphics-library
```

</strike>

Usage
Here is a basic example of how to use the GT Graphics Library 
to create a composition with a layer, rectangle, and text block:
```python
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

        rect1 = Rectangle("Rect 1", 0, 0, 1000, 100)
        rect1.set_fill(RED)
        text1 = TextBlock(
            "Text 1",
            60, 800, 1860, 100,
            "HERE WE ARE",
            TEXT_PROPS.with_attribute(auto_size=AutoSizeOptions.WIDTH_AND_HEIGHT, font_weight="Bold")
        )
        text1.set_fill(WHITE)
        rect1.set_bounding(text1, 15)
        layer1.children.append(rect1)
        layer1.children.append(text1)

        layer2 = proj.create_layer("Layer 2")
        rect2 = Rectangle("Rect 2", 60, 900, 1860, 100)
        rect2.set_fill(WHITE.with_alpha(0.8))
        text2 = TextBlock(
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

        storyboard1 = Storyboard()
        storyboard1.append(RevealAnimation(rect1, 0, 2))
        storyboard1.append(RevealAnimation(text1, 1, 2))
        proj.document.storyboards.append(storyboard1)
```


## Contributing
Contributions are welcome and needed!

## License
This project is licensed under the MIT License.

## Support
If you need help or have any questions, 
please submit an issue on the GitHub repository's issue tracker.

For more information on vMix and GT titles, 
please visit the official vMix website.

- [vMix GT Designer manual](http://help.vmix.com/graphics/)