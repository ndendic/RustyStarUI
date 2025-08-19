"""Theme toggle component using Datastar for reactivity.

Dependencies: button
"""

from starhtml import FT, Div, Icon, Span
from starhtml.datastar import ds_effect, ds_on_click, ds_on_load, ds_show, ds_signals

from .button import Button


def ThemeToggle(alt_theme="dark", default_theme="light", **attrs) -> FT:
    """Reactive theme toggle that syncs with fouc_script."""

    return Div(
        Button(
            Span(Icon("ph:moon-bold", width="20", height="20"), ds_show("!$isDark")),
            Span(Icon("ph:sun-bold", width="20", height="20"), ds_show("$isDark")),
            ds_on_click("$isDark = !$isDark"),
            variant="ghost",
            aria_label="Toggle theme",
            cls="h-9 px-4 py-2 flex-shrink-0",
        ),
        ds_signals(isDark=False),
        ds_on_load(f"""
            const saved = localStorage.getItem('theme');
            $isDark = saved === '{alt_theme}' || (!saved && window.matchMedia('(prefers-color-scheme: dark)').matches);
        """),
        ds_effect(f"""
            document.documentElement.classList.toggle('{alt_theme}', $isDark);
            document.documentElement.setAttribute('data-theme', $isDark ? '{alt_theme}' : '{default_theme}');
            localStorage.setItem('theme', $isDark ? '{alt_theme}' : '{default_theme}');
        """),
        **attrs,
    )
