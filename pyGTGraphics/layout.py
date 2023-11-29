from numbers import Number
from typing import List, Optional


class Layout(dict):
    """
    Represents a rectangular layout area defined by its position and size.

    Attributes:
        x (int): The x-coordinate of the top-left corner of the layout.
        y (int): The y-coordinate of the top-left corner of the layout.
        width (int): The width of the layout.
        height (int): The height of the layout.
    """

    _keys = ['x', 'y', 'width', 'height']

    def __init__(self, x: Number, y: Number, width: Number, height: Number, *args, **kwargs) -> None:
        """
        Initializes a new Layout instance with specified position and dimensions.

        Args:
            x (int): The x-coordinate of the top-left corner of the layout.
            y (int): The y-coordinate of the top-left corner of the layout.
            width (int): The width of the layout.
            height (int): The height of the layout.
        """
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def __getitem__(self, key):
        """
        Allows retrieval of layout properties via subscript notation.

        Args:
            key (str): The property name (e.g., 'x', 'y', 'width', 'height').

        Returns:
            The value of the requested property.
        """
        return getattr(self, key)

    def __setitem__(self, key: str, value: Number) -> None:
        """
        Allows setting of layout properties via subscript notation.

        Args:
            key (str): The property name.
            value: The new value to be set for the given property.
        """
        if key not in self._keys:
            return
        setattr(self, key, value)

    def keys(self) -> List[str]:
        """
        Returns the list of property names that can be accessed via subscript notation.

        Returns:
            List[str]: A list of property names ('x', 'y', 'width', 'height').
        """
        return self._keys

    def items(self):
        """
        Returns key-value pairs of layout properties.

        Returns:
            Iterator of tuples: An iterator over key-value pairs of layout properties.
        """
        return zip(self._keys, (self[k] for k in self._keys))

    def __iter__(self):
        """
        Allows iteration over layout property names.

        Yields:
            str: Names of the layout properties.
        """
        for k, v in self.items():
            yield k

    def take_from_left(self, pixels: Number) -> 'Layout':
        """
        Slices a portion of the layout from the left side and adjusts the layout.

        Args:
            pixels (Number): The width of the portion to be sliced from the left.

        Returns:
            Layout: A new Layout instance representing the sliced portion.
        """
        result = Layout(self.x, self.y, pixels, self.height)
        self.x += pixels
        self.width -= pixels
        return result

    def take_from_top(self, pixels: Number) -> 'Layout':
        """
        Slices a portion of the layout from the top side and adjusts the layout.

        Args:
            pixels (Number): The height of the portion to be sliced from the top.

        Returns:
            Layout: A new Layout instance representing the sliced portion.
        """
        result = Layout(self.x, self.y, self.width, pixels)
        self.y += pixels
        self.height -= pixels
        return result

    def take_from_right(self, pixels: Number) -> 'Layout':
        """
        Slices a portion of the layout from the right side and adjusts the layout.

        Args:
            pixels (Number): The width of the portion to be sliced from the right.

        Returns:
            Layout: A new Layout instance representing the sliced portion.
        """
        result = Layout(self.x + self.width - pixels, self.y, pixels, self.height)
        self.width -= pixels
        return result

    def take_from_bottom(self, pixels: Number) -> 'Layout':
        """
        Slices a portion of the layout from the bottom side and adjusts the layout.

        Args:
            pixels (Number): The height of the portion to be sliced from the bottom.

        Returns:
            Layout: A new Layout instance representing the sliced portion.
        """
        result = Layout(self.x, self.y + self.height - pixels, self.width, pixels)
        self.height -= pixels
        return result

    def pad(
            self,
            left: Number, top: Optional[Number] = None,
            right: Optional[Number] = None, bottom: Optional[Number] = None
    ) -> 'Layout':
        """
        Pads the layout by reducing its size from specified sides.

        Args:
            left (Number): Amount to pad from the left side.
            top (Optional[Number]): Amount to pad from the top. Defaults to left if not provided.
            right (Optional[Number]): Amount to pad from the right. Defaults to left if not provided.
            bottom (Optional[Number]): Amount to pad from the bottom. Defaults to top if not provided.

        Returns:
            Layout: The layout itself after being padded.
        """
        if top is None:
            top = left
        if bottom is None:
            bottom = top
        if right is None:
            right = left
        self.take_from_left(left)
        self.take_from_top(top)
        self.take_from_right(right)
        self.take_from_bottom(bottom)
        return self


if __name__ == "__main__":
    def print_layout(layouts, total_width, total_height):
        """
        Prints a textual representation of the given layouts on a grid.

        Args:
            layouts (dict): A dictionary of layouts labeled by letters.
            total_width (int): The total width of the grid to be printed.
            total_height (int): The total height of the grid to be printed.
        """
        grid = [[' ' for _ in range(total_width)] for _ in range(total_height)]
        for label, layout in layouts.items():
            for i in range(layout.y, layout.y + layout.height):
                for j in range(layout.x, layout.x + layout.width):
                    grid[i][j] = label
        for row in grid:
            print(''.join(row))
        print("")


    # Demo code to showcase the functionality of Layout class and print_layout function
    _total_width, _total_height = 6, 6
    a = Layout(0, 0, _total_width, _total_height)
    _layouts = {'A': a}
    print_layout(_layouts, _total_width, _total_height)

    b = a.take_from_left(2)
    _layouts['B'] = b
    print_layout(_layouts, _total_width, _total_height)

    c = a.take_from_top(2)
    _layouts['C'] = c
    print_layout(_layouts, _total_width, _total_height)

    d = a.take_from_right(2)
    _layouts['D'] = d
    print_layout(_layouts, _total_width, _total_height)

    e = a.take_from_bottom(2)
    _layouts['E'] = e
    print_layout(_layouts, _total_width, _total_height)
