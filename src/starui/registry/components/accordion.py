from typing import Any, Literal
from uuid import uuid4

from rusty_tags import Button, Div, HtmlString, Section, Details, Summary, Svg, Path
from rusty_tags.datastar import Signals

from .utils import Icon, cn

AccordionType = Literal["single", "multiple"]


def Accordion(
    *children: Any,
    type: AccordionType = "single",
    collapsible: bool = False,
    default_value: str | list[str] | None = None,
    signal: str = "",
    cls: str = "accordion",
    **attrs: Any,
) -> HtmlString:
    signal = signal or f"accordion_{uuid4().hex[:8]}"

    match (type, default_value):
        case ("single", _):
            initial_value = default_value or ""
        case ("multiple", None):
            initial_value = []
        case ("multiple", str() as val):
            initial_value = [val]
        case ("multiple", val):
            initial_value = val

    processed_children = [
        child(signal, type, collapsible) if callable(child) else child
        for child in children
    ]

    return Section(
        *processed_children,
        signals=Signals(**{signal: initial_value}),
        data_type=type,
        data_collapsible=str(collapsible).lower(),
        cls=cls,
        **attrs,
    )


def AccordionItem(
    *children: Any,
    summary: str | Any,
    value: str,
    cls: str = "group border-b last:border-b-0",
    **attrs: Any,
) -> HtmlString:
    def create_item(signal, type="single", collapsible=False):
        processed_children = [
            child(signal, type, collapsible, value) if callable(child) else child
            for child in children
        ]
        return Details(
            Summary(
                summary,
                Svg(
                    Path(d='m6 9 6 6 6-6'),
                    xmlns='http://www.w3.org/2000/svg',
                    width='24',
                    height='24',
                    viewbox='0 0 24 24',
                    fill='none',
                    stroke='currentColor',
                    stroke_width='2',
                    stroke_linecap='round',
                    stroke_linejoin='round',
                    cls='text-muted-foreground pointer-events-none size-4 shrink-0 translate-y-0.5 transition-transform duration-200 group-open:rotate-180'
                ),
                cls='flex flex-1 items-start justify-between gap-4 py-4 text-left text-sm font-medium hover:underline'
            ),
            *processed_children,
            data_value=value,
            cls=cls,
            **attrs,
        )

    return create_item


def AccordionTrigger(
    *children: Any,
    class_name: str = "",
    cls: str = "",
    **attrs: Any,
) -> HtmlString:
    def create_trigger(signal, type="single", collapsible=False, item_value=None):
        if not item_value:
            raise ValueError("AccordionTrigger must be used inside AccordionItem")

        is_single = type == "single"

        if is_single:
            click_expr = (
                f"${signal} = ${signal} === '{item_value}' ? '' : '{item_value}'"
                if collapsible
                else f"${signal} = '{item_value}'"
            )
            is_open_expr = f"${signal} === '{item_value}'"
        else:
            click_expr = (
                f"${signal} = ${signal}.includes('{item_value}') "
                f"? ${signal}.filter(v => v !== '{item_value}') "
                f": [...${signal}, '{item_value}']"
            )
            is_open_expr = f"${signal}.includes('{item_value}')"

        return Details(
                Summary(*children),
                on_click=click_expr,
                cls="group border-b last:border-b-0",
                **attrs,
            )

    return create_trigger


def AccordionContent(
    *children: Any,
    class_name: str = "",
    cls: str = "",
    **attrs: Any,
) -> HtmlString:
    def create_content(signal, type="single", collapsible=False, item_value=None):
        if not item_value:
            raise ValueError("AccordionContent must be used inside AccordionItem")

        show_expr = (
            f"${signal} === '{item_value}'"
            if type == "single"
            else f"${signal}.includes('{item_value}')"
        )

        return Summary(
            Div(
                *children,
                cls=cn("pb-4 pt-0", class_name),
            ),
            show=show_expr,
            cls=cn("overflow-hidden text-sm", cls),
            **attrs,
        )

    return create_content
