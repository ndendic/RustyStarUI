from starui import *

# Override specific rusty_tags components with HTML* aliases if needed
from rusty_tags import Input as HTMLInput
from rusty_tags import Label as HTMLLabel
from rusty_tags import Button as HTMLButton
from rusty_tags import Hr as HTMLHr

from rusty_tags.datastar import Signals
from rusty_tags.starlette import datastar_response, sse_elements, sse_signals

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from datastar_py.fastapi import ReadSignals
# Import all registry components at once (this will override starhtml components)
from starlette.staticfiles import StaticFiles

from sidebar import sidebar, navbar
# from starui.registry.components.accordion import Accordion, AccordionItem, AccordionTrigger, AccordionContent
styles = [
    Link(rel="stylesheet", href="/static/css/starui.css", type="text/css"),
    # Link(rel="stylesheet", href="/static/css/input.css", type="text/css"),
]
inspector = Script(src="/static/js/datastar-inspector.js", type="module")
fonts = [
    Link(rel='preconnect', href='https://fonts.googleapis.com'),
    Link(rel='preconnect', href='https://fonts.gstatic.com', crossorigin=''),
    Link(href='https://fonts.googleapis.com/css2?family=Crimson+Text:ital,wght@0,400;0,600;0,700;1,400;1,600;1,700&family=Geist+Mono:wght@100..900&family=Geist:wght@100..900&family=Lora:ital,wght@0,400..700;1,400..700&family=Plus+Jakarta+Sans:ital,wght@0,200..800;1,200..800&family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&family=Roboto+Mono:ital,wght@0,100..700;1,100..700&display=swap', rel='stylesheet')
]

app = FastAPI()
app.mount("/static", StaticFiles(directory="test_sandbox/static"), name="static")

hdrs=(        
        *styles,
        *fonts,
        Script(src="https://unpkg.com/lucide@latest"),
        Script(src='https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4'),
        Script(src='https://cdn.jsdelivr.net/npm/basecoat-css@0.3.2/dist/js/basecoat.min.js', defer=''),
        Script(src='https://cdn.jsdelivr.net/npm/basecoat-css@0.3.2/dist/js/select.min.js', defer=''),
        Script(src='https://cdn.jsdelivr.net/npm/basecoat-css@0.3.2/dist/js/popover.min.js', defer=''),
        Script(src='https://cdn.jsdelivr.net/npm/basecoat-css@0.3.2/dist/js/dropdown-menu.min.js', defer=''),
        Script(src='https://cdn.jsdelivr.net/npm/basecoat-css@0.3.2/dist/js/sidebar.min.js', defer=''),
        Script("(() => {\r\n      try {\r\n        const stored = localStorage.getItem('themeMode');\r\n        if (stored ? stored === 'dark'\r\n                   : matchMedia('(prefers-color-scheme: dark)').matches) {\r\n          document.documentElement.classList.add('dark');\r\n        }\r\n      } catch (_) {}\r\n\r\n      const apply = dark => {\r\n        document.documentElement.classList.toggle('dark', dark);\r\n        try { localStorage.setItem('themeMode', dark ? 'dark' : 'light'); } catch (_) {}\r\n      };\r\n\r\n      document.addEventListener('basecoat:theme', (event) => {\r\n        const mode = event.detail?.mode;\r\n        apply(mode === 'dark' ? true\r\n             : mode === 'light' ? false\r\n             : !document.documentElement.classList.contains('dark'));\r\n      });\r\n    })();"),
        Script("(function() {\r\n      try {\r\n        const storedTheme = localStorage.getItem('themeVariant');\r\n        if (storedTheme) document.documentElement.classList.add(`theme-${storedTheme}`);\r\n      } catch (event) {\r\n        console.error('Could not apply theme variant from localStorage', event);\r\n      }\r\n    })();"),
        # position_handler(),  # Enhanced handler is now built-in
        inspector,
    )
htmlkw=dict(lang="en", dir="ltr")
bodykw=dict(cls="min-h-screen bg-background text-foreground", on_load=DS.get("/updates"))
ftrs=(
    CustomTag("datastar-inspector"),
    Script("lucide.createIcons();"),

    # Script("import { createIcons, icons } from 'https://cdn.jsdelivr.net/npm/lucide@latest/+esm';createIcons({ icons, attrs: { width: 20, height: 20 } });", type='module')
)
page = create_template(hdrs=hdrs, htmlkw=htmlkw, bodykw=bodykw, ftrs=ftrs)

@app.get("/cmds/{command}/{sender}")
@datastar_response
async def commands(command: str, sender: str, request: Request, signals: ReadSignals):
    """Trigger events and broadcast to all connected clients"""
    signals = Signals(signals) if signals else {}
    reply_to = signals.client_id
    backend_signal = event(command)
    await emit_async(backend_signal, reply_to, signals=signals, request=request)

@app.get("/updates")
@datastar_response
async def event_stream(request: Request, signals: ReadSignals):
    """SSE endpoint with automatic client management"""
    client = Client()
    client.topics = {"updates" : [client.client_id, "system"]}
    client.process_topics(client.topics)

    with client:
        yield sse_signals(Signals(client_id=client.client_id))
        async for update in client.stream():
            yield update

@on("playground")
def playground(sender: str, *args,**kwargs):
    # Modern popover testing following LogRocket article
    elements = Div(
        H2("Playground"),

        
        cls="container mx-auto p-8",
        id="content",
    )
    return sse_elements(elements,selector="#content", topic="updates", sender=sender)


@on("component.buttons")
def buttons(sender: str, *args,**kwargs):
    # Button variants
    elements = Div(
        H2("Buttons", cls="text-2xl font-semibold mb-4"),
        Div(
            Button("Default"),
            Button("Destructive", variant="destructive"),
            Button("Outline", variant="outline"),
            Button("Secondary", variant="secondary"),
            Button("Ghost", variant="ghost"),
            Button("Link", variant="link"),
            Button(Icon("settings"), variant="secondary", size="icon"),
            Button("Disabled", disabled=True),
            cls="flex flex-wrap gap-2",
        ),
        cls="container mx-auto p-8",
        id="content",
    )
    return sse_elements(elements,selector="#content", topic="updates", sender=sender)

@on("component.badges")
def badges(sender: str, *args,**kwargs):
    # Button variants
    elements = Div(
                H2("Badges", cls="text-2xl font-semibold mb-4"),
                Div(
                    Badge("Default"),
                    Badge("Secondary", variant="secondary"),
                    Badge("Destructive", variant="destructive"),
                    Badge("Outline", variant="outline"),
                    Badge("Clickable", on_click="alert('Badge clicked!')", cls="cursor-pointer"),
                    cls="flex flex-wrap gap-2",
                ),
            cls="container mx-auto p-8",
            id="content",
        )
    return sse_elements(elements,selector="#content", topic="updates", sender=sender)

@on("component.inputs")
def inputs(sender: str, *args,**kwargs):
    # Button variants
    elements = Div(
                    H2("Inputs", cls="text-2xl font-semibold mb-4"),
                    Div(
                        Div(
                            Label("Text Input", for_="text-input"),
                            Input(
                                bind="name",
                                id="text-input",
                                placeholder="Enter text...",
                            ),
                            cls="space-y-2",
                        ),
                        Div(
                            Label("Email Input", for_="email-input"),
                            Input(
                                bind="email",
                                id="email-input",
                                type="email",
                                placeholder="email@example.com",
                            ),
                            cls="space-y-2",
                        ),
                        Div(
                            Label("Password Input", for_="password-input"),
                            Input(
                                id="password-input", type="password", placeholder="••••••••"
                            ),
                            cls="space-y-2",
                        ),
                        Div(
                            Label("Disabled Input", for_="disabled-input"),
                            Input(
                                id="disabled-input",
                                placeholder="Cannot edit",
                                disabled=True,
                            ),
                            cls="space-y-2",
                        ),
                        cls="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8",
                    ),
            cls="container mx-auto p-8",
            id="content",
        )
    return sse_elements(elements,selector="#content", topic="updates", sender=sender)

@on("component.cards")
def cards(sender: str, *args,**kwargs):
    # Button variants
    elements = Div(
                    H2("Card", cls="text-2xl font-semibold mb-4"),
                    Card(
                        CardHeader(
                            CardTitle("Card Title"),
                            CardDescription(
                                "This is a card description with some example text."
                            ),
                        ),
                        CardContent(
                            P("Card content goes here. You can add any elements you want."),
                            Div(Input(placeholder="Card input field"), cls="mt-4"),
                        ),
                        CardFooter(
                            Button("Cancel", variant="outline"),
                            Button("Save"),
                            cls="flex gap-2",
                        ),
                        cls="max-w-md mb-8",
                    ),
                    cls="container mx-auto p-8",
                    id="content",
                )                
    return sse_elements(elements,selector="#content", topic="updates", sender=sender)

