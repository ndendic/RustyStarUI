from typing import Literal
from uuid import uuid4

from rusty_tags import Div, HtmlString

from .button import Button
from .utils import cn


def PopoverTrigger(*children,
                    popovertarget: str,
                    id: str | None = None,
                    variant="default", cls="",
                    **attrs) -> HtmlString:
    id = id or uuid4().hex[:8]
    return Button(
        *children,
        id=f'{id}',
        type='button',
        aria_controls=popovertarget,
        popovertarget=popovertarget,
        ref=f"{id}Trigger",
        variant=variant,
        cls=cn(cls),
        style=f"anchor-name: --{id};",
        **attrs,
    )

PopoverPosition = Literal[
    "top-left", "top-center", "top-right",
    "bottom-left", "bottom-center", "bottom-right",
    "left-start", "left-center", "left-end",
    "right-start", "right-center", "right-end"
]

def Popover(*children,
            id: str,
            anchor: str | None = None,
            cls="w-80 p-4",
            position: PopoverPosition = "bottom-center",
            **attrs) -> HtmlString:
    side, align = position.split("-")
    return Div(
            *children,
            id=id,
            data_popover=True,
            popover=True,
            ref=f"{id}Content",
            data_side=side,
            data_align=align,
            cls=cls,
            style=f"position-anchor: --{anchor};" if anchor else None,
            **attrs,
        )

