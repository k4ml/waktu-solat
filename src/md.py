"""Markdown rendering for article bodies.

A single shared mistune renderer. Raw HTML in the source is passed through
(``escape=False``) so article authors can drop in a table or a callout when
Markdown is not enough.
"""

import re

import mistune

_renderer = mistune.create_markdown(
    escape=False,
    plugins=["strikethrough", "table", "url", "footnotes"],
)

# mistune emits the same id for every reference to the same footnote, which is
# invalid HTML. The first id is kept so the note's back-link has a target.
_FOOTNOTE_REF_ID = re.compile(r'id="fnref-(\d+)"')


def render(text: str) -> str:
    """Render a Markdown string to HTML."""
    return _dedupe_footnote_ids(_renderer(text or ""))


def _dedupe_footnote_ids(html: str) -> str:
    """Suffix repeated footnote reference ids so every id stays unique."""
    seen = {}

    def repl(match):
        number = match.group(1)
        seen[number] = seen.get(number, 0) + 1
        if seen[number] == 1:
            return match.group(0)
        return f'id="fnref-{number}-{seen[number]}"'

    return _FOOTNOTE_REF_ID.sub(repl, html)

