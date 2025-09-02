from uuid import uuid4

from rusty_tags import Div, HtmlString

from .button import Button
from .utils import cn


def PopoverTrigger(*children, variant="default", cls="", **attrs):
    def create(signal):
        return Button(
            *children,
            ref=f"{signal}Trigger",
            variant=variant,
            aria_expanded="false",
            aria_controls=f"{signal}-popover",
            id=f"{signal}-trigger",
            cls=cls,
            **attrs,
        )

    return create


def PopoverContent(*children, cls="", side="bottom", align="center", **attrs):
    def create_content(signal):
        return Div(
            *children,
            ref=f"{signal}Content",
            data_side=side,
            data_align=align,
            popover="auto",
            data_popover=True,
            aria_hidden="true",
            id=f"{signal}-popover",
            cls=cn("w-80",cls),
            **attrs,
        )

    return create_content

def Popover(*children, signal: str | None = None, cls="relative inline-block", **attrs):
    id = signal or uuid4().hex[:8]
    signal = f"popover_{id}"
    processed_children = []
    for c in children:
        if callable(c):
            processed_children.append(c(signal))
        else:
            processed_children.append(c)
    return Div(
        *processed_children,
        cls=cn("popover",cls),
        **attrs,
    )
