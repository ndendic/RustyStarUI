"""
Tabs component documentation - Layered content sections.
"""

# Component metadata for auto-discovery
TITLE = "Tabs"
DESCRIPTION = "A set of layered sections of content—known as tab panels—that are displayed one at a time."
CATEGORY = "ui"
ORDER = 30
STATUS = "stable"

from rusty_tags import Div, P, H2, H3, H4, Pre, Code, Button as HTMLButton
from starui.registry.components.tabs import Tabs, TabsList, TabsTrigger, TabsContent
from starui.registry.components.button import Button
from widgets.component_preview import ComponentPreview


def examples():
    """Generate Tabs examples using ComponentPreview with tabs."""
    
    # Note: Basic tabs moved to hero example
    # This will be the first example after the hero
    
    # Dashboard tabs
    yield ComponentPreview(
        Tabs(
            TabsList(
                TabsTrigger("Overview", id="overview"),
                TabsTrigger("Analytics", id="analytics"), 
                TabsTrigger("Reports", id="reports")
            ),
            TabsContent(
                Div(
                    P("Welcome to your dashboard. Here you can see a summary of your activity.", cls="text-muted-foreground mb-4"),
                    Div(
                        Div("Total Users: 1,234", cls="p-3 bg-muted rounded-lg text-sm"),
                        Div("Active Sessions: 89", cls="p-3 bg-muted rounded-lg text-sm"),
                        Div("Revenue: $12,450", cls="p-3 bg-muted rounded-lg text-sm"),
                        cls="grid grid-cols-3 gap-3"
                    )
                ),
                id="overview"
            ),
            TabsContent(
                Div(
                    P("View detailed analytics and metrics for your account.", cls="text-muted-foreground mb-4"),
                    Div("📊 Analytics charts would go here", cls="p-8 border border-dashed rounded-lg text-center text-muted-foreground")
                ),
                id="analytics"
            ),
            TabsContent(
                Div(
                    P("Generate and download comprehensive reports for your data.", cls="text-muted-foreground mb-4"),
                    Button("Download Report", variant="outline", cls="mr-2"),
                    Button("Generate New Report")
                ),
                id="reports"
            ),
            default_id="overview",
            cls="w-full"
        ),
        '''Tabs(
    TabsList(
        TabsTrigger("Overview", id="overview"),
        TabsTrigger("Analytics", id="analytics"),
        TabsTrigger("Reports", id="reports")
    ),
    TabsContent(
        P("Welcome to your dashboard with activity summary."),
        id="overview"
    ),
    TabsContent(
        P("View detailed analytics and metrics."),
        id="analytics"
    ),
    TabsContent(
        P("Generate and download reports."),
        id="reports"
    ),
    default_id="overview"
)''',
        title="Dashboard Tabs",
        description="Multiple tabs for different content sections"
    )
    
    # Code preview tabs
    yield ComponentPreview(
        Tabs(
            TabsList(
                TabsTrigger("Preview", id="preview"),
                TabsTrigger("Code", id="code")
            ),
            TabsContent(
                Div(
                    Button("Click me!", cls="mr-2"),
                    Button("Secondary", variant="secondary", cls="mr-2"),
                    Button("Outline", variant="outline"),
                    cls="p-6 border rounded-lg"
                ),
                id="preview"
            ),
            TabsContent(
                Pre(
                    Code('''Button("Click me!")
Button("Secondary", variant="secondary")
Button("Outline", variant="outline")'''),
                    cls="p-4 bg-muted rounded-lg text-sm overflow-x-auto"
                ),
                id="code"
            ),
            default_id="preview",
            cls="w-full"
        ),
        '''Tabs(
    TabsList(
        TabsTrigger("Preview", id="preview"),
        TabsTrigger("Code", id="code")
    ),
    TabsContent(
        Div(
            Button("Click me!"),
            Button("Secondary", variant="secondary"),
            cls="p-6 border rounded-lg"
        ),
        id="preview"
    ),
    TabsContent(
        Pre(Code("Button code here...")),
        id="code"
    ),
    default_id="preview"
)''',
        title="Code Preview",
        description="Tabs for showing preview and code"
    )
    
    # Settings tabs
    yield ComponentPreview(
        Tabs(
            TabsList(
                TabsTrigger("General", id="general"),
                TabsTrigger("Security", id="security"),
                TabsTrigger("Notifications", id="notifications")
            ),
            TabsContent(
                Div(
                    P("Manage your account preferences and basic information.", cls="text-muted-foreground mb-4"),
                    Div(
                        "Username, language, timezone settings would go here",
                        cls="p-4 border rounded-lg text-sm text-muted-foreground"
                    )
                ),
                id="general"
            ),
            TabsContent(
                Div(
                    P("Configure your account security and authentication settings.", cls="text-muted-foreground mb-4"),
                    Div(
                        "Password, two-factor auth settings would go here",
                        cls="p-4 border rounded-lg text-sm text-muted-foreground"
                    )
                ),
                id="security"
            ),
            TabsContent(
                Div(
                    P("Control how and when you receive notifications from our platform.", cls="text-muted-foreground mb-4"),
                    Div(
                        "Email, push notification settings would go here",
                        cls="p-4 border rounded-lg text-sm text-muted-foreground"
                    )
                ),
                id="notifications"
            ),
            default_id="general",
            cls="w-full"
        ),
        '''Tabs(
    TabsList(
        TabsTrigger("General", id="general"),
        TabsTrigger("Security", id="security"),
        TabsTrigger("Notifications", id="notifications")
    ),
    TabsContent(
        Div(
            P("Manage your account preferences."),
            # Settings form here
        ),
        id="general"
    ),
    default_id="general"
)''',
        title="Settings Tabs",
        description="Multi-section settings interface"
    )
    
    # Plain variant tabs
    yield ComponentPreview(
        Tabs(
            TabsList(
                TabsTrigger("Documentation", id="docs"),
                TabsTrigger("Examples", id="examples"),
                TabsTrigger("API Reference", id="api")
            ),
            TabsContent(
                Div(
                    P("Read the comprehensive guides and tutorials to get started.", cls="text-muted-foreground mb-3"),
                    P("Learn how to integrate components into your application with step-by-step instructions and best practices.", cls="text-sm text-muted-foreground")
                ),
                id="docs"
            ),
            TabsContent(
                Div(
                    P("Explore interactive examples and code samples for all components.", cls="text-muted-foreground mb-3"),
                    P("Copy and paste working examples directly into your project with full source code.", cls="text-sm text-muted-foreground")
                ),
                id="examples"
            ),
            TabsContent(
                Div(
                    P("Complete API documentation for all components and their props.", cls="text-muted-foreground mb-3"),
                    P("TypeScript definitions, method signatures, and usage patterns for every component.", cls="text-sm text-muted-foreground")
                ),
                id="api"
            ),
            default_id="docs",
            variant="plain",
            cls="w-full"
        ),
        '''Tabs(
    TabsList(
        TabsTrigger("Documentation", id="docs"),
        TabsTrigger("Examples", id="examples"),
        TabsTrigger("API Reference", id="api")
    ),
    TabsContent(
        P("Read the comprehensive guides and tutorials to get started."),
        id="docs"
    ),
    default_id="docs",
    variant="plain"
)''',
        title="Plain Variant",
        description="Clean minimal tabs without background styling"
    )
    
    # Navigation-style tabs
    yield ComponentPreview(
        Tabs(
            TabsList(
                TabsTrigger("Home", id="home"),
                TabsTrigger("About", id="about"),
                TabsTrigger("Services", id="services"),
                TabsTrigger("Contact", id="contact")
            ),
            TabsContent(
                Div(
                    P("Welcome to our platform! Discover amazing tools and services designed for developers.", cls="text-lg text-muted-foreground mb-4"),
                    Button("Get Started", cls="mr-2"),
                    Button("Learn More", variant="outline")
                ),
                id="home"
            ),
            TabsContent(
                Div(
                    P("We're passionate about building tools that make developers more productive.", cls="text-muted-foreground mb-4"),
                    P("Founded in 2020, we've been creating amazing products for developers worldwide, focusing on simplicity and performance.", cls="text-sm text-muted-foreground")
                ),
                id="about"
            ),
            TabsContent(
                Div(
                    P("We offer comprehensive solutions to help your business grow.", cls="text-muted-foreground mb-4"),
                    Div(
                        "🚀 Web Development - Full-stack applications",
                        "📱 Mobile Apps - iOS and Android development", 
                        "☁️ Cloud Solutions - Scalable infrastructure",
                        cls="grid grid-cols-1 gap-3 text-sm"
                    )
                ),
                id="services"
            ),
            TabsContent(
                Div(
                    P("Ready to work with us? We'd love to hear about your project!", cls="text-muted-foreground mb-4"),
                    Div(
                        P("📧 hello@example.com", cls="text-sm text-muted-foreground"),
                        P("📞 (555) 123-4567", cls="text-sm text-muted-foreground"),
                        cls="space-y-2"
                    )
                ),
                id="contact"
            ),
            default_id="home",
            variant="plain",
            cls="w-full"
        ),
        '''Tabs(
    TabsList(
        TabsTrigger("Home", id="home"),
        TabsTrigger("About", id="about"),
        TabsTrigger("Services", id="services"),
        TabsTrigger("Contact", id="contact")
    ),
    TabsContent(
        Div(
            P("Welcome to our platform!"),
            Button("Get Started")
        ),
        id="home"
    ),
    default_id="home",
    variant="plain"
)''',
        title="Navigation Tabs",
        description="Website navigation-style tabs using plain variant"
    )


