#!/usr/bin/env python3
"""Generate entrepreneurship-redefined-2020.html from pdf-catalog JSON."""

from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "pdf-catalog" / "sections"
OUT = ROOT / "entrepreneurship-redefined-2020.html"
PAGE_IMG = "assets/entrepreneurship-redefined/pages/page-{page:03d}.png"

SECTION_FILES = [
    "00-frontmatter.json",
    "01-redefining.json",
    "02-executive-summary.json",
    "03-narrative-diversity.json",
    "04-narrative-purpose.json",
    "05-narrative-innovation.json",
    "06-appendix.json",
]


def load_sections() -> dict[str, dict]:
    sections = {}
    for name in SECTION_FILES:
        data = json.loads((CATALOG / name).read_text(encoding="utf-8"))
        sections[data["id"]] = data
    return sections


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "section"


def paragraphs(text: str) -> str:
    parts = [p.strip() for p in text.split("\n\n") if p.strip()]
    return "".join(f"<p>{esc(p)}</p>" for p in parts)


def render_stats(stats: list[dict]) -> str:
    if not stats:
        return ""
    items = []
    for stat in stats:
        items.append(
            f"""        <div class="stat-box">
          <div class="stat-number">{esc(stat["value"])}</div>
          <div class="stat-label">{esc(stat["label"])}</div>
        </div>"""
        )
    return f'      <div class="stat-grid">\n' + "\n".join(items) + "\n      </div>"


def render_quotes(quotes: list[dict]) -> str:
    if not quotes:
        return ""
    cards = []
    for quote in quotes:
        cards.append(
            f"""        <figure class="quote-card">
          <blockquote>{esc(quote["text"])}</blockquote>
          <figcaption>{esc(quote.get("attribution", ""))}</figcaption>
        </figure>"""
        )
    return f'      <div class="quote-grid">\n' + "\n".join(cards) + "\n      </div>"


def chart_pages(chart: dict) -> list[int]:
    if "page" in chart:
        return [chart["page"]]
    return chart.get("pages", [])


def render_charts(charts: list[dict]) -> str:
    if not charts:
        return ""
    cards = []
    for chart in charts:
        pages = chart_pages(chart)
        if not pages:
            continue
        page = pages[0]
        cards.append(
            f"""        <figure class="figure-card">
          <img src="{PAGE_IMG.format(page=page)}" alt="{esc(chart['description'])}" loading="lazy">
          <figcaption class="figure-caption"><strong>Figure · PDF page {page}</strong> — {esc(chart['description'])}</figcaption>
        </figure>"""
        )
    if not cards:
        return ""
    return f'      <div class="figure-grid">\n' + "\n".join(cards) + "\n      </div>"


def render_subsections(section: dict) -> str:
    blocks = []
    used_chart_pages: set[int] = set()

    for sub in section.get("sub_sections", []):
        sid = slugify(sub.get("id") or sub["title"])
        block = f'      <h3 class="subsection-title" id="{sid}">{esc(sub["title"])}</h3>\n'
        block += f'      <div class="prose">{paragraphs(sub.get("body", ""))}</div>\n'
        block += render_stats(sub.get("key_stats", [])) + "\n"
        block += render_quotes(sub.get("quotes", [])) + "\n"

        sub_pages = set(sub.get("pages", []))
        sub_charts = [c for c in section.get("charts", []) if any(p in sub_pages for p in chart_pages(c))]
        if sub_charts:
            block += render_charts(sub_charts) + "\n"
            for c in sub_charts:
                used_chart_pages.update(chart_pages(c))

        blocks.append(block)

    leftover = [c for c in section.get("charts", []) if not any(p in used_chart_pages for p in chart_pages(c))]
    if leftover:
        blocks.append(render_charts(leftover))

    return "\n".join(blocks)


def render_frontmatter(data: dict) -> str:
    intro = data.get("introduction_text", "")
    intro = intro.replace("INTRODUCTION\n", "", 1)
    intro_parts = intro.split("\n\nOn behalf of the Slush team,")
    main_intro = intro_parts[0].strip()
    signoff = ""
    if len(intro_parts) > 1:
        signoff = "On behalf of the Slush team," + intro_parts[1]

    toc_items = []
    anchors = {
        "Redefining Entrepreneurship & Why This Matters": "#redefining",
        "20 Predictions for the 2020s": "#predictions",
        "Executive Summary": "#exec-summary",
        "Key Findings": "#key-findings",
        "Narrative 1: Diverse and Inclusive Future": "#narrative-diversity",
        "Narrative 2: Purpose-Driven Change": "#narrative-purpose",
        "Narrative 3: Revolutionary Innovation": "#narrative-innovation",
        "Appendix": "#appendix",
    }
    for item in data.get("table_of_contents", []):
        href = anchors.get(item["section"], "#top")
        toc_items.append(
            f'        <a class="toc-item" href="{href}"><span class="toc-item-title">{esc(item["section"])}</span><span class="toc-item-page">p. {item["page"]}</span></a>'
        )

    signoff_html = ""
    if signoff:
        signoff_lines = [line.strip() for line in signoff.strip().split("\n") if line.strip()]
        signoff_html = "<p><em>" + "<br>".join(esc(line) for line in signoff_lines) + "</em></p>"

    return f"""  <section class="chapter" id="introduction" aria-labelledby="intro-title">
    <div class="chapter-inner">
      <div class="chapter-number">Introduction</div>
      <h2 id="intro-title">Why we need to redefine entrepreneurship</h2>
      <div class="prose">{paragraphs(main_intro)}{signoff_html}</div>

      <div class="section-label">Contents</div>
      <nav class="toc-list" aria-label="Table of contents">
{chr(10).join(toc_items)}
      </nav>
    </div>
  </section>"""


