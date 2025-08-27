from typing import Any, Literal
from uuid import uuid4

from starhtml import FT, Div
from starhtml.datastar import ds_on, ds_signals, ds_ref, ds_style, ds_effect
from fastcore.xml import NotStr

from .utils import cn

HoverCardSide = Literal["top", "right", "bottom", "left"]
HoverCardAlign = Literal["start", "center", "end"]


def HoverCard(
    *children,
    signal: str | None = None,
    default_open: bool = False,
    cls: str = "",
    **attrs: Any,
) -> FT:
    signal = signal or f"hover_card_{uuid4().hex[:8]}"
    return Div(
        *children,
        ds_signals({f"{signal}_open": default_open}),
        cls=cn("relative inline-block", cls),
        **attrs,
    )


def HoverCardTrigger(
    *children,
    signal: str | None = None,
    hover_delay: int = 700,
    hide_delay: int = 300,
    cls: str = "",
    **attrs: Any,
) -> FT:
    signal = signal or "hover_card"
    
    enter_handler = f"""
        clearTimeout(window.hoverTimer_{signal});
        window.hoverTimer_{signal} = setTimeout(() => {{
            ${signal}_open = true;
        }}, {hover_delay});
    """
    
    leave_handler = f"""
        clearTimeout(window.hoverTimer_{signal});
        window.hoverTimer_{signal} = setTimeout(() => {{
            ${signal}_open = false;
        }}, {hide_delay});
    """
    
    return Div(
        *children,
        ds_ref(f"{signal}Trigger"),
        ds_on("mouseenter", enter_handler),
        ds_on("mouseleave", leave_handler),
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
    side: HoverCardSide = "bottom",
    align: HoverCardAlign = "center",
    hide_delay: int = 300,
    cls: str = "",
    **attrs: Any,
) -> FT:
    signal = signal or "hover_card"

    # Content hover handlers to maintain visibility
    content_enter_handler = f"clearTimeout(window.hoverTimer_{signal}); ${signal}_open = true;"
    content_leave_handler = f"clearTimeout(window.hoverTimer_{signal}); window.hoverTimer_{signal} = setTimeout(() => {{ ${signal}_open = false; }}, {hide_delay});"

    # Use reactive positioning like popover to handle viewport bounds

    return Div(
        *children,
        ds_signals({f"{signal}_top": -9999, f"{signal}_left": -9999, f"{signal}_initialScrollY": 0, f"{signal}_initialScrollX": 0}),
        ds_effect(f"""
            const trigger = ${signal}Trigger;
            const content = ${signal}Content;
            if (trigger && content && ${signal}_open) {{
                // Store initial scroll position when hover card opens
                ${signal}_initialScrollY = window.scrollY;
                ${signal}_initialScrollX = window.scrollX;
                
                const tr = trigger.getBoundingClientRect();
                const cr = content.getBoundingClientRect();
                const gap = 8, pad = 8;
                let top, left;
                
                if ('{side}' === 'bottom') {{
                    top = tr.bottom + gap;
                }} else if ('{side}' === 'top') {{
                    top = tr.top - cr.height - gap;
                }} else {{
                    top = tr.top + (tr.height - cr.height) / 2;
                }}
                
                if ('{align}' === 'start') {{
                    left = tr.left;
                }} else if ('{align}' === 'end') {{
                    left = tr.right - cr.width;
                }} else {{
                    left = tr.left + (tr.width - cr.width) / 2;
                }}
                
                left = Math.max(pad, Math.min(left, window.innerWidth - cr.width - pad));
                top = Math.max(pad, Math.min(top, window.innerHeight - cr.height - pad));
                
                ${signal}_top = top;
                ${signal}_left = left;
            }}
        """),
        ds_ref(f"{signal}Content"),
        ds_style(
            position="'fixed'",
            top=f"${signal}_top + 'px'",
            left=f"${signal}_left + 'px'",
            visibility=f"${signal}_open ? 'visible' : 'hidden'"
        ),
        ds_on("mouseenter", content_enter_handler),
        ds_on("mouseleave", content_leave_handler),
        id=f"{signal}-content",
        role="dialog",
        aria_labelledby=f"{signal}-trigger",
        tabindex="-1",
        cls=cn(
            "z-50 w-72 max-w-[90vw] pointer-events-auto",
            "rounded-md border bg-popover p-4 text-popover-foreground shadow-md outline-none dark:border-input",
            cls,
        ),
        # Add scroll handler using delta positioning for smooth movement
        **{f"data-on-scroll__throttle.16ms": NotStr(f"""
            if (${signal}_open) {{
                // Calculate scroll delta from initial position
                const deltaY = window.scrollY - ${signal}_initialScrollY;
                const deltaX = window.scrollX - ${signal}_initialScrollX;
                
                // Apply inverse delta to maintain fixed position relative to document
                ${signal}_top = ${signal}_top - deltaY;
                ${signal}_left = ${signal}_left - deltaX;
                
                // Update stored scroll position for next delta calculation
                ${signal}_initialScrollY = window.scrollY;
                ${signal}_initialScrollX = window.scrollX;
                
                // Check if trigger is still visible (less frequently) - hover cards should close when trigger is off-screen
                if (Math.floor(window.scrollY / 50) !== Math.floor((window.scrollY - deltaY) / 50)) {{
                    const tr = ${signal}Trigger.getBoundingClientRect();
                    const triggerVisible = tr.bottom > 0 && tr.top < window.innerHeight && 
                                         tr.right > 0 && tr.left < window.innerWidth;
                    if (!triggerVisible) {{
                        // Hide hover card when trigger goes off-screen (typical hover behavior)
                        clearTimeout(window.hoverTimer_{signal});
                        ${signal}_open = false;
                    }}
                }}
            }}
        """)},
        **attrs,
    )