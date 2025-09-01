from rusty_tags import Div, HtmlString
from rusty_tags import Span as HTMLSpan
from rusty_tags.datastar import Signals

from .button import Button
from .utils import Icon


def ThemeToggle(alt_theme="dark", default_theme="light", **attrs) -> HtmlString:
    """Reactive theme toggle supporting arbitrary theme names."""

    return Div(
        Button(
            HTMLSpan(Icon("ph:moon-bold", width="20", height="20"), show="!$isAlt"),
            HTMLSpan(Icon("ph:sun-bold", width="20", height="20"), show="$isAlt"),
            on_click="$isAlt = !$isAlt",
            variant="ghost",
            aria_label="Toggle theme",
            cls="h-9 px-4 py-2 flex-shrink-0",
        ),
        signals=Signals(isAlt=False),
        on_load=f"$isAlt = localStorage.getItem('theme') === '{alt_theme}' || "
                f"(!localStorage.getItem('theme') && window.matchMedia('(prefers-color-scheme: dark)').matches)",
        effect=f"""
            const theme = $isAlt ? '{alt_theme}' : '{default_theme}';
            document.documentElement.classList.toggle('{alt_theme}', $isAlt);
            document.documentElement.setAttribute('data-theme', theme);
            localStorage.setItem('theme', theme);
        """,
        **attrs,
    )
