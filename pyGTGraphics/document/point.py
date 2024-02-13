from numbers import Real
from typing import Optional


class Triplet:
    """
    Represents a three-dimensional coordinate or vector.

    Attributes:
        x (Real): The x-coordinate or first dimension value.
        y (Real): The y-coordinate or second dimension value.
        z (Real): The z-coordinate or third dimension value, defaulting to 0.
    """

    _template_string = "{x},{y},{z}"

    def __init__(self, x: Real, y: Real, z: Real = 0) -> None:
        self._x = x
        self._y = y
        self._z = z

    def __repr__(self) -> str:
        return self._template_string.format(x=self._x, y=self._y, z=self._z)

    def __str__(self) -> str:
        return self.__repr__()

    @property
    def x(self) -> Real:
        return self._x

    @x.setter
    def x(self, val: Real):
        self._x = val

    @property
    def y(self) -> Real:
        return self._y

    @y.setter
    def y(self, val: Real):
        self._y = val

    @property
    def z(self) -> Real:
        return self._z

    @z.setter
    def z(self, val: Real):
        self._z = val


class Quadruptet:
    """
    Represents a quadruplet of values, typically used for defining margins, padding, feathering, or ranges.

    Attributes:
        top (Real): The top value.
        right (Real): The right value. Defaults to the top value if not specified.
        bottom (Real): The bottom value. Defaults to the top value if not specified.
        left (Real): The left value. Defaults to the right value if not specified.
    """

    _template_string = "{top},{right},{bottom},{left}"

    def __init__(
        self,
        top: Real,
        right: Optional[Real] = None,
        bottom: Optional[Real] = None,
        left: Optional[Real] = None,
    ) -> None:
        self._top = top
        self._right = top if right is None else right
        self._bottom = top if bottom is None else bottom
        self._left = right if left is None else left

    def __repr__(self) -> str:
        return self._template_string.format(
            left=self._left, top=self._top, right=self._right, bottom=self._bottom
        )

    def __str__(self) -> str:
        return self.__repr__()

    @property
    def top(self) -> Real:
        return self._top

    @top.setter
    def top(self, val: Real):
        self._top = val

    @property
    def right(self) -> Real:
        return self._right

    @right.setter
    def right(self, val: Real):
        self._right = val

    @property
    def bottom(self) -> Real:
        return self._bottom

    @bottom.setter
    def bottom(self, val: Real):
        self._bottom = val

    @property
    def left(self) -> Real:
        return self._left

    @left.setter
    def left(self, val: Real):
        self._left = val


class Dimensions(Triplet):
    """
    Represents the dimensions of an object.
    """

    @classmethod
    def fill(cls, aspect: float):
        # TODO: Write some layput funcs
        def layout_function(ctx):
            """Get context width and height and set in to object"""

        return layout_function

    @classmethod
    def fit(cls, aspect: float):
        # TODO: Write some layput funcs
        def layout_function(ctx):
            """Get context width and height and fit object to it"""

        return layout_function

    def __init__(self, width: Real, height: Real, depth: Real = 0) -> None:
        self._x = width
        self._y = height
        self._z = depth

    @property
    def width(self) -> Real:
        return self._x

    @width.setter
    def width(self, val: Real):
        self._x = val

    @property
    def height(self) -> Real:
        return self._y

    @height.setter
    def height(self, val: Real):
        self._y = val

    @property
    def depth(self) -> Real:
        return self._z

    @depth.setter
    def depth(self, val: Real):
        self._z = val


class Location(Triplet):
    """
    Represents the location of an object.
    """

    @classmethod
    def center(cls):
        # TODO: Write some layput funcs
        def layout_function(ctx):
            """Find context center, having in mind object Dimensions"""

        return layout_function


class Rotate(Triplet):
    """
    Represents rotation angles around the x, y, and z axes.
    """


class Padding(Quadruptet):
    """
    Represents padding around an object, defined by top, right, bottom, and left values.
    """


class Margin(Quadruptet):
    """
    Represents margins around an object, similar to padding but for external spacing.
    """


class Feather(Quadruptet):
    """
    Represents feathering parameters around a crop area, defined by top, right, bottom, and left values.
    """


class Range(Quadruptet):
    """
    Represents a range of values for cropping an image, defined by top, right, bottom, and left coordinates.
    """
