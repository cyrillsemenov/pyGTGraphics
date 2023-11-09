"""
Description: This module defines the Colour class which represents RGBA colours
             and provides methods for colour manipulation.
Author: Cyrill Semenov
Date Created: 2023/11/09
Date Modified: 2023/11/09
Version: 1.0
License: MIT License
"""

class Colour:
    def __init__(self, r: float, g: float, b: float, a: float) -> None:
        """
        Initialize a new Colour instance.

        Parameters:
        - r (float): Red component, range 0.0 to 1.0
        - g (float): Green component, range 0.0 to 1.0
        - b (float): Blue component, range 0.0 to 1.0
        - a (float): Alpha (transparency) component, range 0.0 to 1.0
        """
        self._r = min(max(r, .0), 1.)
        self._g = min(max(g, .0), 1.)
        self._b = min(max(b, .0), 1.)
        self._a = min(max(a, .0), 1.)

    @staticmethod
    def _format(_r: float, _g: float, _b: float, _a: float) -> str:
        """
        Format the colour components into a hexadecimal string.

        Parameters:
        - _r (float): Red component, range 0.0 to 1.0
        - _g (float): Green component, range 0.0 to 1.0
        - _b (float): Blue component, range 0.0 to 1.0
        - _a (float): Alpha (transparency) component, range 0.0 to 1.0

        Returns:
        - str: The colour as a hexadecimal string.
        """
        r = hex(int(255 * _r))[2:].zfill(2)
        g = hex(int(255 * _g))[2:].zfill(2)
        b = hex(int(255 * _b))[2:].zfill(2)
        a = hex(int(255 * _a))[2:].zfill(2)
        return f"#{a}{r}{g}{b}".upper()

    @classmethod
    def from_hex(cls, hex_string: str) -> 'Colour':
        """
        Create a Colour instance from an RGB or RGBA hexadecimal string.

        Parameters:
        - hex_string (str): The colour as an RGB ('#RRGGBB') or RGBA ('#RRGGBBAA') hexadecimal string,
          with or without a leading '#'.

        Returns:
        - Colour: A Colour instance corresponding to the given hexadecimal string.

        Raises:
        - ValueError: If the hex_string is not in the correct format.
        """
        hex_string = hex_string.strip("#")

        if len(hex_string) not in (6, 8):
            raise ValueError("Invalid color format, must be 6 or 8 hexadecimal characters")

        r, g, b = (int(hex_string[i:i + 2], 16) / 255 for i in (0, 2, 4))
        a = 1.0

        if len(hex_string) == 8:
            a = int(hex_string[6:8], 16) / 255

        return cls(r, g, b, a)

    def with_alpha(self, alpha: float) -> str:
        """
        Return the colour as a hexadecimal string with the specified alpha value.

        Parameters:
        - alpha (float): The new alpha (transparency) value, range 0.0 to 1.0.

        Returns:
        - str: The colour as a hexadecimal string with the specified alpha value.
        """
        return self._format(self._r, self._g, self._b, alpha)

    def __str__(self):
        return self._format(self._r, self._g, self._b, self._a)

    def __repr__(self):
        return self.__str__()

