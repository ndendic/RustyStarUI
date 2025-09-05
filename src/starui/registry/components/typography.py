from typing import Literal

from rusty_tags import H1 as HTMLH1
from rusty_tags import H2 as HTMLH2
from rusty_tags import H3 as HTMLH3
from rusty_tags import H4 as HTMLH4
from rusty_tags import H5 as HTMLH5
from rusty_tags import H6 as HTMLH6
from rusty_tags import Blockquote as HTMLBlockquote
from rusty_tags import Code as HTMLCode
from rusty_tags import Div, HtmlString, Ol, Ul
from rusty_tags import Em as HTMLEm
from rusty_tags import Figcaption as HTMLFigcaption
from rusty_tags import Figure as HTMLFigure
from rusty_tags import Hr as HTMLHr
from rusty_tags import Kbd as HTMLKbd
from rusty_tags import Mark as HTMLMark
from rusty_tags import P as HTMLP
from rusty_tags import Strong as HTMLStrong

from .utils import cn, cva

# Type definitions
TextVariant = Literal["body", "lead", "large", "small", "muted"]
ProseSize = Literal["sm", "base", "lg", "xl"]

# CVA configurations
heading_variants = cva(
    base="scroll-m-20 tracking-tight first:mt-0",
    config={
        "variants": {
            "level": {
                "h1": "text-4xl font-extrabold leading-tight mb-8",
                "h2": "text-3xl font-semibold leading-tight mt-10 mb-6",
                "h3": "text-2xl font-semibold leading-tight mt-8 mb-4",
                "h4": "text-xl font-semibold leading-snug mt-6 mb-3",
                "h5": "text-lg font-semibold leading-snug mt-4 mb-2",
                "h6": "text-base font-semibold leading-snug mt-4 mb-2",
            },
            "section": {
                "true": "border-b pb-2",
                "false": "",
            },
        },
        "defaultVariants": {"section": "false"},
    },
)

text_variants = cva(
    base="",
    config={
        "variants": {
            "variant": {
                "body": "leading-7 mb-6 [&:not(:first-child)]:mt-0",
                "lead": "text-xl text-muted-foreground mb-6",
                "large": "text-lg font-semibold mb-6",
                "small": "text-sm font-medium leading-none",
                "muted": "text-sm text-muted-foreground",
            }
        },
        "defaultVariants": {"variant": "body"},
    },
)

prose_variants = cva(
    base="max-w-none text-foreground prose dark:prose-invert prose-headings:text-foreground prose-a:text-primary",
    config={
        "variants": {
            "size": {
                "sm": "prose-sm",
                "base": "prose",
                "lg": "prose-lg",
                "xl": "prose-xl",
            }
        },
        "defaultVariants": {"size": "base"},
    },
)


def Display(*children, class_name="", cls="", **attrs) -> HtmlString:
    return HTMLH1(
        *children,
        cls=cn("text-6xl font-extrabold leading-none mb-8 first:mt-0", class_name, cls),
        **attrs,
    )


def H1(*children, class_name="", cls="", **attrs) -> HtmlString:
    return HTMLH1(
        *children, cls=cn(heading_variants(level="h1"), class_name, cls), **attrs
    )


def H2(*children, section=False, class_name="", cls="", **attrs) -> HtmlString:
    return HTMLH2(
        *children,
        cls=cn(
            heading_variants(level="h2", section=str(section).lower()), class_name, cls
        ),
        **attrs,
    )


def H3(*children, class_name="", cls="", **attrs) -> HtmlString:
    return HTMLH3(
        *children, cls=cn(heading_variants(level="h3"), class_name, cls), **attrs
    )


def H4(*children, class_name="", cls="", **attrs) -> HtmlString:
    return HTMLH4(
        *children, cls=cn(heading_variants(level="h4"), class_name, cls), **attrs
    )


def H5(*children, class_name="", cls="", **attrs) -> HtmlString:
    return HTMLH5(
        *children, cls=cn(heading_variants(level="h5"), class_name, cls), **attrs
    )


def H6(*children, class_name="", cls="", **attrs) -> HtmlString:
    return HTMLH6(
        *children, cls=cn(heading_variants(level="h6"), class_name, cls), **attrs
    )


