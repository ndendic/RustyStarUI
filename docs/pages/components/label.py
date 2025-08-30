"""
Label component documentation - Form field labels.
"""

# Component metadata for auto-discovery
TITLE = "Label"
DESCRIPTION = "Renders an accessible label associated with form controls."
CATEGORY = "ui"
ORDER = 30
STATUS = "stable"

from starhtml import Div, P, Span, Icon
from starui.registry.components.label import Label
from starui.registry.components.input import Input
from starui.registry.components.checkbox import Checkbox, CheckboxWithLabel
from starui.registry.components.radio_group import RadioGroup, RadioGroupItem
from widgets.component_preview import ComponentPreview


def examples():
    """Generate Label examples using ComponentPreview with tabs."""
    
    # Basic usage - moved to hero example
    # This will be the first example after the hero
    
    # Required fields and validation
    yield ComponentPreview(
        Div(
            Div(
                Label(
                    "Password",
                    Span(" *", cls="text-destructive"),
                    for_="password"
                ),
                Input(type="password", id="password", placeholder="Enter your password"),
                cls="space-y-2"
            ),
            Div(
                Label(
                    "Email Address",
                    Span(" *", cls="text-destructive"),
                    for_="email-required"
                ),
                Input(type="email", id="email-required", placeholder="john.doe@example.com", required=True),
                P("Required fields are marked with an asterisk", cls="text-xs text-muted-foreground mt-1"),
                cls="space-y-2"
            ),
            cls="grid gap-4 max-w-md"
        ),
        '''from starui.registry.components.label import Label
from starhtml import Input, Span

Label(
    "Password",
    Span(" *", cls="text-destructive"),
    for_="password"
)
Input(type="password", id="password", placeholder="Enter your password")''',
        title="Required Fields",
        description="Labels with required field indicators"
    )
    
    # Labels with icons
    yield ComponentPreview(
        Div(
            Div(
                Label(
                    Icon("lucide:user", cls="h-4 w-4"),
                    "Username",
                    for_="username-icon",
                    cls="flex items-center gap-2"
                ),
                Input(id="username-icon", placeholder="Enter your username"),
                cls="space-y-2"
            ),
            Div(
                Label(
                    Icon("lucide:mail", cls="h-4 w-4"),
                    "Email",
                    for_="email-icon",
                    cls="flex items-center gap-2"
                ),
                Input(type="email", id="email-icon", placeholder="Enter your email"),
                cls="space-y-2"
            ),
            Div(
                Label(
                    Icon("lucide:lock", cls="h-4 w-4"),
                    "Password",
                    for_="password-icon",
                    cls="flex items-center gap-2"
                ),
                Input(type="password", id="password-icon", placeholder="Enter your password"),
                cls="space-y-2"
            ),
            cls="grid gap-4 max-w-md"
        ),
        '''from starui.registry.components.label import Label
from starhtml import Icon, Input

Label(
    Icon("lucide:user", cls="h-4 w-4"),
    "Username",
    for_="username",
    cls="flex items-center gap-2"
)
Input(id="username", placeholder="Enter your username")''',
        title="Labels with Icons",
        description="Enhance labels with iconography"
    )
    
    # With help text
    yield ComponentPreview(
        Div(
            Div(
                Label("API Key", for_="api-key"),
                Input(id="api-key", placeholder="sk-..."),
                P("Your API key can be found in your account settings.", cls="text-sm text-muted-foreground mt-1"),
                cls="space-y-2"
            ),
            Div(
                Label("Database URL", for_="db-url"),
                Input(id="db-url", placeholder="postgresql://..."),
                P("Connection string for your database", cls="text-sm text-muted-foreground mt-1"),
                cls="space-y-2"
            ),
            cls="grid gap-4 max-w-md"
        ),
        '''from starui.registry.components.label import Label
from starhtml import Input, P

Div(
    Label("API Key", for_="api-key"),
    Input(id="api-key", placeholder="sk-..."),
    P("Your API key can be found in your account settings.", 
      cls="text-sm text-muted-foreground mt-1"),
    cls="space-y-2"
)''',
        title="With Help Text",
        description="Labels with additional helper text"
    )
    
    # Radio and checkbox groups  
    yield ComponentPreview(
        Div(
            Div(
                Label("Preferred Contact Method", cls="text-base font-semibold mb-3 block"),
                RadioGroup(
                    RadioGroupItem("email", "Email"),
                    RadioGroupItem("phone", "Phone"), 
                    RadioGroupItem("mail", "Mail"),
                    initial_value="email"
                ),
                cls="p-4 border rounded-lg"
            ),
            Div(
                Label("Notification Preferences", cls="text-base font-semibold mb-3 block"),
                Div(
                    CheckboxWithLabel("Email notifications", name="notify-email"),
                    CheckboxWithLabel("SMS notifications", name="notify-sms"),
                    CheckboxWithLabel("Push notifications", name="notify-push"),
                    cls="space-y-3"
                ),
                cls="p-4 border rounded-lg"
            ),
            cls="grid gap-4 max-w-md"
        ),
        '''Label("Preferred Contact Method", cls="text-base font-semibold mb-3 block")
RadioGroup(
    RadioGroupItem("email", "Email"),
    RadioGroupItem("phone", "Phone"),
    RadioGroupItem("mail", "Mail"),
    initial_value="email"
)

Label("Notification Preferences", cls="text-base font-semibold mb-3 block")
CheckboxWithLabel("Email notifications", name="notify-email")
CheckboxWithLabel("SMS notifications", name="notify-sms")
CheckboxWithLabel("Push notifications", name="notify-push")''',
        title="Radio & Checkbox Groups",
        description="Labels for grouped form controls"
    )
    
    # File upload
    yield ComponentPreview(
        Div(
            Div(
                Label("Resume Upload", for_="resume"),
                Input(type="file", id="resume", accept=".pdf,.doc,.docx"),
                P("Accepted formats: PDF, DOC, DOCX (Max 5MB)", cls="text-sm text-muted-foreground mt-1"),
                cls="space-y-2"
            ),
            Div(
                Label("Profile Picture", for_="avatar"),
                Input(type="file", id="avatar", accept="image/*"),
                P("Accepted formats: JPG, PNG, GIF (Max 2MB)", cls="text-sm text-muted-foreground mt-1"),
                cls="space-y-2"
            ),
            cls="grid gap-4 max-w-md"
        ),
        '''from starui.registry.components.label import Label
from starhtml import Input, P

Div(
    Label("Resume Upload", for_="resume"),
    Input(type="file", id="resume", accept=".pdf,.doc,.docx"),
    P("Accepted formats: PDF, DOC, DOCX (Max 5MB)", 
      cls="text-sm text-muted-foreground mt-1"),
    cls="space-y-2"
)''',
        title="File Upload",
        description="Labels for file input controls"
    )
    
    # Disabled state
    yield ComponentPreview(
        Div(
            Div(
                Label("Disabled Field", for_="disabled-input", cls="opacity-50"),
                Input(id="disabled-input", placeholder="This field is disabled", disabled=True),
                cls="space-y-2"
            ),
            Div(
                Label("Read-only Field", for_="readonly-input"),
                Input(id="readonly-input", value="Read-only value", readonly=True),
                cls="space-y-2"
            ),
            cls="grid gap-4 max-w-md"
        ),
        '''from starui.registry.components.label import Label
from starhtml import Input

Div(
    Label("Disabled Field", for_="disabled-input", cls="opacity-50"),
    Input(id="disabled-input", placeholder="This field is disabled", disabled=True),
    cls="space-y-2"
)''',
        title="Disabled & Read-only",
        description="Labels for disabled and read-only fields"
    )
    
    # Complete form example
    yield ComponentPreview(
        Div(
            Div(
                Label("First Name", for_="first-name"),
                Input(id="first-name", placeholder="John"),
                cls="space-y-2"
            ),
            Div(
                Label("Last Name", for_="last-name"),
                Input(id="last-name", placeholder="Doe"),
                cls="space-y-2"
            ),
            Div(
                Label(
                    "Email Address",
                    Span(" *", cls="text-destructive"),
                    for_="email-address"
                ),
                Input(type="email", id="email-address", placeholder="john.doe@example.com"),
                cls="space-y-2"
            ),
            Div(
                Label("Phone Number", for_="phone"),
                Input(type="tel", id="phone", placeholder="+1 (555) 123-4567"),
                cls="space-y-2"
            ),
            cls="space-y-4 max-w-md"
        ),
        '''Label("First Name", for_="first-name")
Input(id="first-name", placeholder="John")

Label("First Name", for_="first-name")
Input(id="first-name", placeholder="John")

Label(
    "Email Address",
    Span(" *", cls="text-destructive"),
    for_="email-address"
)
Input(type="email", id="email-address", placeholder="john.doe@example.com")''',
        title="Complete Form",
        description="Labels in a full form layout"
    )


