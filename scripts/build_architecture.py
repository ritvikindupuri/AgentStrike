#!/usr/bin/env python3
"""Build assets/architecture.svg and assets/architecture.png.

Flow, left to right, with the Cursor cloud agent as the central step:
You -> AgentStrike -> Cursor Cloud Agent --reads--> GitHub.
The cloud agent writes the report, which goes to AgentStrike, then to you.
A live-view branch drops from the cloud agent into the box browser.

Rendered with rsvg-convert (librsvg), the same idea as the other Grok Bot
repos: a real image in the README, not a Mermaid block.
"""
from __future__ import annotations

import math
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_SVG = ROOT / "assets" / "architecture.svg"
OUT_PNG = ROOT / "assets" / "architecture.png"

W, H = 1500, 620
RED = "#E11D48"
LINE = "#9AA0A6"
PANEL = "#F7F8F9"
BORDER = "#E4E6EA"
ACCENT_BOX = "#FFF4E8"
ACCENT_EDGE = "#F3D5B0"
ACCENT_TEXT = "#C2410C"
INK = "#1F2328"
MUTED = "#3A4150"

GITHUB_PATH = (
    "M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 "
    "0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 "
    "3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 "
    "1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 "
    "0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 "
    "1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 "
    "2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 "
    "2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"
)
# Official Cursor mark (Simple Icons "cursor").
CURSOR_PATH = (
    "M11.503.131 1.891 5.678a.84.84 0 0 0-.42.726v11.188c0 .3.162.575.42.724l9.609 5.55a1 1 0 0 0 "
    ".998 0l9.61-5.55a.84.84 0 0 0 .42-.724V6.404a.84.84 0 0 0-.42-.726L12.497.131a1.01 1.01 0 0 0-.996 0"
    "M2.657 6.338h18.55c.263 0 .43.287.297.515L12.23 22.918c-.062.107-.229.064-.229-.06V12.335a.59.59 "
    "0 0 0-.295-.51l-9.11-5.257c-.109-.063-.064-.23.061-.23"
)

YOU_X, BOT_X, CLOUD_X, GH_X = 200, 530, 880, 1320
MAIN_Y = 214
BROWSER_Y = 500
REPORT_Y = 500


def arrow_defs() -> str:
    return f'''<defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">
      <path d="M0 0 L10 5 L0 10 z" fill="{LINE}"/>
    </marker>
  </defs>'''


def style() -> str:
    return f'''<style>
    text {{ font-family: ui-sans-serif, Inter, system-ui, -apple-system, "Segoe UI", sans-serif; fill: {INK}; }}
    .title {{ font-size: 28px; font-weight: 700; }}
    .name {{ font-size: 16px; font-weight: 700; }}
    .cap {{ font-size: 14.5px; fill: {MUTED}; }}
    .note {{ font-size: 14.5px; fill: {MUTED}; font-weight: 600; }}
    .phase {{ font-size: 14.5px; fill: {MUTED}; font-weight: 600; }}
  </style>'''


def disk(x: float, y: float, r: float, stroke: str = BORDER) -> str:
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{PANEL}" stroke="{stroke}" stroke-width="1.5"/>'


def badge(x: float, y: float, n: str) -> str:
    return (
        f'<circle cx="{x}" cy="{y}" r="11" fill="{ACCENT_BOX}" stroke="{ACCENT_EDGE}"/>'
        f'<text x="{x}" y="{y + 4}" text-anchor="middle" font-size="12" font-weight="700" fill="{ACCENT_TEXT}">{n}</text>'
    )


def labels_above(x: float, y: float, r: float, name: str, cap: str) -> str:
    # Caption baseline sits clear of the circle.
    return (
        f'<text class="name" x="{x}" y="{y - r - 46}" text-anchor="middle">{name}</text>'
        f'<text class="cap" x="{x}" y="{y - r - 24}" text-anchor="middle">{cap}</text>'
    )


def labels_below(x: float, y: float, r: float, name: str, cap: str) -> str:
    return (
        f'<text class="name" x="{x}" y="{y + r + 28}" text-anchor="middle">{name}</text>'
        f'<text class="cap" x="{x}" y="{y + r + 48}" text-anchor="middle">{cap}</text>'
    )


def dashed_path(points: list[tuple[float, float]]) -> str:
    d = "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in points)
    return (
        f'<path d="{d}" fill="none" stroke="{LINE}" stroke-width="1.8" '
        f'stroke-dasharray="6 5" stroke-linejoin="round" marker-end="url(#arrow)"/>'
    )


def line(x1, y1, x2, y2, head: bool = True, dashed: bool = False) -> str:
    marker = ' marker-end="url(#arrow)"' if head else ""
    dash = ' stroke-dasharray="6 5"' if dashed else ""
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{LINE}" '
        f'stroke-width="1.8"{dash}{marker}/>'
    )


def person(x: float, y: float) -> str:
    return f'''<g transform="translate({x},{y + 2})" fill="#4B5563">
    <circle cx="0" cy="-9" r="8"/>
    <path d="M-15 16c1-9 6.8-13 15-13s14 4 15 13"/>
  </g>'''


