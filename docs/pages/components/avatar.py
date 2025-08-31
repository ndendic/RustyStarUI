"""
Avatar component documentation - User profile images with fallback.
Clean, minimal, and reactive.
"""

# Component metadata for auto-discovery
TITLE = "Avatar"
DESCRIPTION = "An image element with a fallback for representing the user."
CATEGORY = "ui"
ORDER = 15
STATUS = "stable"

from starhtml import Div, P, Span
from starui.registry.components.avatar import (
    Avatar,
    AvatarFallback,
    AvatarImage,
    AvatarWithFallback,
)
from widgets.component_preview import ComponentPreview


def examples():
    """Generate avatar examples using ComponentPreview with tabs."""
    
    # Basic composition
    yield ComponentPreview(
        Div(
            Avatar(
                AvatarImage(
                    src="https://github.com/shadcn.png",
                    alt="@shadcn",
                )
            ),
            Avatar(
                AvatarFallback("CN")
            ),
            Avatar(
                AvatarImage(
                    src="https://avatars.githubusercontent.com/u/1?v=4",
                    alt="User",
                )
            ),
            cls="flex items-center gap-4"
        ),
        '''Avatar(
    AvatarImage(
        src="https://github.com/shadcn.png",
        alt="@shadcn"
    )
)

Avatar(
    AvatarFallback("CN")
)''',
        title="Basic Avatar",
        description="Compose avatars with image and fallback components"
    )
    
    # Sizes using custom classes
    yield ComponentPreview(
        Div(
            Avatar(AvatarFallback("XS"), cls="size-6"),
            Avatar(AvatarFallback("SM"), cls="size-8"),
            Avatar(AvatarFallback("MD")),  # default size-10
            Avatar(AvatarFallback("LG"), cls="size-12"),
            Avatar(AvatarFallback("XL"), cls="size-16"),
            Avatar(AvatarFallback("2X"), cls="size-20"),
            cls="flex items-center gap-4"
        ),
        '''# Extra small
Avatar(AvatarFallback("XS"), cls="size-6")

# Small
Avatar(AvatarFallback("SM"), cls="size-8")

# Default
Avatar(AvatarFallback("MD"))

# Large
Avatar(AvatarFallback("LG"), cls="size-12")

# Extra large
Avatar(AvatarFallback("XL"), cls="size-16")

# 2X large
Avatar(AvatarFallback("2X"), cls="size-20")''',
        title="Avatar Sizes",
        description="Use size classes to create different avatar sizes"
    )
    
    # With Fallback
    yield ComponentPreview(
        Div(
            Avatar(AvatarFallback("CN")),
            Avatar(AvatarFallback("JD")),
            Avatar(AvatarFallback("AB")),
            cls="flex items-center gap-4"
        ),
        '''Avatar(AvatarFallback("CN"))
Avatar(AvatarFallback("JD"))
Avatar(AvatarFallback("AB"))''',
        title="Avatar Fallback",
        description="Display initials when no image is available"
    )
    
    # Automatic Fallback with Datastar
    yield ComponentPreview(
        Div(
            Div(
                AvatarWithFallback(
                    src="https://github.com/shadcn.png",
                    alt="@shadcn",
                    fallback="CN",
                ),
                P("Valid URL", cls="text-xs text-muted-foreground text-center mt-1"),
                cls="flex flex-col items-center"
            ),
            Div(
                AvatarWithFallback(
                    src="https://invalid-url.com/image.jpg",
                    alt="Invalid",
                    fallback="IN",
                ),
                P("Invalid URL", cls="text-xs text-muted-foreground text-center mt-1"),
                cls="flex flex-col items-center"
            ),
            Div(
                AvatarWithFallback(fallback="NI"),
                P("No URL", cls="text-xs text-muted-foreground text-center mt-1"),
                cls="flex flex-col items-center"
            ),
            cls="flex items-start gap-4"
        ),
        '''# Valid image with fallback ready
AvatarWithFallback(
    src="https://github.com/shadcn.png",
    alt="@shadcn",
    fallback="CN"
)

# Invalid URL - will show fallback
AvatarWithFallback(
    src="https://invalid-url.com/image.jpg",
    alt="Invalid", 
    fallback="IN"
)

# No image - shows fallback immediately
AvatarWithFallback(fallback="NI")''',
        title="Automatic Fallback",
        description="Uses Datastar signals to automatically show fallback when image fails"
    )
    
    # Avatar Group Pattern
    yield ComponentPreview(
        Div(
            # Basic group
            Div(
                Avatar(AvatarFallback("JD")),
                Avatar(AvatarFallback("AS")),
                Avatar(AvatarFallback("PQ")),
                Avatar(AvatarFallback("+2", cls="text-xs font-medium")),
                cls="flex -space-x-2 [&>*[data-slot=avatar]]:ring-2 [&>*[data-slot=avatar]]:ring-background"
            ),
            cls="mb-4"
        ),
        '''# Avatar group with overlap
Div(
    Avatar(AvatarFallback("JD")),
    Avatar(AvatarFallback("AS")),
    Avatar(AvatarFallback("PQ")),
    Avatar(AvatarFallback("+2", cls="text-xs font-medium")),
    cls="flex -space-x-2 [&>*[data-slot=avatar]]:ring-2 [&>*[data-slot=avatar]]:ring-background"
)''',
        title="Avatar Group",
        description="Create overlapping avatar groups with Tailwind utilities"
    )
    
    # With Badge Pattern
    yield ComponentPreview(
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
            # Yellow status badge
            Div(
                Avatar(AvatarFallback("PQ")),
                Span(cls="absolute bottom-0 right-0 size-3 bg-yellow-500 rounded-full ring-2 ring-background"),
                cls="relative inline-block"
            ),
            # Badge with count
            Div(
                Avatar(AvatarFallback("MN")),
                Span("5", cls="absolute bottom-0 right-0 size-4 bg-red-500 rounded-full ring-2 ring-background flex items-center justify-center text-[8px] font-bold text-white"),
                cls="relative inline-block"
            ),
            cls="flex items-center gap-4"
        ),
        '''# Status indicator
Div(
    Avatar(AvatarFallback("JD")),
    Span(cls="absolute bottom-0 right-0 size-3 bg-green-500 rounded-full ring-2 ring-background"),
    cls="relative inline-block"
)

# Notification badge with count
Div(
    Avatar(AvatarFallback("MN")),
    Span(
        "5",
        cls="absolute bottom-0 right-0 size-4 bg-red-500 rounded-full ring-2 ring-background flex items-center justify-center text-[8px] font-bold text-white"
    ),
    cls="relative inline-block"
)''',
        title="Avatar with Badge",
        description="Add status indicators or notification badges using absolute positioning"
    )
    
    # Colored Initials Pattern
    yield ComponentPreview(
        Div(
            Avatar(AvatarFallback("JD", cls="bg-red-600 dark:bg-red-500 text-white font-semibold")),
            Avatar(AvatarFallback("AS", cls="bg-blue-600 dark:bg-blue-500 text-white font-semibold")),
            Avatar(AvatarFallback("PQ", cls="bg-green-600 dark:bg-green-500 text-white font-semibold")),
            Avatar(AvatarFallback("MN", cls="bg-purple-600 dark:bg-purple-500 text-white font-semibold")),
            Avatar(AvatarFallback("XY", cls="bg-orange-600 dark:bg-orange-500 text-white font-semibold")),
            cls="flex items-center gap-4"
        ),
        '''# Colored initials with theme support
Avatar(
    AvatarFallback(
        "JD",
        cls="bg-red-600 dark:bg-red-500 text-white font-semibold"
    )
)

Avatar(
    AvatarFallback(
        "AS",
        cls="bg-blue-600 dark:bg-blue-500 text-white font-semibold"
    )
)''',
        title="Colored Initials",
        description="Create colorful initial avatars with theme-aware backgrounds"
    )


