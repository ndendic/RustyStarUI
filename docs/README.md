# StarUI Documentation

Interactive documentation for StarUI components built with StarHTML and Tailwind CSS.

## Overview

This documentation system provides:
- Live component previews with Datastar reactivity
- Automatic code generation and syntax highlighting
- Responsive layout with sidebar navigation
- Dark mode support
- Component API reference
- Installation instructions for each component

## Requirements

- Python 3.12+
- uv (for package management)

## Installation

### Development (uses local StarUI code)

```bash
# From the docs directory
cd docs

# Install with editable StarUI (for developing components)
uv sync
```

This setup uses the local StarUI code from the parent directory, allowing you to see changes immediately as you develop components.

### Production (uses PyPI StarUI)

For production deployment, comment out the `[tool.uv.sources]` section in `pyproject.toml`:

```toml
# [tool.uv.sources]
# starui = { path = "../", editable = true }
```

Then install:

```bash
uv sync
```

This will use the published StarUI package from PyPI.

## Running the Documentation

```bash
# Using uv (recommended)
uv run python app.py

# Or if you've activated the virtual environment
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate  # On Windows
python app.py
```

The documentation will be available at http://localhost:8000

## Development Workflow

When developing StarUI components:

1. **Edit components** in `../src/starui/registry/components/`
2. **Update docs** in `docs/pages/components/`
3. **View changes** immediately (using editable install)
4. **Test thoroughly** before committing

The editable install means changes to StarUI code are reflected immediately without reinstalling.

```bash
# Run development server with auto-reload
uv run python app.py

# Format code
uv run ruff format starui_docs

# Lint code
uv run ruff check starui_docs
```

## Deployment

The documentation can be deployed to any platform that supports Python web applications:

```bash
# Build the package
uv build

# The built package will be in dist/
# Deploy using your preferred method (e.g., Docker, Vercel, Railway, etc.)
```

For production, you can run with:

```bash
uvicorn run:app --host 0.0.0.0 --port 8000 --workers 4
```

## Project Structure

```
docs/
├── pyproject.toml         # Package configuration
├── uv.lock               # Lock file for dependencies
├── .python-version       # Python version (3.12)
├── run.py                # Main application runner
├── starui_docs/          # Main package
│   ├── __init__.py
│   ├── component_registry.py
│   ├── utils.py
│   ├── layouts/          # Layout components
│   │   ├── base.py
│   │   ├── header.py
│   │   ├── sidebar.py
│   │   └── footer.py
│   ├── widgets/          # Documentation widgets
│   │   ├── code_block.py
│   │   ├── preview_card.py
│   │   └── installation_section.py
│   └── pages/            # Documentation pages
│       ├── components/   # Component docs
│       │   └── button.py
│       └── components_index.py
└── static/
    └── css/
        └── styles.css
```

## Adding New Components

1. Create a new file in `docs/pages/components/`:

```python
# docs/pages/components/my_component.py
"""My component documentation."""

TITLE = "My Component"
DESCRIPTION = "Description of my component"
CATEGORY = "ui"
ORDER = 50
STATUS = "stable"

from starhtml import *
from starhtml.datastar import *
from starui.registry.components.my_component import MyComponent


def examples():
    """Generate component examples."""
    yield "Basic", MyComponent("Hello")
    yield "With Props", MyComponent("World", variant="primary")
    
    yield "Interactive", Div(
        MyComponent("Click me", ds_on_click("$count++")),
        P(ds_text("$count")),
        ds_signals(count=0)
    )


def create_my_component_docs():
    """Create documentation page."""
    from starui_docs.utils import auto_generate_page
    
    return auto_generate_page(
        component_name=TITLE,
        description=DESCRIPTION,
        examples=list(examples()),
        cli_command="star add my_component",
        usage_code="""from starui.registry.components.my_component import MyComponent

MyComponent("Hello World")""",
        api_reference={
            "props": [
                {
                    "name": "variant",
                    "type": "str",
                    "default": "'default'",
                    "description": "Component variant"
                }
            ]
        }
    )
```

2. The component will be auto-discovered and added to the documentation.

## Code Quality Guidelines

All documentation code follows the patterns defined in `PATTERNS.md`:

- **Idiomatic**: Pythonic, concise, modern code
- **Datastar-ish**: Reactive signals, no DOM manipulation
- **Clean**: Self-documenting, minimal comments
- **Consistent**: Standard component patterns

Key conventions:
- Use `cls` for final class attributes
- Datastar functions before keyword arguments
- No `.attrs` unpacking
- CVA with `config` parameter
- Reactive state management

## Component Patterns

### Standard Component Structure
```python
def Component(
    *children: Any,
    variant: str = "default",
    class_name: str = "",
    cls: str = "",
    **attrs: Any
) -> FT:
    classes = cn(
        component_variants(variant=variant),
        class_name,
        cls
    )
    return BaseElement(*children, cls=classes, **attrs)
```

### Datastar Integration
```python
# Reactive state
Button(
    ds_text("$loading ? 'Loading...' : 'Submit'"),
    ds_disabled("$loading"),
    ds_on_click("$handleSubmit()")
)

# Conditional rendering
Dialog(
    ds_show("$dialog_open"),
    ds_on_click("$dialog_open = false")
)
```

## Contributing

When contributing documentation:

1. Follow the patterns in existing components
2. Ensure code is idiomatic and datastar-ish
3. Test all interactive examples
4. Verify responsive layout
5. Check dark mode compatibility

## License

MIT