@on("component.checkbox")
def checkbox(sender: str, *args,**kwargs):
    # Button variants
    elements = Div(
                    H2("Checkboxes", cls="text-2xl font-semibold mb-4"),
                    Div(
                        CheckboxWithLabel(
                            "Accept terms and conditions", signal="terms", required=True
                        ),
                        CheckboxWithLabel(
                            "Subscribe to newsletter",
                            signal="newsletter",
                            helper_text="Get weekly updates about new features",
                        ),
                        CheckboxWithLabel(
                            "Enable notifications", signal="notifications", checked=True
                        ),
                        CheckboxWithLabel(
                            "Disabled option",
                            disabled=True,
                            helper_text="This option is currently unavailable",
                        ),
                        CheckboxWithLabel(
                            "Error state example",
                            signal="error_checkbox",
                            error_text="This field is required",
                        ),
                        # Custom styled checkbox with blue background
                        Div(
                            CheckboxWithLabel(
                                "Custom blue checkbox",
                                signal="blue_checkbox",
                                helper_text="With custom blue styling when checked",
                                checkbox_cls="checked:!bg-blue-600 checked:!border-blue-600 dark:checked:!bg-blue-700 dark:checked:!border-blue-700",
                                indicator_cls="!text-white",
                            ),
                            cls="p-4 border rounded-lg",
                        ),
                        cls="space-y-4 mb-8",
                    ),
                    cls="container mx-auto p-8",
                    id="content",
                )                
    return sse_elements(elements,selector="#content", topic="updates", sender=sender)

@on("component.alerts")
def alerts(sender: str, *args,**kwargs):
    elements = Div(
                    Div(
                        H2("Alerts", cls="text-2xl font-semibold mb-4"),
                        Div(
                            Alert(
                                AlertTitle("Default Alert"),
                                AlertDescription("This is a default alert message."),
                            ),
                            Alert(
                                AlertTitle("Destructive Alert"),
                                AlertDescription("This is a destructive alert message."),
                                variant="destructive",
                            ),
                            cls="space-y-4 mb-8",
                        ),
                    ),
                    cls="container mx-auto p-8",
                    id="content",
                )                
    return sse_elements(elements,selector="#content", topic="updates", sender=sender)

@on("component.radios")
def radios(sender: str, *args,**kwargs):
    elements = Div(
                    H2("Radio Groups", cls="text-2xl font-semibold mb-4"),
                    Div(
                        RadioGroupWithLabel(
                            "Select your plan",
                            options=[
                                {"value": "free", "label": "Free - $0/month"},
                                {"value": "pro", "label": "Pro - $10/month"},
                                {"value": "enterprise", "label": "Enterprise - Custom"},
                            ],
                            value="free",
                            signal="plan",
                            helper_text="Choose the plan that best fits your needs",
                        ),
                        RadioGroupWithLabel(
                            label="Notification preferences",
                            options=[
                                {"value": "all", "label": "All notifications"},
                                {"value": "important", "label": "Important only"},
                                {"value": "none", "label": "No notifications"},
                            ],
                            signal="notifications_radio",
                            orientation="horizontal",
                            required=True,
                        ),
                        RadioGroupWithLabel(
                            label="Size",
                            options=[
                                {"value": "sm", "label": "Small"},
                                {"value": "md", "label": "Medium"},
                                {"value": "lg", "label": "Large"},
                                {"value": "xl", "label": "Extra Large", "disabled": True},
                            ],
                            signal="size_radio",
                            required=True,
                            error_text="Please select a size",
                        ),
                        Div(
                            P(
                                "Simple radio group (fully auto-managed):",
                                cls="text-sm font-medium mb-2",
                            ),
                            RadioGroup(
                                RadioGroupItem("small", "Small"),
                                RadioGroupItem("medium", "Medium"),
                                RadioGroupItem("large", "Large"),
                                value="medium",
                            ),
                            cls="p-4 border rounded-lg",
                        ),
                        Div(
                            P(
                                "Custom styled radio group (blue indicator):",
                                cls="text-sm font-medium mb-2",
                            ),
                            RadioGroup(
                                RadioGroupItem(
                                    "option1",
                                    "Option 1",
                                    indicator_cls="[&>div]:bg-blue-600 dark:[&>div]:bg-blue-500",
                                ),
                                RadioGroupItem(
                                    "option2",
                                    "Option 2",
                                    indicator_cls="[&>div]:bg-blue-600 dark:[&>div]:bg-blue-500",
                                ),
                                RadioGroupItem(
                                    "option3",
                                    "Option 3",
                                    disabled=True,
                                    indicator_cls="[&>div]:bg-blue-600 dark:[&>div]:bg-blue-500",
                                ),
                                value="option2",
                            ),
                            cls="p-4 border rounded-lg",
                        ),
                        cls="space-y-6 mb-8",
                    ),
                    cls="container mx-auto p-8",
                    id="content",
                )                
    return sse_elements(elements,selector="#content", topic="updates", sender=sender)

@on("component.breadcrumb")
def breadcrumb(sender: str, *args,**kwargs):
    elements = Div(
                    H2("Breadcrumb", cls="text-2xl font-semibold mb-4"),
                    Breadcrumb(
                        BreadcrumbList(
                            BreadcrumbItem(BreadcrumbLink("Home", href="/")),
                            BreadcrumbSeparator(),
                            BreadcrumbItem(
                                BreadcrumbLink("Components", href="/components")
                            ),
                            BreadcrumbSeparator(),
                            BreadcrumbItem(BreadcrumbPage("Current Page")),
                        )
                    ),
                    cls="container mx-auto p-8",
                    id="content",
                )                
    return sse_elements(elements,selector="#content", topic="updates", sender=sender)

@on("component.tabs")
def tabs(sender: str, *args,**kwargs):
    elements = Div(
                    H2("Tabs - Default Variant", cls="text-2xl font-semibold mb-4"),
                    Tabs(
                        TabsList(
                            TabsTrigger("Preview", id="preview"),
                            TabsTrigger("Code", id="code"),
                            TabsTrigger("Settings", id="settings"),
                        ),
                        TabsContent(
                            Card(
                                H3("Preview Content", cls="text-lg font-semibold mb-2"),
                                P(
                                    "This is the preview tab content with the default boxed style."
                                ),
                                Button(
                                    "Action in Preview", variant="secondary", cls="mt-4"
                                ),
                            ),
                            id="preview",
                        ),
                        TabsContent(
                            Card(
                                H3("Code Content", cls="text-lg font-semibold mb-2"),
                                Pre(
                                    Code(
                                        "# Example code\ndef hello_world():\n    print('Hello, World!')",
                                        cls="block p-4 bg-muted rounded",
                                    )
                                ),
                            ),
                            id="code",
                        ),
                        TabsContent(
                            Card(
                                H3("Settings Content", cls="text-lg font-semibold mb-2"),
                                P("Configure your preferences here."),
                                Div(
                                    Label("Enable notifications", for_="notifications"),
                                    Input(type="checkbox", id="notifications", cls="ml-2"),
                                    cls="flex items-center gap-2 mt-4",
                                ),
                            ),
                            id="settings",
                        ),
                        default_id="preview",
                        variant="default",
                        cls="mb-8",
                    ),
                    H2("Tabs - Plain Variant", cls="text-2xl font-semibold mb-4"),
                    Tabs(
                        TabsList(
                            TabsTrigger("Account", id="account"),
                            TabsTrigger("Password", id="password"),
                            TabsTrigger("Team", id="team"),
                            TabsTrigger("Billing", id="billing"),
                        ),
                        TabsContent(
                            Div(
                                H3("Account Settings", cls="text-lg font-semibold mb-2"),
                                P("Manage your account settings and preferences."),
                                Div(
                                    Label("Username", for_="username"),
                                    Input(
                                        id="username",
                                        placeholder="Enter username",
                                        cls="max-w-sm",
                                    ),
                                    cls="space-y-2 mt-4",
                                ),
                            ),
                            id="account",
                        ),
                        TabsContent(
                            Div(
                                H3("Password & Security", cls="text-lg font-semibold mb-2"),
                                P("Update your password and security settings."),
                                Button("Change Password", variant="outline", cls="mt-4"),
                            ),
                            id="password",
                        ),
                        TabsContent(
                            Div(
                                H3("Team Members", cls="text-lg font-semibold mb-2"),
                                P("Manage your team and collaborate with others."),
                            ),
                            id="team",
                        ),
                        TabsContent(
                            Div(
                                H3("Billing Information", cls="text-lg font-semibold mb-2"),
                                P("View and manage your subscription and payment methods."),
                            ),
                            id="billing",
                        ),
                        default_id="account",
                        variant="plain",
                        cls="mb-8",
                    ),
                    cls="container mx-auto p-8",
                    id="content",
                )                
    return sse_elements(elements,selector="#content", topic="updates", sender=sender)

