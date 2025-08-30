from typing import Any
from starhtml import *
from widgets.installation_section import InstallationSection
from widgets.code_block import CodeBlock


def auto_generate_page(
    component_name: str,
    description: str,
    examples: list[Any],
    cli_command: str | None = None,
    manual_files: list[dict[str, str]] | None = None,
    dependencies: list[str] | None = None,
    usage_code: str | None = None,
    usage_description: str | None = None,
    api_reference: dict[str, Any] | None = None,
    hero_example: Any | None = None,
    hero_example_code: str | None = None,
    examples_data: list[dict[str, str]] | None = None,
    component_slug: str | None = None,
    **layout_attrs
) -> FT:
    """Auto-generate a component documentation page."""
    
    from layouts.base import DocsLayout, LayoutConfig, SidebarConfig
    from app import DOCS_SIDEBAR_SECTIONS
    
    return DocsLayout(
        Div(
            hero_example if hero_example else "",
            InstallationSection(
                cli_command=cli_command,
                manual_files=manual_files,
                dependencies=dependencies,
                cls="my-8"
            ) if (cli_command or manual_files or dependencies) else "",
            _examples_section(examples) if examples else "",
            _usage_section(usage_code, usage_description) if usage_code else "",
            _api_section(api_reference) if api_reference else "",
            # Removed space-y-12 to allow custom spacing
        ),
        layout=LayoutConfig(
            title=component_name,
            description=description,
            component_name=component_slug,
        ),
        sidebar=SidebarConfig(sections=DOCS_SIDEBAR_SECTIONS),
        **layout_attrs
    )


def _usage_section(code: str, description: str | None = None) -> FT:
    """Create usage section."""
    return Div(
        H2("Usage", cls="text-2xl font-bold tracking-tight mb-4 mt-12"),
        P(description, cls="text-muted-foreground mb-4") if description else "",
        CodeBlock(code, language="python"),
        cls="space-y-4"
    )


def _examples_section(examples: list[Any]) -> FT:
    """Create examples section."""
    return Div(
        H2("Examples", cls="text-2xl font-bold tracking-tight mb-6 mt-12"),
        Div(
            *examples,
            # Removed space-y-2 to allow custom spacing on examples
        )
    )


def _api_section(api_reference: dict[str, Any]) -> FT:
    """Create API reference section."""
    props = api_reference.get("props", [])
    # Support both "api" and "components" for backwards compatibility
    api_items = api_reference.get("api", api_reference.get("components", []))
    
    # Only show API Reference section if there's actual content
    if not props and not api_items:
        return ""
    
    content_sections = []
    
    # Props table if props exist
    if props:
        content_sections.append(
            Div(
                H3("Props", cls="text-lg font-semibold mb-4"),
                Div(
                    Table(
                        Thead(
                            Tr(
                                Th("Prop", cls="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider"),
                                Th("Type", cls="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider"),
                                Th("Default", cls="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider"),
                                Th("Description", cls="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider"),
                                cls="bg-muted/50"
                            )
                        ),
                        Tbody(
                            *[
                                Tr(
                                    Td(Code(prop["name"], cls="text-sm font-mono font-medium"), cls="px-6 py-4 whitespace-nowrap"),
                                    Td(Code(prop["type"], cls="text-xs font-mono text-muted-foreground"), cls="px-6 py-4 text-sm"),
                                    Td(Code(prop.get("default", "-"), cls="text-xs font-mono text-muted-foreground"), cls="px-6 py-4 whitespace-nowrap"),
                                    Td(prop.get("description", ""), cls="px-6 py-4 text-sm text-muted-foreground"),
                                    cls="border-t border-border"
                                )
                                for prop in props
                            ],
                            cls="divide-y divide-border"
                        ),
                        cls="w-full"
                    ),
                    cls="overflow-hidden rounded-lg border border-border"
                ),
                cls="overflow-x-auto"
            )
        )
    
    # API items table if they exist (for composite components)
    if api_items:
        # Determine if these items have a "type" field (like props) or just name/description
        has_type = any("type" in item for item in api_items)
        
        if has_type:
            # Display like props table but without "Default" column
            content_sections.append(
                Div(
                    Div(
                        Table(
                            Thead(
                                Tr(
                                    Th("Name", cls="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider"),
                                    Th("Type", cls="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider"),
                                    Th("Description", cls="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider"),
                                    cls="bg-muted/50"
                                )
                            ),
                            Tbody(
                                *[
                                    Tr(
                                        Td(Code(item["name"], cls="text-sm font-mono font-medium"), cls="px-6 py-4 whitespace-nowrap"),
                                        Td(Code(item.get("type", ""), cls="text-xs font-mono text-muted-foreground"), cls="px-6 py-4 text-sm"),
                                        Td(item.get("description", ""), cls="px-6 py-4 text-sm text-muted-foreground"),
                                        cls="border-t border-border"
                                    )
                                    for item in api_items
                                ],
                                cls="divide-y divide-border"
                            ),
                            cls="w-full"
                        ),
                        cls="overflow-hidden rounded-lg border border-border"
                    ),
                    cls="overflow-x-auto"
                )
            )
        else:
            # Simple name/description table for sub-components
            content_sections.append(
                Div(
                    Div(
                        Table(
                            Thead(
                                Tr(
                                    Th("Component", cls="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider"),
                                    Th("Description", cls="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider"),
                                    cls="bg-muted/50"
                                )
                            ),
                            Tbody(
                                *[
                                    Tr(
                                        Td(Code(item["name"], cls="text-sm font-mono font-medium"), cls="px-6 py-4 whitespace-nowrap"),
                                        Td(item.get("description", ""), cls="px-6 py-4 text-sm text-muted-foreground"),
                                        cls="border-t border-border"
                                    )
                                    for item in api_items
                                ],
                                cls="divide-y divide-border"
                            ),
                            cls="w-full"
                        ),
                        cls="overflow-hidden rounded-lg border border-border"
                    ),
                    cls="overflow-x-auto"
                )
            )
    
    return Div(
        H2("API Reference", cls="text-2xl font-bold tracking-tight mb-6 mt-12"),
        *content_sections,
        cls="space-y-6"
    )


