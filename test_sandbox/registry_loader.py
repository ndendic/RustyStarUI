"""Registry component loader for testing with dependency injection."""

import importlib.util
import sys
from pathlib import Path
from typing import Any
from functools import wraps


def _wrap_component_with_dependencies(component_func, component_name: str, module_name: str):
    """Wrap a component function to auto-inject dependencies."""
    
    @wraps(component_func)
    def wrapped_component(*args, **kwargs):
        # Get the original component result
        result = component_func(*args, **kwargs)
        
        # Check if this component needs dependency injection
        try:
            from src.starui.registry.dependencies import ensure_component_dependencies
            
            # Map component function names to metadata names
            metadata_name = _get_metadata_name_from_function(component_name, module_name)
            dependency_scripts = ensure_component_dependencies(metadata_name)
            
            # If we have dependency scripts and the result is a div-like container,
            # inject them at the beginning
            if dependency_scripts and hasattr(result, '__class__'):
                # For components that return containers (like SelectContent, PopoverContent)
                if component_name.endswith('Content'):
                    from starhtml import Div
                    # Inject dependencies into the container
                    return _inject_scripts_into_container(result, dependency_scripts)
                    
        except ImportError:
            # Dependency system not available, return original
            pass
            
        return result
    
    return wrapped_component


def _get_metadata_name_from_function(function_name: str, module_name: str) -> str:
    """Map component function name to metadata registry name."""
    # Extract module name (e.g. select.py -> select)  
    base_name = module_name.split('.')[-1]
    
    # For content components, use the base component name
    if function_name.endswith('Content'):
        return base_name
        
    return base_name


def _inject_scripts_into_container(container, scripts):
    """Inject dependency scripts into a container component."""
    # This is a simplified approach - in a real implementation you'd want
    # more sophisticated container detection and script injection
    from starhtml import Div
    
    # If it's a Div, prepend the scripts
    if hasattr(container, 'children') and hasattr(container, 'attrs'):
        # Create new container with scripts prepended
        new_children = list(scripts) + list(getattr(container, 'children', []))
        return Div(*new_children, **getattr(container, 'attrs', {}))
    
    return container


def load_registry_components() -> dict[str, Any]:
    """Load all components from the registry with dependency injection."""
    # Add parent directory to path
    parent_dir = Path(__file__).parent.parent
    sys.path.insert(0, str(parent_dir))

    registry_path = parent_dir / "src" / "starui" / "registry" / "components"

    if not registry_path.exists():
        return {}

    components = {}

    for py_file in registry_path.glob("*.py"):
        if py_file.name.startswith("_") or py_file.name == "utils.py":
            continue

        module_name = f"src.starui.registry.components.{py_file.stem}"

        try:
            module = importlib.import_module(module_name)

            # Get all callable, uppercase attributes (components)
            for name in dir(module):
                attr = getattr(module, name)
                if name[0].isupper() and callable(attr):
                    # Wrap component with dependency injection
                    wrapped_component = _wrap_component_with_dependencies(attr, name, module_name)
                    components[name] = wrapped_component

        except Exception as e:
            print(f"Failed to load {module_name}: {e}")
            continue

    return components


# Load all components and make them available
_components = load_registry_components()
globals().update(_components)

# Export for * imports
__all__ = list(_components.keys())
