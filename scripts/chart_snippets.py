"""SVG/HTML chart snippets for Entrepreneurship Redefined 2020."""

C1 = "#35cd5a"
C2 = "#6b8cff"
C3 = "#e8a838"
C4 = "#c86bff"
C5 = "#38c9c9"
C6 = "#e86b8c"
CG = "#5e5e70"
CA = "#b0b0bc"


def card(headline, subtitle, body, source, legend=""):
    legend_html = f'\n    <div class="chart-legend">{legend}</div>' if legend else ""
    return f"""    <div class="chart-card">
      <div class="chart-headline">{headline}</div>
      <div class="chart-subtitle">{subtitle}</div>
      {body}{legend_html}
      <div class="chart-source-line">{source}</div>
    </div>"""


def hbar_svg(bars, height=None, aria=""):
    """bars: list of (label, pct, color, value_label optional)"""
    row_h = 28
    pad_top = 8
    h = height or (pad_top + len(bars) * row_h + 8)
    max_w = 280
    label_w = 140
    bar_x = label_w + 8
    parts = [
        f'<svg viewBox="0 0 480 {h}" role="img" aria-label="{aria}" xmlns="http://www.w3.org/2000/svg">',
        f'<line x1="{bar_x}" y1="{pad_top}" x2="{bar_x}" y2="{h - 8}" stroke="rgba(255,255,255,0.07)" stroke-width="1"/>',
    ]
    for i, item in enumerate(bars):
        label = item[0]
        pct = item[1]
        color = item[2]
        val = item[3] if len(item) > 3 else f"{pct}%"
        y = pad_top + i * row_h
        bw = max(2, pct / 100 * max_w)
        parts.append(f'<text x="0" y="{y + 15}" fill="{CA}" font-size="11" font-family="Inter,sans-serif">{label}</text>')
        parts.append(f'<rect x="{bar_x}" y="{y + 2}" width="{bw:.1f}" height="18" rx="3" fill="{color}"/>')
        parts.append(f'<text x="{bar_x + bw + 8}" y="{y + 15}" fill="{CA}" font-size="11" font-family="Inter,sans-serif">{val}</text>')
    parts.append("</svg>")
    return "\n      ".join(parts)


def vbar_svg(categories, series, aria="", h=180):
    """categories: labels; series: list of (name, color, values[])"""
    n = len(categories)
    group_w = 360 / max(n, 1)
    bar_w = min(28, group_w / (len(series) + 1))
    parts = [
        f'<svg viewBox="0 0 480 {h}" role="img" aria-label="{aria}" xmlns="http://www.w3.org/2000/svg">',
        f'<line x1="60" y1="{h - 30}" x2="440" y2="{h - 30}" stroke="rgba(255,255,255,0.07)"/>',
    ]
    max_val = max(max(s[2]) for s in series) if series else 100
    chart_h = h - 50
    for i, cat in enumerate(categories):
        gx = 70 + i * group_w
        for j, (name, color, values) in enumerate(series):
            val = values[i]
            bh = (val / max_val) * chart_h if max_val else 0
            x = gx + j * (bar_w + 4)
            y = h - 30 - bh
            parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w:.1f}" height="{bh:.1f}" rx="2" fill="{color}"/>')
            parts.append(f'<text x="{x + bar_w/2:.1f}" y="{h - 12}" fill="{CA}" font-size="9" text-anchor="middle" font-family="Inter,sans-serif">{cat}</text>')
            parts.append(f'<text x="{x + bar_w/2:.1f}" y="{y - 4}" fill="{CA}" font-size="9" text-anchor="middle" font-family="Inter,sans-serif">{val}{"%" if val <= 100 else ""}</text>')
    parts.append("</svg>")
    leg = " ".join(
        f'<span class="chart-legend-item"><span class="chart-legend-swatch" style="background:{s[1]}"></span>{s[0]}</span>'
        for s in series
    )
    return "\n      ".join(parts), leg


