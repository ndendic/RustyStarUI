"""
Theme Toggle component documentation - Light and dark mode switching.
"""

# Component metadata for auto-discovery
TITLE = "Theme Toggle"
DESCRIPTION = "Toggle between light and dark themes with Datastar reactivity."
CATEGORY = "ui"
ORDER = 95
STATUS = "stable"

from starhtml import Div, Icon, P, Span
from starhtml.datastar import ds_show, ds_on_click, ds_on_load, ds_signals, ds_effect, toggle
from starui.registry.components.theme_toggle import ThemeToggle
from starui.registry.components.button import Button
from widgets.component_preview import ComponentPreview


def examples():
    """Generate Theme Toggle examples using ComponentPreview with tabs."""
    
    # Note: Basic theme toggle moved to hero example
    # This will be the first example after the hero
    
    # Custom outline variant
    yield ComponentPreview(
        Div(
            Button(
                Span(
                    Icon("ph:moon-bold", width="16", height="16"),
                    ds_show("!$isDark")
                ),
                Span(
                    Icon("ph:sun-bold", width="16", height="16"),
                    ds_show("$isDark")
                ),
                ds_on_click(toggle("isDark")),
                variant="outline",
                size="sm",
                aria_label="Toggle theme"
            ),
            ds_signals(isDark=False),
            ds_on_load("""
                const saved = localStorage.getItem('theme');
                const systemDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
                $isDark = saved === 'dark' || (!saved && systemDark);
            """),
            ds_effect("""
                const theme = $isDark ? 'dark' : 'light';
                document.documentElement.setAttribute('data-theme', theme);
                localStorage.setItem('theme', theme);
            """),
            cls="flex items-center justify-center"
        ),
        '''Button(
    Span(
        Icon("ph:moon-bold", width="16", height="16"),
        ds_show("!$isDark")
    ),
    Span(
        Icon("ph:sun-bold", width="16", height="16"),
        ds_show("$isDark")
    ),
    ds_on_click(toggle("isDark")),
    variant="outline",
    aria_label="Toggle theme"
)''',
        title="Custom Toggle",
        description="Custom implementation with outline button variant"
    )
    
    # Multiple toggles with controls
    yield ComponentPreview(
        Div(
            Div(
                P("Theme Controls", cls="font-medium mb-3"),
                Div(
                    ThemeToggle(cls="mr-2"),
                    Button(
                        "Reset Theme",
                        ds_on_click("localStorage.removeItem('theme'); location.reload();"),
                        variant="ghost",
                        size="sm"
                    ),
                    cls="flex items-center gap-2"
                )
            ),
            cls="space-y-4"
        ),
        '''Div(
    ThemeToggle(),
    Button(
        "Reset Theme",
        ds_on_click("localStorage.removeItem('theme'); location.reload();"),
        variant="ghost",
        size="sm"
    ),
    cls="flex items-center gap-2"
)''',
        title="With Controls",
        description="Theme toggle with reset functionality"
    )
    
    # Different button variants
    yield ComponentPreview(
        Div(
            Div(
                P("Button Variants", cls="font-medium mb-3"),
                Div(
                    ThemeToggle(),
                    Button(
                        Span(
                            Icon("ph:moon-bold", width="16", height="16"),
                            ds_show("!$theme2")
                        ),
                        Span(
                            Icon("ph:sun-bold", width="16", height="16"), 
                            ds_show("$theme2")
                        ),
                        ds_on_click(toggle("theme2")),
                        variant="secondary",
                        size="sm",
                        aria_label="Toggle theme",
                        cls="ml-2"
                    ),
                    Button(
                        Span(
                            Icon("ph:moon-bold", width="16", height="16"),
                            ds_show("!$theme3")
                        ),
                        Span(
                            Icon("ph:sun-bold", width="16", height="16"),
                            ds_show("$theme3")
                        ),
                        ds_on_click(toggle("theme3")),
                        variant="outline",
                        size="sm",
                        aria_label="Toggle theme",
                        cls="ml-2"
                    ),
                    cls="flex items-center"
                )
            ),
            ds_signals(theme2=False, theme3=False),
            cls="space-y-4"
        ),
        '''# Ghost variant (default)
ThemeToggle()

# Secondary variant
Button(
    Span(Icon("ph:moon-bold"), ds_show("!$theme")),
    Span(Icon("ph:sun-bold"), ds_show("$theme")),
    ds_on_click(toggle("theme")),
    variant="secondary",
    aria_label="Toggle theme"
)

# Outline variant  
Button(
    Span(Icon("ph:moon-bold"), ds_show("!$theme")),
    Span(Icon("ph:sun-bold"), ds_show("$theme")),
    ds_on_click(toggle("theme")),
    variant="outline",
    aria_label="Toggle theme"
)''',
        title="Button Variants",
        description="Theme toggles using different button variants"
    )


def create_theme_toggle_docs():
    """Create theme toggle documentation page using convention-based approach."""
    from utils import auto_generate_page
    
    # Hero example - basic theme toggle
    hero_example = ComponentPreview(
        Div(
            ThemeToggle(),
            P("Click to toggle between light and dark themes", cls="text-sm text-muted-foreground mt-2"),
            cls="flex flex-col items-center"
        ),
        '''ThemeToggle()'''
    )
    
    return auto_generate_page(
        TITLE,
        DESCRIPTION,
        list(examples()),
        cli_command="star add theme-toggle",
        hero_example=hero_example,
        api_reference={
            "props": [
                {
                    "name": "alt_theme",
                    "type": "str",
                    "default": "dark",
                    "description": "Alternative theme name (typically dark mode)"
                },
                {
                    "name": "default_theme", 
                    "type": "str",
                    "default": "light",
                    "description": "Default theme name (typically light mode)"
                },
                {
                    "name": "cls",
                    "type": "str",
                    "default": "''",
                    "description": "Additional CSS classes"
                }
            ]
        }
    )