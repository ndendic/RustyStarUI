from typing import Any, Literal

from rusty_tags import H2 as HTMLH2
from rusty_tags import Dialog as HTMLDialog
from rusty_tags import Div, HtmlString
from rusty_tags import P as HTMLP
from rusty_tags.datastar import Signals

from .utils import cn

AlertDialogVariant = Literal["default", "destructive"]


def AlertDialog(
    trigger: HtmlString,
    content: HtmlString,
    ref_id: str,
    class_name: str = "",
    cls: str = "",
    **attrs: Any,
) -> HtmlString:
    signal_name = f"{ref_id}_open"

    classes = cn(
        "fixed max-h-[85vh] w-full max-w-lg overflow-auto m-auto bg-background text-foreground border border-input rounded-lg shadow-lg p-0 backdrop:bg-black/50 backdrop:backdrop-blur-sm open:animate-in open:fade-in-0 open:zoom-in-95 open:duration-200 open:backdrop:animate-in open:backdrop:fade-in-0 open:backdrop:duration-200",
        class_name,
        cls,
    )

    dialog_element = HTMLDialog(
        content,
        ref=ref_id,
        on_close=f"${signal_name} = false",
        on_click=f"""
            evt.target === evt.currentTarget &&
            (${ref_id}.close(), ${signal_name} = false)
        """,
        id=ref_id,
        cls=classes,
        **attrs,
    )

    scroll_lock = Div(
        signals=Signals(**{signal_name: False}),
        effect=f"document.body.style.overflow = ${signal_name} ? 'hidden' : ''",
        style="'display: none;'",
    )

    return Div(trigger, dialog_element, scroll_lock)


def AlertDialogTrigger(
    *children: Any,
    ref_id: str,
    variant: str = "default",
    class_name: str = "",
    cls: str = "",
    **attrs: Any,
) -> HtmlString:
    from .button import Button

    return Button(
        *children,
        on_click=f"${ref_id}.showModal(), ${ref_id}_open = true",
        aria_haspopup="dialog",
        variant=variant,
        cls=cn(class_name, cls),
        **attrs,
    )


def AlertDialogContent(
    *children: Any,
    class_name: str = "",
    cls: str = "",
    **attrs: Any,
) -> HtmlString:
    return Div(
        *children,
        cls=cn("relative p-6", class_name, cls),
        **attrs,
    )


def AlertDialogHeader(
    *children: Any,
    class_name: str = "",
    cls: str = "",
    **attrs: Any,
) -> HtmlString:
    return Div(
        *children,
        cls=cn("flex flex-col gap-2 text-center sm:text-leHtmlString", class_name, cls),
        **attrs,
    )


def AlertDialogFooter(
    *children: Any,
    class_name: str = "",
    cls: str = "",
    **attrs: Any,
) -> HtmlString:
    return Div(
        *children,
        cls=cn(
            "flex flex-col-reverse gap-2 sm:flex-row sm:justify-end mt-6",
            class_name,
            cls,
        ),
        **attrs,
    )


def AlertDialogTitle(
    *children: Any,
    class_name: str = "",
    cls: str = "",
    **attrs: Any,
) -> HtmlString:
    return HTMLH2(
        *children,
        cls=cn("text-lg leading-none font-semibold text-foreground", class_name, cls),
        **attrs,
    )


def AlertDialogDescription(
    *children: Any,
    class_name: str = "",
    cls: str = "",
    **attrs: Any,
) -> HtmlString:
    return HTMLP(
        *children,
        cls=cn("text-muted-foreground text-sm", class_name, cls),
        **attrs,
    )


def AlertDialogAction(
    *children: Any,
    ref_id: str,
    action: str = "",
    variant: AlertDialogVariant = "default",
    class_name: str = "",
    cls: str = "",
    **attrs: Any,
) -> HtmlString:
    from .button import Button

    close_expr = f"${ref_id}_open = false, ${ref_id}.close()"
    if action:
        close_expr = f"{action}, {close_expr}"

    return Button(
        *children,
        on_click=close_expr,
        variant="destructive" if variant == "destructive" else "default",
        cls=cn(class_name, cls),
        **attrs,
    )


def AlertDialogCancel(
    *children: Any,
    ref_id: str,
    class_name: str = "",
    cls: str = "",
    **attrs: Any,
) -> HtmlString:
    from .button import Button

    return Button(
        *children,
        on_click=f"${ref_id}_open = false, ${ref_id}.close()",
        variant="outline",
        cls=cn(class_name, cls),
        **attrs,
    )