@on("component.dialogs")
def dialogs(sender: str, *args,**kwargs):
    elements = Div(
                    Div(
                    H2("Dialog (Modal)", cls="text-2xl font-semibold mb-4"),
                    Dialog(
                        trigger=DialogTrigger("Edit Profile", ref_id="edit-profile-dialog"),
                        content=DialogContent(
                            DialogHeader(
                                DialogTitle("Edit Profile"),
                                DialogDescription(
                                    "Make changes to your profile here. Click save when you're done."
                                ),
                            ),
                            Div(
                                Div(
                                    Label("Name", for_="dialog-name"),
                                    Input(
                                        id="dialog-name",
                                        placeholder="Your name",
                                        cls="mt-1",
                                    ),
                                    cls="space-y-2",
                                ),
                                Div(
                                    Label("Email", for_="dialog-email"),
                                    Input(
                                        id="dialog-email",
                                        type="email",
                                        placeholder="your@email.com",
                                        cls="mt-1",
                                    ),
                                    cls="space-y-2",
                                ),
                                cls="grid gap-4 py-4",
                            ),
                            DialogFooter(
                                DialogClose("Cancel", variant="outline"),
                                DialogClose("Save changes"),
                            ),
                        ),
                        ref_id="edit-profile-dialog",
                        size="md",
                    ),
                    cls="mb-8",
                ),
                # Dialog with different size and content
                Separator(cls="my-4"),
                Div(
                    H2("Dialog (Small Size)", cls="text-2xl font-semibold mb-4"),
                    Dialog(
                            trigger=DialogTrigger(
                                "Delete Account", ref_id="delete-dialog", variant="destructive"
                            ),
                            content=DialogContent(
                                DialogHeader(
                                    DialogTitle("Are you absolutely sure?"),
                                    DialogDescription(
                                        "This action cannot be undone. This will permanently delete your "
                                        "account and remove your data from our servers."
                                    ),
                                ),
                                DialogFooter(
                                    DialogClose("Cancel", variant="outline"),
                                    DialogClose("Yes, delete account", variant="destructive"),
                                ),
                            ),
                            ref_id="delete-dialog",
                            size="sm",
                        ),
                        cls="mb-8",
                    ),
                    Separator(cls="my-4"),
                    # Alert Dialog examples
                    Div(
                        H2("Alert Dialog", cls="text-2xl font-semibold mb-4"),
                        Div(
                            # Basic alert dialog
                            AlertDialog(
                                trigger=AlertDialogTrigger(
                                    "Show Alert", 
                                    ref_id="basic_alert"
                                ),
                                content=AlertDialogContent(
                                    AlertDialogHeader(
                                        AlertDialogTitle("Are you absolutely sure?"),
                                        AlertDialogDescription(
                                            "This action cannot be undone. This will permanently delete your "
                                            "account and remove your data from our servers."
                                        ),
                                    ),
                                    AlertDialogFooter(
                                        AlertDialogCancel("Cancel", ref_id="basic_alert"),
                                        AlertDialogAction(
                                            "Continue",
                                            ref_id="basic_alert",
                                            action="console.log('Action confirmed!')",
                                        ),
                                    ),
                                ),
                                ref_id="basic_alert",
                            ),
                            # Destructive alert dialog
                            AlertDialog(
                                trigger=AlertDialogTrigger(
                                    "Delete Item", 
                                    ref_id="destructive_alert",
                                    variant="destructive"
                                ),
                                content=AlertDialogContent(
                                    AlertDialogHeader(
                                        AlertDialogTitle("Delete Item"),
                                        AlertDialogDescription(
                                            "Are you sure you want to delete this item? This action is irreversible."
                                        ),
                                    ),
                                    AlertDialogFooter(
                                        AlertDialogCancel("Cancel", ref_id="destructive_alert"),
                                        AlertDialogAction(
                                            "Delete",
                                            ref_id="destructive_alert",
                                            variant="destructive",
                                            action="console.log('Item deleted!')",
                                        ),
                                    ),
                                ),
                                ref_id="destructive_alert",
                            ),
                            # Alert dialog with custom action
                            AlertDialog(
                                trigger=AlertDialogTrigger(
                                    "Confirm Action", 
                                    ref_id="custom_alert",
                                    variant="outline"
                                ),
                                content=AlertDialogContent(
                                    AlertDialogHeader(
                                        AlertDialogTitle("Confirm Action"),
                                        AlertDialogDescription(
                                            "This will apply the changes you've made. Do you want to proceed?"
                                        ),
                                    ),
                                    AlertDialogFooter(
                                        AlertDialogCancel("Not now", ref_id="custom_alert"),
                                        AlertDialogAction(
                                            "Yes, apply changes",
                                            ref_id="custom_alert",
                                            action="alert('Changes applied successfully!')",
                                        ),
                                    ),
                                ),
                                ref_id="custom_alert",
                            ),
                            cls="flex flex-wrap gap-4",
                        ),
                        cls="mb-8",
                    ),
                
                    cls="container mx-auto p-8",
                    id="content",
                )                
    return sse_elements(elements,selector="#content", topic="updates", sender=sender)

@on("component.switches")
def switches(sender: str, *args,**kwargs):
    elements = Div(
                    H2("Switches", cls="text-2xl font-semibold mb-4"),
                    Div(
                        SwitchWithLabel(
                            "Enable notifications",
                            signal="switch_notifications",
                            checked=True,
                            helper_text="Receive email notifications about updates",
                        ),
                        SwitchWithLabel(
                            "Marketing emails",
                            signal="switch_marketing",
                            helper_text="Get promotional emails and special offers",
                        ),
                        SwitchWithLabel(
                            "Two-factor authentication",
                            signal="switch_2fa",
                            required=True,
                            helper_text="Enhanced security for your account",
                        ),
                        SwitchWithLabel(
                            "Disabled option",
                            disabled=True,
                            helper_text="This feature is not available in your plan",
                        ),
                        SwitchWithLabel(
                            "Error state example",
                            signal="switch_error",
                            error_text="This setting requires admin approval",
                        ),
                        # Simple switches without labels
                        Div(
                            P("Simple switches:", cls="text-sm font-medium mb-2"),
                            Div(
                                Switch(signal="simple1", checked=True),
                                Switch(signal="simple2"),
                                Switch(disabled=True),
                                cls="flex gap-4",
                            ),
                            cls="p-4 border rounded-lg",
                        ),
                        cls="space-y-4 mb-8",
                    ),
                    cls="container mx-auto p-8",
                    id="content",
                )                
    return sse_elements(elements,selector="#content", topic="updates", sender=sender)

@on("component.textareas")
def textareas(sender: str, *args,**kwargs):
    elements = Div(
                    H2("Textareas", cls="text-2xl font-semibold mb-4"),
                    Div(
                        # Basic textarea
                        TextareaWithLabel(
                            "Description",
                            placeholder="Enter your description here...",
                            signal="description",
                            helper_text="Provide a detailed description",
                        ),
                        # Textarea with error
                        TextareaWithLabel(
                            "Bio",
                            placeholder="Tell us about yourself",
                            signal="bio",
                            required=True,
                            error_text="Bio is required and must be at least 50 characters",
                        ),
                        # Disabled textarea
                        TextareaWithLabel(
                            "Notes",
                            value="This field is currently disabled",
                            disabled=True,
                            helper_text="This field will be enabled after verification",
                        ),
                        # Textarea with fixed rows
                        TextareaWithLabel(
                            "Comments",
                            placeholder="Share your thoughts...",
                            signal="comments",
                            rows=5,
                            helper_text="Fixed height with 5 rows",
                        ),
                        # Simple textarea without label
                        Div(
                            P("Simple textarea:", cls="text-sm font-medium mb-2"),
                            Textarea(
                                placeholder="Type something...",
                                signal="simple_textarea",
                                resize="vertical",
                            ),
                            cls="p-4 border rounded-lg",
                        ),
                        cls="space-y-4 mb-8",
                    ),
                    cls="container mx-auto p-8",
                    id="content",
                )                
    return sse_elements(elements,selector="#content", topic="updates", sender=sender)

