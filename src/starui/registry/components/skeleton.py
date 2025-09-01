from rusty_tags import HtmlString, Div

from .utils import cn


def Skeleton(
    *children,
    class_name: str = "",
    cls: str = "",
    **attrs,
) -> HtmlString:
    return Div(
        *children,
        data_slot="skeleton",
        cls=cn(
            "animate-pulse rounded-md bg-muted",
            class_name,
            cls,
        ),
        **attrs,
    )
