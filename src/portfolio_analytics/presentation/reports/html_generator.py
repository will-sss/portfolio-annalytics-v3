# SPDX-License-Identifier: MIT

"""HTML report generation utilities."""

from __future__ import annotations

from typing import Dict, Any


def build_html_report(title: str, sections: Dict[str, str]) -> str:
    """Assemble a simple HTML report from sections.

    This function is a placeholder for a more sophisticated templating
    system (e.g., using Jinja2).  Each section is a HTML fragment.

    Parameters
    ----------
    title:
        The report title.
    sections:
        A mapping of section headings to HTML fragments.

    Returns
    -------
    str
        A complete HTML document.
    """
    html_sections = "\n".join(
        f"<h2>{heading}</h2>\n<div>{content}</div>" for heading, content in sections.items()
    )
    return f"""
    <html>
      <head>
        <meta charset="utf-8" />
        <title>{title}</title>
      </head>
      <body>
        <h1>{title}</h1>
        {html_sections}
      </body>
    </html>
    """
