from uuid import uuid4

from rusty_tags import Div, HtmlString, Script
from rusty_tags.datastar import Signals

from .button import Button
from .utils import cn



def get_position_styles(side: str, align: str) -> str:
    """Generate positioning styles based on side and align"""
    styles = []
    
    # Basic positioning based on side
    if side == "bottom":
        styles.append("top-full mt-1")
    elif side == "top": 
        styles.append("bottom-full mb-1")
    elif side == "right":
        styles.append("left-full ml-1")
    elif side == "left":
        styles.append("right-full mr-1")

    # Alignment
    if side in ["top", "bottom"]:
        if align == "start":
            styles.append("left-0")
        elif align == "center":
            styles.append("left-1/2 -translate-x-1/2")
        elif align == "end":
            styles.append("right-0")
    else:  # left/right
        if align == "start":
            styles.append("top-0")
        elif align == "center":
            styles.append("top-1/2 -translate-y-1/2")
        elif align == "end":
            styles.append("bottom-0")

    return " ".join(styles)

def PopoverTrigger(*children, variant="default", cls="", **attrs) -> HtmlString:
    def create(signal):
        return Button(
            *children,
            id=f'{signal}-popover-trigger',
            type='button',
            aria_expanded='false',
            aria_controls=f'{signal}-popover-content',
                popovertarget=f'{signal}-popover-content',
            ref=f"{signal}Trigger",
            variant=variant,
            on_click=f"${signal}_open = !${signal}_open",
            cls=cn(f'[anchor-name:--{signal}]',cls),
            **attrs,
        )

    return create


def PopoverContent(*children, cls="", side="bottom", align="start", **attrs) -> HtmlString:
    def create_content(signal):
        return Div(
            *children,
            id=f'{signal}-popover-content',
            data_popover=True,
            popover=True,
            data_attr_aria_hidden=f"${signal}_open ? 'false' : 'true'",
            ref=f"{signal}Content",
            data_side=side,
            data_align=align,
            cls=cn("w-80", "[position-anchor:--{signal}]",get_position_styles(side, align), cls),
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
        id=f'{signal}-popover',
        cls=cn("popover inline-block",cls),
        signals=Signals({f"{signal}_open": False}),
        **attrs,
    )
