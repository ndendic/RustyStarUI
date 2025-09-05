from uuid import uuid4

from rusty_tags import Div, HtmlString, Script
from rusty_tags.datastar import Signals

from .button import Button
from .utils import cn


def PopoverTrigger(*children, variant="default", cls="", **attrs) -> HtmlString:
    def create(signal):
        return Button(
            *children,
            id=f'{signal}-popover-trigger',
            type='button',
            aria_expanded='false',
            aria_controls=f'{signal}-popover-content',
            ref=f"{signal}Trigger",
            variant=variant,
            on_click=f"${signal}_open = !${signal}_open",
            cls=cls,
            **attrs,
        )

    return create


def PopoverContent(*children, cls="", side="bottom", align="start", **attrs) -> HtmlString:
    def create_content(signal):
        return Div(
            *children,
            id=f'{signal}-popover-content',
            data_popover='',
            data_attr_aria_hidden=f"${signal}_open ? 'false' : 'true'",
            ref=f"{signal}Content",
            data_side=side,
            data_align=align,
            cls=cn("w-80",cls),
            **attrs,
        )

    return create_content

def Popover(*children, signal: str | None = None, cls="relative inline-block", **attrs) -> HtmlString:
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
        Script("document.dispatchEvent(new Event('basecoat:initialized'));"),
        # id=signal,
        id=f'{signal}-popover',
        cls=cn("popover",cls),
        signals=Signals({f"{signal}_open": False}),
        **attrs,
    )
