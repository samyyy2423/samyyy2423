"""Generates the SVGs used by the profile README (python tools/build_assets.py)."""
from pathlib import Path
from textwrap import wrap
from html import escape

OUT = Path(__file__).resolve().parent.parent / "assets"
SANS = "'Segoe UI', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'Cascadia Code', Consolas, Menlo, monospace"

INK = "#e8ecf8"
MUTED = "#98a3c2"
DIM = "#5d6788"
TEAL = "#2dd4bf"
VIOLET = "#a78bfa"
AMBER = "#fbbf24"
ROSE = "#fb7185"
GREEN = "#4ade80"
TERM_BG = "#0a0e1a"


def e(s):
    return escape(s, quote=True)


def backdrop(w, h, rx, glow_a=TEAL, glow_b=VIOLET, uid="b"):
    return f"""
  <defs>
    <linearGradient id="{uid}bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#0b1020"/><stop offset="1" stop-color="#151a38"/>
    </linearGradient>
    <radialGradient id="{uid}ga"><stop offset="0" stop-color="{glow_a}" stop-opacity=".22"/><stop offset="1" stop-color="{glow_a}" stop-opacity="0"/></radialGradient>
    <radialGradient id="{uid}gb"><stop offset="0" stop-color="{glow_b}" stop-opacity=".20"/><stop offset="1" stop-color="{glow_b}" stop-opacity="0"/></radialGradient>
    <pattern id="{uid}grid" width="28" height="28" patternUnits="userSpaceOnUse">
      <path d="M28 0H0V28" fill="none" stroke="#fff" stroke-opacity=".035"/>
    </pattern>
    <clipPath id="{uid}clip"><rect width="{w}" height="{h}" rx="{rx}"/></clipPath>
  </defs>
  <g clip-path="url(#{uid}clip)">
    <rect width="{w}" height="{h}" fill="url(#{uid}bg)"/>
    <rect width="{w}" height="{h}" fill="url(#{uid}grid)"/>
    <circle cx="{w * 0.12:.0f}" cy="0" r="{max(w, h) * 0.32:.0f}" fill="url(#{uid}ga)"/>
    <circle cx="{w * 0.9:.0f}" cy="{h}" r="{max(w, h) * 0.34:.0f}" fill="url(#{uid}gb)"/>
  </g>
  <rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="{rx}" fill="none" stroke="#fff" stroke-opacity=".09"/>"""


def pill(x, y, text, color, size=13, h=28):
    w = len(text) * size * 0.62 + 26
    return (w, f'<rect x="{x}" y="{y}" width="{w:.0f}" height="{h}" rx="{h / 2}" fill="{color}" fill-opacity=".1" '
               f'stroke="{color}" stroke-opacity=".45"/>'
               f'<text x="{x + w / 2:.0f}" y="{y + h / 2 + size * 0.36:.1f}" text-anchor="middle" font-family="{MONO}" '
               f'font-size="{size}" fill="{color}">{e(text)}</text>')


def pills(x, y, items, gap=10, **kw):
    out = []
    for text, color in items:
        w, svg = pill(x, y, text, color, **kw)
        out.append(svg)
        x += w + gap
    return "".join(out)


