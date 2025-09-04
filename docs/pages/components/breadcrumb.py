"""
Breadcrumb component documentation - Navigation hierarchy paths.
"""

# Component metadata for auto-discovery
TITLE = "Breadcrumb"
DESCRIPTION = "Displays the path to the current resource using a hierarchy of links."
CATEGORY = "navigation"
ORDER = 160
STATUS = "stable"

from starhtml import Div, P, Span, Icon
from starui.registry.components.breadcrumb import (
    Breadcrumb, BreadcrumbList, BreadcrumbItem, 
    BreadcrumbLink, BreadcrumbPage, BreadcrumbSeparator, BreadcrumbEllipsis
)
from starui.registry.components.button import Button
from widgets.component_preview import ComponentPreview


def examples():
    """Generate Breadcrumb examples using ComponentPreview with tabs."""
    
    # Note: Basic breadcrumb moved to hero example
    # This will be the first example after the hero
    
    # Custom separator
    yield ComponentPreview(
        Breadcrumb(
            BreadcrumbList(
                BreadcrumbItem(
                    BreadcrumbLink("Home", href="/")
                ),
                BreadcrumbSeparator(
                    Icon("slash", width="16", height="16", cls="align-middle")
                ),
                BreadcrumbItem(
                    BreadcrumbLink("Library", href="/library")
                ),
                BreadcrumbSeparator(
                    Icon("slash", width="16", height="16", cls="align-middle")
                ),
                BreadcrumbItem(
                    BreadcrumbPage("Data")
                )
            )
        ),
        '''Breadcrumb(
    BreadcrumbList(
        BreadcrumbItem(
            BreadcrumbLink("Home", href="/")
        ),
        BreadcrumbSeparator(
            Icon("slash", width="16", height="16", cls="align-middle")
        ),
        BreadcrumbItem(
            BreadcrumbLink("Library", href="/library")
        ),
        BreadcrumbSeparator(
            Icon("slash", width="16", height="16", cls="align-middle")
        ),
        BreadcrumbItem(
            BreadcrumbPage("Data")
        )
    )
)''',
        title="Custom Separator",
        description="Use custom icons as separators between items"
    )
    
    # Long breadcrumb with ellipsis
    yield ComponentPreview(
        Breadcrumb(
            BreadcrumbList(
                BreadcrumbItem(
                    BreadcrumbLink("Home", href="/")
                ),
                BreadcrumbSeparator(),
                BreadcrumbItem(
                    BreadcrumbEllipsis()
                ),
                BreadcrumbSeparator(),
                BreadcrumbItem(
                    BreadcrumbLink("Components", href="/docs/components")
                ),
                BreadcrumbSeparator(),
                BreadcrumbItem(
                    BreadcrumbPage("Breadcrumb")
                )
            )
        ),
        '''Breadcrumb(
    BreadcrumbList(
        BreadcrumbItem(
            BreadcrumbLink("Home", href="/")
        ),
        BreadcrumbSeparator(),
        BreadcrumbItem(
            BreadcrumbEllipsis()
        ),
        BreadcrumbSeparator(),
        BreadcrumbItem(
            BreadcrumbLink("Components", href="/docs/components")
        ),
        BreadcrumbSeparator(),
        BreadcrumbItem(
            BreadcrumbPage("Breadcrumb")
        )
    )
)''',
        title="Collapsed",
        description="Use ellipsis to indicate hidden intermediate steps"
    )
    
    # Long path without ellipsis
    yield ComponentPreview(
        Breadcrumb(
            BreadcrumbList(
                BreadcrumbItem(
                    BreadcrumbLink("Home", href="/")
                ),
                BreadcrumbSeparator(),
                BreadcrumbItem(
                    BreadcrumbLink("Documentation", href="/docs")
                ),
                BreadcrumbSeparator(),
                BreadcrumbItem(
                    BreadcrumbLink("Components", href="/docs/components")
                ),
                BreadcrumbSeparator(),
                BreadcrumbItem(
                    BreadcrumbLink("Navigation", href="/docs/components/navigation")
                ),
                BreadcrumbSeparator(),
                BreadcrumbItem(
                    BreadcrumbPage("Breadcrumb")
                )
            )
        ),
        '''Breadcrumb(
    BreadcrumbList(
        BreadcrumbItem(
            BreadcrumbLink("Home", href="/")
        ),
        BreadcrumbSeparator(),
        BreadcrumbItem(
            BreadcrumbLink("Documentation", href="/docs")
        ),
        BreadcrumbSeparator(),
        BreadcrumbItem(
            BreadcrumbLink("Components", href="/docs/components")
        ),
        BreadcrumbSeparator(),
        BreadcrumbItem(
            BreadcrumbLink("Navigation", href="/docs/components/navigation")
        ),
        BreadcrumbSeparator(),
        BreadcrumbItem(
            BreadcrumbPage("Breadcrumb")
        )
    )
)''',
        title="Long Path",
        description="Full breadcrumb trail with multiple levels"
    )
    
    # Responsive breadcrumb
    yield ComponentPreview(
        Breadcrumb(
            BreadcrumbList(
                BreadcrumbItem(
                    BreadcrumbLink("Home", href="/")
                ),
                BreadcrumbSeparator(),
                # Show ellipsis on mobile, hide intermediate items  
                BreadcrumbItem(
                    BreadcrumbEllipsis(),
                    cls="md:hidden"
                ),
                BreadcrumbSeparator(cls="md:hidden"),
                # Show full path on desktop
                BreadcrumbItem(
                    BreadcrumbLink("Documentation", href="/docs"),
                    cls="hidden md:inline-flex"
                ),
                BreadcrumbSeparator(cls="hidden md:inline-flex"),
                BreadcrumbItem(
                    BreadcrumbLink("Components", href="/docs/components"),
                    cls="hidden md:inline-flex"
                ),
                BreadcrumbSeparator(cls="hidden md:inline-flex"),
                BreadcrumbItem(
                    BreadcrumbPage("Breadcrumb")
                )
            )
        ),
        '''Breadcrumb(
    BreadcrumbList(
        BreadcrumbItem(
            BreadcrumbLink("Home", href="/")
        ),
        BreadcrumbSeparator(),
        # Ellipsis shown on mobile
        BreadcrumbItem(
            BreadcrumbEllipsis(),
            cls="md:hidden"
        ),
        BreadcrumbSeparator(cls="md:hidden"),
        # Full path shown on desktop
        BreadcrumbItem(
            BreadcrumbLink("Documentation", href="/docs"),
            cls="hidden md:inline-flex"
        ),
        BreadcrumbSeparator(cls="hidden md:inline-flex"),
        BreadcrumbItem(
            BreadcrumbLink("Components", href="/docs/components"),
            cls="hidden md:inline-flex"
        ),
        BreadcrumbSeparator(cls="hidden md:inline-flex"),
        BreadcrumbItem(
            BreadcrumbPage("Breadcrumb")
        )
    )
)''',
        title="Responsive",
        description="Shows ellipsis on mobile, full path on desktop"
    )


