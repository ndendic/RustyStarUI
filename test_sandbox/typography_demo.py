#!/usr/bin/env python3
# Import only what we need from starhtml, with Html prefix for conflicting elements
from starhtml import (
    Div, Section, Li, Ul, Link,
    star_app, fouc_script, position_handler
)
from starhtml import H1 as HTMLH1, H2 as HTMLH2, H3 as HTMLH3, H4 as HTMLH4
from starhtml import P as HTMLP, Blockquote as HTMLBlockquote
from starhtml.datastar import value

# Import all registry components (includes our styled typography H1, H2, etc.)
from registry_loader import *

styles = Link(rel="stylesheet", href="/static/css/starui.css", type="text/css")

app, rt = star_app(
    hdrs=(
        fouc_script(use_data_theme=True),
        styles,
        position_handler(),
    ),
    htmlkw=dict(lang="en", dir="ltr"),
    bodykw=dict(cls="min-h-screen bg-background text-foreground"),
)


@rt("/")
def index():
    return Div(
        # Theme toggle in top-right corner
        Div(ThemeToggle(), cls="absolute top-4 right-4"),
        
        # Main content container
        Div(
            # Hero section
            Display("Typography System"),
            Subtitle("Beautiful, consistent text styling with pragmatic defaults for your Star UI applications."),
            Lead("Explore our comprehensive typography components designed for accessibility, readability, and visual hierarchy."),
            
            Div(cls="h-8"),  # Spacer
            
            # Typography scale showcase
            Section(
                H2("Typography Scale", section=True),
                Lead("A comprehensive hierarchy designed for optimal readability and visual balance."),
                
                # Display Example
                Div(
                    Caption("DISPLAY"),
                    Display("The quick brown fox jumps", cls="!mt-0 !mb-4"),
                    cls="py-6 border-b border-border last:border-0"
                ),
                
                # H1 Example
                Div(
                    Caption("H1 - PRIMARY HEADING"),
                    H1("The quick brown fox jumps over the lazy dog", cls="!mt-0 !mb-4"),
                    cls="py-6 border-b border-border last:border-0"
                ),
                
                # H2 Example
                Div(
                    Caption("H2 - SECONDARY HEADING"),
                    H2("The quick brown fox jumps over the lazy dog", cls="!mt-0 !mb-4"),
                    cls="py-6 border-b border-border last:border-0"
                ),
                
                # H3 Example
                Div(
                    Caption("H3 - TERTIARY HEADING"),
                    H3("The quick brown fox jumps over the lazy dog", cls="!mt-0 !mb-4"),
                    cls="py-6 border-b border-border last:border-0"
                ),
                
                # H4-H6 Examples in grid
                Div(
                    Div(
                        Caption("H4 - QUATERNARY"),
                        H4("The quick brown fox", cls="!mt-0 !mb-4"),
                    ),
                    Div(
                        Caption("H5 - FIFTH LEVEL"), 
                        H5("The quick brown fox", cls="!mt-0 !mb-4"),
                    ),
                    Div(
                        Caption("H6 - SIXTH LEVEL"),
                        H6("The quick brown fox", cls="!mt-0 !mb-4"),
                    ),
                    cls="grid grid-cols-1 md:grid-cols-3 gap-6 py-6"
                ),
            ),
            
            Div(cls="h-8"),  # Spacer
            
            # Text variants
            Section(
                H2("Text Variants", section=True),
                Lead("Semantic text components for different content types and emphasis levels."),
                
                # Lead
                Div(
                    Caption("LEAD - INTRODUCTORY TEXT"),
                    Lead("A modal dialog that interrupts the user with important content and expects a response.", cls="!mt-0 !mb-4"),
                    cls="py-6 border-b border-border last:border-0"
                ),
                
                # Subtitle
                Div(
                    Caption("SUBTITLE - SECONDARY DESCRIPTION"),
                    Subtitle("Perfect for supporting information that accompanies main headings.", cls="!mt-0 !mb-4"),
                    cls="py-6 border-b border-border last:border-0"
                ),
                
                # Paragraph
                Div(
                    Caption("PARAGRAPH - BODY TEXT"),
                    P("The king thought long and hard, and finally came up with a brilliant plan: he would tax the jokes in the kingdom. This is the standard body text with optimal line height for reading.", cls="!mt-0 !mb-4"),
                    cls="py-6 border-b border-border last:border-0"
                ),
                
                # Large
                Div(
                    Caption("LARGE - EMPHASIZED TEXT"),
                    Large("Are you absolutely sure you want to proceed with this action?", cls="!mt-0 !mb-4"),
                    cls="py-6 border-b border-border last:border-0"
                ),
                
                # Small, Muted, Caption grid
                Div(
                    Div(
                        Caption("SMALL - FINE PRINT"),
                        Small("Terms and conditions apply"),
                    ),
                    Div(
                        Caption("MUTED - DE-EMPHASIZED"),
                        Muted("Enter your email address to continue.", cls="!mt-0 !mb-4"),
                    ),
                    Div(
                        Caption("CAPTION - METADATA"),
                        Caption("Last updated: March 2024"),
                    ),
                    cls="grid grid-cols-1 md:grid-cols-3 gap-6 py-6 border-b border-border last:border-0"
                ),
                
                # Text component variants
                Div(
                    Caption("TEXT COMPONENT - FLEXIBLE VARIANTS"),
                    Div(
                        Text("Body variant with normal weight", variant="body"),
                        Text("Body variant with bold weight", variant="body", weight="bold"),
                        Text("Lead variant with center alignment", variant="lead", align="center"),
                        Text("Small variant with medium weight", variant="small", weight="medium"),
                        cls="space-y-4"
                    ),
                    cls="py-6 border-b border-border last:border-0"
                ),
                
                # Inline Code
                Div(
                    Caption("INLINE CODE - CODE SNIPPETS"),
                    P("Use the ", InlineCode("H1"), " component for main headings and ", InlineCode("<Text variant='body'>"), " for flexible body text with variants.", cls="!mt-0 !mb-4"),
                    cls="py-6"
                ),
            ),
            
            Div(cls="h-8"),  # Spacer
            
            # Special elements
            Section(
                H2("Special Elements", section=True),
                Lead("Specialized components for quotes, lists, and structured content."),
                
                # Blockquote
                Div(
                    Caption("BLOCKQUOTE - QUOTED CONTENT"),
                    Blockquote(
                        "Design is not just what it looks like and feels like. Design is how it works. Great typography is the foundation of all great design.",
                        cls="!mt-0 !mb-4"
                    ),
                    cls="py-6 border-b border-border last:border-0"
                ),
                
                # Lists
                Div(
                    Div(
                        Caption("UNORDERED LIST"),
                        List(
                            Li("Consistent vertical rhythm throughout all components"),
                            Li("Semantic HTML elements for accessibility"),
                            Li("Responsive typography that scales beautifully"),
                            Li("Dark mode support with proper contrast ratios"),
                            cls="!mt-0 !mb-4"
                        ),
                    ),
                    Div(
                        Caption("ORDERED LIST"),
                        List(
                            Li("Analyze your content hierarchy needs"),
                            Li("Choose appropriate heading levels (H1-H6)"),
                            Li("Select text variants based on semantic meaning"),
                            Li("Apply consistent spacing using our scale"),
                            ordered=True,
                            cls="!mt-0 !mb-4"
                        ),
                    ),
                    cls="grid grid-cols-1 lg:grid-cols-2 gap-8 py-6 border-b border-border last:border-0"
                ),
                
                # Figure and Figcaption
                Div(
                    Caption("FIGURE - IMAGE WITH CAPTION"),
                    Figure(
                        Div(
                            "📊", 
                            cls="w-full h-48 bg-muted rounded-lg flex items-center justify-center text-6xl"
                        ),
                        Figcaption("Fig 1. Typography usage statistics across modern web applications showing consistent hierarchy patterns."),
                        cls="!mt-0 !mb-4"
                    ),
                    cls="py-6"
                ),
                
            ),
            
            Div(cls="h-12"),  # Large spacer before prose
            
            # Prose component demo
            Section(
                H2("Prose Component", section=True),
                Lead("The Prose component uses the Tailwind Typography plugin for beautiful, consistent styling of content-rich areas like articles, blog posts, and documentation."),
                Subtitle("Powered by @tailwindcss/typography with design system integration. Compare different sizes and see how the typography scales consistently."),
                
                # Size comparison
                Div(
                    # Small prose example
                    Div(
                        Caption("SIZE: SMALL - COMPACT CONTENT"),
                        Div(
                            Prose(
                                HTMLH2("Typography Principles"),
                                HTMLP("Good typography creates hierarchy, guides the eye, and enhances readability. It should be invisible to the reader while making content easy to consume."),
                                Ul(
                                    Li("Consistent spacing and rhythm"),
                                    Li("Clear visual hierarchy"),
                                    Li("Optimal line lengths and heights")
                                ),
                                size="sm"
                            ),
                            cls="bg-card rounded-lg border p-6"
                        ),
                        cls="mb-8"
                    ),
                    
                    # Base prose example  
                    Div(
                        Caption("SIZE: BASE - STANDARD CONTENT"),
                        Div(
                            Prose(
                                HTMLH1("The Power of Typography"),
                                HTMLP("Typography is the art and technique of arranging type to make written language legible, readable, and appealing when displayed. It's one of the most important aspects of design."),
                                
                                HTMLH2("Why Typography Matters"),
                                HTMLP("Good typography can make the difference between content that engages and content that frustrates. It guides the reader's eye and creates a hierarchy that makes information easy to process."),
                                
                                HTMLBlockquote(
                                    "Typography is the craft of endowing human language with a durable visual form."
                                ),
                                
                                HTMLH3("Key Principles"),
                                HTMLP("When working with typography, consider these essential elements:"),
                                
                                Ul(
                                    Li("**Hierarchy** - Use size, weight, and spacing to create clear information levels"),
                                    Li("**Contrast** - Ensure sufficient contrast for accessibility and readability"),
                                    Li("**Consistency** - Maintain uniform spacing and styling throughout"),
                                    Li("**Readability** - Choose appropriate line heights and lengths")
                                ),
                                
                                HTMLP("Modern web typography also needs to be ", HTMLCode("responsive"), " and work across all devices and screen sizes."),
                                
                                size="base"
                            ),
                            cls="bg-card rounded-lg border p-8"
                        ),
                        cls="mb-8"
                    ),
                    
                    # Large prose example
                    Div(
                        Caption("SIZE: LARGE - FEATURE CONTENT"),
                        Div(
                            Prose(
                                HTMLH1("Design at Scale"),
                                HTMLP("Creating typography systems that work at scale requires careful consideration of every detail, from the smallest caption to the largest display text."),
                                
                                HTMLH2("Implementation"),
                                HTMLP("Our typography system uses semantic tokens and consistent spacing to ensure harmony across all components."),
                                
                                size="lg"
                            ),
                            cls="bg-card rounded-lg border p-8"
                        ),
                    ),
                    
                    cls="space-y-8 mt-8"
                ),
            ),
            
            # Usage examples
            Section(
                H2("Usage Examples", section=True),
                Lead("See how typography components work together in real-world scenarios."),
                
                Div(
                    # Card example
                    Div(
                        Caption("CARD LAYOUT WITH TYPOGRAPHY"),
                        Div(
                            H3("Welcome to StarUI"),
                            Subtitle("Build beautiful interfaces with our component library"),
                            P("StarUI provides a comprehensive set of components designed for modern web applications. Each component follows accessibility best practices and supports dark mode out of the box."),
                            Large("Key Features:"),
                            List(
                                Li("Accessible by default"),
                                Li("Dark mode support"),
                                Li("Responsive design"),
                                Li("TypeScript ready")
                            ),
                            Muted("Get started today with our comprehensive documentation."),
                            cls="bg-card rounded-lg border p-6"
                        ),
                    ),
                    
                    # Documentation example
                    Div(
                        Caption("DOCUMENTATION LAYOUT"),
                        Div(
                            H2("API Reference"),
                            Lead("Complete guide to the Typography component API"),
                            
                            H3("Props"),
                            P("The following props are available for the ", InlineCode("Text"), " component:"),
                            
                            # Simple table using divs
                            Div(
                                Div(
                                    Small("variant"),
                                    Muted("TextVariant"),
                                    Small("'body'"),
                                    cls="grid grid-cols-3 gap-4 py-2 border-b font-medium"
                                ),
                                Div(
                                    Small("weight"),
                                    Muted("FontWeight"),
                                    Small("undefined"),
                                    cls="grid grid-cols-3 gap-4 py-2 border-b"
                                ),
                                Div(
                                    Small("align"),
                                    Muted("TextAlign"),
                                    Small("undefined"),
                                    cls="grid grid-cols-3 gap-4 py-2"
                                ),
                                cls="border border-border rounded-lg p-4"
                            ),
                            
                            cls="bg-card rounded-lg border p-6"
                        ),
                    ),
                    
                    cls="grid grid-cols-1 lg:grid-cols-2 gap-8 mt-8"
                ),
            ),
            
            
            cls="max-w-6xl mx-auto px-6 py-12"
        ),
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)