def bot_icon(x: float, y: float, size: float = 46) -> str:
    """Official mark from assets/icon.svg, scaled to fit the node circle."""
    raw = (ROOT / "assets" / "icon.svg").read_text()
    raw = re.sub(r"<svg[^>]*>", "", raw, count=1)
    raw = raw.replace("</svg>", "")
    scale = size / 64
    return (
        f'<g transform="translate({x},{y})">'
        f'<g transform="translate({-size / 2:.2f},{-size / 2:.2f}) scale({scale:.4f})">{raw}</g>'
        f"</g>"
    )


def brand(x: float, y: float, path: str, size: float) -> str:
    return (
        f'<g transform="translate({x},{y})">'
        f'<g transform="translate({-size / 2:.2f},{-size / 2:.2f}) scale({size / 24:.4f})" fill="#181717">'
        f'<path d="{path}"/></g></g>'
    )


def browser(x: float, y: float) -> str:
    return f'''<g transform="translate({x},{y})">
    <rect x="-20" y="-15" width="40" height="30" rx="4" fill="#FFFFFF" stroke="#181717" stroke-width="1.6"/>
    <path d="M-20-8h40" stroke="#181717" stroke-width="1.4"/>
    <circle cx="-13" cy="-11.5" r="1.6" fill="{RED}"/>
    <circle cx="-8" cy="-11.5" r="1.6" fill="#D1D5DB"/>
    <circle cx="-3" cy="-11.5" r="1.6" fill="#D1D5DB"/>
    <rect x="-13" y="-3" width="18" height="2.2" rx="1" fill="#D1D5DB"/>
    <rect x="-13" y="2" width="24" height="2.2" rx="1" fill="#E5E7EB"/>
    <rect x="-13" y="7" width="14" height="2.2" rx="1" fill="#E5E7EB"/>
  </g>'''


def report_icon(x: float, y: float) -> str:
    bars = [(-9, RED), (-3, "#F97316"), (3, "#EAB308"), (9, "#94A3B8")]
    rects = "".join(
        f'<rect x="-11" y="{yy}" width="22" height="3.4" rx="1" fill="{color}"/>'
        for yy, color in bars
    )
    return f'''<g transform="translate({x},{y})">
    <path fill="#FFFFFF" stroke="#181717" stroke-width="1.6" d="M-13-17h17l9 9v26h-26z"/>
    <path fill="none" stroke="#181717" stroke-width="1.4" d="M4-17v9h9"/>
    {rects}
  </g>'''


