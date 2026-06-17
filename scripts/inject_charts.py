#!/usr/bin/env python3
"""Replace PDF screenshot figure-cards with coded SVG/HTML charts."""

from __future__ import annotations

import re
from pathlib import Path

from chart_snippets import CHART_BY_PAGE

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "entrepreneurship-redefined-2020.html"

FIGURE_RE = re.compile(
    r'<figure class="figure-card">\s*'
    r'<img src="assets/entrepreneurship-redefined/pages/(page-\d+\.png)"[^>]*>\s*'
    r'<figcaption class="figure-caption">.*?</figcaption>\s*'
    r'</figure>',
    re.DOTALL,
)

# Track duplicate page keys (page-050, page-051, etc.)
duplicate_queues: dict[str, list[str]] = {}
for key, val in CHART_BY_PAGE.items():
    if isinstance(val, list):
        duplicate_queues[key] = list(val)


def next_chart(page: str) -> str:
    if page in duplicate_queues and duplicate_queues[page]:
        return duplicate_queues[page].pop(0)
    chart = CHART_BY_PAGE.get(page)
    if chart is None:
        raise KeyError(f"No chart defined for {page}")
    if isinstance(chart, list):
        return chart[0]
    return chart


def replace_figure(match: re.Match[str]) -> str:
    page = match.group(1)
    return next_chart(page)


def main() -> None:
    text = HTML.read_text(encoding="utf-8")
    count = len(FIGURE_RE.findall(text))
    updated = FIGURE_RE.sub(replace_figure, text)
    updated = updated.replace('class="figure-grid"', 'class="inline-charts two-col"')
    # Single-card grids in redefining section — use one-col
    updated = updated.replace(
        '      <div class="inline-charts two-col">\n    <div class="chart-card">\n      <div class="chart-headline">16 European scaleups',
        '      <div class="inline-charts one-col">\n    <div class="chart-card">\n      <div class="chart-headline">16 European scaleups',
        1,
    )
    remaining = len(re.findall(r"page-\d+\.png", updated))
    HTML.write_text(updated, encoding="utf-8")
    print(f"Replaced {count} figure cards.")
    print(f"Remaining page-*.png references: {remaining}")
    if remaining:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