@on("component.selects")
def selects(sender: str, *args,**kwargs):
    elements = Div(
                    H2("Select", cls="text-2xl font-semibold mb-4"),
                    Div(
                        # Basic select
                        SelectWithLabel(
                            "Country",
                            options=["United States", "Canada", "Mexico", "United Kingdom", "France", "Germany"],
                            placeholder="Choose a country",
                            signal="country",
                            helper_text="Select your country of residence",
                        ),
                        P(text="$country"),
                        SelectWithLabel(
                            "Language",
                            options=[
                                ("en", "English"),
                                ("es", "Spanish"),
                                ("fr", "French"),
                                ("de", "German"),
                                ("jp", "Japanese"),
                            ],
                            value="en",
                            signal="language",
                            helper_text="Choose your preferred language",
                        ),
                        # # Select with groups
                        SelectWithLabel(
                            "Framework",
                            options=[
                                {"group": "Frontend", "items": ["React", "Vue", "Angular", "Svelte"]},
                                {"group": "Backend", "items": [("django", "Django"), ("fastapi", "FastAPI"), ("flask", "Flask")]},
                                {"group": "Full Stack", "items": ["Next.js", "Nuxt", "SvelteKit"]},
                            ],
                            placeholder="Select a framework",
                            signal="framework",
                            required=True,
                        ),
                        # Select with error state
                        SelectWithLabel(
                            "Department",
                            options=["Engineering", "Design", "Marketing", "Sales", "Support"],
                            signal="department",
                            error_text="Please select a valid department",
                            required=True,
                        ),
                        # Disabled select
                        SelectWithLabel(
                            "Plan",
                            options=["Free", "Pro", "Enterprise"],
                            value="Free",
                            disabled=True,
                            helper_text="Upgrade your account to change plans",
                        ),
                        # Simple select without label
                        Div(
                            P("Simple select:", cls="text-sm font-medium mb-2"),
                            Select(
                                SelectTrigger(
                                    SelectValue(placeholder="Pick an option", signal="simple_select"),
                                    signal="simple_select",
                                ),
                                SelectContent(
                                    SelectItem("Option 1", signal="simple_select"),
                                    SelectItem("Option 2", signal="simple_select"),
                                    SelectItem("Option 3", signal="simple_select"),
                                    SelectItem("Disabled", disabled=True, signal="simple_select"),
                                    signal="simple_select",
                                ),
                                signal="simple_select",
                            ),
                            cls="p-4 border rounded-lg",
                        ),
                        cls="space-y-4 mb-8",
                    ),
                    
                    cls="container mx-auto p-8",
                    id="content",
                )                
    return sse_elements(elements,selector="#content", topic="updates", sender=sender)

@on("component.popovers")
def popovers(sender: str, *args,**kwargs):

    # Correct combinations for proper side/align mapping
    combinations = [
        ("top", "left"), ("top", "center"), ("top", "right"),
        ("bottom", "left"), ("bottom", "center"), ("bottom", "right"), 
        ("left", "start"), ("left", "center"), ("left", "end"), 
        ("right", "start"), ("right", "center"), ("right", "end")
    ]

    elements = Div(
                    H2("Popovers with CSS Anchor Positioning", cls="text-2xl font-semibold mb-4"),
                    P("All combinations of side and align with proper anchor positioning and transitions:", cls="text-muted-foreground mb-6"),
                    
                    # Grid layout for triggers, but each popover uses proper anchor positioning
                    Div(
                        *[Div(
                            Div(
                                PopoverTrigger(
                                    f"{combination[0].title()}-{combination[1].title()}",
                                    id=f"{combination[0]}{combination[1]}-trigger",
                                    variant="outline",
                                    popovertarget=f"{combination[0]}{combination[1]}-popover"
                                ),
                                Popover(
                                    Div(
                                        H4(f"{combination[0].title()}-{combination[1].title()}", cls="font-semibold mb-2"),
                                        Div(
                                            f"This popover is positioned on the {combination[0]} side with {combination[1]} alignment using CSS anchor positioning.",
                                            cls="text-sm text-muted-foreground",
                                        ),
                                    ),
                                    position=f"{combination[0]}-{combination[1]}",
                                    id=f"{combination[0]}{combination[1]}-popover",
                                    anchor=f"{combination[0]}{combination[1]}-trigger",
                                    cls="w-64 p-4"
                                ),
                                signal=f"{combination[0]}{combination[1]}"
                            ),
                            cls="flex items-center justify-center p-4"
                        ) for combination in combinations],
                        cls="grid grid-cols-3 gap-6 mb-8",
                    ),
                    
                    # Additional examples with different content
                    Div(
                        H3("Advanced Popover Examples", cls="text-lg font-semibold mb-4"),
                        Div(
                            # Complex content example
                            PopoverTrigger(
                                "Rich Content", 
                                variant="default",
                                popovertarget="rich-popover",
                                id="rich-popover-trigger",
                            ),
                            Popover(
                                Div(
                                    H4("User Profile", cls="font-semibold mb-3"),
                                    Div(
                                        Div("👤", cls="w-12 h-12 bg-muted rounded-full flex items-center justify-center text-2xl"),
                                        Div(
                                            P("John Doe", cls="font-medium"),
                                            P("@johndoe", cls="text-sm text-muted-foreground"),
                                            P("Full-stack developer passionate about building great user experiences.", cls="text-sm"),
                                            Div(
                                                Button("Follow", size="sm"),
                                                Button("Message", variant="outline", size="sm"),
                                                cls="flex items-center gap-2 w-full"
                                            )
                                        ),
                                        cls="flex flex-col items-center gap-2"
                                    ),
                                    cls="text-center flex flex-col items-center gap-2"
                                ),
                                position="bottom-center",
                                anchor="rich-popover-trigger",
                                id="rich-popover",
                            ),
                            
                            # Form in popover
                            PopoverTrigger("Quick Form", variant="secondary", popovertarget="quick-form", id="quick-form-trigger"),
                            Popover(
                                Form(
                                    H4("Quick Contact", cls="font-semibold mb-3"),
                                    Div(
                                        Label("Name", for_="quick-name"),
                                        Input(id="quick-name", placeholder="Your name", cls="mb-3"),
                                        Label("Email", for_="quick-email"),
                                        Input(id="quick-email", type="email", placeholder="your@email.com", cls="mb-3"),
                                        Button("Send", size="sm", cls="w-full"),
                                        cls="space-y-2"
                                    )
                                ),
                                position="top-left",
                                anchor="quick-form-trigger",
                                id="quick-form",
                                cls="w-72 p-4"
                            ),
                            
                            # Menu-style popover
                            PopoverTrigger("Actions Menu", variant="ghost", popovertarget="actions-menu", id="actions-menu-trigger"),
                            Popover(
                                Div(
                                    H4(Span("Actions",cls="font-semibold ms-2"), cls="mb-2 pb-2 border-b"),
                                    Div(
                                        Button("Edit", variant="ghost", size="sm", cls="w-full justify-start"),
                                        Button("Duplicate", variant="ghost", size="sm", cls="w-full justify-start"),
                                        Button("Share", variant="ghost", size="sm", cls="w-full justify-start"),
                                        Separator(cls="my-2"),
                                        Button("Delete", variant="ghost", size="sm", cls="w-full justify-start text-destructive"),
                                        cls="flex flex-col space-y-1"
                                    )
                                ),
                                position="left-end",
                                anchor="actions-menu-trigger",
                                id="actions-menu",
                                cls="w-48"
                            ),
                            cls="flex gap-4 justify-center"
                        ),
                    ),
                    
                    cls="container mx-auto p-8",
                    id="content",
                )                
    return sse_elements(elements,selector="#content", topic="updates", sender=sender)

