"""
Badge component documentation - Convention-based functional approach.
Clean, minimal, and easy to extend.
"""

# Component metadata for auto-discovery
TITLE = "Badge"
DESCRIPTION = "Displays a badge or a component that looks like a badge."
CATEGORY = "ui"
ORDER = 20
STATUS = "stable"

from starhtml import Div, P, Span, Icon, A, H3, H4
from starhtml.datastar import ds_on_click, ds_show, ds_signals, ds_text
from starui.registry.components.badge import Badge
from starui.registry.components.button import Button
from widgets.component_preview import ComponentPreview


def examples():
    """Generate badge examples using ComponentPreview with tabs."""
    
    # Note: First example will be used as hero if no explicit hero_example is provided
    # We'll define hero_example explicitly in create_badge_docs
    
    # Basic variants (will not be yielded if used as hero)
    yield ComponentPreview(
        Div(
            Badge("Badge", cls="mr-2"),
            Badge("Secondary", variant="secondary", cls="mr-2"),
            Badge("Destructive", variant="destructive", cls="mr-2"),
            Badge("Outline", variant="outline"),
            cls="flex flex-wrap gap-2"
        ),
        '''from starui.registry.components.badge import Badge

Badge("Badge")
Badge("Secondary", variant="secondary")
Badge("Destructive", variant="destructive")
Badge("Outline", variant="outline")''',
        title="Badge Variants",
        description="Different visual styles for badges"
    )
    
    # With icons
    yield ComponentPreview(
        Div(
            Badge(Icon("star", cls="w-3 h-3"), "Featured", cls="mr-2"),
            Badge(
                Div(cls="w-2 h-2 bg-green-500 rounded-full"),
                "Online",
                variant="outline"
            ),
            cls="flex gap-2"
        ),
        '''from starui.registry.components.badge import Badge
from starhtml import Icon, Div

Badge(Icon("star", cls="w-3 h-3"), "Featured")
Badge(
    Div(cls="w-2 h-2 bg-green-500 rounded-full"),
    "Online",
    variant="outline"
)''',
        title="Badges with Icons",
        description="Enhance badges with icons or status indicators"
    )
    
    # Different content types
    yield ComponentPreview(
        Div(
            Badge("99+", variant="destructive", cls="mr-2"),
            Badge("v2.1.0", variant="secondary", cls="mr-2"),
            Badge("NEW", variant="default"),
            cls="flex gap-2"
        ),
        '''from starui.registry.components.badge import Badge

Badge("99+", variant="destructive")
Badge("v2.1.0", variant="secondary")
Badge("NEW", variant="default")''',
        title="Content Types",
        description="Numbers, versions, and labels"
    )
    
    # As links
    yield ComponentPreview(
        Div(
            Badge("Documentation", href="/docs", variant="outline", cls="mr-2"),
            Badge(
                Icon("external-link", cls="w-3 h-3"),
                "GitHub",
                href="https://github.com",
                variant="secondary"
            ),
            cls="flex gap-2"
        ),
        '''from starui.registry.components.badge import Badge
from starhtml import Icon

Badge("Documentation", href="/docs", variant="outline")
Badge(
    Icon("external-link", cls="w-3 h-3"),
    "GitHub",
    href="https://github.com",
    variant="secondary"
)''',
        title="Link Badges",
        description="Badges that act as links"
    )
    
    # Status indicators
    yield ComponentPreview(
        Div(
            Badge("Active", variant="default", cls="mr-2"),
            Badge("Pending", variant="secondary", cls="mr-2"),
            Badge("Error", variant="destructive", cls="mr-2"),
            Badge("Draft", variant="outline"),
            cls="flex gap-2 flex-wrap"
        ),
        '''from starui.registry.components.badge import Badge

Badge("Active", variant="default")
Badge("Pending", variant="secondary")
Badge("Error", variant="destructive")
Badge("Draft", variant="outline")''',
        title="Status Indicators",
        description="Use badges to show different states"
    )
    
    # Category tags
    yield ComponentPreview(
        Div(
            Badge("React", variant="outline", cls="mr-2"),
            Badge("TypeScript", variant="outline", cls="mr-2"),
            Badge("Next.js", variant="outline", cls="mr-2"),
            Badge("TailwindCSS", variant="outline"),
            cls="flex gap-2 flex-wrap"
        ),
        '''from starui.registry.components.badge import Badge

Badge("React", variant="outline")
Badge("TypeScript", variant="outline")
Badge("Next.js", variant="outline")
Badge("TailwindCSS", variant="outline")''',
        title="Category Tags",
        description="Use badges as category or technology tags"
    )
    
    # Notification badges - Professional implementation based on research
    yield ComponentPreview(
        Div(
            # Icon badges with properly proportioned icons and badges
            Div(
                Icon("bell", width="40", height="40", cls="text-muted-foreground block"),
                Span("3", 
                     cls="absolute -top-1 -right-1 z-10 min-w-[1.25rem] h-5 px-1 rounded-full bg-destructive text-destructive-foreground text-xs font-bold flex items-center justify-center ring-2 ring-background"),
                cls="relative inline-block"
            ),
            Div(
                Icon("mail", width="40", height="40", cls="text-muted-foreground block"),
                Span("12", 
                     cls="absolute -top-1 -right-1 z-10 min-w-[1.25rem] h-5 px-1 rounded-full bg-primary text-primary-foreground text-xs font-bold flex items-center justify-center ring-2 ring-background"),
                cls="relative inline-block"
            ),
            Div(
                Icon("inbox", width="40", height="40", cls="text-muted-foreground block"),
                Span("99+", 
                     cls="absolute -top-1 -right-1 z-10 min-w-[1.5rem] h-5 px-1 rounded-full bg-destructive text-destructive-foreground text-xs font-bold flex items-center justify-center ring-2 ring-background"),
                cls="relative inline-block"
            ),
            cls="flex items-center gap-8"
        ),
        '''from starhtml import Div, Icon, Span

# Icon with notification counter
Div(
    Icon("bell", width="40", height="40", cls="text-muted-foreground"),
    Span("3", cls="absolute -top-1 -right-1 min-w-[1.25rem] h-5 px-1 rounded-full bg-destructive text-white text-xs font-bold flex items-center justify-center ring-2 ring-white"),
    cls="relative inline-block"
)''',
        title="Notification Badges on Icons",
        description="Show notification counts overlapping icons with professional positioning"
    )
    
    # Avatar badges - Professional status indicators for user interfaces
    yield ComponentPreview(
        Div(
            # Avatar with unread message count
            Div(
                Div("JD", cls="size-10 rounded-full bg-blue-500 flex items-center justify-center text-white font-semibold text-sm"),
                Span("3", cls="absolute -top-1 -right-1 size-4 rounded-full bg-red-500 text-white text-xs font-bold flex items-center justify-center ring-2 ring-white"),
                cls="relative inline-block"
            ),
            # Avatar with online status - Discord-style masked ring
            Div(
                Div("AS", cls="size-10 rounded-full bg-green-500 flex items-center justify-center text-white font-semibold text-sm"),
                Span(cls="absolute bottom-0 right-0 size-3 rounded-full bg-green-400 shadow-[0_0_0_2px_theme(colors.background)]"),
                cls="relative inline-block"
            ),
            # Avatar with away status - Discord-style masked ring  
            Div(
                Div("MK", cls="size-10 rounded-full bg-orange-500 flex items-center justify-center text-white font-semibold text-sm"),
                Span(cls="absolute bottom-0 right-0 size-3 rounded-full bg-orange-400 shadow-[0_0_0_2px_theme(colors.background)]"),
                cls="relative inline-block"
            ),
            # Avatar with verified badge
            Div(
                Div("VU", cls="size-10 rounded-full bg-purple-500 flex items-center justify-center text-white font-semibold text-sm"),
                Span(
                    Icon("check", width="12", height="12", cls="text-white font-bold"),
                    cls="absolute -bottom-0.5 -right-0.5 size-4 rounded-full bg-blue-600 flex items-center justify-center shadow-[0_0_0_2px_theme(colors.background)]"
                ),
                cls="relative inline-block"
            ),
            cls="flex items-center gap-8"
        ),
        '''from starhtml import Div, Span, Icon

# Avatar with message count
Div(
    Div("JD", cls="size-10 rounded-full bg-blue-500 flex items-center justify-center text-white font-semibold"),
    Span("3", cls="absolute -top-1 -right-1 size-4 rounded-full bg-red-500 text-white text-xs font-bold flex items-center justify-center ring-2 ring-white"),
    cls="relative inline-block"
)

# Avatar with status dot (Discord-style masked ring)
Div(
    Div("AS", cls="size-10 rounded-full bg-green-500 flex items-center justify-center text-white font-semibold"),
    Span(cls="absolute bottom-0 right-0 size-3 rounded-full bg-green-400 shadow-[0_0_0_2px_theme(colors.background)]"),
    cls="relative inline-block"
)''',
        title="Avatar Status Indicators", 
        description="Avatar status indicators with clean background masking"
    )
    
    # Size variations (custom implementation)
    yield ComponentPreview(
        Div(
            Badge("Small", cls="px-1.5 py-0.5 text-xs mr-2"),
            Badge("Default", cls="px-2 py-0.5 text-xs mr-2"),
            Badge("Large", cls="px-3 py-1 text-sm"),
            cls="flex gap-2 items-center"
        ),
        '''from starui.registry.components.badge import Badge

Badge("Small", cls="px-1.5 py-0.5 text-xs")
Badge("Default", cls="px-2 py-0.5 text-xs")
Badge("Large", cls="px-3 py-1 text-sm")''',
        title="Size Variations",
        description="Custom size variations for different use cases"
    )


