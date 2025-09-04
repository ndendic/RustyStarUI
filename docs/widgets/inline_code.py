from starhtml import Div, Button, Span, FT, NotStr, Icon
from starhtml.datastar import ds_on_click, ds_show, ds_text, ds_signals
from starui.registry.components.utils import cn

try:
    from starlighter import highlight
except ImportError:
    def highlight(code: str, language: str = "python") -> str:
        return f'<pre><code class="language-{language}">{code}</code></pre>'


def InlineCode(
    code: str,
    *,
    language: str = "bash",
    cls: str = "",
    copy_button: bool = True,
    **attrs
) -> FT:
    signal = f"copied_{abs(hash(code))}"
    
    return Div(
        Div(
            NotStr(highlight(code, language)),
            copy_button and Button(
                Span(Icon("check", cls="h-3 w-3"), ds_show(f"${signal}")),
                Span(Icon("copy", cls="h-3 w-3"), ds_show(f"!${signal}")),
                Span(ds_text(f"${signal} ? 'Copied!' : 'Copy'"), cls="sr-only"),
                ds_on_click(f'@clipboard(evt.target.closest(".inline-flex").querySelector("code").textContent, "{signal}", 2000)'),
                variant="ghost",
                size="sm",
                cls="h-6 w-6 p-0 ml-3 text-muted-foreground hover:text-foreground transition-colors flex-shrink-0",
                type="button",
                aria_label="Copy code"
            ),
            cls="code-container inline-flex items-center gap-0 !py-2 !pl-4 !pr-3"
        ),
        copy_button and ds_signals({signal: False}),
        cls=cn("inline-block", cls),
        **attrs
    )