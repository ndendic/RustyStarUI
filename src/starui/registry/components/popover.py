from uuid import uuid4

from rusty_tags import Div, HtmlString, Script
from rusty_tags.datastar import Signals

from .button import Button
from .utils import cn


def get_anchor_styles(side: str, align: str) -> str:
    """Generate CSS anchor positioning styles based on side and align"""
    styles = []
    
    # Position based on side
    if side == "bottom":
        styles.extend(["[top:anchor(bottom)]", "[left:anchor(left)]"])
    elif side == "top":
        styles.extend(["[bottom:anchor(top)]", "[left:anchor(left)]"])
    elif side == "right":
        styles.extend(["[top:anchor(top)]", "[left:anchor(right)]"])
    elif side == "left":
        styles.extend(["[top:anchor(top)]", "[right:anchor(left)]"])
    
    # Alignment adjustments
    if side in ["top", "bottom"]:
        if align == "center":
            styles.append("[left:anchor(center)] [translate:-50%_0]")
        elif align == "end":
            styles.append("[right:anchor(right)]")
        # start is default, no additional styles needed
    else:  # left/right sides
        if align == "center":
            styles.append("[top:anchor(center)] [translate:0_-50%]")
        elif align == "end":
            styles.append("[bottom:anchor(bottom)]")
        # start is default, no additional styles needed
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
            ref=f"{signal}Content",
            data_side=side,
            data_align=align,
            cls=cn("w-80", "[position-anchor:--{signal}]", cls),
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