def create_badge_docs():
    """Create badge documentation page using convention-based approach."""
    from utils import auto_generate_page
    
    # Hero example - comprehensive showcase matching ShadCN
    hero_example = ComponentPreview(
        Div(
            # First row - all variants
            Div(
                Badge("Badge"),
                Badge("Secondary", variant="secondary"),
                Badge("Destructive", variant="destructive"),
                Badge("Outline", variant="outline"),
                cls="flex w-full flex-wrap gap-2"
            ),
            # Second row - practical examples
            Div(
                Badge(
                    Icon("badge-check", cls="w-3 h-3 mr-1"),
                    "Verified",
                    variant="secondary",
                    cls="bg-blue-500 text-white dark:bg-blue-600"
                ),
                Badge(
                    "8",
                    cls="h-5 min-w-[1.25rem] rounded-full px-1 font-mono tabular-nums"
                ),
                Badge(
                    "99",
                    variant="destructive",
                    cls="h-5 min-w-[1.25rem] rounded-full px-1 font-mono tabular-nums"
                ),
                Badge(
                    "20+",
                    variant="outline",
                    cls="h-5 min-w-[1.25rem] rounded-full px-1 font-mono tabular-nums"
                ),
                cls="flex w-full flex-wrap gap-2"
            ),
            cls="flex flex-col items-center gap-2"
        ),
        '''# Basic variants
Badge("Badge")
Badge("Secondary", variant="secondary")
Badge("Destructive", variant="destructive")
Badge("Outline", variant="outline")

# Practical examples
Badge(
    Icon("badge-check", cls="w-3 h-3 mr-1"),
    "Verified",
    variant="secondary",
    cls="bg-blue-500 text-white dark:bg-blue-600"
)
Badge("8", cls="h-5 min-w-[1.25rem] rounded-full px-1 font-mono tabular-nums")
Badge("99", variant="destructive", cls="h-5 min-w-[1.25rem] rounded-full px-1 font-mono tabular-nums")
Badge("20+", variant="outline", cls="h-5 min-w-[1.25rem] rounded-full px-1 font-mono tabular-nums")''',
        title="",
        description=""
    )
    
    return auto_generate_page(
        TITLE,
        DESCRIPTION,
        list(examples()),
        cli_command="star add badge",
        hero_example=hero_example,
        component_slug="badge",
        api_reference={
            "props": [
                {
                    "name": "variant",
                    "type": "Literal['default', 'secondary', 'destructive', 'outline']",
                    "default": "'default'",
                    "description": "Badge visual variant"
                },
                {
                    "name": "href",
                    "type": "str | None",
                    "default": "None",
                    "description": "Optional URL to make badge a link"
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