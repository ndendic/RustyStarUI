from uuid import uuid4

from rusty_tags import Div, HtmlString

from .button import Button
from .utils import cn


def PopoverTrigger(*children, variant="default", cls="", **attrs):
    def create(signal):
        return Button(
            *children,
            id=f'{signal}-popover-trigger',
            type='button',
            aria_expanded='false',
            aria_controls=f'{signal}-popover-content',
            ref=f"{signal}Trigger",
            variant=variant,
            cls=cls,
            **attrs,
        )

    return create


def PopoverContent(*children, cls="", side="bottom", align="start", **attrs):
    def create_content(signal):
        return Div(
            *children,
            id=f'{signal}-popover-content',
            data_popover='',
            aria_hidden='true',
            ref=f"{signal}Content",
            data_side=side,
            data_align=align,
            cls=cn("w-80",cls),
            **attrs,
        )

    return create_content

def Popover(*children, signal: str | None = None, cls="relative inline-block", **attrs):
    id = signal or uuid4().hex[:8]
    signal = f"popover-{id}"
    processed_children = []
    for c in children:
        if callable(c):
            processed_children.append(c(signal))
        else:
            processed_children.append(c)
    return Div(
        *processed_children,
        # id=signal,
        id=f'{signal}-popover',
        cls=cn("popover",cls),
        **attrs,
    )