def render_redefining(data: dict) -> str:
    intro = data.get("intro_text", "")
    intro = re.sub(r"^REDEFINING ENTREPRENEURSHIP WITH\s*\n*", "", intro, flags=re.IGNORECASE).strip()

    quotes = []
    for quote in data.get("partner_quotes", []):
        quotes.append(
            f"""        <figure class="partner-quote-card">
          <blockquote>{esc(quote["text"])}</blockquote>
          <figcaption>{esc(quote["attribution"])}</figcaption>
        </figure>"""
        )

    predictions = []
    for pred in data.get("predictions", []):
        predictions.append(
            f"""        <div class="prediction-card">
          <div class="prediction-number">{pred["number"]}</div>
          <div class="prediction-text">{esc(pred["prediction"])}</div>
        </div>"""
        )

    return f"""  <section class="chapter" id="redefining" aria-labelledby="redefining-title">
    <div class="chapter-inner">
      <div class="chapter-number">Redefining entrepreneurship</div>
      <h2 id="redefining-title">Joined by 16 European scaleups</h2>
      <div class="prose"><p>{esc(intro)}</p></div>
      <div class="figure-grid">
        <figure class="figure-card">
          <img src="{PAGE_IMG.format(page=4)}" alt="Partner endorsements from European scaleups and investors" loading="lazy">
          <figcaption class="figure-caption"><strong>Figure · PDF pages 4–7</strong> — Endorsements from European scaleups and ecosystem leaders.</figcaption>
        </figure>
      </div>
      <div class="partner-quote-grid">
{chr(10).join(quotes)}
      </div>
    </div>
  </section>

  <section class="chapter" id="predictions" aria-labelledby="predictions-title">
    <div class="chapter-inner">
      <div class="chapter-number">Predictions</div>
      <h2 id="predictions-title">20 predictions for the 2020s</h2>
      <div class="predictions-grid">
{chr(10).join(predictions)}
      </div>
    </div>
  </section>"""


def render_exec_summary(data: dict) -> str:
    summaries = []
    for item in data.get("exec_summary", []):
        summaries.append(
            f"""        <article class="narrative-summary-card">
          <h3>{esc(item["narrative"])}</h3>
          <p>{esc(item["summary_text"])}</p>
        </article>"""
        )

    findings = []
    for finding in data.get("key_findings", []):
        findings.append(
            f"""        <article class="finding-item">
          <div class="finding-item-number">Finding {finding["number"]}</div>
          <h3>{esc(finding["title"])}</h3>
          <p>{esc(finding["body"])}</p>
        </article>"""
        )

    return f"""  <section class="chapter" id="exec-summary" aria-labelledby="exec-title">
    <div class="chapter-inner">
      <div class="chapter-number">Executive summary</div>
      <h2 id="exec-title">Three narratives shaping European entrepreneurship</h2>
      <div class="narrative-summary-grid">
{chr(10).join(summaries)}
      </div>
    </div>
  </section>

  <section class="chapter" id="key-findings" aria-labelledby="findings-title">
    <div class="chapter-inner">
      <div class="chapter-number">Key findings</div>
      <h2 id="findings-title">Seven findings from Slush 2019 data</h2>
      <div class="finding-list">
{chr(10).join(findings)}
      </div>
    </div>
  </section>"""


def render_narrative(section: dict) -> str:
    sid = section["id"].replace("03-", "").replace("04-", "").replace("05-", "")
    anchor = sid
    title = section["title"]
    eyebrow = section.get("eyebrow", "")

    return f"""  <section class="chapter" id="{anchor}" aria-labelledby="{anchor}-title">
    <div class="chapter-inner">
      <div class="chapter-number">{esc(eyebrow)}</div>
      <h2 id="{anchor}-title">{esc(title)}</h2>
      <div class="prose"><p>{esc(section.get("intro_text", ""))}</p></div>
{render_subsections(section)}
    </div>
  </section>"""