def create_avatar_docs():
    """Create the Avatar component documentation page."""
    from utils import auto_generate_page
    
    api_reference = {
        "components": [
            {
                "name": "Avatar",
                "description": "Container component for avatar content",
                "props": [
                    {
                        "name": "class_name / cls",
                        "type": "str",
                        "default": "''",
                        "description": "Additional CSS classes for customization"
                    },
                    {
                        "name": "*children",
                        "type": "Any",
                        "description": "Avatar content (usually AvatarImage or AvatarFallback)"
                    }
                ]
            },
            {
                "name": "AvatarImage",
                "description": "The image element for the avatar",
                "props": [
                    {
                        "name": "src",
                        "type": "str",
                        "required": True,
                        "description": "Image source URL"
                    },
                    {
                        "name": "alt",
                        "type": "str",
                        "default": "''",
                        "description": "Alt text for accessibility"
                    },
                    {
                        "name": "loading",
                        "type": "str",
                        "default": "'lazy'",
                        "description": "Loading strategy ('lazy' or 'eager')"
                    }
                ]
            },
            {
                "name": "AvatarFallback",
                "description": "Fallback content shown when image fails to load",
                "props": [
                    {
                        "name": "*children",
                        "type": "Any",
                        "description": "Content to display (usually initials)"
                    },
                    {
                        "name": "class_name / cls",
                        "type": "str",
                        "default": "''",
                        "description": "Additional CSS classes"
                    }
                ]
            },
            {
                "name": "AvatarWithFallback",
                "description": "Complete avatar with automatic error handling",
                "props": [
                    {
                        "name": "src",
                        "type": "Optional[str]",
                        "default": "None",
                        "description": "Optional image source URL"
                    },
                    {
                        "name": "alt",
                        "type": "str",
                        "default": "''",
                        "description": "Alt text"
                    },
                    {
                        "name": "fallback",
                        "type": "str",
                        "default": "'?'",
                        "description": "Fallback text/initials"
                    }
                ]
            }
        ]
    }
    
    # Hero example showing diverse avatar types
    hero_example = ComponentPreview(
        Div(
            # Regular avatars with images
            Avatar(
                AvatarImage(
                    src="https://github.com/shadcn.png",
                    alt="@shadcn"
                )
            ),
            Avatar(
                AvatarImage(
                    src="https://avatars.githubusercontent.com/u/2?v=4",
                    alt="User 2"
                )
            ),
            # Fallback avatars
            Avatar(AvatarFallback("CN")),
            # Colored initials
            Avatar(AvatarFallback("JD", cls="bg-red-600 dark:bg-red-500 text-white font-semibold")),
            Avatar(AvatarFallback("AS", cls="bg-blue-600 dark:bg-blue-500 text-white font-semibold")),
            # With badge
            Div(
                Avatar(
                    AvatarImage(
                        src="https://avatars.githubusercontent.com/u/3?v=4",
                        alt="User 3"
                    )
                ),
                Span(cls="absolute bottom-0 right-0 size-3 bg-green-500 rounded-full ring-2 ring-background"),
                cls="relative inline-block"
            ),
            Div(
                Avatar(AvatarFallback("MN")),
                Span("3", cls="absolute bottom-0 right-0 size-4 bg-red-500 rounded-full ring-2 ring-background flex items-center justify-center text-[8px] font-bold text-white"),
                cls="relative inline-block"
            ),
            # Group
            Div(
                Avatar(AvatarFallback("A", cls="text-xs")),
                Avatar(AvatarFallback("B", cls="text-xs")),
                Avatar(AvatarFallback("+2", cls="text-xs font-medium")),
                cls="flex -space-x-3 [&>*[data-slot=avatar]]:ring-2 [&>*[data-slot=avatar]]:ring-background [&>*[data-slot=avatar]]:size-8"
            ),
            cls="flex items-center gap-3 flex-wrap justify-center"
        ),
        '''# Basic avatars
Avatar(AvatarImage(src="...", alt="..."))
Avatar(AvatarFallback("CN"))

# Colored initials
Avatar(
    AvatarFallback(
        "JD",
        cls="bg-red-600 dark:bg-red-500 text-white font-semibold"
    )
)

# With status badge
Div(
    Avatar(AvatarImage(...)),
    Span(cls="absolute bottom-0 right-0 size-3 bg-green-500 rounded-full ring-2 ring-background"),
    cls="relative inline-block"
)

# Grouped avatars
Div(
    Avatar(AvatarFallback("A")),
    Avatar(AvatarFallback("B")),
    Avatar(AvatarFallback("+2")),
    cls="flex -space-x-3 [&>*[data-slot=avatar]]:ring-2 [&>*[data-slot=avatar]]:ring-background"
)''',
        copy_button=True
    )
    
    return auto_generate_page(
        TITLE,
        DESCRIPTION,
        list(examples()),
        cli_command="star add avatar",
        api_reference=api_reference,
        hero_example=hero_example,
        component_slug="avatar"
    )