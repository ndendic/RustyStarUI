from typing import Any
from uuid import uuid4

from rusty_tags import Button as HTMLButton
from rusty_tags import Circle, Div, Header, HtmlString, Path, Span, Svg
from rusty_tags import Input as HTMLInput
from rusty_tags import Label as HTMLLabel
from rusty_tags import Optgroup as HTMLOptionGroup
from rusty_tags import OptionEl as HTMLOption
from rusty_tags import P as HTMLP
from rusty_tags import Select as HTMLSelect
from rusty_tags.datastar import Signals

from .utils import Icon, cn


def Select(
        *children,
        initial_value: str | None = None,
        signal: str | None = None,
        cls: str = "",
        **attrs: Any,
    ) -> HtmlString:
    signal = signal or f"select_{uuid4().hex[:8]}"
    return Div(
        *children,
        HTMLInput(type='hidden', name=f'select-{signal}-value', value=initial_value or ''),
        id=signal,
        cls=cn('select', cls)
    )

def SelectTrigger(
    *children,
    signal: str | None = None,
    width: str = "w-[180px]",
    cls: str = "",
    **attrs: Any,
) -> HtmlString:
    signal = signal or "select"
    trigger_id = attrs.pop("id", f"select-{signal}-trigger")
    trigger= HTMLButton(
        *children,
        Svg(
            Path(d='m7 15 5 5 5-5'),
            Path(d='m7 9 5-5 5 5'),
            xmlns='http://www.w3.org/2000/svg',
            width='24',
            height='24',
            viewbox='0 0 24 24',
            fill='none',
            stroke='currentColor',
            stroke_width='2',
            stroke_linecap='round',
            stroke_linejoin='round',
            cls='lucide lucide-chevrons-up-down-icon lucide-chevrons-up-down text-muted-foreground opacity-50 shrink-0'
        ),
        type='button',
        id=trigger_id,
        aria_haspopup='listbox',
        aria_expanded='false',
        aria_controls= f"select-{signal}-listbox",
        cls=cn('btn-outline justify-between font-normal',width,cls),
    )
    return trigger

def SelectValue(
    placeholder: str = "Select an option",
    signal: str | None = None,
    cls: str = "",
    **attrs: Any,
) -> HtmlString:
    signal = signal or "select"
    return Span(
        placeholder,
        # text=f"${signal}_label || '{placeholder}'",
        # data_class={"text-muted-foreground": f"!${signal}_label"},
        cls=cn("pointer-events-none", cls),
        **attrs,
    )

def SelectContent(
        *children,
        signal: str | None = None,
        cls: str = "",
        **attrs: Any,
    ) -> HtmlString:
    signal = signal or "select"

    return Div(
            Header(
                Svg(
                    Circle(cx='11', cy='11', r='8'),
                    Path(d='m21 21-4.3-4.3'),
                    xmlns='http://www.w3.org/2000/svg',
                    width='24',
                    height='24',
                    viewbox='0 0 24 24',
                    fill='none',
                    stroke='currentColor',
                    stroke_width='2',
                    stroke_linecap='round',
                    stroke_linejoin='round',
                    cls='lucide lucide-search-icon lucide-search'
                ),
                HTMLInput(type='text', value='', placeholder='Search entries...', autocomplete='off', autocorrect='off', spellcheck='false', aria_autocomplete='list', role='combobox', aria_expanded='false', aria_controls=f'select-{signal}-listbox', aria_labelledby=f'select-{signal}-trigger')
            ),
            Div(
                *children,
                role='listbox',
                id=f'select-{signal}-listbox',
                aria_orientation='vertical',
                aria_labelledby=f'select-{signal}-trigger'
            ),
            id=f'select-{signal}-popover',
            data_popover=True,
            aria_hidden='false',
            cls=cls,
            **attrs,
        )

def SelectItem(
    value: str,
    label: str | None = None,
    signal: str | None = None,
    disabled: bool = False,
    selected: bool = False,
    cls: str = "",
    **attrs: Any,
) -> HtmlString:
    label = label or value
    signal = signal or "select"
    id = f'select-{signal}-items-{uuid4().hex[:8]}'
    return Div(label, id=id, role='option', data_value=value,  disabled=disabled, cls=cls, **attrs)

def SelectGroup(
    *children,
    label: str,
    signal: str | None = None,
    cls: str = "",
    **attrs: Any,
) -> HtmlString:
    signal = signal or "select"
    id = f'group-label-select-{signal}-items-{uuid4().hex[:8]}'
    return Div(
            Div(label, role='heading', id=id),
           *children,
            role='group',
            aria_labelledby=id
        )

def SelectLabel(
    text: str,
    cls: str = "",
    **attrs: Any,
) -> HtmlString:
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
    ) -> HtmlString:
    # Generate signal if not provided
    if not signal:
        signal = f"select_{uuid4().hex[:8]}"

    # Use the signal-based ID that SelectTrigger expects
    select_id = f"{signal}-trigger"

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
        HTMLLabel(
            label,
            Span(" *", cls="text-destructive") if required else "",
            for_=select_id,
            cls=cn("block text-sm font-medium mb-1.5", label_cls),
        ),
        Select(
            SelectTrigger(
                SelectValue(value or placeholder, signal=signal),
                signal=signal,
                cls=select_cls,
                disabled=disabled,
                # aria_invalid="true" if error_text else None,
                # Don't override the ID - SelectTrigger will set it correctly
            ),
            SelectContent(*build_options(options), signal=signal),
            initial_value=value,
            signal=signal,
            name=name or signal,
            **attrs,
        ),
        error_text and HTMLP(error_text, cls="text-sm text-destructive mt-1.5"),
        helper_text
        and not error_text
        and HTMLP(helper_text, cls="text-sm text-muted-foreground mt-1.5"),
        cls=cn("space-y-1.5", cls),
    )

def SelectWithLabelSimple(
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
    cls: str = "",
    label_cls: str = "",
    **attrs: Any,
) -> HtmlString:
    items = []
    for opt in options:
        if isinstance(opt, str):
            items.append(HTMLOption(value=opt, label=opt, signal=signal))
        elif isinstance(opt, tuple) and len(opt) == 2:
            items.append(HTMLOption(value=opt[0], label=opt[1], signal=signal))

    return Div(
            HTMLLabel(label, cls=cn("label", label_cls)) if label else None,
            HTMLSelect(
                HTMLOptionGroup(
                    *items,
                    label=label,
                ),
                value=value,
                placeholder=placeholder,
                name=name,
                disabled=disabled,
                required=required,
                cls=cn("select ", cls),
                bind=signal,
                **attrs,
            ),
            cls="grid gap-3"
        )