@on("component.tables")
def tables(sender: str, *args,**kwargs):
    elements = Div(
                    H2("Tables", cls="text-2xl font-semibold mb-4"),
                    Div(
                        # Basic table
                        Div(
                            H3("Basic Table", cls="text-lg font-medium mb-2"),
                            Table(
                                TableHeader(
                                    TableRow(
                                        TableHead("Invoice"),
                                        TableHead("Status"),
                                        TableHead("Method"),
                                        TableHead("Amount", cls="text-right"),
                                    )
                                ),
                                TableBody(
                                    TableRow(
                                        TableCell("INV001"),
                                        TableCell(Badge("Paid", variant="secondary")),
                                        TableCell("Credit Card"),
                                        TableCell("$250.00", cls="text-right"),
                                    ),
                                    TableRow(
                                        TableCell("INV002"),
                                        TableCell(Badge("Pending", variant="outline")),
                                        TableCell("PayPal"),
                                        TableCell("$150.00", cls="text-right"),
                                    ),
                                    TableRow(
                                        TableCell("INV003"),
                                        TableCell(Badge("Unpaid", variant="destructive")),
                                        TableCell("Bank Transfer"),
                                        TableCell("$350.00", cls="text-right"),
                                    ),
                                    TableRow(
                                        TableCell("INV004"),
                                        TableCell(Badge("Paid", variant="secondary")),
                                        TableCell("Credit Card"),
                                        TableCell("$450.00", cls="text-right"),
                                    ),
                                ),
                                TableFooter(
                                    TableRow(
                                        TableCell("Total", colspan="3", cls="font-medium"),
                                        TableCell("$1,200.00", cls="text-right font-medium"),
                                    )
                                ),
                                cls="mb-6",
                            ),
                            cls="mb-8",
                        ),
                        # Table with selection
                        Div(
                            H3("Table with Selection", cls="text-lg font-medium mb-2"),
                            Table(
                                TableCaption("A list of users with selection capabilities."),
                                TableHeader(
                                    TableRow(
                                        TableHead("Select"),
                                        TableHead("Name"),
                                        TableHead("Email"),
                                        TableHead("Role"),
                                        TableHead("Actions"),
                                    )
                                ),
                                TableBody(
                                    TableRow(
                                        TableCell(Checkbox(signal="user_1")),
                                        TableCell("John Doe"),
                                        TableCell("john@example.com"),
                                        TableCell(Badge("Admin")),
                                        TableCell(
                                            Button("Edit", variant="ghost", size="sm"),
                                            cls="space-x-2",
                                        ),
                                    ),
                                    TableRow(
                                        TableCell(Checkbox(signal="user_2", checked=True)),
                                        TableCell("Jane Smith"),
                                        TableCell("jane@example.com"),
                                        TableCell(Badge("User", variant="secondary")),
                                        TableCell(
                                            Button("Edit", variant="ghost", size="sm"),
                                            cls="space-x-2",
                                        ),
                                        selected=True,
                                    ),
                                    TableRow(
                                        TableCell(Checkbox(signal="user_3")),
                                        TableCell("Bob Johnson"),
                                        TableCell("bob@example.com"),
                                        TableCell(Badge("User", variant="secondary")),
                                        TableCell(
                                            Button("Edit", variant="ghost", size="sm"),
                                            cls="space-x-2",
                                        ),
                                    ),
                                ),
                                cls="mb-6",
                            ),
                            cls="mb-8",
                        ),
                        # Compact table
                        Div(
                            H3("Compact Table", cls="text-lg font-medium mb-2"),
                            Table(
                                TableHeader(
                                    TableRow(
                                        TableHead("Product"),
                                        TableHead("Price"),
                                        TableHead("Stock"),
                                        TableHead("Category"),
                                    )
                                ),
                                TableBody(
                                    TableRow(
                                        TableCell("Laptop"),
                                        TableCell("$999"),
                                        TableCell("12"),
                                        TableCell("Electronics"),
                                    ),
                                    TableRow(
                                        TableCell("Mouse"),
                                        TableCell("$29"),
                                        TableCell("45"),
                                        TableCell("Electronics"),
                                    ),
                                    TableRow(
                                        TableCell("Keyboard"),
                                        TableCell("$79"),
                                        TableCell("8"),
                                        TableCell("Electronics"),
                                    ),
                                ),
                                cls="text-xs [&_th]:h-8 [&_td]:p-1 [&_th]:p-1",
                            ),
                            cls="mb-8",
                        ),
                        cls="space-y-4 mb-8",
                    ),
                    cls="container mx-auto p-8",
                    id="content",
                )                
    return sse_elements(elements,selector="#content", topic="updates", sender=sender)

@on("component.dropdown_menu")
def dropdown_menu(sender: str, *args,**kwargs):
    # Button variants
    elements = Div(
                    H2("Dropdown Menus", cls="text-2xl font-semibold mb-4"),
                    Div(
                        # Basic dropdown
                        DropdownMenu(
                            DropdownMenuTrigger("Open Menu"),
                            DropdownMenuContent(
                                DropdownMenuLabel("My Account"),
                                DropdownMenuSeparator(),
                                DropdownMenuItem("Profile", DropdownMenuShortcut("⇧⌘P")),
                                DropdownMenuItem("Billing", DropdownMenuShortcut("⌘B")),
                                DropdownMenuItem("Settings", DropdownMenuShortcut("⌘S")),
                                DropdownMenuSeparator(),
                                DropdownMenuItem("Log out", DropdownMenuShortcut("⇧⌘Q"), variant="destructive"),
                            ),
                        ),
                        # Dropdown with checkboxes
                        DropdownMenu(
                            DropdownMenuTrigger("Options", variant="secondary"),
                            DropdownMenuContent(
                                DropdownMenuLabel("Appearance"),
                                DropdownMenuSeparator(),
                                DropdownMenuCheckboxItem("Status Bar", checked_signal="statusBar"),
                                DropdownMenuCheckboxItem("Activity Bar", checked_signal="activityBar", disabled=True),
                                DropdownMenuCheckboxItem("Panel", checked_signal="panel"),
                            ),
                            signal="checkbox_dropdown",
                        ),
                        # Dropdown with radio items
                        DropdownMenu(
                            DropdownMenuTrigger("Select Position", variant="outline"),
                            DropdownMenuContent(
                                DropdownMenuLabel("Position"),
                                DropdownMenuSeparator(),
                                DropdownMenuRadioGroup(
                                    DropdownMenuRadioItem("Top", value="top", value_signal="position"),
                                    DropdownMenuRadioItem("Bottom", value="bottom", value_signal="position"),
                                    DropdownMenuRadioItem("Right", value="right", value_signal="position"),
                                    value_signal="position",
                                ),
                            ),
                            signal="radio_dropdown",
                        ),
                        signals= Signals({
                            "statusBar": True,
                            "activityBar": False,
                            "panel": False,
                            "position": "bottom",
                        }),
                        cls="flex flex-wrap gap-4 mb-8",
                    ),
                    cls="container mx-auto p-8",
                    id="content",
                )                
    return sse_elements(elements,selector="#content", topic="updates", sender=sender)

@on("component.hover_cards")
def hover_cards(sender: str, *args,**kwargs):
    # Button variants
    elements = Div(
                    H2("Hover Cards", cls="text-2xl font-semibold mb-4"),
                    Div(
                        # Basic hover card
                        HoverCardTrigger(
                            Span("@username", cls="text-blue-600 underline cursor-pointer"),
                            id="userHoverTrigger",
                            popovertarget="userHoverContent",
                        ),
                        HoverCard(
                            Div(
                                Div(
                                    Div("👤", cls="w-12 h-12 bg-muted rounded-full flex items-center justify-center text-2xl mb-3"),
                                    H3("John Doe", cls="font-semibold mb-1"),
                                    P("@username", cls="text-sm text-muted-foreground mb-2"),
                                    P("Full-stack developer passionate about building great user experiences.", cls="text-sm"),
                                    cls="text-center",
                                ),
                            ),
                            id="userHoverContent",
                            anchor="userHoverTrigger",
                        ),
                        # Hover card with different positioning
                        HoverCardTrigger(
                            Button("Hover for info", variant="outline"),
                            id="infoHoverTrigger",
                            popovertarget="infoHoverContent",
                        ),
                        HoverCard(
                            Div(
                                H3("Quick Info", cls="font-semibold mb-2"),
                                P("This hover card appears when you hover over the trigger element.", cls="text-sm text-muted-foreground mb-2"),
                                P("It stays open while you're hovering over either the trigger or the content.", cls="text-sm"),
                            ),
                            id="infoHoverContent",
                            anchor="infoHoverTrigger",
                            side="top",
                        ),
                        # Product hover card
                        HoverCardTrigger(
                            Badge("Product Info", variant="secondary"),
                            id="productHoverTrigger",
                            popovertarget="productHoverContent",
                        ),
                        HoverCard(
                            Div(
                                Div(
                                    H3("StarUI Components", cls="font-semibold mb-2"),
                                    Badge("v1.0.0", variant="outline", cls="mb-2"),
                                    P("A modern component library built with StarHTML and Datastar for reactive Python web apps.", cls="text-sm text-muted-foreground mb-3"),
                                    Div(
                                        Badge("Python"),
                                        Badge("StarHTML", variant="secondary"),
                                        Badge("Datastar", variant="outline"),
                                        cls="flex gap-1",
                                    ),
                                ),
                            ),
                            id="productHoverContent",
                            anchor="productHoverTrigger",
                            position="left-start",
                        ),
                        cls="flex flex-wrap gap-4 mb-8",
                    ),
                    cls="container mx-auto p-8",
                    id="content",
                )                
    return sse_elements(elements,selector="#content", topic="updates", sender=sender)

