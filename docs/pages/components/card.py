"""
Card component documentation - Flexible content containers.
"""

# Component metadata for auto-discovery
TITLE = "Card"
DESCRIPTION = "Displays a card with header, content, and footer."
CATEGORY = "layout"
ORDER = 10
STATUS = "stable"

from starhtml import Div, P, H3, H4, Span, Icon, A, Img
from starui.registry.components.card import (
    Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter
)
from starui.registry.components.button import Button
from starui.registry.components.badge import Badge
from starui.registry.components.input import Input
from starui.registry.components.label import Label
from widgets.component_preview import ComponentPreview


def examples():
    """Generate Card examples using ComponentPreview with tabs."""
    
    # Note: Basic card moved to hero example
    # This will be the first example after the hero
    
    # Feature cards
    yield ComponentPreview(
        Div(
            Card(
                CardHeader(
                    Icon("rocket", width="24", height="24", cls="text-blue-500 mb-2"),
                    CardTitle("Fast Performance"),
                    CardDescription("Lightning-fast rendering with server-side optimization")
                ),
                CardContent(
                    P("Built for speed with minimal JavaScript and efficient server rendering.", cls="text-sm text-muted-foreground")
                )
            ),
            Card(
                CardHeader(
                    Icon("shield-check", width="24", height="24", cls="text-green-500 mb-2"),
                    CardTitle("Secure by Default"),
                    CardDescription("Enterprise-grade security built into every component")
                ),
                CardContent(
                    P("CSRF protection, XSS prevention, and secure authentication patterns.", cls="text-sm text-muted-foreground")
                )
            ),
            Card(
                CardHeader(
                    Icon("code", width="24", height="24", cls="text-purple-500 mb-2"),
                    CardTitle("Developer Friendly"),
                    CardDescription("Simple Python APIs with full TypeScript support")
                ),
                CardContent(
                    P("Write modern UI entirely in Python with excellent IDE support.", cls="text-sm text-muted-foreground")
                )
            ),
            cls="grid grid-cols-1 md:grid-cols-3 gap-4"
        ),
        '''Card(
    CardHeader(
        Icon("rocket", width="24", height="24"),
        CardTitle("Fast Performance"),
        CardDescription("Lightning-fast rendering")
    ),
    CardContent(
        P("Built for speed with minimal JavaScript.")
    )
)''',
        title="Feature Cards",
        description="Cards highlighting key features or benefits"
    )
    
    # User profile cards
    yield ComponentPreview(
        Div(
            Card(
                CardHeader(
                    Div(
                        Div("JD", cls="w-12 h-12 rounded-full bg-blue-500 flex items-center justify-center text-white font-bold"),
                        Div(
                            CardTitle("John Doe", cls="text-lg"),
                            CardDescription("Product Designer"),
                            cls="ml-4"
                        ),
                        cls="flex items-center"
                    )
                ),
                CardContent(
                    P("Passionate about creating user-centered designs that solve real problems.", cls="text-sm text-muted-foreground")
                ),
                CardFooter(
                    Button("View Profile", variant="outline", size="sm", cls="mr-2"),
                    Button("Message", size="sm")
                )
            ),
            Card(
                CardHeader(
                    Div(
                        Div("AS", cls="w-12 h-12 rounded-full bg-green-500 flex items-center justify-center text-white font-bold"),
                        Div(
                            CardTitle("Anna Smith", cls="text-lg"),
                            CardDescription("Frontend Developer"),
                            cls="ml-4"
                        ),
                        cls="flex items-center"
                    )
                ),
                CardContent(
                    P("Full-stack developer with expertise in Python and modern web technologies.", cls="text-sm text-muted-foreground")
                ),
                CardFooter(
                    Button("View Profile", variant="outline", size="sm", cls="mr-2"),
                    Button("Message", size="sm")
                )
            ),
            cls="grid grid-cols-1 md:grid-cols-2 gap-4 max-w-2xl"
        ),
        '''Card(
    CardHeader(
        Div(
            Div("JD", cls="w-12 h-12 rounded-full bg-blue-500 flex items-center justify-center text-white font-bold"),
            Div(
                CardTitle("John Doe"),
                CardDescription("Product Designer"),
                cls="ml-4"
            ),
            cls="flex items-center"
        )
    ),
    CardContent(
        P("Passionate about creating user-centered designs.")
    ),
    CardFooter(
        Button("View Profile", variant="outline"),
        Button("Message")
    )
)''',
        title="Profile Cards",
        description="User profile cards with actions"
    )
    
    # Stats cards
    yield ComponentPreview(
        Div(
            Card(
                CardHeader(
                    CardTitle("Total Revenue"),
                    CardDescription("Last 30 days")
                ),
                CardContent(
                    Div(
                        Span("$45,231.89", cls="text-3xl font-bold"),
                        Span("+20.1% from last month", cls="text-sm text-green-600 mt-2 block")
                    )
                )
            ),
            Card(
                CardHeader(
                    CardTitle("Active Users"),
                    CardDescription("Currently online")
                ),
                CardContent(
                    Div(
                        Span("2,350", cls="text-3xl font-bold"),
                        Span("+12% from yesterday", cls="text-sm text-green-600 mt-2 block")
                    )
                )
            ),
            Card(
                CardHeader(
                    CardTitle("Conversion Rate"),
                    CardDescription("This quarter")
                ),
                CardContent(
                    Div(
                        Span("3.2%", cls="text-3xl font-bold"),
                        Span("-2.4% from last quarter", cls="text-sm text-red-600 mt-2 block")
                    )
                )
            ),
            cls="grid grid-cols-1 md:grid-cols-3 gap-4"
        ),
        '''Card(
    CardHeader(
        CardTitle("Total Revenue"),
        CardDescription("Last 30 days")
    ),
    CardContent(
        Div(
            Span("$45,231.89", cls="text-3xl font-bold"),
            Span("+20.1% from last month", cls="text-sm text-green-600")
        )
    )
)''',
        title="Stats Cards",
        description="Metric and statistics display cards"
    )
    
    # Form card
    yield ComponentPreview(
        Card(
            CardHeader(
                CardTitle("Create Account"),
                CardDescription("Enter your details below to create your account")
            ),
            CardContent(
                Div(
                    Div(
                        Label("Email", for_="email"),
                        Input(type="email", id="email", placeholder="name@example.com"),
                        cls="space-y-2"
                    ),
                    Div(
                        Label("Password", for_="password"),
                        Input(type="password", id="password", placeholder="Enter your password"),
                        cls="space-y-2"
                    ),
                    Div(
                        Label("Confirm Password", for_="confirm"),
                        Input(type="password", id="confirm", placeholder="Confirm your password"),
                        cls="space-y-2"
                    ),
                    cls="space-y-4"
                )
            ),
            CardFooter(
                Div(
                    Button("Create Account", cls="w-full mb-2"),
                    P("Already have an account? ", A("Sign in", href="#", cls="underline"), cls="text-sm text-center text-muted-foreground"),
                    cls="w-full"
                )
            ),
            cls="w-full max-w-md"
        ),
        '''Card(
    CardHeader(
        CardTitle("Create Account"),
        CardDescription("Enter your details below")
    ),
    CardContent(
        Div(
            Div(
                Label("Email", for_="email"),
                Input(type="email", id="email", placeholder="name@example.com"),
                cls="space-y-2"
            ),
            Div(
                Label("Password", for_="password"),  
                Input(type="password", id="password"),
                cls="space-y-2"
            ),
            cls="space-y-4"
        )
    ),
    CardFooter(
        Button("Create Account", cls="w-full")
    )
)''',
        title="Form Card",
        description="Cards containing forms and inputs"
    )
    
    # Notification cards
    yield ComponentPreview(
        Div(
            Card(
                CardContent(
                    Div(
                        Div(
                            Icon("check-circle", width="20", height="20", cls="text-green-500"),
                            Div(
                                P("Payment successful", cls="font-medium text-sm"),
                                P("Your payment has been processed successfully.", cls="text-sm text-muted-foreground"),
                                cls="ml-3"
                            ),
                            cls="flex items-start"
                        ),
                        Button("View Receipt", variant="ghost", size="sm", cls="mt-3"),
                        cls="p-4"
                    )
                )
            ),
            Card(
                CardContent(
                    Div(
                        Div(
                            Icon("alert-circle", width="20", height="20", cls="text-orange-500"),
                            Div(
                                P("Action required", cls="font-medium text-sm"),
                                P("Please verify your email address to continue.", cls="text-sm text-muted-foreground"),
                                cls="ml-3"
                            ),
                            cls="flex items-start"
                        ),
                        Button("Verify Email", size="sm", cls="mt-3"),
                        cls="p-4"
                    )
                )
            ),
            cls="space-y-3 max-w-md"
        ),
        '''Card(
    CardContent(
        Div(
            Icon("check-circle", width="20", height="20", cls="text-green-500"),
            Div(
                P("Payment successful", cls="font-medium"),
                P("Your payment has been processed.", cls="text-muted-foreground"),
                cls="ml-3"
            ),
            cls="flex items-start"
        )
    )
)''',
        title="Notification Cards",
        description="Alert and notification style cards"
    )


