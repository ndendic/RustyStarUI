from starhtml import FT, Div

from .utils import cn


def Skeleton(
    *children,
    class_name: str = "",
    cls: str = "",
    **attrs,
) -> FT:
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