@on("component.toggles")
def toggles(sender: str, *args,**kwargs):
    elements = Div(
                    H2("Toggles", cls="text-2xl font-semibold mb-4"),
                    Div(
                        # Basic toggles
                        Div(
                            P("Basic toggles:", cls="text-sm font-medium mb-2"),
                            Div(
                                Toggle(Icon("bold"), signal="toggle_bold"),
                                Toggle(Icon("italic"), signal="toggle_italic", pressed=True),
                                Toggle(Icon("underline"), signal="toggle_underline"),
                                Toggle(Icon("strikethrough"), disabled=True),
                                cls="flex gap-1",
                            ),
                            cls="mb-4",
                        ),
                        # Outline variant toggles
                        Div(
                            P("Outline variant:", cls="text-sm font-medium mb-2"),
                            Div(
                                Toggle(Icon("align-left"), variant="outline", signal="align_left"),
                                Toggle(Icon("align-center"), variant="outline", signal="align_center", pressed=True),
                                Toggle(Icon("align-right"), variant="outline", signal="align_right"),
                                Toggle(Icon("align-justify"), variant="outline", signal="align_justify"),
                                cls="flex gap-1",
                            ),
                            cls="mb-4",
                        ),
                        # Different sizes
                        Div(
                            P("Different sizes:", cls="text-sm font-medium mb-2"),
                            Div(
                                Toggle("Small", size="sm", variant="outline", signal="size_sm"),
                                Toggle("Default", size="default", variant="outline", signal="size_default"),
                                Toggle("Large", size="lg", variant="outline", signal="size_lg"),
                                cls="flex gap-2 items-center",
                            ),
                            cls="mb-4",
                        ),
                        # Toggle with text
                        Div(
                            P("Toggle with text:", cls="text-sm font-medium mb-2"),
                            Div(
                                Toggle(
                                    Icon("wifi"),
                                    Span("WiFi", cls="ml-1"),
                                    variant="outline",
                                    signal="wifi_toggle",
                                ),
                                Toggle(
                                    Icon("bluetooth"),
                                    Span("Bluetooth", cls="ml-1"),
                                    variant="outline",
                                    signal="bluetooth_toggle",
                                    pressed=True,
                                ),
                                Toggle(
                                    Icon("plane"),
                                    Span("Airplane Mode", cls="ml-1"),
                                    variant="outline",
                                    signal="airplane_toggle",
                                ),
                                cls="flex gap-2",
                            ),
                            cls="mb-4",
                        ),
                        cls="space-y-4 mb-8",
                    ),
                    H2("Toggle Groups", cls="text-2xl font-semibold mb-4"),
                    Div(
                        # Single selection toggle group
                        Div(
                            P("Text formatting (single selection):", cls="text-sm font-medium mb-2"),
                            SingleToggleGroup(
                                ("bold", Icon("bold")),
                                ("italic", Icon("italic")),
                                ("underline", Icon("underline")),
                                signal="text_format",
                                variant="outline",
                            ),
                            cls="mb-4",
                        ),
                        # Multiple selection toggle group
                        Div(
                            P("Text options (multiple selection):", cls="text-sm font-medium mb-2"),
                            MultipleToggleGroup(
                                ("bold", Icon("bold")),
                                ("italic", Icon("italic")),
                                ("underline", Icon("underline")),
                                ("strikethrough", Icon("strikethrough")),
                                signal="text_options",
                                variant="outline",
                            ),
                            cls="mb-4",
                        ),
                        # Alignment toggle group
                        Div(
                            P("Text alignment:", cls="text-sm font-medium mb-2"),
                            SingleToggleGroup(
                                ("left", Icon("align-left")),
                                ("center", Icon("align-center")),
                                ("right", Icon("align-right")),
                                ("justify", Icon("align-justify")),
                                signal="alignment",
                                variant="default",
                            ),
                            cls="mb-4",
                        ),
                        # Size toggle group
                        Div(
                            P("Size selection:", cls="text-sm font-medium mb-2"),
                            SingleToggleGroup(
                                ("sm", "Small"),
                                ("md", "Medium"),
                                ("lg", "Large"),
                                ("xl", "Extra Large"),
                                signal="size_selection",
                                variant="outline",
                                size="lg",
                            ),
                            cls="mb-4",
                        ),
                        # View mode toggle group
                        Div(
                            P("View mode:", cls="text-sm font-medium mb-2"),
                            SingleToggleGroup(
                                ("list", Div(Icon("list"), Span("List", cls="ml-1"))),
                                ("grid", Div(Icon("layout-grid"), Span("Grid", cls="ml-1"))),
                                ("gallery", Div(Icon("image"), Span("Gallery", cls="ml-1"))),
                                signal="view_mode",
                                variant="outline",
                            ),
                            cls="mb-4",
                        ),
                        # Disabled toggle group
                        Div(
                            P("Disabled group:", cls="text-sm font-medium mb-2"),
                            SingleToggleGroup(
                                ("option1", "Option 1"),
                                ("option2", "Option 2"),
                                ("option3", "Option 3"),
                                signal="disabled_group",
                                variant="outline",
                                disabled=True,
                            ),
                            cls="mb-4",
                        ),
                        cls="space-y-4 mb-8",
                    ),
                    cls="container mx-auto p-8",
                    id="content",
                )                
    return sse_elements(elements,selector="#content", topic="updates", sender=sender)

@on("component.avatars")
def avatars(sender: str, *args,**kwargs):
    # Button variants
    elements = Div(
                    H2("Avatars", cls="text-2xl font-semibold mb-4"),
                    Div(
                        # Basic Avatar with image
                        Div(
                            H3("Basic Avatar", cls="text-lg font-medium mb-2"),
                            Div(
                                Avatar(
                                    AvatarImage(
                                        src="https://github.com/shadcn.png",
                                        alt="@shadcn"
                                    )
                                ),
                                Avatar(
                                    AvatarFallback("CN")
                                ),
                                Avatar(
                                    AvatarImage(
                                        src="https://avatars.githubusercontent.com/u/1?v=4",
                                        alt="User"
                                    )
                                ),
                                cls="flex gap-4 items-center"
                            ),
                            cls="mb-6",
                        ),
                        # Different sizes (composition example)
                        Div(
                            H3("Avatar Sizes", cls="text-lg font-medium mb-2"),
                            P("Use size classes to customize:", cls="text-sm text-muted-foreground mb-2"),
                            Div(
                                Avatar(AvatarFallback("XS"), cls="size-6"),
                                Avatar(AvatarFallback("SM"), cls="size-8"),
                                Avatar(AvatarFallback("MD")),  # default size-10
                                Avatar(AvatarFallback("LG"), cls="size-12"),
                                Avatar(AvatarFallback("XL"), cls="size-16"),
                                Avatar(AvatarFallback("2X"), cls="size-20"),
                                cls="flex gap-4 items-center"
                            ),
                            cls="mb-6",
                        ),
                        # Avatar with automatic fallback
                        Div(
                            H3("Automatic Fallback", cls="text-lg font-medium mb-2"),
                            P("The second avatar will show fallback as the image URL is invalid:", cls="text-sm text-muted-foreground mb-2"),
                            Div(
                                AvatarWithFallback(
                                    src="https://github.com/shadcn.png",
                                    alt="@shadcn",
                                    fallback="CN"
                                ),
                                AvatarWithFallback(
                                    src="https://invalid-url.com/image.jpg",
                                    alt="Invalid",
                                    fallback="IN"
                                ),
                                AvatarWithFallback(
                                    fallback="NI"
                                ),
                                cls="flex gap-4 items-center"
                            ),
                            cls="mb-6",
                        ),
                        # Avatar Group (composition example)
                        Div(
                            H3("Avatar Group", cls="text-lg font-medium mb-2"),
                            P("Compose avatars with overlapping styles:", cls="text-sm text-muted-foreground mb-2"),
                            Div(
                                Div(
                                    Avatar(AvatarFallback("JD")),
                                    Avatar(AvatarFallback("AS")),
                                    Avatar(AvatarFallback("PQ")),
                                    Avatar(AvatarFallback("+2", cls="text-xs font-medium")),
                                    cls="flex -space-x-2 [&>*[data-slot=avatar]]:ring-2 [&>*[data-slot=avatar]]:ring-background"
                                ),
                                cls="mb-2"
                            ),
                            cls="mb-6",
                        ),
                        # Avatar with Badge (composition example)
                        Div(
                            H3("Avatar with Badge", cls="text-lg font-medium mb-2"),
                            P("Compose with absolute positioning:", cls="text-sm text-muted-foreground mb-2"),
                            Div(
                                # Green status badge
                                Div(
                                    Avatar(AvatarFallback("JD")),
                                    Span(cls="absolute bottom-0 right-0 size-3 bg-green-500 rounded-full ring-2 ring-background"),
                                    cls="relative inline-block"
                                ),
                                # Red status badge
                                Div(
                                    Avatar(AvatarFallback("AS")),
                                    Span(cls="absolute bottom-0 right-0 size-3 bg-red-500 rounded-full ring-2 ring-background"),
                                    cls="relative inline-block"
                                ),
                                # Badge with count
                                Div(
                                    Avatar(AvatarFallback("MN")),
                                    Span("5", cls="absolute bottom-0 right-0 size-4 bg-red-500 rounded-full ring-2 ring-background flex items-center justify-center text-[8px] font-bold text-white"),
                                    cls="relative inline-block"
                                ),
                                cls="flex gap-4 items-center"
                            ),
                            cls="mb-6",
                        ),
                        # Avatar from Initials (composition example)
                        Div(
                            H3("Avatar from Initials", cls="text-lg font-medium mb-2"),
                            P("Use colored backgrounds for initials:", cls="text-sm text-muted-foreground mb-2"),
                            Div(
                                Avatar(AvatarFallback("JD", cls="bg-red-600 dark:bg-red-500 text-white font-semibold")),
                                Avatar(AvatarFallback("AS", cls="bg-blue-600 dark:bg-blue-500 text-white font-semibold")),
                                Avatar(AvatarFallback("PQ", cls="bg-green-600 dark:bg-green-500 text-white font-semibold")),
                                Avatar(AvatarFallback("MN", cls="bg-purple-600 dark:bg-purple-500 text-white font-semibold")),
                                Avatar(AvatarFallback("XY", cls="bg-orange-600 dark:bg-orange-500 text-white font-semibold")),
                                cls="flex gap-4 items-center"
                            ),
                            cls="mb-6",
                        ),
                        cls="space-y-4 mb-8",
                    ),
                    cls="container mx-auto p-8",
                    id="content",
                )                
    return sse_elements(elements,selector="#content", topic="updates", sender=sender)


