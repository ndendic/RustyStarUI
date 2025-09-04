from starhtml import Div, P, A, Icon, Span, FT, H3
from starui.registry.components.card import Card, CardHeader, CardTitle, CardDescription, CardContent
from starui.registry.components.badge import Badge
from component_registry import ComponentRegistry
from layouts.base import DocsLayout, LayoutConfig, SidebarConfig


def create_components_index(registry: ComponentRegistry, sidebar_sections: list = None) -> FT:
    components = sorted(
        registry.components.items(),
        key=lambda x: (x[1].get("order", 100), x[1].get("title", x[0]))
    )
    
    categories = {}
    for name, comp in components:
        cat = comp.get("category", "ui")
        if cat not in categories:
            categories[cat] = []
        categories[cat].append((name, comp))
    
    def component_icon(name: str) -> str:
        icons = {
            "button": "mouse-pointer-click",
            "input": "type", 
            "tabs": "folder",
            "card": "credit-card",
            "badge": "tag",
            "alert": "alert-circle",
            "label": "tag",
            "theme_toggle": "sun-moon",
            "breadcrumb": "navigation"
        }
        return icons.get(name, "component")
    
    def status_badge(status: str) -> FT:
        if status == "beta":
            return Badge("Beta", variant="secondary", cls="ml-auto text-xs")
        elif status == "experimental": 
            return Badge("Experimental", variant="outline", cls="ml-auto text-xs")
        return None
    
    def component_card(name: str, comp: dict) -> FT:
        return A(
            Card(
                CardHeader(
                    Div(
                        Div(
                            Icon(component_icon(name), width="32", height="32", cls="text-primary/60 dark:text-primary/70 relative z-10"),
                            cls="relative mb-4 w-12 h-12 rounded-xl bg-gradient-to-br from-primary/8 via-primary/4 to-primary/12 dark:from-primary/15 dark:via-primary/8 dark:to-primary/25 shadow-inner dark:shadow-[inset_2px_2px_4px_rgba(0,0,0,0.3),inset_-1px_-1px_2px_rgba(255,255,255,0.1)] flex items-center justify-center backdrop-blur-sm border border-primary/10 dark:border-primary/20"
                        ),
                        Div(
                            CardTitle(comp["title"], cls="text-lg font-semibold"),
                            status_badge(comp.get("status", "stable")),
                            cls="flex items-center justify-between"
                        ),
                        CardDescription(comp.get("description", ""), cls="text-sm text-muted-foreground mt-2"),
                        cls="p-6"
                    )
                ),
                cls="group hover:shadow-lg hover:border-primary/30 transition-all duration-300 cursor-pointer h-full bg-gradient-to-br from-background via-background/80 to-muted/50 backdrop-blur-sm relative overflow-hidden"
            ),
            href=f"/components/{name}",
            cls="block"
        )
    
    def category_section(category: str, items: list) -> FT:
        return Div(
            H3(
                category.title().replace("_", " "), 
                cls="text-xl font-semibold mb-4 text-foreground"
            ),
            Div(
                *[component_card(name, comp) for name, comp in items],
                cls="grid gap-6 sm:grid-cols-2 lg:grid-cols-3"
            ),
            cls="mb-12"
        )
    
    return DocsLayout(
        Div(
            Div(
                P(
                    "Beautifully designed components built with Python and Tailwind CSS.",
                    cls="text-xl text-muted-foreground mb-2"
                ),
                P(
                    "Accessible. Customizable. Open Source.",
                    cls="text-muted-foreground mb-8"
                ),
                cls="text-center mb-12"
            ),
            
            
            *[category_section(cat, items) for cat, items in categories.items()],
            
            cls="max-w-6xl mx-auto"
        ),
        layout=LayoutConfig(
            title="Components",
            description="Explore all available starUI components"
        ),
        sidebar=SidebarConfig(sections=sidebar_sections or [])
    )