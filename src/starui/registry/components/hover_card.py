from typing import Literal
from uuid import uuid4

from rusty_tags import Div, HtmlString

from .button import Button
from .utils import cn


def togglePopover(element_id: str, delay: int, action: Literal["toggle", "show", "hide"] = "toggle"):
    command = f"clearTimeout(window.{element_id}Timer); window.{element_id}Timer = setTimeout(() => {{ document.getElementById('{element_id}').{action}Popover(); }}, {delay});"
    print(command)
    return command

def HoverCardTrigger(*children,
                    popovertarget: str,
                    id: str | None = None,
                    hover_delay: int = 700,
                    hide_delay: int = 300,
                    variant="default", cls="",
                    **attrs) -> HtmlString:
    id = id or uuid4().hex[:8]
    return Div(
        *children,
        id=f'{id}',
        aria_controls=popovertarget,
        popovertarget=popovertarget,
        onmouseenter=togglePopover(popovertarget, hover_delay, "show"),
        onmouseleave=togglePopover(popovertarget, hide_delay, "hide"),
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

def HoverCard(*children,
            id: str,
            anchor: str | None = None,
            cls="w-80 p-4",
            position: PopoverPosition = "bottom-center",
            hover_delay: int = 700,
            hide_delay: int = 300,
            **attrs) -> HtmlString:
    side, align = position.split("-")
    return Div(
            *children,
            id=id,
            data_popover=True,
            popover="hint",
            ref=f"{id}Content",
            data_side=side,
            data_align=align,
            cls=cls,
            onmouseenter=togglePopover(id, hide_delay, "show"),
            onmouseleave=togglePopover(id, hide_delay, "hide"),
            style=f"position-anchor: --{anchor};" if anchor else None,
            **attrs,
        )
