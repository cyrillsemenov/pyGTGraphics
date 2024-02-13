r"""
CenterAxis, Delay, Direction, Duration, Interpolation, Object, Reverse, Speed
'Storyboard': Animations, DataName, Type
    'Storyboard.Animations'
        'Bounce': Delay, Direction, Duration, Object
        'Expand': Delay, Direction, Duration, Interpolation, Object, Reverse
        'Fade': Delay, Duration, Interpolation, Object, Reverse
        'FillOffset': Direction, Object, Speed
        'Fly': Delay, Direction, Duration, Interpolation, Object, Reverse
        'Hidden': Delay, Duration, Object
        'ImageSequenceLoop': Object
        'None': Delay, Duration, Interpolation, Object, Reverse
        'Reveal': CenterAxis, Delay, Direction, Duration, Interpolation, Object, Reverse
        'Rotate': Delay, Direction, Duration, Interpolation, Object
        'RotateContinuous': Direction, Object, Speed
        'StrokeOffset': Direction, Object, Speed
        'Zoom': Delay, Duration, Interpolation, Object
        'ZoomFade': Delay, Duration, Interpolation, Object

>>> import xml.etree.ElementTree as ET
>>> storyboard = Storyboard.transition_in()
>>> storyboard.append(
...    AnimationBounce("Test"),
...    AnimationExpand("append"),
...    AnimationFade("function"),
... )
>>> storyboard.add_fill_offset("and dedicated one")
>>> ET.tostring(storyboard.to_xml(), xml_declaration=False, encoding='unicode')
'<Storyboard Type="TransitionIn"><Storyboard.Animations><Bounce Object="Test" /><Expand Object="append" /><Fade Object="function" /><FillOffset Object="and dedicated one" /></Storyboard.Animations></Storyboard>'

"""

from enum import Enum
from numbers import Real
from typing import Optional, Union

from base_node import Arg, Node, Reference


class AnimationInterpolation(Enum):
    LINEAR: str = "Linear"
    CUBE_EASE_IN: str = "CubicEasingIn"
    CUBE_EASE_OUT: str = "CubicEasingOut"
    CUBE_EASE_IN_OUT: str = "CubicEasingInOut"
    BOUNCE_IN: str = "BounceIn"
    BOUNCE_OUT: str = "BounceOut"


class AnimationDirection(Enum):
    TOP: str = "Top"
    DOWN: str = "Down"
    LEFT: str = "Left"
    RIGHT: str = "Right"


class AnimationCenterAxis(Enum):
    X: str = "X"
    Y: str = "Y"


class AnimationBase(
    Node,
    init_args=[
        Arg("object", type=Reference, optional=False),
        Arg("duration", type=Real),
        Arg("speed", type=Real),
        Arg("delay", type=Real),
        Arg("interpolation", type=AnimationInterpolation),
        Arg("direction", type=AnimationDirection),
        Arg("reverse", type=bool),
        Arg("center_axis", type=AnimationDirection),
    ],
):

    def __init__(
        self,
        object: Union[str, Node],
        duration: Optional[Real] = None,
        delay: Optional[Real] = None,
        speed: Optional[Real] = None,
        interpolation: Union[None, str, AnimationInterpolation] = None,
        direction: Union[None, str, AnimationDirection] = None,
        center_axis: Union[None, str, AnimationDirection] = None,
        reverse: Optional[bool] = None,
        **kwargs,
    ):
        if isinstance(object, Node):
            object = object.name
        if isinstance(interpolation, Enum):
            interpolation = interpolation.value
        if isinstance(direction, Enum):
            direction = direction.value
        if isinstance(center_axis, Enum):
            center_axis = center_axis.value
        kwargs.update(
            object=object,
            duration=duration,
            delay=delay,
            speed=speed,
            interpolation=interpolation,
            direction=direction,
            center_axis=center_axis,
            reverse=reverse,
        )
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        super().__init__(**kwargs)


class AnimationBounce(AnimationBase, tag="Bounce"):
    pass


class AnimationExpand(AnimationBase, tag="Expand"):
    pass


