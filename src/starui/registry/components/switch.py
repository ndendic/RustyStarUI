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
            HTMLSpan(
                data_class=f"{{'translate-x-3.5': ${signal},'translate-x-0': !${signal},'dark:bg-primary-foreground': ${signal},'dark:bg-white': !${signal},}}",
                cls="pointer-events-none block size-4 rounded-full bg-white ring-0 transition-transform",
                data_slot="switch-thumb",
            ),
            on_click=f"${signal} = !${signal}",
            data_class={
                "bg-primary": f"${signal}",
                "bg-input": f"!${signal}",
            },
            type="checkbox",
            role="switch",
            id=switch_id,
            disabled=disabled,
            aria_checked=f"${{{signal}}}",
            aria_required="true" if required else None,
            data_slot="switch",
            cls=cn(
                "peer inline-flex h-[1.15rem] w-8 shrink-0 items-center rounded-full",
                "border border-transparent shadow-xs transition-all outline-none",
                "focus-visible:ring-[3px] focus-visible:border-ring focus-visible:ring-ring/50",
                "disabled:cursor-not-allowed disabled:opacity-50",
                class_name,
                cls,
            ),
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
    class_name: str = "",
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
                label,
                HTMLSpan(" *", cls="text-destructive") if required else None,
                for_=switch_id,
                cls=cn(
                    "text-sm font-medium",
                    "cursor-pointer"
                    if not disabled
                    else "cursor-not-allowed opacity-50",
                    label_cls,
                ),
            ),
            Switch(
                checked=checked,
                signal=signal,
                disabled=disabled,
                required=required,
                cls=switch_cls,
                aria_invalid="true" if error_text else None,
                id=switch_id,
            ),
            cls="flex items-center gap-3",
        ),
        error_text and HTMLP(error_text, cls="text-sm text-destructive mt-1.5") or None,
        helper_text
        and not error_text
        and HTMLP(helper_text, cls="text-sm text-muted-foreground mt-1.5")
        or None,
        cls=cn("space-y-1.5", class_name, cls),
        **attrs,
    )