@on("component.separators")
def separators(sender: str, *args,**kwargs):
    # Button variants
    elements = Div(
                    H2("Separators", cls="text-2xl font-semibold mb-4"),
                    Div(
                        Div(
                            P("Content above separator", cls="mb-4"),
                            Separator(),
                            P("Content below separator", cls="mt-4"),
                            cls="mb-6",
                        ),
                        Div(
                            H3("Vertical Separators", cls="text-lg font-medium mb-2"),
                            Div(
                                Span("Left content"),
                                Separator(orientation="vertical", cls="mx-4"),
                                Span("Right content"),
                                cls="flex items-center h-8",
                            ),
                            cls="mb-6",
                        ),
                        Div(
                            H3("Custom Styling", cls="text-lg font-medium mb-2"),
                            Div(
                                P("Custom colored separator below:", cls="mb-2"),
                                Separator(cls="bg-red-500 h-0.5"),
                                P("Thicker separator with different color:", cls="mt-4 mb-2"),
                                Separator(cls="bg-blue-500 h-1"),
                            ),
                        ),
                        cls="space-y-4 mb-8",
                    ),
                    


                    cls="container mx-auto p-8",
                    id="content",
                )                
    return sse_elements(elements,selector="#content", topic="updates", sender=sender)

@on("component.skeletons")
def skeletons(sender: str, *args,**kwargs):
    # Button variants
    elements = Div(
                    H2("Skeleton", cls="text-2xl font-semibold mb-4"),
                    Div(
                        # Basic skeleton shapes
                        Div(
                            H3("Basic Shapes", cls="text-lg font-medium mb-2"),
                            Div(
                                Skeleton(cls="h-4 w-64"),  # Text line
                                Skeleton(cls="h-4 w-48"),  # Shorter text line
                                Skeleton(cls="h-4 w-56"),  # Another text line
                                cls="space-y-2 mb-4",
                            ),
                            cls="mb-6",
                        ),
                        # Card skeleton
                        Div(
                            H3("Card Skeleton", cls="text-lg font-medium mb-2"),
                            Div(
                                Div(
                                    Skeleton(cls="h-12 w-12 rounded-full"),  # Avatar
                                    Div(
                                        Skeleton(cls="h-4 w-32"),  # Name
                                        Skeleton(cls="h-3 w-24"),  # Subtitle
                                        cls="space-y-2",
                                    ),
                                    cls="flex items-center space-x-4",
                                ),
                                Skeleton(cls="h-32 w-full mt-4"),  # Content area
                                Skeleton(cls="h-4 w-full mt-4"),  # Footer line
                                cls="p-4 border rounded-lg",
                            ),
                            cls="mb-6",
                        ),
                        # Article skeleton
                        Div(
                            H3("Article Skeleton", cls="text-lg font-medium mb-2"),
                            Div(
                                Skeleton(cls="h-8 w-3/4 mb-4"),  # Title
                                Skeleton(cls="h-3 w-32 mb-6"),  # Date
                                Div(
                                    Skeleton(cls="h-4 w-full"),
                                    Skeleton(cls="h-4 w-full"),
                                    Skeleton(cls="h-4 w-2/3"),
                                    cls="space-y-2 mb-4",
                                ),
                                Skeleton(cls="h-40 w-full"),  # Image placeholder
                                cls="p-4 border rounded-lg",
                            ),
                            cls="mb-6",
                        ),
                        # Interactive skeleton toggle
                        Div(
                            H3("Loading State Toggle", cls="text-lg font-medium mb-2"),
                            Div(
                                Button(
                                    text="$loading ? 'Stop Loading' : 'Start Loading'",
                                    on_click="$loading = !$loading",
                                    variant="outline",
                                    cls="mb-4",
                                ),
                                # Content that toggles based on loading state
                                Div(
                                    Skeleton(cls="h-6 w-48 mb-2"),
                                    Skeleton(cls="h-4 w-64 mb-4"),
                                    Skeleton(cls="h-20 w-full"),
                                    show="$loading",
                                ),
                                Div(
                                    H4("Content Loaded!", cls="text-lg font-semibold mb-2"),
                                    P("This content appears when loading is complete.", cls="mb-4"),
                                    Div(
                                        "This is the actual content that would load.",
                                        cls="p-4 bg-muted rounded-lg",
                                    ),
                                    show="!$loading",
                                ),
                                signals= Signals(loading=True),
                                cls="p-4 border rounded-lg",
                            ),
                            cls="mb-6",
                        ),
                        cls="space-y-4 mb-8",
                    ),
                    cls="container mx-auto p-8",
                    id="content",
                )                
    return sse_elements(elements,selector="#content", topic="updates", sender=sender)

# @on("component.cards")
# def cards(sender: str, *args,**kwargs):
#     # Button variants
#     elements = Div(
#                     H2("Card", cls="text-2xl font-semibold mb-4"),
#                     


#                     cls="container mx-auto p-8",
#                     id="content",
#                 )                
#     return sse_elements(elements,selector="#content", topic="updates", sender=sender)