def generate_component_markdown(
    component_name: str,
    description: str,
    examples_data: list[dict[str, str]],
    cli_command: str | None = None,
    usage_code: str | None = None,
    api_reference: dict[str, Any] | None = None,
    hero_example_code: str | None = None,
) -> str:
    """Generate markdown content for a component documentation page."""
    
    lines = []
    
    # Header
    lines.append(f"# {component_name}")
    lines.append("")
    lines.append(description)
    lines.append("")
    
    # Hero Example
    if hero_example_code:
        lines.append("## Preview")
        lines.append("")
        lines.append("```python")
        lines.append(hero_example_code)
        lines.append("```")
        lines.append("")
    
    # Installation
    if cli_command:
        lines.append("## Installation")
        lines.append("")
        lines.append("### CLI")
        lines.append("")
        lines.append("Install the component using the StarUI CLI:")
        lines.append("")
        lines.append(f"```bash")
        lines.append(cli_command)
        lines.append("```")
        lines.append("")
    
    # Examples
    if examples_data:
        lines.append("## Examples")
        lines.append("")
        
        for example in examples_data:
            title = example.get("title")
            description = example.get("description")
            code = example.get("code", "")
            
            if title:
                lines.append(f"### {title}")
                lines.append("")
            
            if description:
                lines.append(description)
                lines.append("")
            
            lines.append("```python")
            lines.append(code)
            lines.append("```")
            lines.append("")
    
    # Usage
    if usage_code:
        lines.append("## Usage")
        lines.append("")
        lines.append("```python")
        lines.append(usage_code)
        lines.append("```")
        lines.append("")
    
    # API Reference
    if api_reference and "props" in api_reference:
        lines.append("## API Reference")
        lines.append("")
        lines.append("### Props")
        lines.append("")
        
        # Create markdown table
        lines.append("| Prop | Type | Default | Description |")
        lines.append("|------|------|---------|-------------|")
        
        for prop in api_reference["props"]:
            name = prop.get("name", "")
            type_str = prop.get("type", "")
            default = prop.get("default", "")
            desc = prop.get("description", "")
            lines.append(f"| `{name}` | `{type_str}` | `{default}` | {desc} |")
        
        lines.append("")
    
    return "\n".join(lines)