class Layout:
    _keys = ['x', 'y', 'width', 'height']

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        if key not in self._keys:
            return
        setattr(self, key, value)

    def keys(self):
        return self._keys


if __name__ == "__main__":
    a = Layout(1, 2, 3, 4)
    layout_dict = dict(**a)
    print(layout_dict)
