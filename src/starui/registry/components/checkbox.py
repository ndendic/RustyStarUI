from typing import Any
from uuid import uuid4

from starhtml import FT, Div, Icon, Input, Label, P, Span
from starhtml import Button as HTMLButton
from starhtml.datastar import ds_class, ds_on_click, ds_signals

from .utils import cn


def Checkbox(
    checked: bool | None = None,
    name: str | None = None,
    value: str | None = None,
    signal: str | None = None,
    disabled: bool = False,
    required: bool = False,
    class_name: str = "",
    cls: str = "",
    **attrs: Any,
) -> FT:
    signal = signal or f"checkbox_{str(uuid4())[:8]}"
    state_expr = f"${signal} ? 'checked' : 'unchecked'"

    return HTMLButton(
        Span(
            Icon("lucide:check", cls="size-3.5"),
            ds_class(**{"opacity-100": f"${signal}", "opacity-0": f"!${signal}"}),
            data_state=state_expr,
            data_slot="checkbox-indicator",
            cls="flex items-center justify-center text-current transition-none",
            style="pointer-events: none;",
        ),
        Input(
            type="checkbox",
            name=name,
            value=value or "on",
            checked=f"${signal}",
            disabled=disabled,
            required=required,
            tabindex="-1",
            cls="absolute opacity-0 pointer-events-none",
            **attrs,
        ),
        ds_signals(**{signal: checked or False}),
        ds_on_click(f"${signal} = !${signal}"),
        data_state=state_expr,
        data_slot="checkbox",
        type="button",
        role="checkbox",
        aria_checked=f"${signal}",
        disabled=disabled,
        cls=cn(
            "peer border-input dark:bg-input/30 data-[state=checked]:bg-primary data-[state=checked]:text-primary-foreground dark:data-[state=checked]:bg-primary data-[state=checked]:border-primary focus-visible:border-ring focus-visible:ring-ring/50 aria-invalid:ring-destructive/20 dark:aria-invalid:ring-destructive/40 aria-invalid:border-destructive size-4 shrink-0 rounded-[4px] border shadow-xs transition-shadow outline-none focus-visible:ring-[3px] disabled:cursor-not-allowed disabled:opacity-50",
            class_name,
            cls,
        ),
    )


def CheckboxWithLabel(
    label: str,
    checked: bool | None = None,
    name: str | None = None,
    value: str | None = None,
    signal: str | None = None,
    helper_text: str | None = None,
    error_text: str | None = None,
    disabled: bool = False,
    required: bool = False,
    class_name: str = "",
    cls: str = "",
    label_cls: str = "",
    checkbox_cls: str = "",
    **attrs: Any,
) -> FT:
    checkbox_id = f"checkbox_{str(uuid4())[:8]}"

    return Div(
        Div(
            Checkbox(
                checked=checked,
                name=name,
                value=value,
                signal=signal,
                disabled=disabled,
                required=required,
                id=checkbox_id,
                aria_invalid="true" if error_text else None,
                cls=checkbox_cls,
            ),
            Div(
                Label(
                    label,
                    required and Span(" *", cls="text-destructive") or "",
                    for_=checkbox_id,
                    cls=cn(
                        "flex items-center gap-2 text-sm leading-none font-medium select-none group-data-[disabled=true]:pointer-events-none group-data-[disabled=true]:opacity-50 peer-disabled:cursor-not-allowed peer-disabled:opacity-50",
                        "opacity-50 cursor-not-allowed" if disabled else "",
                        label_cls,
                    ),
                    data_slot="label",
                ),
                helper_text
                and P(
                    helper_text,
                    cls=cn(
                        "text-muted-foreground text-sm",
                        "opacity-50" if disabled else "",
                    ),
                )
                or None,
                cls="grid gap-1.5" if helper_text else None,
            ),
            cls="flex items-start gap-3",
        ),
        error_text and P(error_text, cls="text-sm text-destructive mt-1.5") or None,
        cls=cn(class_name, cls),
        **attrs,
    )
