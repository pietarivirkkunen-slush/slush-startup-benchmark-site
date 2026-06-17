# PDF Data Catalog Schema

## Purpose
This catalog converts the PDF "Entrepreneurship Redefined — Slush 2020" into structured JSON data that an agent can use to build a webpage.

## Section Files
Each section is saved as `sections/<section-id>.json` with this schema:

```json
{
  "id": "narrative-1-diversity",
  "title": "Narrative 1: Diverse & Inclusive Future",
  "subtitle": "Optional subtitle",
  "type": "narrative|intro|exec-summary|key-findings|appendix|predictions",
  "pages": [18, 19, 20, ...],
  "eyebrow": "Short label e.g. 'Narrative 1'",
  "intro_text": "Opening paragraph(s) for this section",
  "sub_sections": [
    {
      "title": "Sub-section heading",
      "pages": [19, 20],
      "body": "Full text content...",
      "key_stats": [
        { "value": "82%", "label": "of founders had received a university degree" }
      ],
      "quotes": [
        {
          "text": "Quote text here",
          "attribution": "— Founder"
        }
      ]
    }
  ],
  "key_stats": [],
  "quotes": [],
  "charts": [
    {
      "page": 24,
      "description": "Bar chart showing funding rates by gender",
      "data_note": "Raw numbers not extractable from PDF"
    }
  ]
}
```

## Section Map
| File | Pages | Title |
|------|-------|-------|
| 00-frontmatter.json | 1-3 | Cover, Introduction, Contents |
| 01-redefining.json | 4-9 | Redefining Entrepreneurship + 20 Predictions |
| 02-executive-summary.json | 10-17 | Executive Summary + Key Findings |
| 03-narrative-diversity.json | 18-43 | Narrative 1: Diverse & Inclusive Future |
| 04-narrative-purpose.json | 44-68 | Narrative 2: Purpose-Driven Change |
| 05-narrative-innovation.json | 69-90 | Narrative 3: Revolutionary Innovation |
| 06-appendix.json | 91-96 | Appendix |