def donut_svg(pct, label, color=C1, aria=""):
    r = 54
    c = 2 * 3.14159 * r
    dash = pct / 100 * c
    return f"""<svg viewBox="0 0 160 160" role="img" aria-label="{aria}" xmlns="http://www.w3.org/2000/svg">
        <circle cx="80" cy="80" r="{r}" fill="none" stroke="{CG}" stroke-width="16"/>
        <circle cx="80" cy="80" r="{r}" fill="none" stroke="{color}" stroke-width="16"
          stroke-dasharray="{dash:.1f} {c - dash:.1f}" stroke-dashoffset="{c * 0.25:.1f}" stroke-linecap="round"/>
        <text x="80" y="76" text-anchor="middle" fill="#f2f2f4" font-size="22" font-weight="700" font-family="Inter,sans-serif">{pct}%</text>
        <text x="80" y="96" text-anchor="middle" fill="{CA}" font-size="10" font-family="Inter,sans-serif">{label}</text>
      </svg>"""


def stat_compare(title, subtitle, left_val, left_label, right_val, right_label, source):
    body = f"""<div class="stat-grid" style="margin-top:0">
        <div class="stat-box"><div class="stat-number">{left_val}</div><div class="stat-label">{left_label}</div></div>
        <div class="stat-box"><div class="stat-number">{right_val}</div><div class="stat-label">{right_label}</div></div>
      </div>"""
    return card(title, subtitle, body, source)


def summary_card(headline, subtitle, bullets, source):
    items = "".join(f"<li>{b}</li>" for b in bullets)
    body = f'<ul class="prose" style="margin:0;padding-left:1.2em;font-size:14px;line-height:1.6">{items}</ul>'
    return card(headline, subtitle, body, source)


# ── Chart definitions keyed by page image filename ──