# ---------------------------------------------------------------- banner
def banner():
    W, H, T = 1200, 340, 12.0
    tx, ty, tw, th = 650, 46, 500, 252
    lx, cw = tx + 24, 14.5 * 0.6
    lines = [  # (kind, text, color, start_s, end_s)
        ("cmd", "harbor run -p task/ --agent oracle", None, 0.4, 1.7),
        ("out", "  ✓ reward 1.0 · 12/12 tests pass", GREEN, 2.1, None),
        ("cmd", "harbor run -p task/ --agent nop", None, 2.9, 4.0),
        ("out", "  ✗ reward 0.0 · verifier holds", ROSE, 4.4, None),
        ("cmd", "splitpoint align --pair 42", None, 5.2, 6.1),
        ("out", "  ↳ runs split at step 14", AMBER, 6.5, None),
        ("cursor", "", None, 7.0, None),
    ]
    pct = lambda s: f"{s / T * 100:.2f}%"
    css, body = [], []
    y = ty + 76
    for i, (kind, text, color, s, end) in enumerate(lines):
        if kind == "cmd":
            n = len(text) + 2
            css.append(f"@keyframes c{i}{{0%,{pct(s)}{{transform:translateX(0);animation-timing-function:steps({n},end)}}"
                       f"{pct(end)}{{transform:translateX({n * cw:.1f}px)}}{pct(end + 0.05)},100%{{transform:translateX({tw}px)}}}}"
                       f".c{i}{{transform:translateX({tw}px);animation:c{i} {T}s linear infinite}}")
            body.append(f'<text x="{lx}" y="{y}" font-family="{MONO}" font-size="14.5" fill="{INK}">'
                        f'<tspan fill="{TEAL}">$</tspan> {e(text)}</text>'
                        f'<rect class="c{i}" x="{lx - 2}" y="{y - 16}" width="{tw - 24}" height="22" fill="{TERM_BG}"/>')
        else:
            css.append(f"@keyframes o{i}{{0%,{pct(s)}{{opacity:0}}{pct(s + 0.12)},100%{{opacity:1}}}}"
                       f".o{i}{{animation:o{i} {T}s linear infinite}}")
            if kind == "out":
                body.append(f'<text class="o{i}" x="{lx}" y="{y}" font-family="{MONO}" font-size="14.5" '
                            f'fill="{color}">{e(text)}</text>')
            else:
                body.append(f'<g class="o{i}"><text x="{lx}" y="{y}" font-family="{MONO}" font-size="14.5" '
                            f'fill="{TEAL}">$</text><rect class="blink" x="{lx + 16}" y="{y - 13}" width="9" '
                            f'height="17" fill="{INK}"/></g>')
        y += 25
    css.append(f"@keyframes run{{0%,{pct(T - 0.8)}{{opacity:1}}{pct(T - 0.4)},100%{{opacity:0}}}}"
               f".run{{animation:run {T}s linear infinite}}"
               "@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}}.blink{animation:blink 1s step-end infinite}"
               "@media (prefers-reduced-motion:reduce){*{animation:none!important}}")

    left = f"""
  <text x="64" y="104" font-family="{MONO}" font-size="16" letter-spacing="2" fill="{TEAL}">hello, I'm</text>
  <text x="62" y="166" font-family="{SANS}" font-size="62" font-weight="700" fill="{INK}">Samyak Pudke</text>
  <text x="64" y="210" font-family="{SANS}" font-size="28" font-weight="600" fill="url(#role)">AI evaluation engineer</text>
  <text x="64" y="244" font-family="{SANS}" font-size="22" fill="{MUTED}">&amp; full-stack developer</text>
  {pills(64, 270, [("agent benchmarks", TEAL), ("verifiers & graders", VIOLET), ("RL environments", AMBER)])}"""
    term = f"""
  <rect x="{tx}" y="{ty}" width="{tw}" height="{th}" rx="14" fill="{TERM_BG}" stroke="#fff" stroke-opacity=".1"/>
  <circle cx="{tx + 22}" cy="{ty + 20}" r="6" fill="#ff5f57"/><circle cx="{tx + 42}" cy="{ty + 20}" r="6" fill="#febc2e"/>
  <circle cx="{tx + 62}" cy="{ty + 20}" r="6" fill="#28c840"/>
  <text x="{tx + tw / 2}" y="{ty + 25}" text-anchor="middle" font-family="{MONO}" font-size="12.5" fill="{DIM}">~/evals</text>
  <path d="M{tx} {ty + 40}H{tx + tw}" stroke="#fff" stroke-opacity=".07"/>
  <clipPath id="tclip"><rect x="{tx + 1}" y="{ty + 41}" width="{tw - 2}" height="{th - 42}"/></clipPath>
  <g clip-path="url(#tclip)"><g class="run">{''.join(body)}</g></g>"""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Samyak Pudke, AI evaluation engineer and full-stack developer">
  <style>{''.join(css)}</style>{backdrop(W, H, 24)}
  <defs><linearGradient id="role" x1="0" x2="1"><stop offset="0" stop-color="{TEAL}"/><stop offset="1" stop-color="{VIOLET}"/></linearGradient></defs>{left}{term}
