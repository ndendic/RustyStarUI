from rusty_tags import Div, HtmlString, Span
from rusty_tags.datastar import Signals, if_, toggle
from starui.registry.components.button import Button
from starui.registry.components.utils import Icon, cn
from starui.registry.components.code_block import CodeBlock as BaseCodeBlock


def CodeBlock(
    code: str,
    language: str = "python",
    show_copy: bool = True,
    collapsible: bool = True,
    default_collapsed: bool = False,
    cls: str = "",
    **attrs
) -> HtmlString:
    code_id = f"code_{abs(hash(code))}"
    collapsed_signal = f"collapsed_{code_id}"
    
    header_cls = cn(
        "flex items-center justify-between px-3 py-2",
        collapsible and "cursor-pointer select-none hover:bg-muted/50 transition-colors",
        if_(f"${collapsed_signal}", "", "border-b border-border/50") if collapsible else "border-b border-border/50"
    )
    
    return Div(
        Div(
            Div(
                _chevron_button(collapsed_signal) if collapsible else Div(cls="w-6"),
                Span(language, cls="text-xs font-medium text-muted-foreground"),
                _copy_button(code_id, code) if show_copy else Div(cls="w-8"),
                **({"on_click": toggle(collapsed_signal)} if collapsible else {}),
                cls=header_cls
            ),
            Div(
                BaseCodeBlock(code, language, cls="font-mono text-sm !border-0 !border-none"),
                data_class={
                    "max-h-0": f"${collapsed_signal}",
                    "overflow-hidden": f"${collapsed_signal}",
                    "max-h-[2000px]": f"!${collapsed_signal}"
                },
                cls="transition-all duration-300 ease-in-out"
            ),
            signals=Signals({
                collapsed_signal: default_collapsed,
                f"copied_{code_id}": False
            }),
            cls="bg-muted/30 border border-border rounded-lg overflow-hidden group"
        ),
        cls=cn("relative mb-6", cls),
        **attrs
    )



def _chevron_button(collapsed_signal: str) -> HtmlString:
    return Div(
        Span(
            Icon("lucide:chevron-up", cls="h-4 w-4"),
            data_class={
                "rotate-180": f"${collapsed_signal}",
                "rotate-0": f"!${collapsed_signal}"
            },
            cls="inline-block transition-transform duration-300"
        ),
        on_click=f"evt.stopPropagation(); {toggle(collapsed_signal)}",
        role="button",
        tabindex="0",
        aria_label="Toggle code block",
        cls="inline-flex items-center justify-center h-6 w-6 text-muted-foreground hover:text-foreground cursor-pointer"
    )


def _copy_button(code_id: str, code: str) -> HtmlString:
    signal = f"copied_{code_id}"
    
    return Button(
        Span(Icon("lucide:check", cls="h-3 w-3"), show=f"${signal}"),
        Span(Icon("lucide:copy", cls="h-3 w-3"), show=f"!${signal}"),
        Span(text=f"${signal} ? 'Copied!' : 'Copy'", cls="sr-only"),
        on_click=f'evt.stopPropagation(); @clipboard(evt.target.closest(".group").querySelector("code").textContent, "{signal}", 2000)',
        variant="ghost",
        size="sm",
        cls="h-5 w-5 p-0 text-muted-foreground hover:text-foreground hover:bg-muted transition-all duration-200",
        type="button",
        aria_label="Copy code"
    )