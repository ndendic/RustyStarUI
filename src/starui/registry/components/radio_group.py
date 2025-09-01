from itertools import count
from typing import Any
from uuid import uuid4

from rusty_tags import HtmlString, Div
from rusty_tags import Input as HTMLInput
from rusty_tags import Label as HTMLLabel
from rusty_tags import P as HTMLP
from rusty_tags import Span as HTMLSpan
from rusty_tags.datastar import Signals

from .utils import cn

_radio_group_ids = count(1)


def RadioGroup(
    *children: Any,
    initial_value: str | None = None,
    signal: str = "",
    disabled: bool = False,
    required: bool = False,
    class_name: str = "",
    cls: str = "",
    **attrs: Any,
) -> HtmlString:
    signal = signal or f"radio_{next(_radio_group_ids)}"
    group_name = f"radio_group_{signal}"

    processed_children = [
        child(signal, group_name, initial_value) if callable(child) else child
        for child in children
    ]

    return Div(
        *processed_children,
        signals=Signals({signal: initial_value or ""}),
        cls=cn("grid gap-2", class_name, cls),
        data_slot="radio-group",
        data_radio_signal=signal,
        data_radio_name=group_name,
        role="radiogroup",
        aria_required="true" if required else None,
        **attrs,
    )


def RadioGroupItem(
    value: str,
    label: str | None = None,
    disabled: bool = False,
    class_name: str = "",
    cls: str = "",
    indicator_cls: str = "",
    **attrs: Any,
) -> HtmlString:
    def create_item(signal, group_name, default_value=None):
        radio_id = f"radio_{str(uuid4())[:8]}"
        filtered_attrs = {k: v for k, v in attrs.items() if k != "name"}

        radio_input = HTMLInput(
            on_change=f"${signal} = '{value}'",
            type="radio",
            id=radio_id,
            value=value,
            name=group_name,
            disabled=disabled,
            data_slot="radio-input",
            cls="input",
            **filtered_attrs,
        )

        if not label:
            return Div(
                radio_input,
                # visual_radio,
                cls="relative inline-flex items-center",
                data_slot="radio-container",
            )

        return HTMLLabel(
            radio_input,
            # visual_radio,
            HTMLSpan(
                label,
                cls="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-50",
            ),
            for_=radio_id,
            cls="label flex items-center gap-2 cursor-pointer",
            data_slot="radio-container",
        )

    return create_item


def RadioGroupWithLabel(
    label: str,
    options: list[dict[str, Any]],
    value: str | None = None,
    signal: str | None = None,
    name: str | None = None,
    helper_text: str | None = None,
    error_text: str | None = None,
    disabled: bool = False,
    required: bool = False,
    orientation: str = "vertical",
    cls: str = "",
    **attrs: Any,
) -> HtmlString:
    base_id = str(uuid4())[:8]
    signal = signal or f"radio_{base_id}"
    name = name or f"radio_group_{signal}"
    group_id = f"radiogroup_{base_id}"

    radio_group_classes = cn(
        "flex gap-2",
        "flex-col" if orientation == "vertical" else "flex-row gap-2",
    )

    return Div(
        label
        and HTMLLabel(
            label,
            required and HTMLSpan("*", cls="text-destructive") or None,
            cls="text-sm font-medium mb-3 block",
            for_=group_id,
        )
        or None,
        RadioGroup(
            *[
                RadioGroupItem(
                    value=option["value"],
                    label=option.get("label"),
                    disabled=disabled or option.get("disabled", False),
                )
                for option in options
            ],
            value=value,
            signal=signal,
            name=name,
            disabled=disabled,
            required=required,
            cls=radio_group_classes,
            id=group_id,
            aria_invalid="true" if error_text else None,
        ),
        error_text and HTMLP(error_text, cls="text-sm text-destructive mt-1.5") or None,
        helper_text
        and not error_text
        and HTMLP(helper_text, cls="text-sm text-muted-foreground mt-1.5")
        or None,
        cls=cn("space-y-1.5", cls),
        **attrs,
    )
