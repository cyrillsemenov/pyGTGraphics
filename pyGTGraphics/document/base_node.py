# trunk-ignore-all(bandit/B405)
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from typing import Any, List, Optional, Type


@dataclass
class Arg:
    """
    A class for defining metadata about attributes of nodes in an XML serialization system.

    >>> color_arg = Arg(attribute="color", type=str, default="red", optional=True)
    >>> color_arg.attribute
    'color'
    >>> color_arg.type
    <class 'str'>
    >>> color_arg.default
    'red'
    >>> color_arg.optional
    True
    >>> color_arg.ignore_if_none
    True

    >>> position_arg = Arg(attribute="position", type=float, optional=False, ignore_if_none=False)
    >>> position_arg.attribute
    'position'
    >>> position_arg.type
    <class 'float'>
    >>> position_arg.default is None
    True
    >>> position_arg.optional
    False
    >>> position_arg.ignore_if_none
    False
    """

    attribute: str
    type: Optional[Type] = None
    default: Any = None
    optional: bool = True
    ignore_if_none: bool = True


class Reference:
    def __init__(self, object: "Node", key: str = "name") -> None:
        self._object = object
        self._key = key

    def __repr__(self) -> str:
        return self._object[self._key]

    def __str__(self) -> str:
        return self.__repr__()


class Node:
    """
    Base class for creating XML node representations. Each Node subclass can define its
    XML tag, arguments (attributes), and children nodes.

    Subclasses should define _tag and _args class variables to specify the XML tag name
    and the attributes of the XML element, respectively.

    Example:
    >>> class ColorNode(
    ...     Node,
    ...     tag = "Color",
    ...     init_args = [Arg("value", str, optional=False)]
    ... ):
    ...     pass
    >>> color_node = ColorNode(value="red")
    >>> ET.tostring(color_node.to_xml(), xml_declaration=False, encoding='unicode')
    '<Color Value="red" />'
    """

    _tag: str = ...
    _args: List[Arg] = []

    def to_xml(self, parent: Optional[ET.Element] = None) -> ET.Element:
        """
        Serializes the node and its children to an XML Element.

        If a parent element is provided, the node is added as a SubElement to the parent.
        Otherwise, a new Element is created.

        Example:
        >>> root_node = Node()
        >>> xml_element = root_node.to_xml()
        >>> isinstance(xml_element, ET.Element)
        True
        """
        element = (
            ET.Element(self._tag)
            if parent is None
            else ET.SubElement(parent, self._tag)
        )
        for arg in self._args:
            if arg.ignore_if_none and self[arg.attribute] is None:
                continue
            attr_name = "".join(t.title() for t in arg.attribute.split("_"))
            # Handle case when attribute is node
            if isinstance(self[arg.attribute], Node):
                node_attrib = ET.SubElement(
                    element, "{tag}.{attr}".format(tag=self._tag, attr=attr_name)
                )
                self[arg.attribute].to_xml(node_attrib)
            # Attribute is iterable
            elif isinstance(
                self[arg.attribute],
                (
                    list,
                    tuple,
                    set,
                ),
            ):
                node_attrib = ET.SubElement(element, f"{self._tag}.{attr_name}")
                for c in self[arg.attribute]:
                    c.to_xml(node_attrib)
            # Default case
            else:
                attr = self[arg.attribute]
                element.set(attr_name, str(attr))
        for c in self.children:
            c.to_xml(element)
        return element

    def __init__(self, **kwargs):
        """
        Initializes a Node instance with specified attributes and optional children nodes.

        Attributes are provided as keyword arguments according to the definitions in _args.
        Children nodes are specified through the 'children' keyword argument as a list.

        The method validates required attributes and their types, raising a TypeError
        if validations fail.

        Example:
        >>> class ColorNode(
        ...     Node,
        ...     tag = "Color",
        ...     init_args = [Arg("value", str, optional=False)]
        ... ):
        ...     pass
        >>> node = Node()
        >>> node.append(ColorNode(value="blue"))
        >>> len(node.children)
        1
        """
        self.children: List[Node] = kwargs.pop("children", [])
        for a in self._args:
            k, v = a.attribute, kwargs.get(a.attribute, a.default)
            if not (a.optional or v is not None):
                raise TypeError(f"{self.__class__.__name__} takes {k} attribute")
            if v is not None and a.type and not isinstance(v, (a.type,)):
                raise TypeError(
                    f"{self.__class__.__name__}.{k} requires "
                    f"a '{a.type.__name__}' but received a '{type(v).__name__}'"
                )
            setattr(self, k, v)

    def append(self, *children: "Node"):
        """
        Adds one or more child nodes to this node.

        Example:
        >>> parent_node = Node()
        >>> child_node = Node()
        >>> parent_node.append(child_node)
        >>> len(parent_node.children)
        1
        """
        for c in children:
            self.children.append(c)

    def __init_subclass__(cls, **_kwargs) -> None:
        super().__init_subclass__()
        # Set tag
        cls._tag = _kwargs.get("tag", cls.__name__)
        # Inherit args from all the parents
        cls._args = []
        for parent in cls.__mro__[1:-1]:
            if not hasattr(parent, "_args"):
                continue
            cls._args.extend([a for a in parent._args if a not in cls._args])
        cls._args.extend(_kwargs.get("init_args", []))

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key: str, value) -> None:
        setattr(self, key, value)

    def keys(self):
        return [k.attribute for k in self._args if self[k.attribute] is not None]

    def items(self):
        return ((key, self[key]) for key in self.keys())

    def __iter__(self):
        return iter(self.keys())


if __name__ == "__main__":
    import doctest

    print(doctest.testmod())
