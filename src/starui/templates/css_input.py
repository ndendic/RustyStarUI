"""CSS input template generation."""

from typing import Optional
from ..config import ProjectConfig
from ..themes import THEMES, generate_theme_css

CSS_TEMPLATE_BASE = '@import "tailwindcss";'

CSS_RESET = """\
*, *::before, *::after {
  box-sizing: border-box;
}

* {
  margin: 0;
}

@media (prefers-reduced-motion: no-preference) {
  html {
    interpolate-size: allow-keywords;
  }
}

body {
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
}

img, picture, video, canvas, svg {
  display: block;
  max-width: 100%;
}

input, button, textarea, select {
  font: inherit;
}

p, h1, h2, h3, h4, h5, h6 {
  overflow-wrap: break-word;
}

p {
  text-wrap: pretty;
}

h1, h2, h3, h4, h5, h6 {
  text-wrap: balance;
}

#root, #__next {
  isolation: isolate;
}"""


def generate_css_input(
    config: Optional[ProjectConfig] = None, 
    include_reset: bool = True
) -> str:
    """Generate CSS input file content for Tailwind v4 with default theme."""
    content = CSS_TEMPLATE_BASE

    if include_reset:
        content += "\n\n" + CSS_RESET

    content += "\n\n" + generate_theme_css(THEMES["default"])
    return content