</svg>
"""


# ---------------------------------------------------------------- link buttons
ICONS = {
    "globe": lambda c: f'<circle cx="0" cy="0" r="8.5" fill="none" stroke="{c}" stroke-width="1.8"/>'
                       f'<ellipse cx="0" cy="0" rx="3.8" ry="8.5" fill="none" stroke="{c}" stroke-width="1.6"/>'
                       f'<path d="M-8.5 0H8.5" stroke="{c}" stroke-width="1.6"/>',
    "in": lambda c: f'<rect x="-9" y="-9" width="18" height="18" rx="3.5" fill="{c}"/>'
                    f'<text x="0" y="5" text-anchor="middle" font-family="{SANS}" font-size="13" font-weight="700" fill="#0b1020">in</text>',
    "mail": lambda c: f'<rect x="-9.5" y="-7" width="19" height="14" rx="2.5" fill="none" stroke="{c}" stroke-width="1.8"/>'
                      f'<path d="M-9 -6L0 1L9 -6" fill="none" stroke="{c}" stroke-width="1.8" stroke-linejoin="round"/>',
    "dot": lambda c: f'<circle cx="0" cy="0" r="5" fill="{c}"><animate attributeName="opacity" values="1;.35;1" dur="2s" repeatCount="indefinite"/></circle>',
}


def button(label, icon, color, uid):
    w, h = int(len(label) * 8.6 + 64), 44
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{e(label)}">
  <rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="12" fill="#0f1428" stroke="{color}" stroke-opacity=".5"/>
  <g transform="translate(24 22)">{ICONS[icon](color)}</g>
  <text x="44" y="27.5" font-family="{SANS}" font-size="15" font-weight="600" fill="{INK}">{e(label)}</text>
</svg>
"""


