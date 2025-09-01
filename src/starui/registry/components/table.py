from typing import Any

from rusty_tags import (
    HtmlString,
    Caption,
    Div,
    Tbody,
    Td,
    Tfoot,
    Th,
    Thead,
    Tr,
)
from rusty_tags import (
    Table as HTMLTable,
)

from .utils import cn


def Table(
    *children: Any,
    class_name: str = "",
    cls: str = "",
    **attrs: Any,
) -> HtmlString:
    classes = cn("w-full caption-bottom text-sm", class_name, cls)
    return Div(
        HTMLTable(*children, data_slot="table", cls=classes, **attrs),
        data_slot="table-container",
        cls="relative w-full overflow-x-auto",
    )


def TableHeader(
    *children: Any,
    class_name: str = "",
    cls: str = "",
    **attrs: Any,
) -> HtmlString:
    classes = cn("[&_tr]:border-b [&_tr]:border-input", class_name, cls)
    return Thead(*children, data_slot="table-header", cls=classes, **attrs)


def TableBody(
    *children: Any,
    class_name: str = "",
    cls: str = "",
    **attrs: Any,
) -> HtmlString:
    classes = cn("[&_tr:last-child]:border-0", class_name, cls)
    return Tbody(*children, data_slot="table-body", cls=classes, **attrs)


def TableFooter(
    *children: Any,
    class_name: str = "",
    cls: str = "",
    **attrs: Any,
) -> HtmlString:
    classes = cn(
        "bg-muted/50 border-t border-input font-medium [&>tr]:last:border-b-0",
        class_name,
        cls,
    )
    return Tfoot(*children, data_slot="table-footer", cls=classes, **attrs)


def TableRow(
    *children: Any,
    selected: bool = False,
    class_name: str = "",
    cls: str = "",
    **attrs: Any,
) -> HtmlString:
    classes = cn(
        "border-b border-input transition-colors hover:bg-muted/50 data-[state=selected]:bg-muted",
        class_name,
        cls,
    )

    if selected:
        attrs["data_state"] = "selected"

    return Tr(*children, data_slot="table-row", cls=classes, **attrs)


def TableHead(
    *children: Any,
    class_name: str = "",
    cls: str = "",
    **attrs: Any,
) -> HtmlString:
    classes = cn(
        "text-foreground h-10 px-2 text-left align-middle font-medium whitespace-nowrap [&:has([role=checkbox])]:pr-0 [&>[role=checkbox]]:translate-y-[2px]",
        class_name,
        cls,
    )
    return Th(*children, data_slot="table-head", cls=classes, **attrs)


def TableCell(
    *children: Any,
    class_name: str = "",
    cls: str = "",
    **attrs: Any,
) -> HtmlString:
    classes = cn(
        "p-2 align-middle whitespace-nowrap [&:has([role=checkbox])]:pr-0 [&>[role=checkbox]]:translate-y-[2px]",
        class_name,
        cls,
    )
    return Td(*children, data_slot="table-cell", cls=classes, **attrs)


def TableCaption(
    *children: Any,
    class_name: str = "",
    cls: str = "",
    **attrs: Any,
) -> HtmlString:
    classes = cn("mt-4 text-sm text-muted-foreground", class_name, cls)
    return Caption(*children, data_slot="table-caption", cls=classes, **attrs)
