"""
Alert component documentation - Important messages and notifications.
"""

# Component metadata for auto-discovery
TITLE = "Alert"
DESCRIPTION = "Displays a callout for user attention."
CATEGORY = "ui"
ORDER = 2
STATUS = "stable"

from starhtml import Div, P, Strong, Code, Ul, Li, Icon
from starui.registry.components.alert import Alert, AlertTitle, AlertDescription
from starui.registry.components.button import Button
from utils import auto_generate_page
from widgets.component_preview import ComponentPreview


def examples():
    """Generate alert examples using ComponentPreview with tabs."""
    
    # Note: Basic alerts will be used as hero example
    # This will be the first example after the hero
    
    # Different message types
    yield ComponentPreview(
        Div(
            Alert(
                Icon("check-circle", width="16", height="16", cls="text-green-600"),
                AlertTitle("Success"),
                AlertDescription("Your account has been created successfully!"),
                cls="mb-4"
            ),
            Alert(
                Icon("alert-triangle", width="16", height="16", cls="text-amber-600"),
                AlertTitle("Warning"),
                AlertDescription("This action cannot be undone. Please review carefully."),
                cls="mb-4"
            ),
            Alert(
                Icon("info", width="16", height="16", cls="text-blue-600"),
                AlertTitle("Information"),
                AlertDescription("New features are now available in your dashboard.")
            ),
            cls="space-y-4"
        ),
        '''# Success alert with green styling
Alert(
    Icon("check-circle", width="16", height="16", cls="text-green-600"),
    AlertTitle("Success"),
    AlertDescription("Your account has been created successfully!")
)

# Warning alert with amber styling  
Alert(
    Icon("alert-triangle", width="16", height="16", cls="text-amber-600"),
    AlertTitle("Warning"),
    AlertDescription("This action cannot be undone. Please review carefully.")
)

# Info alert with blue styling
Alert(
    Icon("info", width="16", height="16", cls="text-blue-600"),
    AlertTitle("Information"),
    AlertDescription("New features are now available in your dashboard.")
)''',
        title="Message Types",
        description="Success, warning, and info styled alerts"
    )
    
    # Complex content
    yield ComponentPreview(
        Alert(
            Icon("alert-circle", width="16", height="16"),
            AlertTitle("Unable to process payment"),
            AlertDescription(
                P("There was an issue processing your payment. Please check the following:"),
                Ul(
                    Li("Verify your card details are correct"),
                    Li("Ensure you have sufficient funds"),
                    Li("Check that your billing address matches"),
                    cls="mt-2 ml-6 list-disc space-y-1 text-sm"
                )
            ),
            variant="destructive"
        ),
        '''Alert(
    Icon("alert-circle", width="16", height="16"),
    AlertTitle("Unable to process payment"),
    AlertDescription(
        P("There was an issue processing your payment. Please check the following:"),
        Ul(
            Li("Verify your card details are correct"),
            Li("Ensure you have sufficient funds"), 
            Li("Check that your billing address matches"),
            cls="mt-2 ml-6 list-disc space-y-1 text-sm"
        )
    ),
    variant="destructive"
)''',
        title="Rich Content",
        description="Alerts with lists and formatted text"
    )
    
    # Without icon
    yield ComponentPreview(
        Alert(
            AlertTitle("Pro tip"),
            AlertDescription("You can use Ctrl+K to quickly search and navigate through the documentation.")
        ),
        '''Alert(
    AlertTitle("Pro tip"), 
    AlertDescription("You can use Ctrl+K to quickly search and navigate through the documentation.")
)''',
        title="Without Icon",
        description="Simple alert without an icon"
    )


def create_alert_docs():
    """Create alert documentation page using convention-based approach."""
    from utils import auto_generate_page
    
    # Hero example - basic alert variants showcase
    hero_example = ComponentPreview(
        Div(
            Alert(
                Icon("terminal", width="16", height="16"),
                AlertTitle("Heads up!"),
                AlertDescription("You can add components and dependencies to your app using the CLI."),
                cls="mb-4"
            ),
            Alert(
                Icon("alert-circle", width="16", height="16"),
                AlertTitle("Error occurred"),
                AlertDescription("Your session has expired. Please log in again."),
                variant="destructive"
            ),
            cls="space-y-4"
        ),
'''Alert(
    Icon("terminal", width="16", height="16"),
    AlertTitle("Heads up!"),
    AlertDescription("You can add components and dependencies to your app using the CLI.")
)

Alert(
    Icon("alert-circle", width="16", height="16"),
    AlertTitle("Error occurred"),
    AlertDescription("Your session has expired. Please log in again."),
    variant="destructive"
)''',
    )
    
    return auto_generate_page(
        TITLE,
        DESCRIPTION,
        list(examples()),
        cli_command="star add alert",
        hero_example=hero_example,
        component_slug="alert",
        api_reference={
            "props": [
                {
                    "name": "variant",
                    "type": "Literal['default', 'destructive']",
                    "default": "default",
                    "description": "Visual style variant of the alert"
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