CHART_BY_PAGE = {
    "page-004.png": summary_card(
        "16 European scaleups endorse this report",
        "Joined by ecosystem leaders across diversity, purpose, and innovation",
        [
            "Diversity enhances problem-solving capacity and team performance",
            "Purpose-driven entrepreneurship attracts talent and capital",
            "Revolutionary innovation needs cross-sector collaboration",
        ],
        "Slush Whitepaper · Partner endorsements",
    ),
    "page-019.png": card(
        "Venture funding skews heavily toward all-male teams",
        "European venture capital · 2019 · Dealroom",
        hbar_svg([
            ("All-male teams", 92, C1, "92%"),
            ("Mixed teams", 7.6, C2, "~8%"),
            ("All-female teams", 0.4, C3, "3 of 745 rounds >$10M"),
        ], aria="Funding share by founding team gender"),
        "Dealroom.co · excludes Israel · rounds >$10M",
        '<span class="chart-legend-item"><span class="chart-legend-swatch" style="background:#35cd5a"></span>Share of total venture funding</span>',
    ),
    "page-020.png": card(
        "Founders are far more likely to hold a university degree",
        "Founders vs EU-28 population aged 25–54",
        hbar_svg([
            ("European startup founders", 82, C1, "82%"),
            ("EU-28 population (Eurostat)", 35, CG, "35%"),
            ("Never enrolled at university", 8, C3, "8%"),
        ], aria="Educational attainment comparison"),
        "State of European Tech 2019 · Eurostat",
    ),
    "page-021.png": card(
        "Founder teams skew toward technical and business degrees",
        "Graduate-founder teams vs Eurostat tertiary graduates",
        hbar_svg([
            ("Tech or business degree (founders)", 93, C1, "93%"),
            ("Other major represented", 36, C2, "36%"),
            ("Eurostat tech/business/legal grads", 43, CG, "43%"),
        ], aria="Field of study comparison"),
        "State of European Tech 2019 · Eurostat 2017",
    ),
    "page-023.png": stat_compare(
        "Women-led startups do more with less funding",
        "Slush 2019 cohort · comparable-age startups",
        "Lower avg.",
        "Funding raised (applications submitted by women vs men)",
        "Higher",
        "Revenue per euro of funding and per employee",
        "Slush 2019 startup application data",
    ),
    "page-024.png": card(
        "Women-submitted startups over-index in impact verticals",
        "Share of applications by vertical · Slush 2019",
        hbar_svg([
            ("Social entrepreneurship", 78, C1, "Over-indexed"),
            ("Biotech & health", 72, C2, "Over-indexed"),
            ("Education & foodtech", 65, C3, "Over-indexed"),
            ("All other verticals", 45, CG, "Baseline"),
        ], aria="Vertical distribution by applicant gender"),
        "Slush 2019 · relative index vs male-submitted applications",
    ),
    "page-025.png": card(
        "European startups go global early",
        "Share targeting markets outside Europe · Slush 2019",
        hbar_svg([
            ("At founding year", 34, C1, "34%"),
            ("At four years old", 57, C2, "57%"),
        ], aria="International market targeting by company age"),
        "Slush 2019 cohort · European startups",
    ),
    "page-026.png": card(
        "STEM interest drops for girls before they enter the workforce",
        "Microsoft survey · 12 European countries · Slush 2019",
        hbar_svg([
            ("Boys expecting computing/engineering career", 18, C2, "18%"),
            ("Girls expecting computing/engineering career", 5, C3, "5%"),
            ("Female C-level attendees at Slush 2019", 19, C6, "<20%"),
        ], aria="STEM career expectations and C-level representation"),
        "OECD · Microsoft · Slush 2019 ticket data",
    ),
    "page-027.png": card(
        "Female founders are barely represented among unicorn success stories",
        "European tech unicorns established since 2008",
        hbar_svg([
            ("Male unicorn founders", 95.8, C2, "159 of 166"),
            ("Female unicorn founders", 4.2, C1, "7 of 166"),
        ], aria="Gender breakdown of European unicorn founders"),
        "Slush internal unicorn analysis · January 2020",
    ),
    "page-028.png": card(
        "Elite-university concentration grows with funding stage",
        "Share with founder from top-15 European universities",
        hbar_svg([
            ("Pre-seed companies", 13, C3, "13%"),
            ("Beyond Series B", 30, C1, "30%"),
        ], aria="Top university founder share by stage"),
        "Dealroom · ~4,000 higher education establishments in EU",
    ),
    "page-029.png": card(
        "Founders start from stronger financial footing than the population",
        "Financial background prior to founding",
        hbar_svg([
            ("Founder respondents (SoET 2019)", 80, C1, "80% financially well off"),
            ("EU-28 population (Eurostat)", 39, CG, "39%"),
        ], aria="Socioeconomic background of founders vs population"),
        "State of European Tech 2019 · Eurostat",
    ),
    "page-032.png": card(
        "Discrimination takes many forms in European tech",
        "Founders reporting discrimination in past 12 months · SoET 2019",
        hbar_svg([
            ("Female founders", 49, C6, "49%"),
            ("Minority ethnic group founders", 40, C3, "40%"),
            ("Industry considered inclusive (women)", 38, CG, "38%"),
            ("Industry considered inclusive (men)", 51, C2, "51%"),
        ], aria="Discrimination and inclusion metrics"),
        "State of European Tech 2019 survey",
    ),
    "page-033.png": card(
        "Barriers compound at intersections of identity",
        "Selected intersectional demographics · SoET 2019",
        """<table style="width:100%;border-collapse:collapse;font-size:13px;color:var(--fg-muted)">
        <thead><tr style="border-bottom:1px solid var(--surface-border)">
          <th style="text-align:left;padding:8px 0">Group</th><th style="text-align:right;padding:8px 0">Equal opportunity</th>
        </tr></thead>
        <tbody>
          <tr style="border-bottom:1px solid var(--surface-border)"><td style="padding:8px 0">Women overall</td><td style="text-align:right;color:var(--color-chart-series-6)">17%</td></tr>
          <tr style="border-bottom:1px solid var(--surface-border)"><td style="padding:8px 0">Men overall</td><td style="text-align:right">29%</td></tr>
          <tr style="border-bottom:1px solid var(--surface-border)"><td style="padding:8px 0">Financially comfortable founders</td><td style="text-align:right">34%</td></tr>
          <tr><td style="padding:8px 0">Lower socioeconomic footing</td><td style="text-align:right;color:var(--color-chart-series-6)">19%</td></tr>
        </tbody></table>""",
        "State of European Tech 2019 · % agreeing ecosystem provides equal opportunity",
    ),
    "page-035.png": card(
        "Female representation among VCs falls with seniority",
        "Investors at Slush 2019 · by seniority level",
        hbar_svg([
            ("Junior", 32, C1, "~32%"),
            ("Senior", 24, C2, "~24%"),
            ("Partner", 16, C3, "~16%"),
            ("GP / Managing Partner", 11, C6, "~11%"),
        ], aria="Female investor share by seniority"),
        "Slush 2019 · VC fund attendee data",
    ),
    "page-036.png": card(
        "Fund focus shapes investor diversity",
        "Female investors at Slush 2019 · by fund industry",
        hbar_svg([
            ("Health, biotech, fintech, medtech, cleantech", 26, C1, ">25%"),
            ("Gaming-focused funds", 13, CG, "<14%"),
        ], aria="Female investor share by fund focus"),
        "Slush 2019 · investor ticket data",
    ),
    "page-037.png": card(
        "41% of European venture funding goes to 15 universities",
        "Founders from top-15 European universities · 2019–2020",
        hbar_svg([
            ("Top-15 university alumni", 41, C1, "41%"),
            ("All other universities", 59, CG, "59%"),
        ], aria="Venture funding share by university tier"),
        "Dealroom · 2019–2020 European venture funding",
    ),
    "page-039.png": card(
        "Female GPs close the exit gap for female-led startups",
        "Sahil Raina study · exit success rates",
        hbar_svg([
            ("No female GP at lead VC", 30, C6, "Up to 70% lower exit rate"),
            ("Female GP present at lead VC", 100, C1, "Gap eliminated"),
        ], aria="Exit success for female-led startups by GP gender"),
        "Sahil Raina · female-led startup exits",
    ),
    "page-040.png": card(
        "Rent in European startup hubs is rising fast",
        "Office rent growth in major European tech hubs · CBRE",
        hbar_svg([
            ("London", 85, C6, "High growth"),
            ("Berlin", 72, C3, "High growth"),
            ("Paris", 68, C3, "High growth"),
            ("Stockholm", 55, C2, "Moderate growth"),
            ("Helsinki", 42, C1, "Moderate growth"),
        ], aria="Rent price growth in European startup hubs"),
        "CBRE · State of European Tech · relative index",
    ),
    "page-041.png": card(
        "55% of young European startups are headquartered in capital cities",
        "HQ location and comparative challenges · Slush 2019",
        hbar_svg([
            ("Headquartered in capital city", 55, C1, "55%"),
            ("Non-capital — harder fundraising", 62, C6, "Higher challenge"),
            ("Non-capital — easier talent attraction", 38, C2, "Lower challenge"),
        ], aria="Capital vs non-capital city startup dynamics"),
        "Slush 2019 · European startup applications",
    ),
    "page-042.png": card(
        "Sudden remote work hurt more teams than it helped",
        "COVID-19 Startup Survey · April 2020",
        hbar_svg([
            ("Reported drop in well-being", 58, C6, "Majority"),
            ("Reported improvement in well-being", 28, C1, "Minority"),
            ("Reported drop in productivity", 54, C3, "Majority"),
            ("Reported productivity gain", 31, C2, "Minority"),
        ], aria="Remote work impact on startup teams"),
        "Slush COVID-19 Startup Survey · 97% switched to remote",
    ),
    "page-044.png": summary_card(
        "Narrative 2: Purpose-Driven Change",
        "A new generation reshapes European entrepreneurship",
        [
            "36.7% of Slush 2019 startups were purpose-driven (UN SDG core to product)",
            "Employees increasingly prioritize purpose alignment",
            "First-time founders drive the shift toward impact",
        ],
        "Slush 2019 · State of European Tech 2019",
    ),
    "page-045.png": stat_compare(
        "Purpose alignment is rising across the ecosystem",
        "State of European Tech 2019 · past 12 months",
        "Majority",
        "Respondents saw increase in employees emphasizing purpose",
        "36.7%",
        "Slush 2019 startups purpose-driven by SDG taxonomy",
        "State of European Tech 2019 · Slush 2019",
    ),
    "page-046.png": card(
        "Over a third of Slush 2019 startups are purpose-driven",
        "Companies pursuing UN SDGs as core product aspect",
        f'<div style="display:flex;align-items:center;gap:24px">{donut_svg(36.7, "Purpose-driven", C1, "36.7 percent purpose-driven startups")}</div>',
        "Slush 2019 · SDG + product keyword taxonomy",
    ),
    "page-047.png": card(
        "First-time founders lead the purpose shift",
        "Purpose-driven share by founder experience · Europe",
        hbar_svg([
            ("First-time founders", 72, C1, "Higher share"),
            ("Repeat founders", 48, CG, "Lower share"),
            ("Younger ventures (2017–2019)", 68, C2, "Higher share"),
        ], aria="Purpose-driven startups by founder experience"),
        "State of European Tech 2019 · purpose-driven taxonomy",
    ),
    "page-048.png": card(
        "Investments in purpose-driven companies more than doubled",
        "Year-over-year change · Europe · 2019",
        hbar_svg([
            ("Purpose-driven companies", 100, C1, ">2× YoY"),
            ("Other companies", 45, CG, "Baseline growth"),
        ], aria="Purpose-driven investment growth"),
        "State of European Tech 2019 · Dealroom",
    ),
    "page-049.png": card(
        "Purpose-driven startups raised more recently",
        "Share that raised latest round in 2019 · Slush 2019",
        hbar_svg([
            ("Purpose-driven startups", 62, C1, "62%"),
            ("Other startups", 53, CG, "53%"),
        ], aria="Recent fundraising by purpose alignment"),
        "Slush 2019 startup data",
    ),
    "page-050.png": [  # two distinct charts share page-050
        card(
            "Top SDG themes by investor meeting demand",
            "Investor meeting requests at Slush 2019 · by SDG",
            hbar_svg([
                ("Gender equality", 88, C1, "Top theme"),
                ("Affordable & clean energy", 82, C2, "High"),
                ("Decent work", 76, C3, "High"),
                ("Climate action", 71, C4, "High"),
                ("No poverty / Zero hunger", 58, C5, "Moderate"),
            ], aria="Investor meeting requests by SDG theme"),
            "Slush 2019 matchmaking data",
        ),
        card(
            "Angels and corporates lead on SDG investing",
            "Self-reported SDG investment commitment · Slush 2019",
            hbar_svg([
                ("Angel investors", 68, C1, "Highest"),
                ("Corporate investors", 58, C2, "High"),
                ("VC firms", 42, CG, "Lower"),
            ], aria="SDG investment commitment by investor type"),
            "Slush 2019 · investor application data",
        ),
    ],
    "page-051.png": [
        card(
            "Corporates allocate more to purpose-driven companies than VCs",
            "European investment allocation trend · SoET 2019",
            hbar_svg([
                ("Corporate investors (purpose-driven share)", 72, C1, "Growing faster"),
                ("Traditional VCs (purpose-driven share)", 38, CG, "Slower shift"),
            ], aria="Corporate vs VC purpose-driven allocation"),
            "State of European Tech 2019",
        ),
        card(
            "LP SDG commitment decreases for later-stage funds",
            "Limited partners at Slush 2019 · by stage focus",
            hbar_svg([
                ("Early-stage focused LPs", 52, C1, "Higher commitment"),
                ("Growth-stage focused LPs", 34, C2, "Moderate"),
                ("Late-stage focused LPs", 22, CG, "Lower commitment"),
            ], aria="LP SDG commitment by stage focus"),
            "Slush 2019 · LP survey data",
        ),
    ],
    "page-052.png": card(
        "SDG-committed VCs struggle more to raise new funds",
        "VC firms raising a new fund at Slush 2019",
        hbar_svg([
            ("SDG-committed · fundraising a priority", 78, C6, "55% more likely"),
            ("Not SDG-committed · fundraising a priority", 50, CG, "Baseline"),
        ], aria="Fundraising priority for SDG-committed VCs"),
        "Slush 2019 · VC firm applications",
    ),
    "page-054.png": card(
        "Younger purpose-driven startups generate more revenue",
        "Revenue comparison by founding cohort · Slush 2019",
        hbar_svg([
            ("Purpose-driven · founded 2017–2019", 72, C1, "Higher revenue"),
            ("Non-purpose · founded 2017–2019", 48, CG, "Lower revenue"),
            ("Purpose-driven · founded ≤2016", 44, C3, "Reversed"),
            ("Non-purpose · founded ≤2016", 52, C2, "Higher revenue"),
        ], aria="Revenue by purpose alignment and founding year"),
        "Slush 2019 cohort data",
    ),
    "page-055.png": [
        card(
            "Holistic SDG commitment correlates with higher revenue",
            "SDG claim + product keyword vs claim only · Slush 2019",
            hbar_svg([
                ("SDG claim + product keyword", 78, C1, "Highest revenue"),
                ("SDG claim only", 42, C3, "Lower revenue"),
                ("Neither", 50, CG, "Baseline"),
            ], aria="Revenue by SDG commitment holism"),
            "Slush 2019 · purpose-driven taxonomy",
        ),
        card(
            "Purpose advantage holds when controlling for headcount",
            "Revenue at 12 months before application · Slush 2019",
            hbar_svg([
                ("Purpose-driven (matched employees)", 68, C1, "Higher"),
                ("Non-purpose (matched employees)", 52, CG, "Lower"),
            ], aria="Revenue comparison controlling for employee count"),
            "Slush 2019 · employee count controlled",
        ),
    ],
    "page-061.png": card(
        "Unicorn valuations outpace revenue at the milestone",
        "Revenue in billion-dollar valuation year · European unicorns",
        hbar_svg([
            ("Founded 2008–2012 cohort", 55, C2, "Higher revenue at minting"),
            ("Founded 2014–2015 cohort", 28, C6, "Lower revenue at minting"),
        ], aria="Unicorn milestone revenue by founding cohort"),
        "Slush unicorn analysis · 60 European unicorns",
    ),
    "page-062.png": [
        card(
            "Recent unicorns grow revenue faster at minting",
            "Average compound revenue growth · at unicorn milestone",
            hbar_svg([
                ("Founded 2008–2012", 48, C2, "Below 2×"),
                ("Founded 2014–2015", 100, C1, "~4× YoY"),
            ], aria="Revenue growth rate at unicorn milestone"),
            "Slush unicorn analysis · January 2020",
        ),
        card(
            "Equity raised before unicorn round has roughly doubled",
            "Funding prior to billion-dollar valuation · by cohort",
            hbar_svg([
                ("Earlier cohorts", 50, CG, "Baseline"),
                ("Recent cohorts", 100, C1, "~2×"),
            ], aria="Pre-unicorn equity funding by cohort"),
            "Slush unicorn analysis · venture-backed companies",
        ),
    ],
    "page-064.png": card(
        "Few unicorns are profitable at reasonable valuations",
        "European unicorns · P/S ratio vs profitability",
        """<div class="stat-grid" style="margin-top:0">
        <div class="stat-box"><div class="stat-number">8</div><div class="stat-label">companies profitable at P/S below 10</div></div>
        <div class="stat-box"><div class="stat-number">60</div><div class="stat-label">European unicorns analysed since 2008</div></div>
        </div>
        <p style="margin-top:16px;font-size:13px;color:var(--fg-muted)">Most venture-backed unicorns trade at high P/S ratios without profitability. Gaming outliers Mojang and Outfit7 reached profitability without significant external funding.</p>""",
        "Slush unicorn analysis · Dealroom + public disclosures",
    ),
    "page-066.png": card(
        "European seed funding has stagnated since 2016",
        "Seed rounds and capital · Europe · 2014–2019",
        hbar_svg([
            ("Seed rounds 2016 (peak)", 100, C2, "Peak"),
            ("Seed rounds 2019", 70, C6, "−30%"),
            ("Total seed capital 2019", 55, C3, "Stagnated"),
        ], aria="European seed funding 2014 to 2019"),
        "Dealroom · European seed stage",
    ),
    "page-067.png": [
        card(
            "2019: founders found fundraising harder for the first time",
            "State of European Tech · year-over-year sentiment",
            hbar_svg([
                ("Found it harder to raise (2019)", 58, C6, "First time in survey history"),
                ("Found it easier (prior years avg.)", 62, C1, "Previously easier"),
            ], aria="Founder sentiment on fundraising ease"),
            "State of European Tech 2019 · pre-COVID survey",
        ),
        card(
            "Investors expect 20%+ early-stage valuation cuts in 2020",
            "COVID-19 impact estimates · investor respondents",
            hbar_svg([
                ("Expect 20%+ valuation reduction", 72, C6, "Majority"),
                ("Expect smaller or no reduction", 28, CG, "Minority"),
            ], aria="Expected valuation cuts due to COVID-19"),
            "Slush COVID-19 report · investor survey",
        ),
    ],
    "page-069.png": summary_card(
        "Narrative 3: Revolutionary Innovation",
        "Europe must unlock deeptech's full potential",
        [
            "30% of Slush 2019 startups were deeptech by taxonomy",
            "Past unicorns skew toward mobile, software, and fintech — not frontier science",
            "Collaboration across startups, universities, corporates, and government is essential",
        ],
        "Slush 2019 · BCG / Hello Tomorrow deeptech definition",
    ),
    "page-070.png": card(
        "Deeptech is one-third of Slush startups; unicorns skew digital",
        "Slush 2019 deeptech share · unicorn industries since 2008",
        hbar_svg([
            ("Deeptech at Slush 2019", 30, C1, "30%"),
            ("Mobile & software unicorns", 68, C2, "Dominant industries"),
            ("Fintech unicorns", 52, C3, "Common"),
            ("Healthcare unicorns", 38, C4, "Less common"),
        ], aria="Deeptech share and unicorn industry breakdown"),
        "Slush 2019 · 60 European unicorns analysed",
    ),
    "page-072.png": card(
        "Deeptech seed rounds are in steep decline",
        "Seed-stage deeptech funding · Europe · 2015–2019",
        hbar_svg([
            ("Total deeptech investment 2019", 100, C1, "$8.4B · 24% of tech"),
            ("Seed round count trend", 35, C6, "Steep decline"),
            ("Seed capital invested", 48, C3, "Stagnated"),
        ], aria="Deeptech seed funding trends"),
        "Dealroom · excludes Israel · as of May 2020",
    ),
    "page-074.png": [
        card(
            "Deeptech startups reach scale phase more slowly",
            "Growth & Scale phase · same average age 2.6 years · Slush 2019",
            hbar_svg([
                ("Other startups in Growth & Scale", 44, C2, "44%"),
                ("Deeptech in Growth & Scale", 27, C1, "27%"),
            ], aria="Growth phase share deeptech vs others"),
            "Slush 2019 startup applications",
        ),
        card(
            "Hardware revenue overtakes software after five years",
            "Revenue trajectory · Slush 2019 cohort",
            """<svg viewBox="0 0 480 140" role="img" aria-label="Hardware vs software revenue over time" xmlns="http://www.w3.org/2000/svg">
        <line x1="50" y1="110" x2="430" y2="110" stroke="rgba(255,255,255,0.07)"/>
        <polyline points="50,95 130,88 210,72 290,55 370,38 430,28" fill="none" stroke="#35cd5a" stroke-width="2.5"/>
        <polyline points="50,100 130,82 210,58 290,42 370,35 430,32" fill="none" stroke="#6b8cff" stroke-width="2.5"/>
        <text x="50" y="125" fill="#b0b0bc" font-size="10" font-family="Inter,sans-serif">Year 0</text>
        <text x="430" y="125" fill="#b0b0bc" font-size="10" text-anchor="end" font-family="Inter,sans-serif">Year 5+</text>
        <text x="430" y="22" fill="#35cd5a" font-size="10" text-anchor="end" font-family="Inter,sans-serif">Hardware</text>
        <text x="430" y="48" fill="#6b8cff" font-size="10" text-anchor="end" font-family="Inter,sans-serif">Software</text>
      </svg>
      <div class="chart-legend">
        <span class="chart-legend-item"><span class="chart-legend-swatch" style="background:#35cd5a"></span>Hardware (slower start, overtakes at 5y)</span>
        <span class="chart-legend-item"><span class="chart-legend-swatch" style="background:#6b8cff"></span>Software</span>
      </div>""",
            "Slush 2019 · hardware vs software startups",
        ),
    ],
    "page-075.png": card(
        "Deeptech startups are far more likely to hold patents",
        "Patent ownership · Slush 2019",
        hbar_svg([
            ("Deeptech startups", 54, C1, "54%"),
            ("Other startups", 19, CG, "19%"),
        ], aria="Patent ownership deeptech vs other"),
        "Slush 2019 startup application data",
    ),
    "page-076.png": card(
        "Deeptech punches above its weight in grant funding",
        "Share of companies, funding, and rounds · Europe since 2018",
        hbar_svg([
            ("Share of under-3-year companies", 17, C3, "17%"),
            ("Share of grant funding", 25, C1, "25%"),
            ("Share of grant rounds", 28, C2, "28%"),
        ], aria="Deeptech grant funding share"),
        "Dealroom · European grant funding",
    ),
    "page-078.png": card(
        "CVCs participate more in deeptech seed rounds",
        "CVC participation in seed rounds · 2019",
        hbar_svg([
            ("Deeptech seed rounds", 25, C1, "25%"),
            ("Other seed rounds", 17, CG, "17%"),
        ], aria="CVC participation in seed rounds"),
        "Dealroom · 2019 European seed rounds",
    ),
    "page-081.png": card(
        "Hardware startups seek co-development early, market access later",
        "What startups want from corporates · by stage · Slush 2019",
        hbar_svg([
            ("Early: funding & co-development", 82, C1, "Priority"),
            ("Early: market access", 35, CG, "Lower priority"),
            ("Scale: market access", 78, C2, "Priority"),
            ("Scale: co-development", 42, C3, "Lower priority"),
        ], aria="Corporate collaboration needs by stage"),
        "Slush 2019 · corporate engagement applications",
    ),
    "page-086.png": [
        card(
            "Researchers cite lack of funding as top barrier to founding",
            "Reservations about founding or joining a startup · SoET 2019",
            hbar_svg([
                ("Lack of funding", 78, C6, "Primary barrier"),
                ("Risk aversion", 52, C3, "Significant"),
                ("Academic career path", 45, C2, "Significant"),
                ("Commercialization support", 38, CG, "Moderate"),
            ], aria="Researcher reservations about startups"),
            "State of European Tech 2019 · researcher respondents",
        ),
        card(
            "Deeptech investment correlates with researcher density",
            "European countries · researcher/developer density vs deeptech volume",
            """<p style="font-size:13px;color:var(--fg-muted);line-height:1.6">Countries with higher densities of researchers and developers attract disproportionately more deeptech investment. Switzerland, UK, and Nordics lead on both metrics — spinout activity remains minimal elsewhere in Europe.</p>
        <div class="stat-grid" style="margin-top:12px">
        <div class="stat-box"><div class="stat-number">ETH Zurich</div><div class="stat-label">Most consistent spinout university globally · 20+ companies/year since 2007</div></div>
        </div>""",
            "State of European Tech 2019 · Global University Venturing",
        ),
    ],
    "page-089.png": card(
        "Disinformation, AI, and data privacy top regulatory priorities",
        "Areas needing increased regulatory attention · SoET 2019",
        hbar_svg([
            ("Disinformation", 88, C6, "Top priority"),
            ("Artificial intelligence", 84, C1, "Top priority"),
            ("Data privacy", 79, C2, "Top priority"),
            ("Biotech / gene editing", 58, C3, "Moderate"),
            ("Autonomous systems", 52, C4, "Moderate"),
        ], aria="Regulatory priority areas"),
        "State of European Tech 2019 survey",
    ),
}
