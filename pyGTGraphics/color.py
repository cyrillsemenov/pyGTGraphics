from random import random


class ColorMeta(type):
    """
    A metaclass for creating Color instances with predefined color presets.

    Attributes:
        presets (dict): A dictionary of predefined color presets. Each key is a color name
                        (e.g., 'red', 'green') and its value is a tuple representing
                        the color in RGBA format.

    Methods:
        __getattr__(cls, name: str) -> Any: A class method that enables accessing
                                           predefined colors as class attributes.
    """

    presets = dict(
        red=(1, 0, 0),
        green=(0, 1, 0),
        blue=(1, 0, 0),
        white=(1, 1, 1),
        black=(0, 0, 0),
        transparent_white=(1, 1, 1, 0),
        transparent_black=(0, 0, 0, 0),
        lime=(0, 1, 0),
        salmon=(0.98, 0.5, 0.45),
        cyan=(0, 1, 1),
        magenta=(1, 0, 1),
        yellow=(1, 1, 0),
        navy=(0, 0, 0.5),
        olive=(0.5, 0.5, 0),
        teal=(0, 0.5, 0.5),
        maroon=(0.5, 0, 0),
        purple=(0.5, 0, 0.5),
        gray=(0.5, 0.5, 0.5),
        silver=(0.75, 0.75, 0.75),
        orange=(1, 0.65, 0),
        brown=(0.65, 0.16, 0.16),
        pink=(1, 0.75, 0.8),
        gold=(1, 0.84, 0),
    )

    def __getattr__(cls, __name: str) -> "Color":
        """
        Allows access to predefined color presets as class attributes.

        Args:
            name (str): The name of the color preset to access.

        Returns:
            A new instance of the class with the specified color preset.

        Raises:
            AttributeError: If the specified color name is not a predefined preset.
        """
        if __name in cls.presets:
            return cls(*cls.presets[__name])
        raise AttributeError("%r object has no attribute %r" % (cls.__name__, __name))


class Color(metaclass=ColorMeta):
    """
    Color class for creating and manipulating colors.

    Attributes:
        r (float): The red component of the color.
        g (float): The green component of the color.
        b (float): The blue component of the color.
        a (float): The alpha (transparency) component of the color.
        string_template (str): A template string for representing the color as a string.

    Methods:
        from_hex(hex: str, brga: bool = False): Creates a Color instance from a hexadecimal string.
        from_int(r: int, g: int, b: int, a: int = 255): Creates a Color instance from integer values.
    """

    string_template: str = "#{b:02X}{g:02X}{r:02X}{a:02X}"

    def __init__(self, r: float, g: float, b: float, a: float = 1.0) -> None:
        self.r: float = r
        self.g: float = g
        self.b: float = b
        self.a: float = a

    def __iter__(self):
        iters = dict(
            r=self.r,
            g=self.g,
            b=self.b,
            a=self.a,
        )
        for k, v in iters.items():
            yield k, v

    def __repr__(self) -> str:
        return self.string_template.format(**{k: int(v * 255) for k, v in self})

    def __str__(self) -> str:
        return self.__repr__()

    @classmethod
    def from_hex(cls, hex: str, brga: bool = False) -> "Color":
        """
        Creates a Color instance from a hexadecimal string.

        Args:
            hex (str): The hexadecimal string representing the color.
            brga (bool, optional): If True, treats the input as BGRA. Defaults to False.

        Returns:
            Color: The created Color instance.
        """
        hex = hex.lstrip("#")
        r, g, b, a = (
            int(hex[:2], 16) / 255,
            int(hex[2:4], 16) / 255,
            int(hex[4:6], 16) / 255,
            int(hex[6:] or "ff", 16) / 255,
        )
        if brga:
            r, b = b, r
        new_color = cls(r, g, b, a)
        return new_color

    @classmethod
    def from_int(cls, r: int, g: int, b: int, a: int = 255) -> "Color":
        """
        Creates a Color instance from a 8-bit integer values.

        Args:
            r (float): The 8-bit (0-255) red component of the color.
            g (float): The 8-bit (0-255) green component of the color.
            b (float): The 8-bit (0-255) blue component of the color.
            a (float, optional): The 8-bit (0-255) alpha (transparency) component of the color.  Defaults to 255.

        Returns:
            Color: The created Color instance.
        """
        return cls(r / 255, g / 255, b / 255, a / 255)

    @classmethod
    def random_color(cls) -> "Color":
        """
        Generates a random Color. Useful for testing purporses.

        Returns:
            Color: The created Color instance.
        """
        # trunk-ignore(bandit/B311)
        return cls(random(), random(), random())

    def with_alpha(self, a: float) -> "Color":
        return Color(**dict(self, a=a))


if __name__ == "__main__":
    pass
