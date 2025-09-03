from typing import Any, Literal
from uuid import uuid4

from rusty_tags import Button as HTMLButton
from rusty_tags import Div, Hr, HtmlString, Script, Signals, Span

from .button import Button
from .utils import Icon, cn


def DropdownMenu(
    *children, signal: str | None = None, cls: str = "", **attrs: Any
) -> HtmlString:
    signal = signal or f"dropdown_{uuid4().hex[:8]}"
    return Div(
        *[child(signal) if callable(child) else child for child in children],
        cls=cn("relative inline-block","dropdown-menu", cls),
        signals=Signals({f"{signal}_open": False}),
        **attrs,
    )


def DropdownMenuTrigger(
    *children,
    variant: Literal[
        "default", "destructive", "outline", "secondary", "ghost", "link"
    ] = "outline",
    size: Literal["default", "sm", "lg", "icon"] = "default",
    cls: str = "btn-outline",
    **attrs: Any,
):
    def create(signal):
        trigger_id = f"{signal}dropdown-menu-trigger"

        return Button(
            *children,
            aria_haspopup='menu',
            aria_controls=f"{signal}-dropdown-menu-popover",
            # aria_expanded='false',
            ref=f"{signal}Trigger",
            variant=variant,
            size=size,
            id=trigger_id,
            type="button",
            on_click=f"${signal}_open = !${signal}_open",
            cls=cn(cls),
            **attrs,
        )

    return create


def DropdownMenuContent(
    *children,
    side: Literal["top", "right", "bottom", "left"] = "bottom",
    align: Literal["start", "center", "end"] = "start",
    side_offset: int = 4,
    cls: str = "",
    class_name: str = "",
    **attrs: Any,
):
    def create(signal):
        return Div(
                Div(
                    *[child(signal) if callable(child) else child for child in children],
                    role='menu',
                    id=f'{signal}-dropdown-menu-menu',
                    aria_labelledby=f'{signal}-dropdown-menu-trigger'
                ),
            id=f'{signal}-dropdown-menu-popover',
            # show=f"${signal}_open",
            on_intersect=f"${signal}_open = true",
            data_popover=True,
            data_side=side,
            data_align=align,
            data_side_offset=side_offset,
            aria_hidden='true',
            cls=cn('min-w-56', class_name, cls),
            **attrs,
        )

    return create


def DropdownMenuItem(
    *children,
    onclick: str | None = None,
    variant: Literal["default", "destructive"] = "default",
    inset: bool = False,
    disabled: bool = False,
    cls: str = "",
    class_name: str = "",
    **attrs: Any,
):
    variant_classes = {
        "default": "hover:bg-accent hover:text-accent-foreground focus:bg-accent focus:text-accent-foreground",
        "destructive": "text-destructive hover:bg-destructive/10 hover:text-destructive focus:bg-destructive/10 focus:text-destructive",
    }

    def create(signal):
        handlers = []
        if onclick:
            handlers.append(onclick)

        return HTMLButton(
            *children,
            **({"on_click": "; ".join(handlers)} if handlers and not disabled else {}),
            cls=cn(
                "relative flex w-full cursor-default select-none items-center gap-2 rounded-sm px-2 py-1.5",
                "text-sm outline-none transition-colors",
                variant_classes.get(variant, variant_classes["default"]),
                "pl-8" if inset else "",
                "pointer-events-none opacity-50" if disabled else "",
                "[&_svg]:pointer-events-none [&_svg]:shrink-0 [&_svg]:size-4",
                "[&_iconify-icon]:size-4 [&_iconify-icon]:shrink-0",
                class_name,
                cls,
            ),
            type="button",
            disabled=disabled,
            role="menuitem",
            **attrs,
        )

    return create


def DropdownMenuCheckboxItem(
    *children,
    checked_signal: str,
    inset: bool = False,
    disabled: bool = False,
    cls: str = "",
    class_name: str = "",
    **attrs: Any,
):
    def create(signal):
        handlers = []
        if not disabled:
            handlers.append(
                f"${checked_signal} = !${checked_signal}; "
            )

        return HTMLButton(
            Span(
                Icon("lucide:check"),
                show=f"${checked_signal}",
                cls="absolute left-2 flex size-3.5 items-center justify-center",
            ),
            *children,
            **({"on_click": handlers[0]} if handlers else {}),
            cls=cn(
                "relative flex w-full cursor-default select-none items-center gap-2 rounded-sm",
                "py-1.5 pr-2 pl-8 text-sm outline-none transition-colors",
                "hover:bg-accent hover:text-accent-foreground",
                "focus:bg-accent focus:text-accent-foreground",
                "pointer-events-none opacity-50" if disabled else "",
                "[&_svg]:pointer-events-none [&_svg]:shrink-0",
                "[&_iconify-icon]:size-4 [&_iconify-icon]:shrink-0",
                class_name,
                cls,
            ),
            type="button",
            role="menuitemcheckbox",
            aria_checked=f"${{{checked_signal}}} ? 'true' : 'false'",
            disabled=disabled,
            **attrs,
        )

    return create