def P(*children, class_name="", cls="", **attrs) -> HtmlString:
    return HTMLP(
        *children, cls=cn(text_variants(variant="body"), class_name, cls), **attrs
    )


def Lead(*children, class_name="", cls="", **attrs) -> HtmlString:
    return HTMLP(
        *children, cls=cn(text_variants(variant="lead"), class_name, cls), **attrs
    )


def Large(*children, class_name="", cls="", **attrs) -> HtmlString:
    return Div(
        *children, cls=cn(text_variants(variant="large"), class_name, cls), **attrs
    )


def Small(*children, class_name="", cls="", **attrs) -> HtmlString:
    return Div(*children, cls=cn("text-sm font-medium", class_name, cls), **attrs)


def Muted(*children, class_name="", cls="", **attrs) -> HtmlString:
    return HTMLP(
        *children, cls=cn(text_variants(variant="muted"), class_name, cls), **attrs
    )


def Subtitle(*children, class_name="", cls="", **attrs) -> HtmlString:
    return HTMLP(
        *children,
        cls=cn("text-lg leading-relaxed text-muted-foreground mb-6", class_name, cls),
        **attrs,
    )


def Caption(*children, class_name="", cls="", **attrs) -> HtmlString:
    return Div(
        *children,
        cls=cn(
            "text-xs uppercase tracking-wider text-muted-foreground mb-2",
            class_name,
            cls,
        ),
        **attrs,
    )


def Text(*children, variant="body", class_name="", cls="", **attrs) -> HtmlString:
    return HTMLP(
        *children, cls=cn(text_variants(variant=variant), class_name, cls), **attrs
    )


def InlineCode(*children, class_name="", cls="", **attrs) -> HtmlString:
    return HTMLCode(
        *children,
        cls=cn(
            "relative rounded bg-muted px-[0.3rem] py-[0.2rem] font-mono text-sm font-semibold",
            class_name,
            cls,
        ),
        **attrs,
    )


def Blockquote(*children, class_name="", cls="", **attrs) -> HtmlString:
    return HTMLBlockquote(
        *children, cls=cn("mt-6 border-l-2 pl-6 italic", class_name, cls), **attrs
    )


def List(*children, ordered=False, class_name="", cls="", **attrs) -> HtmlString:
    classes = cn(
        "my-6 ml-6", "list-decimal" if ordered else "list-disc", class_name, cls
    )
    return (Ol if ordered else Ul)(*children, cls=classes, **attrs)


def Prose(*children, size: ProseSize = "base", class_name="", cls="", **attrs) -> HtmlString:
    return Div(*children, cls=cn(prose_variants(size=size), class_name, cls), **attrs)


def Kbd(*children, class_name="", cls="", **attrs) -> HtmlString:
    return HTMLKbd(
        *children,
        cls=cn(
            "pointer-events-none inline-flex h-5 select-none items-center gap-1 rounded border bg-muted px-1.5 font-mono text-xs font-medium text-muted-foreground",
            class_name,
            cls,
        ),
        **attrs,
    )


def Mark(*children, class_name="", cls="", **attrs) -> HtmlString:
    return HTMLMark(
        *children,
        cls=cn(
            "bg-yellow-200 dark:bg-yellow-800/30 px-1 py-0.5 rounded", class_name, cls
        ),
        **attrs,
    )


def Strong(*children, class_name="", cls="", **attrs) -> HtmlString:
    return HTMLStrong(*children, cls=cn("font-semibold", class_name, cls), **attrs)


def Em(*children, class_name="", cls="", **attrs) -> HtmlString:
    return HTMLEm(*children, cls=cn("italic", class_name, cls), **attrs)


def Hr(class_name="", cls="", **attrs) -> HtmlString:
    return HTMLHr(cls=cn("my-8 border-0 h-px bg-border", class_name, cls), **attrs)


def Figure(*children, class_name="", cls="", **attrs) -> HtmlString:
    return HTMLFigure(*children, cls=cn("my-8 space-y-3", class_name, cls), **attrs)


def Figcaption(*children, class_name="", cls="", **attrs) -> HtmlString:
    return HTMLFigcaption(
        *children,
        cls=cn("text-sm text-muted-foreground text-center italic", class_name, cls),
        **attrs,
    )
