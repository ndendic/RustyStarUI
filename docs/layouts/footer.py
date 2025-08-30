from typing import Any
from starhtml import *


def _attribution_section(attribution: str, hosting_info: str) -> FT:
    """Create the attribution text section."""
    return P(
        attribution, ". ", hosting_info, ".", 
        cls="text-sm text-muted-foreground"
    )


def _github_repositories_section() -> FT:
    """Create the GitHub repositories section with both repos elegantly displayed."""
    return Div(
        P(
            "Find us on GitHub:",
            cls="text-sm font-medium text-foreground mb-3"
        ),
        Div(
            # StarHTML Framework Repository
            A(
                Div(
                    Icon("lucide:code", cls="h-4 w-4 flex-shrink-0"),
                    Div(
                        Span("starHTML", cls="font-medium text-foreground"),
                        Span("Web framework", cls="text-xs text-muted-foreground"),
                        cls="flex flex-col leading-tight"
                    ),
                    cls="flex items-center gap-2"
                ),
                href="https://github.com/banditburai/starhtml",
                target="_blank",
                rel="noopener noreferrer",
                cls="flex items-center p-2 rounded-md border border-border/50 hover:border-border hover:bg-accent/50 transition-colors group"
            ),
            # StarUI Component Library Repository  
            A(
                Div(
                    Icon("lucide:palette", cls="h-4 w-4 flex-shrink-0"),
                    Div(
                        Span("starUI", cls="font-medium text-foreground"),
                        Span("Component library", cls="text-xs text-muted-foreground"),
                        cls="flex flex-col leading-tight"
                    ),
                    cls="flex items-center gap-2"
                ),
                href="https://github.com/banditburai/starui",
                target="_blank", 
                rel="noopener noreferrer",
                cls="flex items-center p-2 rounded-md border border-border/50 hover:border-border hover:bg-accent/50 transition-colors group"
            ),
            cls="grid grid-cols-1 sm:grid-cols-2 gap-2"
        ),
        cls="space-y-2"
    )


def _additional_links_section(links: list[dict[str, Any]]) -> FT:
    """Create the additional links section."""
    return Div(
        *[
            A(
                link["label"],
                href=link["href"],
                cls="text-sm text-muted-foreground hover:text-foreground transition-colors underline-offset-4 hover:underline",
            )
            for link in links
        ],
        cls="flex flex-wrap gap-4 mt-2",
    )


def _footer_content(
    attribution: str,
    hosting_info: str, 
    source_text: str,
    source_href: str,
    links: list[dict[str, Any]] | None = None,
    show_github_repos: bool = True,
) -> FT:
    """Create the main footer content area."""
    sections = [
        _attribution_section(attribution, hosting_info),
    ]
    
    if show_github_repos:
        sections.append(_github_repositories_section())
    
    if links:
        sections.append(_additional_links_section(links))
    
    return Div(
        *sections,
        cls="space-y-4",
    )


def DocsFooter(
    attribution: str = "Built with StarHTML",
    hosting_info: str = "Component library for Python web apps",
    source_text: str = "The source code is available on GitHub",
    source_href: str = "https://github.com/banditburai/starui",
    links: list[dict[str, Any]] | None = None,
    show_github_repos: bool = True,
    class_name: str = "",
    **attrs,
) -> FT:
    """Create a documentation footer with attribution, GitHub repositories, and optional additional links."""
    return Footer(
        Div(
            _footer_content(
                attribution=attribution,
                hosting_info=hosting_info,
                source_text=source_text,
                source_href=source_href,
                links=links,
                show_github_repos=show_github_repos,
            ),
            cls="container mx-auto max-w-full px-4 py-6 md:py-8",
        ),
        cls=f"border-t border-border/40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 {class_name}",
        **attrs,
    )