def create_breadcrumb_docs():
    """Create breadcrumb documentation page using convention-based approach."""
    from utils import auto_generate_page
    
    # Hero example - basic breadcrumb
    hero_example = ComponentPreview(
        Breadcrumb(
            BreadcrumbList(
                BreadcrumbItem(
                    BreadcrumbLink("Home", href="/")
                ),
                BreadcrumbSeparator(),
                BreadcrumbItem(
                    BreadcrumbLink("Components", href="/components")
                ),
                BreadcrumbSeparator(),
                BreadcrumbItem(
                    BreadcrumbPage("Breadcrumb")
                )
            )
        ),
        '''Breadcrumb(
    BreadcrumbList(
        BreadcrumbItem(
            BreadcrumbLink("Home", href="/")
        ),
        BreadcrumbSeparator(),
        BreadcrumbItem(
            BreadcrumbLink("Components", href="/components")
        ),
        BreadcrumbSeparator(),
        BreadcrumbItem(
            BreadcrumbPage("Breadcrumb")
        )
    )
)'''
    )
    
    return auto_generate_page(
        TITLE,
        DESCRIPTION,
        list(examples()),
        cli_command="star add breadcrumb",
        hero_example=hero_example,
        component_slug="breadcrumb",
        api_reference={
            "components": [
                {
                    "name": "Breadcrumb",
                    "description": "The root breadcrumb container"
                },
                {
                    "name": "BreadcrumbList",
                    "description": "Contains the ordered list of breadcrumb items"
                },
                {
                    "name": "BreadcrumbItem",
                    "description": "Individual breadcrumb item container"
                },
                {
                    "name": "BreadcrumbLink",
                    "description": "Clickable breadcrumb link"
                },
                {
                    "name": "BreadcrumbPage",
                    "description": "Current page breadcrumb item (non-clickable)"
                },
                {
                    "name": "BreadcrumbSeparator",
                    "description": "Visual separator between breadcrumb items"
                },
                {
                    "name": "BreadcrumbEllipsis",
                    "description": "Collapsed breadcrumb indicator"
                }
            ]
        }
    )