from typing import Any
from uuid import uuid4

from starhtml import FT, Button, Div, Icon, Label, P, Span
from starhtml.datastar import (
    ds_class,
    ds_on_click,
    ds_show,
    ds_signals,
    ds_text,
    ds_ref,
    ds_style,
    ds_on_toggle,
)
from fastcore.xml import NotStr


from .utils import cn


def Select(
    *children,
    value: str | None = None,
    signal: str | None = None,
    cls: str = "",
    **attrs: Any,
) -> FT:
    signal = signal or f"select_{uuid4().hex[:8]}"
    return Div(
        *children,
        # Track select state including open state for positioning
        ds_signals({
            f"{signal}_value": value or "",
            f"{signal}_label": "",
            f"{signal}_open": False,
        }),
        cls=cn("relative inline-block", cls),
        **attrs,
    )


def SelectTrigger(
    *children,
    signal: str | None = None,
    width: str = "w-[180px]",
    cls: str = "",
    **attrs: Any,
) -> FT:
    signal = signal or "select"
    trigger_id = attrs.pop("id", f"{signal}-trigger")
    
    return Button(
        *children,
        Icon("lucide:chevron-down", cls="size-4 shrink-0 opacity-50"),
        ds_ref(f"{signal}Trigger"),
        popovertarget=f"{signal}-content",
        popoveraction="toggle",
        type="button",
        role="combobox",
        aria_haspopup="listbox",
        aria_controls=f"{signal}-content",
        data_placeholder=f"!${signal}_label",        
        id=trigger_id,
        cls=cn(
            width,
            "flex h-9 items-center justify-between gap-2 rounded-md border border-input",
            "bg-transparent px-3 py-2 text-sm whitespace-nowrap shadow-xs",
            "transition-[color,box-shadow] outline-none",
            "dark:bg-input/30 dark:hover:bg-input/50",
            "focus-visible:border-ring focus-visible:ring-ring/50 focus-visible:ring-[3px]",
            "aria-invalid:ring-destructive/20 dark:aria-invalid:ring-destructive/40",
            "aria-invalid:border-destructive",
            "disabled:cursor-not-allowed disabled:opacity-50",
            "data-[placeholder]:text-muted-foreground",
            cls,
        ),
        **attrs,
    )


def SelectValue(
    placeholder: str = "Select an option",
    signal: str | None = None,
    cls: str = "",
    **attrs: Any,
) -> FT:
    signal = signal or "select"
    return Span(
        ds_text(f"${signal}_label || '{placeholder}'"),
        ds_class(text_muted_foreground=f"!${signal}_label"),
        cls=cn("pointer-events-none", cls),
        **attrs,
    )