# ---------------------------------------------------------------- what I do
def focus():
    W, H = 1200, 196
    tiles = [
        (TEAL, "Agent benchmarks", ["Long-horizon tasks for coding agents,", "calibrated across model families"]),
        (VIOLET, "Verifiers & graders", ["Dockerised test harnesses that grade", "the outcome, not the keystrokes"]),
        (AMBER, "Full-stack web", ["React / Next.js front ends, Node and", "Python back ends, 3D on the web"]),
    ]
    out, x, tw = [], 0, (W - 2 * 24) / 3
    glyphs = [
        lambda c: f'<path d="M-9 8V-2M-3 8V-8M3 8V1M9 8V-5" stroke="{c}" stroke-width="3" stroke-linecap="round"/>',
        lambda c: f'<path d="M-9 0L-3 6L9 -7" fill="none" stroke="{c}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>',
        lambda c: f'<path d="M-4 -7L-10 0L-4 7M4 -7L10 0L4 7" fill="none" stroke="{c}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>',
    ]
    for i, (color, title, text) in enumerate(tiles):
        out.append(f"""
  <g transform="translate({x:.0f} 0)">
    <rect x=".5" y=".5" width="{tw - 1:.0f}" height="{H - 1}" rx="18" fill="#0f1428" stroke="#fff" stroke-opacity=".08"/>
    <rect x="0" y="0" width="{tw:.0f}" height="4" rx="2" fill="{color}" fill-opacity=".85"/>
    <rect x="28" y="30" width="44" height="44" rx="12" fill="{color}" fill-opacity=".12" stroke="{color}" stroke-opacity=".4"/>
    <g transform="translate(50 52)">{glyphs[i](color)}</g>
    <text x="28" y="112" font-family="{SANS}" font-size="25" font-weight="700" fill="{INK}">{e(title)}</text>
    <text font-family="{SANS}" font-size="17.5" fill="{MUTED}"><tspan x="28" y="144">{e(text[0])}</tspan><tspan x="28" y="169">{e(text[1])}</tspan></text>
  </g>""")
        x += tw + 24
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="What I do: agent benchmarks, verifiers and graders, full-stack web">{''.join(out)}
</svg>
"""


# ---------------------------------------------------------------- flagship card
def flagship():
    W, H = 1200, 350
    desc = wrap("Where did the failing agent run go wrong? Splitpoint lines up a passing and a failing "
                "SWE-agent run on the same task, finds the step where they split, and has an LLM judge "
                "explain why, scored against blind human labels.", 50)
    desc_svg = "".join(f'<tspan x="48" y="{150 + i * 28}">{e(t)}</tspan>' for i, t in enumerate(desc))
    rows = [("view", "issue.md", "view", "issue.md"), ("run", "grep -rn crop", "run", "grep -rn crop"),
            ("view", "src/crop.py", "view", "src/crop.py"), ("test", "test_crop.py", "test", "test_crop.py"),
            ("edit", "src/crop.py", "edit", "utils/io.py"), ("test", "3/3 pass", "test", "1/3 pass"),
            ("submit", "patch", "submit", "patch")]
    split = 4
    ax, bx, cwid, ry0, rh = 660, 936, 220, 76, 36
    diagram = [f'<text x="{ax}" y="54" font-family="{MONO}" font-size="14" fill="{GREEN}">✓ passing run</text>',
               f'<text x="{bx}" y="54" font-family="{MONO}" font-size="14" fill="{ROSE}">✗ failing run</text>']
    for i, (a1, a2, b1, b2) in enumerate(rows):
        y = ry0 + i * rh
        after = i > split
        ca = TEAL if i == split else ("#2a3150" if not after else "#1f3a3a")
        cb = ROSE if i == split else ("#2a3150" if not after else "#3a2233")
        for x, verb, arg, c, fg in ((ax, a1, a2, ca, INK if i <= split else "#9fd8cf"),
                                    (bx, b1, b2, cb, INK if i <= split else "#e7a3b1")):
            hi = i == split
            diagram.append(f'<rect x="{x}" y="{y}" width="{cwid}" height="28" rx="7" fill="{c}" '
                           f'fill-opacity="{".18" if hi else ".55"}" stroke="{c}" stroke-opacity="{".9" if hi else "0"}"/>'
                           f'<text x="{x + 12}" y="{y + 19}" font-family="{MONO}" font-size="14" fill="{fg}">'
                           f'<tspan fill="{MUTED}">{verb}</tspan> {e(arg)}</text>')
        if i < split:
            diagram.append(f'<path d="M{ax + cwid} {y + 14}H{bx}" stroke="{DIM}" stroke-dasharray="2 4"/>')
    sy = ry0 + split * rh + 14
    diagram.append(f'<g class="pulse"><path d="M{ax - 16} {sy}H{ax - 4}M{bx + cwid + 4} {sy}H{bx + cwid + 16}" stroke="{AMBER}" stroke-width="2.5"/>'
                   f'<text x="{(ax + cwid + bx) / 2}" y="{sy + 4.5}" text-anchor="middle" font-family="{MONO}" '
                   f'font-size="13" font-weight="700" fill="{AMBER}">split</text></g>')
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Splitpoint: finds where a failing coding-agent run split from a passing one">
  <style>@keyframes p{{0%,100%{{opacity:1}}50%{{opacity:.35}}}}.pulse{{animation:p 1.8s ease-in-out infinite}}</style>{backdrop(W, H, 22, glow_a=AMBER, glow_b=TEAL, uid="f")}
  <text x="48" y="54" font-family="{MONO}" font-size="13" letter-spacing="1.5" fill="{AMBER}">★ FEATURED · samyyy2423/splitpoint</text>
  <text x="46" y="104" font-family="{SANS}" font-size="44" font-weight="700" fill="{INK}">Splitpoint</text>
  <text font-family="{SANS}" font-size="19" fill="{MUTED}">{desc_svg}</text>
  {pills(48, 288, [("Python", TEAL), ("DuckDB", TEAL), ("Needleman–Wunsch", VIOLET), ("LLM judge", AMBER), ("Next.js", VIOLET)], size=13, h=28)}
  {''.join(diagram)}
</svg>
"""


