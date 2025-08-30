import hashlib
from starhtml import FT, Div, P, H3, Icon, Span
from starui.registry.components.tabs import Tabs, TabsContent, TabsList, TabsTrigger
from starui.registry.components.code_block import CodeBlock as BaseCodeBlock
from starui.registry.components.button import Button
from starui.registry.components.utils import cn
from starhtml.datastar import ds_on_click, ds_show, ds_signals, ds_text

def ComponentPreview(
    preview_content: FT,
    code_content: str,
    *,
    title: str | None = None,
    description: str | None = None,
    preview_class: str = "",
    copy_button: bool = True,
    default_tab: str = "preview",
    preview_id: str | None = None,
    include_imports: bool = True,
    **attrs,
) -> FT:
    if include_imports and not code_content.strip().startswith(('from starhtml import', 'from starui import')):
        code_content = f"from starhtml import *\nfrom starui import *\n\n{code_content}"
    
    preview_id = preview_id or f"preview_{hashlib.md5(code_content.encode()).hexdigest()[:8]}"

    header = None
    if title or description:
        header = Div(
            H3(title, cls="text-lg font-semibold mt-6") if title else None,
            P(description, cls="text-sm text-muted-foreground mt-1") if description else None,
            cls="mb-3"
        )

    return Div(
        header,
        Div(
            Tabs(
                TabsList(
                    TabsTrigger("Preview", id="preview"), 
                    TabsTrigger("Code", id="code"),
                ),
                TabsContent(
                    Div(
                        preview_content,
                        cls=cn("flex min-h-[350px] w-full items-center justify-center p-10", preview_class),
                    ),
                    id="preview",
                    cls="mt-2"
                ),
                TabsContent(
                    Div(
                        BaseCodeBlock(
                            code_content,
                            language="python",
                            cls="max-h-[650px] overflow-auto"
                        ),
                        _copy_button(preview_id) if copy_button else None,
                        cls="relative group overflow-x-auto"
                    ),
                    id="code",
                    cls="mt-2 overflow-x-auto min-w-0 max-w-full"
                ),
                default_id=default_tab,
                signal=f"{preview_id}_tab",
                cls="w-full min-w-0"
            ),
            cls="rounded-lg border p-6 min-w-0 overflow-hidden",
        ),
        ds_signals({f"copied_{preview_id}": False}) if copy_button else None,
        cls=cn("relative mb-8 w-full", attrs.get("cls", "")),
        **{k: v for k, v in attrs.items() if k != "cls"},
    )

def _copy_button(preview_id: str) -> FT:
    signal = f"copied_{preview_id}"
    
    return Button(
        Span(Icon("lucide:check", cls="h-3 w-3"), ds_show(f"${signal}")),
        Span(Icon("lucide:copy", cls="h-3 w-3"), ds_show(f"!${signal}")),
        Span(ds_text(f"${signal} ? 'Copied!' : 'Copy'"), cls="sr-only"),
        ds_on_click(f'@clipboard(evt.target.closest(".relative.group").querySelector("code").textContent, "{signal}", 2000)'),
        variant="ghost",
        size="sm",
        cls="absolute top-3 right-3 h-7 w-7 p-0 text-muted-foreground hover:text-foreground hover:bg-muted opacity-0 group-hover:opacity-100 transition-all duration-200",
        type="button",
        aria_label="Copy code"
    )