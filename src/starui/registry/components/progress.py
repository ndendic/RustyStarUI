"""Progress component - Loading and completion indicators."""

from typing import Any
from uuid import uuid4

from rusty_tags import Div, HtmlString
from rusty_tags.datastar import Signals

from .utils import cn


def Progress(
    progress_value: float | None = None,
    max_value: float = 100,
    signal: str = "",
    class_name: str = "",
    cls: str = "",
    **attrs: Any,
) -> HtmlString:
    signal = signal or f"progress_{str(uuid4())[:8]}"

    initial_percentage = max(
        0,
        min(
            100,
            (progress_value / max_value) * 100
            if progress_value is not None and max_value > 0
            else 0,
        ),
    )
    initial_percentage = (
        int(initial_percentage)
        if initial_percentage.is_integer()
        else initial_percentage
    )

    return Div(
        Div(
            style_={"width": f"${signal} + '%'"},
            cls="bg-primary h-full transition-all duration-300 ease-out",
            style=f"'width: {initial_percentage}%'",
        ),
        signals=Signals({signal: initial_percentage}),
        role="progressbar",
        aria_valuemin="0",
        aria_valuemax=str(max_value),
        aria_valuenow=str(progress_value) if progress_value is not None else None,
        cls=cn(
            "bg-primary/20 relative h-2 w-full overflow-hidden rounded-full",
            class_name,
            cls,
        ),
        **attrs,
    )
