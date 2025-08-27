"""Popover component with native HTML popover API and reactive positioning."""

from typing import Any
from starhtml import *
from starhtml.datastar import ds_ref, ds_signals, ds_style, ds_on_toggle
from fastcore.xml import NotStr
from .utils import cn
from .button import Button


def PopoverTrigger(*children, signal="", variant="default", cls="", **attrs):
    """Trigger button for native popover."""
    return Button(
        *children,
        ds_ref(f"{signal}Trigger"),
        variant=variant,
        popovertarget=f"{signal}-content",
        popoveraction="toggle",        
        id=f"{signal}-trigger",
        cls=cls,
        **attrs,
    )


def PopoverContent(*children, signal="", cls="", side="bottom", align="center", **attrs):
    """Popover content with reactive positioning."""
    return Div(
        *children,
        ds_signals({f"{signal}_top": 0, f"{signal}_left": 0, f"{signal}_open": False, f"{signal}_initialScrollY": 0, f"{signal}_initialScrollX": 0}),
        ds_on_toggle(f"""
            ${signal}_open = event.newState === 'open';
            if (event.newState === 'open' && ${signal}Trigger && ${signal}Content) {{
                requestAnimationFrame(() => {{
                    // Store initial scroll position
                    ${signal}_initialScrollY = window.scrollY;
                    ${signal}_initialScrollX = window.scrollX;
                    
                    const tr = ${signal}Trigger.getBoundingClientRect();
                    const cr = ${signal}Content.getBoundingClientRect();
                    const gap = 8, pad = 8;                    
                    let top = ('{side}' === 'bottom') ? tr.bottom + gap : tr.top - cr.height - gap;
                    let left = ('{align}' === 'center') ? tr.left + (tr.width - cr.width) / 2 :
                               ('{align}' === 'start') ? tr.left : tr.right - cr.width;                    
                    left = Math.max(pad, Math.min(left, window.innerWidth - cr.width - pad));
                    top = Math.max(pad, Math.min(top, window.innerHeight - cr.height - pad));                    
                    ${signal}_top = top;
                    ${signal}_left = left;
                }});
            }}
        """),
        ds_ref(f"{signal}Content"),
        ds_style(
            position="'fixed'",
            top=f"${signal}_top + 'px'",
            left=f"${signal}_left + 'px'"
        ),
        popover="auto",
        id=f"{signal}-content",
        role="dialog",
        aria_labelledby=f"{signal}-trigger",
        tabindex="-1",
        cls=cn(
            "z-50 w-72 rounded-md border bg-popover p-4 text-popover-foreground shadow-md outline-none dark:border-input",
            cls,
        ),
        **attrs,
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
                
                // Check if trigger is still visible (less frequently)
                if (Math.floor(window.scrollY / 100) !== Math.floor((window.scrollY - deltaY) / 100)) {{
                    const tr = ${signal}Trigger.getBoundingClientRect();
                    const triggerVisible = tr.bottom > 0 && tr.top < window.innerHeight && 
                                         tr.right > 0 && tr.left < window.innerWidth;
                    if (!triggerVisible) {{
                        el.hidePopover();
                    }}
                }}
            }}
        """)},
    )


def PopoverClose(*children, signal="", cls="", **attrs):
    """Close button for popover."""
    variant = attrs.pop("variant", "ghost")
    size = attrs.pop("size", "sm")
    
    return Button(
        *children,
        popovertarget=f"{signal}-content",
        popoveraction="hide",
        variant=variant,
        size=size,
        cls=cn("absolute right-2 top-2", cls),
        aria_label="Close popover",
        **attrs,
    )


def Popover(*children, signal="popover", **attrs):
    """Complete popover component."""
    return Div(*children, signal=signal, cls="relative inline-block", **attrs)