def build() -> str:
    cloud_r, node_r, report_r = 46, 36, 32
    # Below the dashed fix path, which runs under the read arrow.
    phase_y = MAIN_Y + cloud_r + 52
    deliver_y = MAIN_Y + node_r + 40
    # Leave the cloud circle at its lower-left edge, under the forward arrow.
    rim_x, rim_y = CLOUD_X - 4, MAIN_Y + 42
    # Far enough right that "Writes the findings" fits on the horizontal
    # run with a gap before this drop, and still left of the phase line.
    drop_x = CLOUD_X - 140
    ask_x = (YOU_X + node_r + BOT_X - node_r) / 2
    start_x = (BOT_X + node_r + CLOUD_X - cloud_r) / 2
    read_x = (CLOUD_X + cloud_r + GH_X - node_r) / 2
    # Leave the cloud circle low, run well under "Reads the code", then
    # angle up into the lower edge of the GitHub circle.
    leave = math.radians(58)
    fix_x1 = CLOUD_X + cloud_r * math.cos(leave) + 2
    fix_y1 = MAIN_Y + cloud_r * math.sin(leave) + 1
    low_y = MAIN_Y + 64
    fix_x_low = CLOUD_X + cloud_r + 16
    arrive = math.radians(112)
    fix_x2 = GH_X + node_r * math.cos(arrive) - 1
    fix_y2 = MAIN_Y + node_r * math.sin(arrive)
    bend_x = fix_x2 - 56
    fix_points = [
        (fix_x1, fix_y1),
        (fix_x_low, low_y),
        (bend_x, low_y),
        (fix_x2, fix_y2),
    ]
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="How AgentStrike works">',
        f'<rect width="{W}" height="{H}" fill="#FFFFFF"/>',
        arrow_defs(),
        style(),
        f'<text class="title" x="{W / 2}" y="46" text-anchor="middle">How AgentStrike works</text>',
        # You -> AgentStrike -> Cursor Cloud Agent.
        line(YOU_X + node_r + 8, MAIN_Y, BOT_X - node_r - 10, MAIN_Y),
        line(BOT_X + node_r + 8, MAIN_Y, CLOUD_X - cloud_r - 10, MAIN_Y),
        # Solid read-only arrow, then a dashed opt-in fix arrow below it.
        line(CLOUD_X + cloud_r + 8, MAIN_Y, GH_X - node_r - 10, MAIN_Y),
        dashed_path(fix_points),
        f'<text class="note" x="{ask_x}" y="{MAIN_Y - 16}" text-anchor="middle">Asks for a review</text>',
        f'<text class="note" x="{start_x}" y="{MAIN_Y - 16}" text-anchor="middle">Starts the run</text>',
        f'<text class="note" x="{read_x}" y="{MAIN_Y - 16}" text-anchor="middle">Reads the code</text>',
        f'<text class="note" x="{(fix_x_low + bend_x) / 2}" y="{low_y - 20}" text-anchor="middle">Opens a fix PR (only if you ask)</text>',
        # What the cloud agent checks, under the circle. Live view continues below that line.
        f'<text class="phase" x="{CLOUD_X}" y="{phase_y}" text-anchor="middle">Security checks: STRIDE + OWASP</text>',
        line(CLOUD_X, phase_y + 14, CLOUD_X, BROWSER_Y - node_r - 12),
        f'<text class="note" x="{CLOUD_X + 18}" y="{(phase_y + 14 + BROWSER_Y - node_r) / 2 + 4}">Shows the live run</text>',
        # Cloud agent writes the report, then AgentStrike sends it up and delivers it to you.
        line(rim_x, rim_y, drop_x, rim_y, head=False),
        line(drop_x, rim_y, drop_x, REPORT_Y, head=False),
        line(drop_x - 4, REPORT_Y, BOT_X + report_r + 14, REPORT_Y),
        line(BOT_X, REPORT_Y - report_r - 8, BOT_X, MAIN_Y + node_r + 8),
        # Centered on the horizontal run, clear of the report circle and the drop.
        f'<text class="note" x="{(BOT_X + report_r + 20 + drop_x - 18) / 2}" y="{REPORT_Y - 22}" text-anchor="middle">Writes the findings</text>',
        f'<text class="note" x="{BOT_X + 16}" y="{(REPORT_Y + MAIN_Y) / 2 - 20}">Sends the findings</text>',
        # AgentStrike delivers the report to you, below the forward arrow.
        line(BOT_X - 20, MAIN_Y + 30, BOT_X - 20, deliver_y, head=False),
        line(BOT_X - 20, deliver_y, YOU_X + 24, deliver_y, head=False),
        line(YOU_X + 24, deliver_y, YOU_X + 24, MAIN_Y + 27),
        f'<text class="note" x="{(YOU_X + BOT_X) / 2}" y="{deliver_y - 12}" text-anchor="middle">Delivers the report</text>',
    ]

    nodes = [
        (YOU_X, MAIN_Y, node_r, "1", "You", "Picks the target, reads the report", lambda x, y: person(x, y)),
        (BOT_X, MAIN_Y, node_r, "2", "AgentStrike", "Starts a run on one AI app", lambda x, y: bot_icon(x, y, 46)),
        (CLOUD_X, MAIN_Y, cloud_r, "3", "Cursor Cloud Agent", "Security review, read-only by default", lambda x, y: brand(x, y, CURSOR_PATH, 40)),
        (GH_X, MAIN_Y, node_r, "4", "GitHub", "Repository for the AI app", lambda x, y: brand(x, y, GITHUB_PATH, 34)),
    ]
    for x, y, r, n, name, cap, draw in nodes:
        parts.append(disk(x, y, r))
        parts.append(draw(x, y))
        parts.append(labels_above(x, y, r, name, cap))
        # Number sits just outside the upper-left rim, clear of the caption.
        parts.append(badge(x - r - 2, y - r + 16, n))

    parts.append(disk(CLOUD_X, BROWSER_Y, node_r))
    parts.append(browser(CLOUD_X, BROWSER_Y))
    parts.append(labels_below(CLOUD_X, BROWSER_Y, node_r, "Box browser", "Live view in the Computer tab"))
    parts.append(badge(CLOUD_X + node_r + 16, BROWSER_Y - node_r + 8, "5"))

    parts.append(disk(BOT_X, REPORT_Y, report_r))
    parts.append(report_icon(BOT_X, REPORT_Y))
    parts.append(labels_below(BOT_X, REPORT_Y, report_r, "Report", "Ranked findings and fixes"))
    parts.append(badge(BOT_X - report_r - 16, REPORT_Y - 4, "6"))

    parts.append("</svg>")
    return "\n".join(parts)


def render_png(svg_path: Path, png_path: Path) -> None:
    rsvg = shutil.which("rsvg-convert")
    if not rsvg:
        raise SystemExit("rsvg-convert is not installed")
    out = subprocess.run(
        [rsvg, "-w", str(W * 2), "-h", str(H * 2), str(svg_path), "-o", str(png_path)],
        capture_output=True,
        text=True,
    )
    if out.returncode != 0 or not png_path.exists():
        raise SystemExit(f"rsvg-convert failed: {out.stderr[-800:]}")


def main() -> int:
    OUT_SVG.parent.mkdir(parents=True, exist_ok=True)
    OUT_SVG.write_text(build())
    render_png(OUT_SVG, OUT_PNG)
    print(f"wrote {OUT_SVG} ({OUT_SVG.stat().st_size} bytes)")
    print(f"wrote {OUT_PNG} ({OUT_PNG.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