def create_label_docs():
    """Create label documentation page using convention-based approach."""
    from utils import auto_generate_page
    
    # Hero example - showcase different label patterns
    hero_example = ComponentPreview(
        Div(
            # Basic form fields
            Div(
                Label("Email", for_="email"),
                Input(type="email", id="email", placeholder="Enter your email"),
                cls="space-y-2"
            ),
            # Required field
            Div(
                Label(
                    "Password",
                    Span(" *", cls="text-destructive"),
                    for_="password"
                ),
                Input(type="password", id="password", placeholder="Enter your password"),
                cls="space-y-2"
            ),
            # Label with icon
            Div(
                Label(
                    Icon("lucide:user", width="16", height="16"),
                    "Username",
                    for_="username",
                    cls="flex items-center gap-2"
                ),
                Input(id="username", placeholder="Enter your username"),
                cls="space-y-2"
            ),
            cls="grid gap-6 max-w-sm"
        ),
        '''Label("Email", for_="email")
Input(type="email", id="email", placeholder="Enter your email")

Label(
    "Password",
    Span(" *", cls="text-destructive"),
    for_="password"
)

Label(
    Icon("lucide:user", width="16", height="16"),
    "Username", 
    for_="username",
    cls="flex items-center gap-2"
)'''
    )
    
    return auto_generate_page(
        TITLE,
        DESCRIPTION,
        list(examples()),
        cli_command="star add label",
        hero_example=hero_example,
        api_reference={
            "props": [
                {
                    "name": "for_",
                    "type": "str | None",
                    "default": "None",
                    "description": "ID of the form control this label is for"
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