def create_tabs_docs():
    """Create tabs documentation page using convention-based approach."""
    from utils import auto_generate_page
    
    # Hero example - simple account/password tabs
    hero_example = ComponentPreview(
        Tabs(
            TabsList(
                TabsTrigger("Account", id="account"),
                TabsTrigger("Password", id="password")
            ),
            TabsContent(
                Div(
                    H4("Account", cls="text-lg font-medium mb-2"),
                    P("Make changes to your account here. Click save when you're done.", cls="text-muted-foreground")
                ),
                id="account"
            ),
            TabsContent(
                Div(
                    H4("Password", cls="text-lg font-medium mb-2"),
                    P("Change your password here. After saving, you'll be logged out.", cls="text-muted-foreground")
                ),
                id="password"
            ),
            default_id="account",
            cls="w-full max-w-md"
        ),
        '''Tabs(
    TabsList(
        TabsTrigger("Account", id="account"),
        TabsTrigger("Password", id="password")
    ),
    TabsContent(
        Div(
            H4("Account"),
            P("Make changes to your account here.")
        ),
        id="account"
    ),
    TabsContent(
        Div(
            H4("Password"),
            P("Change your password here.")
        ),
        id="password"
    ),
    default_id="account"
)'''
    )
    
    return auto_generate_page(
        TITLE,
        DESCRIPTION,
        list(examples()),
        cli_command="star add tabs",
        hero_example=hero_example,
        component_slug="tabs",
        api_reference={
            "props": [
                {
                    "name": "default_id",
                    "type": "str",
                    "default": "required",
                    "description": "The id of the tab that should be active when initially rendered"
                },
                {
                    "name": "variant",
                    "type": "Literal['default', 'plain']",
                    "default": "default",
                    "description": "Visual style variant of the tabs"
                },
                {
                    "name": "id",
                    "type": "str",
                    "default": "required",
                    "description": "The unique identifier for each TabsTrigger and TabsContent pair"
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