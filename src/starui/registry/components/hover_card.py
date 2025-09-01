from typing import Literal
from uuid import uuid4

from rusty_tags import Div, HtmlString
from rusty_tags.datastar import Signals

from .utils import cn


def HoverCard(
    *children,
    signal: str | None = None,
    default_open: bool = False,
    cls: str = "",
    **attrs,
):
    signal = signal or f"hover_card_{uuid4().hex[:8]}"
    return Div(
        *children,
        signals=Signals({f"{signal}_open": default_open}),
        cls=cn("relative inline-block", cls),
        **attrs,
    )


def HoverCardTrigger(
    *children,
    signal: str | None = None,
    hover_delay: int = 700,
    hide_delay: int = 300,
    cls: str = "",
    **attrs,
):
    signal = signal or "hover_card"

    return Div(
        *children,
        ref=f"{signal}Trigger",
        on_mouseenter=f"""
            clearTimeout(window.hoverTimer_{signal});
            window.hoverTimer_{signal} = setTimeout(() => {{
                ${signal}_open = true;
            }}, {hover_delay});
        """,
        on_mouseleave=f"""
            clearTimeout(window.hoverTimer_{signal});
            window.hoverTimer_{signal} = setTimeout(() => {{
                ${signal}_open = false;
            }}, {hide_delay});
        """,
        aria_expanded=f"${signal}_open",
        aria_haspopup="dialog",
        aria_describedby=f"{signal}-content",
        cls=cn("inline-block cursor-pointer", cls),
        id=f"{signal}-trigger",
        **attrs,
    )


def HoverCardContent(
    *children,
    signal: str | None = None,
    side: Literal["top", "right", "bottom", "left"] = "bottom",
    align: Literal["start", "center", "end"] = "center",
    hide_delay: int = 300,
    cls: str = "",
    **attrs,
):
    signal = signal or "hover_card"
    placement = f"{side}-{align}" if align != "center" else side

    return Div(
        *children,
        ref=f"{signal}Content",
        show=f"${signal}_open",
        position={
            "anchor": f"{signal}-trigger",
            "placement": placement,
            "offset": 8,
            "flip": True,
            "shift": True,
            "hide": True,
        },
        on_mouseenter=f"clearTimeout(window.hoverTimer_{signal}); ${signal}_open = true;",
        on_mouseleave=f"""
            clearTimeout(window.hoverTimer_{signal});
            window.hoverTimer_{signal} = setTimeout(() => {{
                ${signal}_open = false;
            }}, {hide_delay});
        """,
        id=f"{signal}-content",
        role="dialog",
        aria_labelledby=f"{signal}-trigger",
        tabindex="-1",
        cls=cn(
            "fixed z-50 w-72 max-w-[90vw] pointer-events-auto",
            "rounded-md border bg-popover p-4 text-popover-foreground shadow-md outline-none dark:border-input",
            cls,
        ),
        **attrs,
    )