def create_card_docs():
    """Create card documentation page using convention-based approach."""
    from utils import auto_generate_page
    
    # Hero example - basic card structure
    hero_example = ComponentPreview(
        Card(
            CardHeader(
                CardTitle("Card Title"),
                CardDescription("Card description with supporting text below.")
            ),
            CardContent(
                P("This is the main content area of the card where you can place any content you need.")
            ),
            CardFooter(
                Button("Action", cls="mr-2"),
                Button("Cancel", variant="outline")
            ),
            cls="w-full max-w-md"
        ),
        '''Card(
    CardHeader(
        CardTitle("Card Title"),
        CardDescription("Card description with supporting text below.")
    ),
    CardContent(
        P("This is the main content area of the card.")
    ),
    CardFooter(
        Button("Action"),
        Button("Cancel", variant="outline")
    )
)'''
    )
    
    return auto_generate_page(
        TITLE,
        DESCRIPTION,
        list(examples()),
        cli_command="star add card",
        hero_example=hero_example,
        component_slug="card",
        api_reference={
            "components": [
                {
                    "name": "Card",
                    "description": "The main card container"
                },
                {
                    "name": "CardHeader",
                    "description": "Contains the card title and description"
                },
                {
                    "name": "CardTitle",
                    "description": "The main heading of the card"
                },
                {
                    "name": "CardDescription",
                    "description": "Supporting text for the card title"
                },
                {
                    "name": "CardContent",
                    "description": "The main content area of the card"
                },
                {
                    "name": "CardFooter",
                    "description": "Contains actions and additional information"
                }
            ]
        }
    )