# ---------------------------------------------------------------- project cards
def card(repo, title, desc, lang, lang_color, chips, accent):
    W, H = 590, 250
    lines = wrap(desc, 52)[:3]
    d = "".join(f'<tspan x="30" y="{118 + i * 27}">{e(t)}</tspan>' for i, t in enumerate(lines))
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{e(title)}: {e(desc)}">{backdrop(W, H, 18, glow_a=accent, glow_b=accent, uid="c")}
  <text x="30" y="42" font-family="{MONO}" font-size="14" fill="{DIM}">samyyy2423/<tspan fill="{accent}">{e(repo)}</tspan></text>
  <text x="29" y="78" font-family="{SANS}" font-size="30" font-weight="700" fill="{INK}">{e(title)}</text>
  <text font-family="{SANS}" font-size="18.5" fill="{MUTED}">{d}</text>
  <circle cx="37" cy="{H - 36}" r="7" fill="{lang_color}"/>
  <text x="51" y="{H - 30.5}" font-family="{SANS}" font-size="16" fill="{MUTED}">{e(lang)}</text>
  {pills(30 + len(lang) * 9 + 48, H - 52, [(c, accent) for c in chips], gap=8, size=14, h=30)}
</svg>
"""


CARDS = {
    "card-topcoder": ("topcoder", "Creative Asset Automation",
                      "TopCoder challenge build: upload, edit and batch-generate platform-ready marketing "
                      "assets with pluggable AI image providers.", "JavaScript", "#f1e05a", ["React", "Flask", "Fabric.js"], VIOLET),
    "card-dependency-checker": ("dependency_checker", "Dependency Checker",
                                "TypeScript CLI that finds outdated npm packages, runs npm audit, auto-fixes, and "
                                "writes JSON + Markdown reports. Monorepo-aware.", "TypeScript", "#3178c6", ["Node.js", "npm audit", "CLI"], TEAL),
    "card-webserver": ("webserver_with_C", "HTTP Server in C",
                       "A web server from scratch: TCP sockets, request-line parsing, a binary-search-tree "
                       "router, HTML templates and static files.", "C", "#8a9bb0", ["sockets", "HTTP", "Make"], AMBER),
    "card-portfolio": ("portfolio", "Portfolio",
                       "My personal site: scroll-driven sections, a 3D planet hero and animated type. "
                       "Live at samyaksportfolio.vercel.app", "JavaScript", "#f1e05a", ["React", "three.js", "GSAP"], ROSE),
}


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    files = {
        "banner.svg": banner(),
        "focus.svg": focus(),
        "splitpoint.svg": flagship(),
        "btn-portfolio.svg": button("Portfolio", "globe", TEAL, "p"),
        "btn-linkedin.svg": button("LinkedIn", "in", "#4d9fff", "l"),
        "btn-email.svg": button("Email", "mail", VIOLET, "m"),
        "btn-open.svg": button("Open to remote contracts", "dot", GREEN, "o"),
    }
    files.update({f"{k}.svg": card(*v) for k, v in CARDS.items()})
    for name, svg in files.items():
        (OUT / name).write_text(svg, encoding="utf-8", newline="\n")
        print(name, len(svg))