def DropdownMenuRadioGroup(
    *children,
    value_signal: str,
    cls: str = "",
    class_name: str = "",
    **attrs: Any,
):
    return lambda signal: Div(
        *[child(signal) if callable(child) else child for child in children],
        role="radiogroup",
        cls=cn(class_name, cls),
        **attrs,
    )


def DropdownMenuRadioItem(
    *children,
    value: str,
    value_signal: str,
    disabled: bool = False,
    cls: str = "",
    class_name: str = "",
    **attrs: Any,
):
    def create(signal):
        handlers = []
        if not disabled:
            handlers.append(f"${value_signal} = '{value}'; ")

        return HTMLButton(
            Span(
                Icon("lucide:circle", cls="size-2 fill-current"),
                show=f"${value_signal} === '{value}'",
                cls="absolute left-2 flex size-3.5 items-center justify-center",
            ),
            *children,
            **({"on_click": handlers[0]} if handlers else {}),
            cls=cn(
                "relative flex w-full cursor-default select-none items-center gap-2 rounded-sm",
                "py-1.5 pr-2 pl-8 text-sm outline-none transition-colors",
                "hover:bg-accent hover:text-accent-foreground",
                "focus:bg-accent focus:text-accent-foreground",
                "pointer-events-none opacity-50" if disabled else "",
                "[&_svg]:pointer-events-none [&_svg]:shrink-0",
                "[&_iconify-icon]:size-4 [&_iconify-icon]:shrink-0",
                class_name,
                cls,
            ),
            type="button",
            role="menuitemradio",
            aria_checked=f"${{{value_signal}}} === '{value}' ? 'true' : 'false'",
            disabled=disabled,
            **attrs,
        )

    return create


def DropdownMenuSeparator(cls: str = "", class_name: str = "", **attrs: Any):
    return lambda signal: Hr(
        cls=cn("-mx-1 my-1 border-t border-input", class_name, cls), **attrs
    )


def DropdownMenuLabel(
    *children, inset: bool = False, cls: str = "", class_name: str = "", **attrs: Any
):
    return lambda signal: Div(
        *children,
        cls=cn(
            "px-2 py-1.5 text-sm font-medium",
            "pl-8" if inset else "",
            class_name,
            cls,
        ),
        **attrs,
    )


def DropdownMenuShortcut(
    *children,
    cls: str = "",
    class_name: str = "",
    **attrs: Any,
) -> HtmlString:
    return Span(
        *children,
        cls=cn(
            "ml-auto text-xs tracking-widest text-muted-foreground",
            class_name,
            cls,
        ),
        **attrs,
    )


def DropdownMenuGroup(
    *children,
    cls: str = "",
    class_name: str = "",
    **attrs: Any,
) -> HtmlString:
    return Div(
        *children,
        role="group",
        cls=cn(class_name, cls),
        **attrs,
    )


def DropdownMenuSub(
    *children,
    signal: str | None = None,
    cls: str = "",
    class_name: str = "",
    **attrs: Any,
) -> HtmlString:
    signal = signal or f"dropdown_sub_{uuid4().hex[:8]}"
    return Div(
        *children,
        cls=cn("relative", class_name, cls),
        **attrs,
    )


def DropdownMenuSubTrigger(
    *children,
    signal: str,
    inset: bool = False,
    cls: str = "",
    class_name: str = "",
    **attrs: Any,
) -> HtmlString:
    return HTMLButton(
        *children,
        Icon("lucide:chevron-right", cls="ml-auto size-4"),
        on_click=f"${signal}_open = !${signal}_open",
        cls=cn(
            "flex w-full cursor-default select-none items-center rounded-sm px-2 py-1.5",
            "text-sm outline-none transition-colors",
            "hover:bg-accent hover:text-accent-foreground",
            "focus:bg-accent focus:text-accent-foreground",
            "data-[state=open]:bg-accent data-[state=open]:text-accent-foreground",
            "pl-8" if inset else "",
            class_name,
            cls,
        ),
        data_state=f"${{{signal}_open}} ? 'open' : 'closed'",
        type="button",
        role="menuitem",
        aria_haspopup="menu",
        aria_expanded=f"${{{signal}_open}} ? 'true' : 'false'",
        **attrs,
    )


def DropdownMenuSubContent(
    *children,
    signal: str,
    cls: str = "",
    class_name: str = "",
    **attrs: Any,
) -> HtmlString:
    return Div(
        *children,
        show=f"${signal}_open",
        cls=cn(
            "absolute left-full top-0 ml-1 z-50",
            "min-w-[8rem] overflow-hidden rounded-md border border-input",
            "bg-popover text-popover-foreground shadow-lg",
            "p-1",
            class_name,
            cls,
        ),
        role="menu",
        **attrs,
    )
