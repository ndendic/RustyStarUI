"""StarUI component registry system."""

from .client import RegistryClient
from .local import discover_components

# Import dependencies with graceful fallback
try:
    from .dependencies import ensure_component_dependencies, require_scroll_handler
    dependencies_available = True
except ImportError:
    dependencies_available = False
    ensure_component_dependencies = None
    require_scroll_handler = None

# Import loader components with fallback
try:
    from .loader import ComponentLoader, DependencyResolver
    loader_available = True
except ImportError:
    loader_available = False
    ComponentLoader = None
    DependencyResolver = None

__all__ = [
    "RegistryClient",
    "discover_components",
]

if dependencies_available:
    __all__.extend([
        "require_scroll_handler",
        "ensure_component_dependencies",
    ])

if loader_available:
    __all__.extend([
        "ComponentLoader",
        "DependencyResolver",
    ])
