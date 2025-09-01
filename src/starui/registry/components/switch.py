from typing import Any
from uuid import uuid4

from rusty_tags import Div, HtmlString
from rusty_tags import Input as HTMLInput
from rusty_tags import Label as HTMLLabel
from rusty_tags import P as HTMLP
from rusty_tags import Span as HTMLSpan
from rusty_tags.datastar import Signals

from .utils import cn


def Switch(
    checked: bool | None = None,
    signal: str = "",
    disabled: bool = False,
    required: bool = False,
    class_name: str = "",
    cls: str = "",
    **attrs: Any,
) -> HtmlString:
    signal = signal or f'switch_{str(uuid4())[:8]}'
    switch_id = attrs.pop("id", f"switch_{str(uuid4())[:8]}")

    return Div(
        HTMLInput(
            on_click=f"${signal} = !${signal}",
            type="checkbox",
            role="switch",
            id=switch_id,
            disabled=disabled,
            aria_checked=f"${{{signal}}}",
            aria_required="true" if required else None,
            data_slot="switch",
            cls=cn("input",cls),
            **attrs,
        ),
        signals=Signals({signal: checked or False}),
    )


def SwitchWithLabel(
    label: str,
    checked: bool | None = None,
    signal: str = "",
    helper_text: str | None = None,
    error_text: str | None = None,
    disabled: bool = False,
    required: bool = False,
    cls: str = "",
    label_cls: str = "",
    switch_cls: str = "",
    **attrs: Any,
) -> HtmlString:
    signal = signal or f"switch_{str(uuid4())[:8]}"
    switch_id = f"switch_{str(uuid4())[:8]}"

    return Div(
        Div(
            HTMLLabel(
                Switch(
                    checked=checked,
                    signal=signal,
                    disabled=disabled,
                    required=required,
                    cls=switch_cls,
                    aria_invalid="true" if error_text else None,
                    id=switch_id,
                ),
                label,
                HTMLSpan("*", cls="text-destructive") if required else None,
                for_=switch_id,
                cls=cn("label",label_cls),
            ),
            cls="flex items-center gap-3",
        ),
        error_text and HTMLP(error_text, cls="text-sm text-destructive mt-1.5") or None,
        helper_text
        and not error_text
        and HTMLP(helper_text, cls="text-sm text-muted-foreground mt-1.5")
        or None,
        cls=cn("space-y-1.5", cls),
        **attrs,
    )