class AnimationFade(AnimationBase, tag="Fade"):
    pass


class AnimationFillOffset(AnimationBase, tag="FillOffset"):
    pass


class AnimationFly(AnimationBase, tag="Fly"):
    pass


class AnimationHidden(AnimationBase, tag="Hidden"):
    pass


class AnimationImageSequenceLoop(AnimationBase, tag="ImageSequenceLoop"):
    pass


class AnimationNone(AnimationBase, tag="None"):
    pass


class AnimationReveal(AnimationBase, tag="Reveal"):
    pass


class AnimationRotate(AnimationBase, tag="Rotate"):
    pass


class AnimationRotateContinuous(AnimationBase, tag="RotateContinuous"):
    pass


class AnimationStrokeOffset(AnimationBase, tag="StrokeOffset"):
    pass


class AnimationZoom(AnimationBase, tag="Zoom"):
    pass


class AnimationZoomFade(AnimationBase, tag="ZoomFade"):
    pass


class Storyboard(
    Node,
    init_args=[
        Arg("animations", type=list, default=[]),
        Arg("data_name", type=str),
        Arg("type", type=str, optional=False),
        Arg("name", type=str),
    ],
):
    r"""
    A class to represent a storyboard containing animations.

    ...

    >>> import xml.etree.ElementTree as ET
    >>> storyboard = Storyboard.transition_in()
    >>> storyboard.append(
    ...     AnimationBounce("Test"),
    ...     AnimationExpand("append"),
    ...     AnimationFade("function"),
    ... )
    >>> ET.tostring(storyboard.to_xml(), xml_declaration=False, encoding='unicode')
    '<Storyboard Type="TransitionIn"><Storyboard.Animations><Bounce Object="Test" /><Expand Object="append" /><Fade Object="function" /></Storyboard.Animations></Storyboard>'
    """

    _last_page_num: int = 0

    def append(self, *children: AnimationBase):
        """
        Appends given animation children to the storyboard.

        >>> storyboard = Storyboard(type="Demo")
        >>> storyboard.append(AnimationBounce("DemoObject"))
        >>> len(storyboard.animations)
        1
        """
        for c in children:
            self.animations.append(c)

    @classmethod
    def page(
        cls, *children: AnimationBase, page_num: Optional[int] = None
    ) -> "Storyboard":
        """
        Creates a page-type storyboard with given animations.

        >>> s = Storyboard.page(AnimationBounce("Page1"))
        >>> s.type
        'Page 0'
        >>> len(s.animations)
        1
        """
        if page_num is None or page_num == cls._last_page_num:
            page_num = cls._last_page_num
            cls._last_page_num += 1
        return Storyboard(type=f"Page {page_num}", animations=list(children))

    @classmethod
    def continious(cls, *children: AnimationBase) -> "Storyboard":
        """Continuous"""
        return Storyboard(type="Continious", animations=list(children))

    @classmethod
    def transition_in(cls, *children: AnimationBase) -> "Storyboard":
        """TransitionIn"""
        return Storyboard(type="TransitionIn", animations=list(children))

    @classmethod
    def transition_out(cls, *children: AnimationBase) -> "Storyboard":
        """TransitionOut"""
        return Storyboard(type="TransitionOut", animations=list(children))

    @classmethod
    def data_change_in(cls, data_name: str, *children: AnimationBase) -> "Storyboard":
        """DataChangeIn"""
        # DataName="Object_Name.Attribute"
        return Storyboard(
            type="DataChangeIn", data_name=data_name, animations=list(children)
        )

    @classmethod
    def data_change_out(cls, data_name: str, *children: AnimationBase) -> "Storyboard":
        """DataChangeOut"""
        # DataName="Object_Name.Attribute"
        return Storyboard(
            type="DataChangeOut", data_name=data_name, animations=list(children)
        )

    def add_bounce(
        self,
        object: Node,
        duration: Optional[Real] = None,
        delay: Optional[Real] = None,
        speed: Optional[Real] = None,
        interpolation: Union[str, AnimationInterpolation, None] = None,
        direction: Union[str, AnimationDirection, None] = None,
        center_axis: Union[str, AnimationCenterAxis, None] = None,
        reverse: Optional[bool] = None,
    ) -> None:
        self.append(
            AnimationBounce(
                Reference(object),
                duration,
                delay,
                speed,
                interpolation,
                direction,
                center_axis,
                reverse,
            )
        )

    def add_expand(
        self,
        object: Node,
        duration: Optional[Real] = None,
        delay: Optional[Real] = None,
        speed: Optional[Real] = None,
        interpolation: Union[str, AnimationInterpolation, None] = None,
        direction: Union[str, AnimationDirection, None] = None,
        center_axis: Union[str, AnimationCenterAxis, None] = None,
        reverse: Optional[bool] = None,
    ) -> None:
        self.append(
            AnimationExpand(
                Reference(object),
                duration,
                delay,
                speed,
                interpolation,
                direction,
                center_axis,
                reverse,
            )
        )

    def add_fade(
        self,
        object: Node,
        duration: Optional[Real] = None,
        delay: Optional[Real] = None,
        speed: Optional[Real] = None,
        interpolation: Union[str, AnimationInterpolation, None] = None,
        direction: Union[str, AnimationDirection, None] = None,
        center_axis: Union[str, AnimationCenterAxis, None] = None,
        reverse: Optional[bool] = None,
    ) -> None:
        self.append(
            AnimationFade(
                Reference(object),
                duration,
                delay,
                speed,
                interpolation,
                direction,
                center_axis,
                reverse,
            )
        )

    def add_fill_offset(
        self,
        object: Node,
        duration: Optional[Real] = None,
        delay: Optional[Real] = None,
        speed: Optional[Real] = None,
        interpolation: Union[str, AnimationInterpolation, None] = None,
        direction: Union[str, AnimationDirection, None] = None,
        center_axis: Union[str, AnimationCenterAxis, None] = None,
        reverse: Optional[bool] = None,
    ) -> None:
        self.append(
            AnimationFillOffset(
                Reference(object),
                duration,
                delay,
                speed,
                interpolation,
                direction,
                center_axis,
                reverse,
            )
        )

    def add_fly(
        self,
        object: Node,
        duration: Optional[Real] = None,
        delay: Optional[Real] = None,
        speed: Optional[Real] = None,
        interpolation: Union[str, AnimationInterpolation, None] = None,
        direction: Union[str, AnimationDirection, None] = None,
        center_axis: Union[str, AnimationCenterAxis, None] = None,
        reverse: Optional[bool] = None,
    ) -> None:
        self.append(
            AnimationFly(
                Reference(object),
                duration,
                delay,
                speed,
                interpolation,
                direction,
                center_axis,
                reverse,
            )
        )

    def add_hidden(
        self,
        object: Node,
        duration: Optional[Real] = None,
        delay: Optional[Real] = None,
        speed: Optional[Real] = None,
        interpolation: Union[str, AnimationInterpolation, None] = None,
        direction: Union[str, AnimationDirection, None] = None,
        center_axis: Union[str, AnimationCenterAxis, None] = None,
        reverse: Optional[bool] = None,
    ) -> None:
        self.append(
            AnimationHidden(
                Reference(object),
                duration,
                delay,
                speed,
                interpolation,
                direction,
                center_axis,
                reverse,
            )
        )

    def add_image_sequence_loop(
        self,
        object: Node,
        duration: Optional[Real] = None,
        delay: Optional[Real] = None,
        speed: Optional[Real] = None,
        interpolation: Union[str, AnimationInterpolation, None] = None,
        direction: Union[str, AnimationDirection, None] = None,
        center_axis: Union[str, AnimationCenterAxis, None] = None,
        reverse: Optional[bool] = None,
    ) -> None:
        self.append(
            AnimationImageSequenceLoop(
                Reference(object),
                duration,
                delay,
                speed,
                interpolation,
                direction,
                center_axis,
                reverse,
            )
        )

    def add_none(
        self,
        object: Node,
        duration: Optional[Real] = None,
        delay: Optional[Real] = None,
        speed: Optional[Real] = None,
        interpolation: Union[str, AnimationInterpolation, None] = None,
        direction: Union[str, AnimationDirection, None] = None,
        center_axis: Union[str, AnimationCenterAxis, None] = None,
        reverse: Optional[bool] = None,
    ) -> None:
        self.append(
            AnimationNone(
                Reference(object),
                duration,
                delay,
                speed,
                interpolation,
                direction,
                center_axis,
                reverse,
            )
        )

    def add_reveal(
        self,
        object: Node,
        duration: Optional[Real] = None,
        delay: Optional[Real] = None,
        speed: Optional[Real] = None,
        interpolation: Union[str, AnimationInterpolation, None] = None,
        direction: Union[str, AnimationDirection, None] = None,
        center_axis: Union[str, AnimationCenterAxis, None] = None,
        reverse: Optional[bool] = None,
    ) -> None:
        self.append(
            AnimationReveal(
                Reference(object),
                duration,
                delay,
                speed,
                interpolation,
                direction,
                center_axis,
                reverse,
            )
        )

    def add_rotate(
        self,
        object: Node,
        duration: Optional[Real] = None,
        delay: Optional[Real] = None,
        speed: Optional[Real] = None,
        interpolation: Union[str, AnimationInterpolation, None] = None,
        direction: Union[str, AnimationDirection, None] = None,
        center_axis: Union[str, AnimationCenterAxis, None] = None,
        reverse: Optional[bool] = None,
    ) -> None:
        self.append(
            AnimationRotate(
                Reference(object),
                duration,
                delay,
                speed,
                interpolation,
                direction,
                center_axis,
                reverse,
            )
        )

    def add_rotate_continuous(
        self,
        object: Node,
        duration: Optional[Real] = None,
        delay: Optional[Real] = None,
        speed: Optional[Real] = None,
        interpolation: Union[str, AnimationInterpolation, None] = None,
        direction: Union[str, AnimationDirection, None] = None,
        center_axis: Union[str, AnimationCenterAxis, None] = None,
        reverse: Optional[bool] = None,
    ) -> None:
        self.append(
            AnimationRotateContinuous(
                Reference(object),
                duration,
                delay,
                speed,
                interpolation,
                direction,
                center_axis,
                reverse,
            )
        )

    def add_stroke_offset(
        self,
        object: Node,
        duration: Optional[Real] = None,
        delay: Optional[Real] = None,
        speed: Optional[Real] = None,
        interpolation: Union[str, AnimationInterpolation, None] = None,
        direction: Union[str, AnimationDirection, None] = None,
        center_axis: Union[str, AnimationCenterAxis, None] = None,
        reverse: Optional[bool] = None,
    ) -> None:
        self.append(
            AnimationStrokeOffset(
                Reference(object),
                duration,
                delay,
                speed,
                interpolation,
                direction,
                center_axis,
                reverse,
            )
        )

    def add_zoom(
        self,
        object: Node,
        duration: Optional[Real] = None,
        delay: Optional[Real] = None,
        speed: Optional[Real] = None,
        interpolation: Union[str, AnimationInterpolation, None] = None,
        direction: Union[str, AnimationDirection, None] = None,
        center_axis: Union[str, AnimationCenterAxis, None] = None,
        reverse: Optional[bool] = None,
    ) -> None:
        self.append(
            AnimationZoom(
                Reference(object),
                duration,
                delay,
                speed,
                interpolation,
                direction,
                center_axis,
                reverse,
            )
        )

    def add_zoom_fade(
        self,
        object: Node,
        duration: Optional[Real] = None,
        delay: Optional[Real] = None,
        speed: Optional[Real] = None,
        interpolation: Union[str, AnimationInterpolation, None] = None,
        direction: Union[str, AnimationDirection, None] = None,
        center_axis: Union[str, AnimationCenterAxis, None] = None,
        reverse: Optional[bool] = None,
    ) -> None:
        self.append(
            AnimationZoomFade(
                Reference(object),
                duration,
                delay,
                speed,
                interpolation,
                direction,
                center_axis,
                reverse,
            )
        )


if __name__ == "__main__":
    import doctest

    print(doctest.testmod())
