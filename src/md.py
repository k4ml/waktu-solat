"""Markdown rendering for article bodies.

A single shared mistune renderer. Raw HTML in the source is passed through
(``escape=False``) so article authors can drop in a table or a callout when
Markdown is not enough.
"""

import mistune

_renderer = mistune.create_markdown(
    escape=False,
    plugins=["strikethrough", "table", "url"],
)


def render(text: str) -> str:
    """Render a Markdown string to HTML."""
    return _renderer(text or "")
