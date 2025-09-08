from typing import Any, Literal
from uuid import uuid4

from rusty_tags import Button, Details, Div, HtmlString, Path, Section, Summary, Svg
from rusty_tags.datastar import Signals

from .utils import Icon, cn


def Accordion(
    *children: Any,
    type: Literal["single", "multiple"] = "single",
    signal: str = "",
    cls: str = "accordion",
    **attrs: Any,
) -> HtmlString:
    signal = signal or f"accordion_{uuid4().hex[:8]}"

    processed_children = [
        child(signal, type) if callable(child) else child
        for child in children
    ]

    return Section(
        *processed_children,
        signals=Signals(**{signal: ""}),
        data_type=type,
        cls=cls,
        **attrs,
    )


def AccordionItem(
    *children: Any,
    summary: str | Any,
    open: bool = False,
    cls: str = "group border-b last:border-b-0",
    **attrs: Any,
) -> HtmlString:
    id = attrs.pop("id", f"accordion-item-{str(uuid4())[:8]}")
    def create_item(signal, type="single"):
        if type == "single":
            open_params = {"data_attr_open": f"${signal} === '{id}'"}
        else:
            open_params = {"open": open}

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
            Div(*children, cls="pb-4"),
            **open_params,
            on_click=f"${signal} === '{id}' ? ${signal} = '' : ${signal} = '{id}'",
            id=id,
            cls=cls,
            **attrs,
        )

    return create_item
