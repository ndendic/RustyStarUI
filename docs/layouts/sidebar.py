from typing import Any
from starhtml import *


def DocsSidebar(
    sections: list[dict[str, Any]] | None = None,
    class_name: str = "",
    **attrs
) -> FT:
    sections = sections or []
    
    return Div(
        Aside(
            Div(
                Nav(
                    *[_sidebar_section(section) for section in sections],
                    cls="grid items-start px-2 text-sm font-medium lg:px-4",
                ),
                cls="relative h-full py-2",
                style="overflow-y: auto; scrollbar-width: thin; scrollbar-color: transparent transparent;",
            ),
            cls="hidden xl:block xl:sticky xl:top-14 xl:w-64 xl:h-[calc(100vh-3.5rem)] xl:bg-background xl:border-r xl:border-border",
        ),
        Div(cls="hidden xl:block xl:w-64 xl:shrink-0"),
    )


def MobileSidebar(sections: list[dict[str, Any]] | None = None) -> FT:
    sections = sections or []
    
    return Nav(
        *[_sidebar_section(section) for section in sections],
        cls="grid items-start px-4 text-sm font-medium pt-6 bg-background h-full overflow-y-auto space-y-2",
    )


def _sidebar_section(section: dict[str, Any]) -> FT:
    return Div(
        H4(
            section.get("title", ""),
            cls="mb-4 px-2 text-sm font-semibold text-foreground"
        ) if section.get("title") else "",
        Div(
            *[_sidebar_item(item) for item in section.get("items", [])],
            cls="grid grid-flow-row auto-rows-max text-sm mb-6 space-y-1"
        )
    )


def _sidebar_item(item: dict[str, Any]) -> FT:
    is_active = item.get("active", False)
    is_disabled = item.get("disabled", False)
    
    if is_disabled:
        return Span(
            item.get("label", ""),
            cls="flex w-full items-center rounded-md p-2 text-sm text-muted-foreground cursor-not-allowed opacity-60"
        )
    
    return A(
        item.get("label", ""),
        href=item.get("href", "#"),
        cls=f"flex w-full items-center rounded-md p-2 text-sm transition-colors hover:bg-accent hover:text-accent-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring {'bg-accent text-accent-foreground font-medium' if is_active else 'text-muted-foreground'}"
    )