def SelectContent(
    *children,
    signal: str | None = None,
    cls: str = "",
    **attrs: Any,
) -> FT:
    signal = signal or "select"
    
    return Div(
        Div(*children, cls="p-1 max-h-[300px] overflow-auto"),
        ds_signals({f"{signal}_top": -9999, f"{signal}_left": -9999, f"{signal}_width": 180, f"{signal}_open": False, f"{signal}_initialScrollY": 0, f"{signal}_initialScrollX": 0}),
        ds_on_toggle(f"""
            ${signal}_open = event.newState === 'open';
            if (event.newState === 'open' && ${signal}Trigger && ${signal}Content) {{
                requestAnimationFrame(() => {{
                    // Store initial scroll position
                    ${signal}_initialScrollY = window.scrollY;
                    ${signal}_initialScrollX = window.scrollX;
                    
                    const tr = ${signal}Trigger.getBoundingClientRect();
                    const cr = ${signal}Content.getBoundingClientRect();
                    const gap = 4, pad = 8;                    
                    ${signal}_width = tr.width;                    
                    let top = tr.bottom + gap;
                    if (top + cr.height > window.innerHeight - pad) {{
                        top = tr.top - cr.height - gap;
                    }}                                        
                    let left = tr.left;
                    left = Math.max(pad, Math.min(left, window.innerWidth - tr.width - pad));                    
                    ${signal}_top = top;
                    ${signal}_left = left;
                }});
            }}
        """),
        ds_ref(f"{signal}Content"),
        ds_style(
            position="'fixed'",
            top=f"${signal}_top + 'px'",
            left=f"${signal}_left + 'px'",
            width=f"${signal}_width + 'px'",
            minWidth=f"${signal}_width + 'px'"
        ),
        popover="auto",
        id=f"{signal}-content",
        role="listbox",
        aria_labelledby=f"{signal}-trigger",
        tabindex="-1",
        cls=cn(
            "z-50 min-w-[8rem] overflow-hidden rounded-md border bg-popover text-popover-foreground shadow-md dark:border-input",
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
        **attrs,
    )


def SelectItem(
    value: str,
    label: str | None = None,
    signal: str | None = None,
    disabled: bool = False,
    cls: str = "",
    **attrs: Any,
) -> FT:
    label = label or value
    signal = signal or "select"
    
    children = [
        Span(label),
        Span(
            Icon("lucide:check", cls="h-4 w-4"),
            ds_show(f"${signal}_value === '{value}'"),
            cls="absolute right-2 flex h-3.5 w-3.5 items-center justify-center",
        )
    ]
    
    if not disabled:
        # Set value and label, then programmatically close the popover
        children.append(ds_on_click(f"${signal}_value='{value}';${signal}_label='{label}';document.getElementById('{signal}-content').hidePopover()"))
    
    return Div(
        *children,
        role="option",
        data_value=value,
        data_selected=f"${signal}_value === '{value}'",
        data_disabled="true" if disabled else None,
        cls=cn(
            "relative flex w-full cursor-default select-none items-center rounded-sm py-1.5 pl-2 pr-8 text-sm outline-none",
            "hover:bg-accent hover:text-accent-foreground focus:bg-accent focus:text-accent-foreground",
            "data-[disabled]:pointer-events-none data-[disabled]:opacity-50",
            cls,
        ),
        **attrs,
    )


def SelectGroup(
    *children,
    label: str | None = None,
    cls: str = "",
    **attrs: Any,
) -> FT:
    return Div(
        SelectLabel(label) if label else "",
        *children,
        cls=cls,
        **attrs,
    )


def SelectLabel(
    text: str,
    cls: str = "",
    **attrs: Any,
) -> FT:
    return Div(
        text,
        cls=cn("text-muted-foreground px-2 py-1.5 text-xs", cls),
        **attrs,
    )


def SelectWithLabel(
    label: str,
    options: list[str | tuple[str, str] | dict],
    value: str | None = None,
    placeholder: str = "Select an option",
    name: str | None = None,
    signal: str | None = None,
    helper_text: str | None = None,
    error_text: str | None = None,
    required: bool = False,
    disabled: bool = False,
    label_cls: str = "",
    select_cls: str = "",
    cls: str = "",
    **attrs: Any,
) -> FT:
    select_id = f"select_{str(uuid4())[:8]}"

    def build_options(opts):
        items = []
        for opt in opts:
            if isinstance(opt, str):
                items.append(SelectItem(value=opt, label=opt, signal=signal))
            elif isinstance(opt, tuple) and len(opt) == 2:
                items.append(SelectItem(value=opt[0], label=opt[1], signal=signal))
            elif isinstance(opt, dict):
                if "group" in opt and "items" in opt:
                    group_items = []
                    for item in opt["items"]:
                        if isinstance(item, str):
                            group_items.append(
                                SelectItem(value=item, label=item, signal=signal)
                            )
                        elif isinstance(item, tuple) and len(item) == 2:
                            group_items.append(
                                SelectItem(value=item[0], label=item[1], signal=signal)
                            )
                    items.append(SelectGroup(*group_items, label=opt["group"]))
        return items

    return Div(
        Label(
            label,
            Span(" *", cls="text-destructive") if required else "",
            for_=select_id,
            cls=cn("block text-sm font-medium mb-1.5", label_cls),
        ),
        Select(
            SelectTrigger(
                SelectValue(placeholder=placeholder, signal=signal),
                signal=signal,
                cls=select_cls,
                disabled=disabled,
                aria_invalid="true" if error_text else None,
                id=select_id,
            ),
            SelectContent(*build_options(options), signal=signal),
            value=value,
            name=name,
            signal=signal,
            **attrs,
        ),
        error_text and P(error_text, cls="text-sm text-destructive mt-1.5"),
        helper_text
        and not error_text
        and P(helper_text, cls="text-sm text-muted-foreground mt-1.5"),
        cls=cn("space-y-1.5", cls),
    )