def render_appendix(data: dict) -> str:
    methodology = data.get("methodology", {})
    methodology_items = []
    for key, body in methodology.items():
        label = key.replace("_", " ").title()
        methodology_items.append(
            f"""        <div class="methodology-item">
          <h3>{esc(label)}</h3>
          <p>{esc(body)}</p>
        </div>"""
        )

    creators = data.get("creators", {})
    authors = ", ".join(creators.get("authors", []))
    supporting = ", ".join(creators.get("supporting_authors", []))
    design = ", ".join(creators.get("design_tech", []))
    dataset = data.get("slush_2019_dataset_sizes", {})

    return f"""  <section class="chapter" id="appendix" aria-labelledby="appendix-title">
    <div class="chapter-inner">
      <div class="chapter-number">Appendix</div>
      <h2 id="appendix-title">About Slush, methodology &amp; credits</h2>

      <div class="prose"><p>{esc(data.get("about_slush", ""))}</p></div>

      <div class="exec-meta-layout">
        <div class="exec-summary">
          <p><strong>Authors:</strong> {esc(authors)}</p>
          <p><strong>Supporting authors:</strong> {esc(supporting)}</p>
          <p><strong>Design &amp; tech:</strong> {esc(design)}</p>
          <p>{esc(data.get("contributors_note", ""))}</p>
        </div>
        <aside class="meta-panel">
          <div class="meta-row">
            <div class="meta-label">Published</div>
            <div class="meta-value">Slush 2020</div>
          </div>
          <div class="meta-row">
            <div class="meta-label">Contact</div>
            <div class="meta-value"><a href="mailto:{esc(data.get('contact', 'hello@slush.org'))}">{esc(data.get("contact", "hello@slush.org"))}</a></div>
          </div>
          <div class="meta-row">
            <div class="meta-label">Slush 2019 data</div>
            <div class="meta-value">{dataset.get("startups", 0):,} startups · {dataset.get("vc_firms", 0):,} VC firms</div>
            <div class="meta-sub">{dataset.get("meeting_requests_sent", 0):,} meeting requests · {dataset.get("meetings_held", 0):,} meetings held</div>
          </div>
          <div class="meta-row">
            <div class="meta-label">Interviews</div>
            <div class="meta-value">{data.get("interview_sample", {}).get("total", 58)} anonymous expert interviews</div>
            <div class="meta-sub">{data.get("interview_sample", {}).get("percent_women", "34%")} women</div>
          </div>
        </aside>
      </div>

      <div class="section-label">Methodology</div>
      <div class="methodology-grid">
{chr(10).join(methodology_items)}
      </div>
    </div>
  </section>"""


def build_html(sections: dict[str, dict]) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Entrepreneurship Redefined — Slush 2020</title>
  <meta name="description" content="Slush whitepaper on diversity, purpose-driven entrepreneurship, and revolutionary innovation in European tech.">
  <link rel="apple-touch-icon" href="assets/slush-s-icon.jpeg" />
  <meta name="theme-color" content="#000000" />
  <link rel="icon" type="image/jpeg" href="assets/logo.jpeg" />
  <link rel="shortcut icon" type="image/jpeg" href="assets/logo.jpeg" />

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;900&display=swap" rel="stylesheet">

  <link rel="stylesheet" href="design-system/slush.css">
</head>

<body>

  <nav class="topnav" aria-label="Chapter navigation">
    <a class="topnav-brand" href="/" aria-label="Slush — Impact Report Series">
      <img class="topnav-logo" src="assets/slush-logo.png" alt="Slush">
      <span>Entrepreneurship Redefined</span>
    </a>
    <span class="topnav-divider" aria-hidden="true"></span>
    <ul class="topnav-links">
      <li><a href="/">All reports</a></li>
      <li><a href="#introduction">Introduction</a></li>
      <li><a href="#exec-summary">Summary</a></li>
      <li><a href="#narrative-diversity">Diversity</a></li>
      <li><a href="#narrative-purpose">Purpose</a></li>
      <li><a href="#narrative-innovation">Innovation</a></li>
      <li><a href="#appendix">Appendix</a></li>
    </ul>
  </nav>

  <section class="hero" id="top" aria-labelledby="hero-title">
    <div class="hero-image" role="img" aria-label="Slush hero visual"></div>
    <div class="hero-overlay"></div>
    <div class="hero-content">
      <div class="eyebrow">Slush Whitepaper · 2020</div>
      <h1 id="hero-title">Entrepreneurship Redefined</h1>
      <div class="hero-meta">
        Diversity · Purpose · Revolutionary innovation in European tech · <a href="Entrepreneurship-Redefined-Slush-2020.pdf" style="color:inherit;">Download PDF</a>
      </div>
    </div>
  </section>

{render_frontmatter(sections["00-frontmatter"])}

{render_redefining(sections["01-redefining"])}

{render_exec_summary(sections["02-executive-summary"])}

{render_narrative(sections["03-narrative-diversity"])}

{render_narrative(sections["04-narrative-purpose"])}

{render_narrative(sections["05-narrative-innovation"])}

{render_appendix(sections["06-appendix"])}

  <footer>
    Slush Research · Entrepreneurship Redefined (2020)
  </footer>

</body>
</html>
"""


def main() -> None:
    sections = load_sections()
    html_out = build_html(sections)
    OUT.write_text(html_out, encoding="utf-8")
    print(f"Wrote {OUT} ({len(html_out):,} bytes)")

    # Replace PDF screenshot placeholders with coded charts
    import inject_charts

    inject_charts.main()


if __name__ == "__main__":
    main()