@app.get("/")
@page(title="RustyStarUi Component Test", wrap_in=HTMLResponse)
def index():
    return Div(
        sidebar,
        Main(navbar,
            # Main content container
            Div(
                H1("StarUI Component Test"),

                # Sheet example
                Div(
                    # H2("Sheet (Modal Drawer)", cls="text-2xl font-semibold mb-4"),
                    # Sheet(
                    #     SheetTrigger("Open Sheet", signal="demo_sheet"),
                    #     SheetContent(
                    #         SheetHeader(
                    #             SheetTitle("Sheet Title", signal="demo_sheet"),
                    #             SheetDescription(
                    #                 "This is a sheet description.", signal="demo_sheet"
                    #             ),
                    #         ),
                    #         Div(
                    #             P(
                    #                 "Sheet content goes here. Press ESC or click outside to close."
                    #             ),
                    #             Input(placeholder="Type something..."),
                    #             cls="p-6 space-y-4",
                    #         ),
                    #         SheetFooter(
                    #             Button(
                    #                 "Cancel",
                    #                 on_click="$demo_sheet_open = false",
                    #                 variant="outline",
                    #             ),
                    #             Button("Save Changes"),
                    #         ),
                    #         signal="demo_sheet",
                    #         side="right",
                    #         size="md",
                    #     ),
                    #     signal="demo_sheet",
                    #     side="right",
                    #     size="md",
                    #     modal=True,
                    # ),
                    # cls="mb-8",
                ),                
                    
                Separator(cls="my-4"),
                # Accordion examples
                Div(
                    H2("Accordion", cls="text-2xl font-semibold mb-4"),
                    Div(
                        # Single accordion with collapsible
                        Div(
                            P(
                                "Single selection (collapsible):",
                                cls="text-sm font-medium mb-2",
                            ),
                            Accordion(
                                AccordionItem(
                                    AccordionContent(
                                        "Yes. It adheres to the WAI-ARIA design pattern.",
                                        value="item-1",
                                    ),
                                    summary="Is it accessible?",
                                    value="item-1",
                                ),
                                AccordionItem(
                                    AccordionContent(
                                        "Yes. It comes with default styles that matches the other components' aesthetic.",
                                        value="item-2",
                                    ),
                                    summary="Is it styled?",
                                    value="item-2",
                                ),
                                AccordionItem(                              
                                    AccordionContent(
                                        "Yes. It's animated by default, but you can disable it if you prefer.",
                                        value="item-3",
                                    ),
                                    summary="Is it animated?",
                                    value="item-3",
                                ),
                                type="single",
                                collapsible=True,
                                default_value="item-1",
                                signal="accordion_single",
                                cls="w-full",
                            ),
                            cls="mb-6",
                        ),
                        # Multiple selection accordion
                        Div(
                            P("Multiple selection:", cls="text-sm font-medium mb-2"),
                            Accordion(
                                AccordionItem(
                                    
                                    AccordionContent(
                                        Div(
                                            P(
                                                "To get started with our product, follow these steps:",
                                                cls="mb-2",
                                            ),
                                            Ul(
                                                Li("1. Sign up for an account"),
                                                Li("2. Complete your profile"),
                                                Li("3. Explore the dashboard"),
                                                cls="list-disc pl-6",
                                            ),
                                        ),
                                        value="getting-started",
                                    ),
                                    summary="Getting Started",
                                    value="getting-started",
                                ),
                                AccordionItem(
                                    AccordionContent(
                                        Div(
                                            P(
                                                "Our platform offers these key features:",
                                                cls="mb-2",
                                            ),
                                            Ul(
                                                Li("Real-time collaboration"),
                                                Li("Advanced analytics"),
                                                Li("Custom integrations"),
                                                Li("24/7 support"),
                                                cls="list-disc pl-6",
                                            ),
                                        ),
                                        value="features",
                                    ),
                                    summary="Features",
                                    value="features",
                                ),
                                AccordionItem(
                                    AccordionContent(
                                        Div(
                                            P(
                                                "We offer flexible pricing plans:",
                                                cls="mb-2",
                                            ),
                                            Div(
                                                Div(
                                                    "Free: $0/month - Basic features",
                                                    cls="py-1",
                                                ),
                                                Div(
                                                    "Pro: $29/month - Advanced features",
                                                    cls="py-1",
                                                ),
                                                Div(
                                                    "Enterprise: Custom - Full access",
                                                    cls="py-1",
                                                ),
                                            ),
                                        ),
                                        value="pricing",
                                    ),
                                    summary="Pricing",
                                    value="pricing",
                                ),
                                type="multiple",
                                default_value=["getting-started"],
                                signal="accordion_multiple",
                                cls="w-full",
                            ),
                            cls="mb-6",
                        ),
                        cls="space-y-4 mb-8",
                    ),
                ),

                Separator(cls="my-4"),

                # Progress examples
                Div(
                    H2("Progress", cls="text-2xl font-semibold mb-4"),
                    Div(
                        # Basic examples
                        Div(
                            H3("Basic Examples", cls="text-lg font-medium mb-2"),
                            Div(
                                P("Default (25%):", cls="mb-2"),
                                Progress(progress_value=25),
                                P("Half-way (50%):", cls="mt-4 mb-2"),
                                Progress(progress_value=50),
                                P("Complete (100%):", cls="mt-4 mb-2"),
                                Progress(progress_value=100),
                            ),
                            cls="mb-6",
                        ),
                        # Reactive progress with signals
                        Div(
                            H3("Interactive Progress", cls="text-lg font-medium mb-2"),
                            Div(
                                Progress(progress_value=35, signal="demo_progress"),
                                Div(
                                    Button("Increase", on_click="$demo_progress = Math.min(100, $demo_progress + 10)"),
                                    Button("Decrease", on_click="$demo_progress = Math.max(0, $demo_progress - 10)"),
                                    Button("Reset", on_click="$demo_progress = 0"),
                                    cls="flex gap-2 mt-4",
                                ),
                                P(
                                    Span("Current: "),
                                    Span(text="$demo_progress", cls="font-bold"),
                                    Span("%"),
                                    cls="mt-2 text-sm text-muted-foreground",
                                ),
                            ),
                            cls="mb-6",
                        ),
                        # Auto-incrementing progress
                        Div(
                            H3("Auto-incrementing Progress", cls="text-lg font-medium mb-2"),
                            Div(
                                Progress(progress_value=0, signal="auto_progress"),
                                Div(
                                    Button(
                                        "Start", 
                                        on_click="""
                                            if (!window.autoProgressInterval) {
                                                $auto_progress = 0;
                                                window.autoProgressInterval = setInterval(() => {
                                                    if ($auto_progress < 100) {
                                                        $auto_progress += 2;
                                                    } else {
                                                        clearInterval(window.autoProgressInterval);
                                                        window.autoProgressInterval = null;
                                                    }
                                                }, 100);
                                            }
                                        """ ,
                                        variant="default"
                                    ),
                                    Button(
                                        "Stop", 
                                        on_click="""
                                            if (window.autoProgressInterval) {
                                                clearInterval(window.autoProgressInterval);
                                                window.autoProgressInterval = null;
                                            }
                                        """,
                                        variant="destructive"
                                    ),
                                    Button(
                                        "Reset", 
                                        on_click="""
                                            if (window.autoProgressInterval) {
                                                clearInterval(window.autoProgressInterval);
                                                window.autoProgressInterval = null;
                                            }
                                            $auto_progress = 0;
                                        """,
                                        variant="secondary"
                                    ),
                                    cls="flex gap-2 mt-4",
                                ),
                                P(
                                    Span("Progress: "),
                                    Span(text="$auto_progress", cls="font-bold"),
                                    Span("%"),
                                    cls="mt-2 text-sm text-muted-foreground",
                                ),
                            ),
                            cls="mb-6",
                        ),
                        # Custom styling
                        Div(
                            H3("Custom Styling", cls="text-lg font-medium mb-2"),
                            Div(
                                P("Large progress bar:", cls="mb-2"),
                                Progress(progress_value=60, cls="h-4"),
                                P("Custom color:", cls="mt-4 mb-2"),
                                Progress(progress_value=80, class_name="bg-green-200", cls="[&>div]:bg-green-500"),
                            ),
                        ),
                        cls="space-y-4 mb-8",
                    ),
                ),
                Separator(cls="my-4"),
                # Interactive counter with Datastar
                Div(
                    H2("Interactive Counter (Datastar)", cls="text-2xl font-semibold mb-4"),
                    Div(
                        Div(
                            Span("Count: ", cls="font-semibold"),
                            Span(text="$count"),
                            cls="text-xl mb-4",
                        ),
                        Div(
                            Button("-", on_click="$count--", variant="outline"),
                            Button("Reset", on_click="$count = 0", variant="secondary"),
                            Button("+", on_click="$count++", variant="outline"),
                            cls="flex gap-2",
                        ),
                        signals= Signals(count=0),
                        cls="p-4 border rounded-lg mb-8",
                    ),
                ),



                Separator(cls="my-4"),
                # Form with validation example
                Div(
                    H2(
                        "Form with Validation (Datastar)", cls="text-2xl font-semibold mb-4"
                    ),
                    Form(
                        Div(
                            Label("Name", for_="name"),
                            Input(
                                bind="name", id="name", placeholder="Enter your name"
                            ),
                            Span(
                                "Name is required",
                                show="$submitted && !$name",
                                cls="text-sm text-destructive",
                            ),
                            cls="space-y-2",
                        ),
                        Div(
                            Label("Email", for_="email"),
                            Input(
                                bind="email",
                                id="email",
                                type="email",
                                placeholder="email@example.com",
                            ),
                            Span(
                                "Invalid email",
                                show="$email && !$email.includes('@')",
                                cls="text-sm text-destructive",
                            ),
                            cls="space-y-2",
                        ),
                        Button(
                            "Submit",
                            on_click="$submitted = true",
                            # data_class="{'opacity-50': '!$name || !$email || !$email.includes('@')'}",
                            type="submit",
                        ),
                        signals= Signals(name="", email="", submitted=False),
                        on_submit="event.preventDefault(); if($name && $email.includes('@')) alert('Form submitted!')",
                        cls="space-y-4 max-w-md",
                    ),
                ),
                
                cls="container mx-auto p-8",
                id="content",
            ),                    
        ),
        cls="min-h-screen relative",
    )

