#!/usr/bin/env python3
"""Fetch public GitHub contribution data and render Imad's animated profile SVGs."""
from __future__ import annotations

import datetime as dt
import html
import json
import os
import re
import sys
from pathlib import Path

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
CARDS = ROOT / "cards"
USER = os.environ.get("GH_PROFILE_USER", "JENNAH-IMAD")
PAPER, INK, MUTED, BLUE, RULE = "#f3f3f1", "#111111", "#6e6e73", "#2369b3", "#dcdcd7"
SERIF = "Georgia,serif"
SANS = "system-ui,-apple-system,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,monospace"
CSS = """
@keyframes rise{from{opacity:0;transform:translateY(15px)}to{opacity:1;transform:translateY(0)}}
@keyframes fade{from{opacity:0}to{opacity:1}}
@keyframes grow{from{transform:scaleY(0)}to{transform:scaleY(1)}}
@keyframes pulse{0%,100%{opacity:.4}50%{opacity:1}}
.rise{opacity:0;animation:rise .75s cubic-bezier(.2,.7,.2,1) both}.fade{opacity:0;animation:fade .8s ease-out both}
.bar{transform-box:fill-box;transform-origin:bottom;transform:scaleY(0);animation:grow .75s cubic-bezier(.2,.7,.2,1) both}
.pulse{animation:pulse 2.4s ease-in-out infinite}
@media(prefers-reduced-motion:reduce){.rise,.fade,.bar,.pulse{animation:none!important;opacity:1!important;transform:none!important}}
"""


def fetch_days() -> list[dict]:
    url = f"https://github.com/users/{USER}/contributions"
    res = requests.get(url, headers={"User-Agent": "profile-readme-cards/1.0"}, timeout=30)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")
    cells = soup.select("td.ContributionCalendar-day")
    if not cells:
        raise RuntimeError("GitHub contribution calendar was not found in the response")
    days = []
    for cell in cells:
        date = cell.get("data-date")
        if not date:
            continue
        tip = soup.find("tool-tip", attrs={"for": cell.get("id")}) if cell.get("id") else None
        label = tip.get_text(" ", strip=True) if tip else ""
        count_match = re.search(r"(\d+)\s+contributions?", label, re.I)
        count = int(count_match.group(1)) if count_match else 0
        days.append({"date": date, "count": count, "level": int(cell.get("data-level") or 0)})
    if not days:
        raise RuntimeError("GitHub returned a contribution table without dated cells")
    return sorted(days, key=lambda d: d["date"])[-371:]


def stats(days: list[dict]) -> dict:
    today = dt.date.today().isoformat()
    index = len(days) - 1 if days[-1]["date"] < today else len(days) - 2
    streak = 0
    while index >= 0 and days[index]["count"] > 0:
        streak += 1
        index -= 1
    monthly: dict[str, int] = {}
    for day in days:
        month = day["date"][:7]
        monthly[month] = monthly.get(month, 0) + day["count"]
    return {"total": sum(d["count"] for d in days), "active": sum(d["count"] > 0 for d in days),
            "streak": streak, "monthly": sorted(monthly.items())[-12:]}


def write(name: str, width: int, height: int, body: str, label: str) -> None:
    CARDS.mkdir(parents=True, exist_ok=True)
    content = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
               f'viewBox="0 0 {width} {height}" role="img" aria-label="{html.escape(label)}">'
               f'<title>{html.escape(label)}</title><style>{CSS}</style>{body}</svg>')
    (CARDS / name).write_text(content, encoding="utf-8")


def rect(x: float, y: float, w: float, h: float, fill: str, radius: int = 3, extra: str = "") -> str:
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{radius}" fill="{fill}" {extra}/>'


def render_hero() -> None:
    body = f'''<rect width="1000" height="250" rx="18" fill="#f7f4ed" stroke="{RULE}"/>
<path d="M42 38h44" stroke="{BLUE}" stroke-width="4" stroke-linecap="round"/>
<text class="fade" x="42" y="72" font-family="{MONO}" font-size="14" letter-spacing="2" fill="{BLUE}">FULL STACK ENGINEER � CASABLANCA, MOROCCO</text>
<text class="rise" x="40" y="153" style="animation-delay:.15s" font-family="{SERIF}" font-size="68" fill="{INK}">Imad Jennah</text>
<text class="rise" x="44" y="192" style="animation-delay:.3s" font-family="{SANS}" font-size="18" fill="#4e5865">Building production-ready software, from thoughtful interfaces to automated delivery.</text>
<text class="fade" x="44" y="226" style="animation-delay:.5s" font-family="{MONO}" font-size="13" fill="{BLUE}">REACT  /  SPRING BOOT  /  .NET  /  DOCKER  /  CI/CD</text>
<circle class="pulse" cx="930" cy="63" r="6" fill="{BLUE}"/><text x="868" y="176" font-family="{SERIF}" font-size="56" fill="{BLUE}" opacity=".82">IJ</text>'''
    write("hero.svg", 1000, 250, body, "Imad Jennah, Full Stack Engineer in Casablanca, Morocco")


def render_tiles() -> None:
    worlds = [
        ("build", "01 / BUILD", "Full stack apps", "From thoughtful UI to reliable APIs", "#2458ff", "#ffffff"),
        ("automate", "02 / AUTOMATE", "Ship with confidence", "Docker � GitHub Actions � CI/CD", "#ef3b2d", "#ffffff"),
        ("explore", "03 / EXPLORE", "Cloud + AI", "Curious by design, learning by building", "#f3c928", INK),
    ]
    for i, (file, kicker, title, subtitle, color, foreground) in enumerate(worlds):
        body = f'''<rect x="4" y="4" width="324" height="174" rx="14" fill="{color}"/>
<text class="fade" x="24" y="36" font-family="{MONO}" font-size="12" letter-spacing="1.5" fill="{foreground}">{kicker}</text>
<text class="rise" x="22" y="94" style="animation-delay:{i*.15:.2f}s" font-family="{SERIF}" font-size="29" fill="{foreground}">{title}</text>
<text class="fade" x="24" y="130" style="animation-delay:{i*.15+.2:.2f}s" font-family="{SANS}" font-size="13" fill="{foreground}">{subtitle}</text>
<text class="fade" x="287" y="38" font-family="{MONO}" font-size="16" fill="{foreground}">?</text>'''
        write(f"{file}.svg", 332, 182, body, f"{kicker}: {title}. {subtitle}")


def render_heatmap(days: list[dict]) -> None:
    width, height, cell, gap, left, top = 1000, 178, 12, 5, 42, 76
    first = dt.date.fromisoformat(days[0]["date"])
    leading = (first.weekday() + 1) % 7
    colors = ["#e6e5e1", "#c7d4ff", "#91aaff", "#5d82ff", BLUE]
    cells, months, seen = [], [], set()
    for index, item in enumerate(days):
        col, row = divmod(index + leading, 7)
        date = dt.date.fromisoformat(item["date"])
        if date.day <= 7 and (date.year, date.month) not in seen and row == 0:
            seen.add((date.year, date.month))
            months.append(f'<text x="{left+col*(cell+gap)}" y="62" font-family="{MONO}" font-size="10" fill="{MUTED}">{date.strftime("%b")}</text>')
        level = min(4, max(0, item["level"]))
        title = f'{item["date"]}: {item["count"]} contributions'
        cells.append(f'<g class="fade" style="animation-delay:{min(1.5,col*.015+row*.01):.2f}s">{rect(left+col*(cell+gap), top+row*(cell+gap), cell, cell, colors[level], 3)}<title>{title}</title></g>')
    body = f'''<rect width="{width}" height="{height}" rx="16" fill="{PAPER}"/>
<text class="rise" x="42" y="38" font-family="{SERIF}" font-size="27" fill="{INK}">A year of showing up, <tspan font-style="italic" fill="{BLUE}">in blue</tspan></text>
{''.join(months)}{''.join(cells)}
<text x="885" y="38" text-anchor="end" font-family="{MONO}" font-size="11" fill="{MUTED}">REFRESHED DAILY</text>'''
    write("heatmap.svg", width, height, body, "Animated GitHub contribution calendar, refreshed daily")


def render_activity(data: dict) -> None:
    width, height, base, chart_top = 1000, 310, 244, 125
    monthly = data["monthly"]
    max_value = max((value for _, value in monthly), default=1) or 1
    x0, step, barw = 48, 48, 30
    bars = []
    for i, (month, value) in enumerate(monthly):
        barh = max(3, round((base-chart_top)*value/max_value))
        x, y = x0+i*step, base-barh
        color = BLUE if value == max_value else "#292929"
        label = dt.date.fromisoformat(month+"-01").strftime("%b")
        bars.append(f'<rect class="bar" style="animation-delay:{.9+i*.06:.2f}s" x="{x}" y="{y}" width="{barw}" height="{barh}" rx="4" fill="{color}"><title>{label}: {value} contributions</title></rect>')
        bars.append(f'<text x="{x+barw/2}" y="{base+21}" text-anchor="middle" font-family="{MONO}" font-size="10" fill="{MUTED}">{label}</text>')
    body = f'''<rect width="{width}" height="{height}" rx="16" fill="{PAPER}"/>
<text class="rise" x="42" y="48" font-family="{SERIF}" font-size="32" fill="{INK}">{data["total"]:,} <tspan font-style="italic">contributions</tspan></text>
<text x="42" y="82" font-family="{MONO}" font-size="11" letter-spacing="1" fill="{MUTED}">MONTH BY MONTH</text>
{''.join(bars)}
<path d="M680 36v230" stroke="{RULE}"/>
<text x="718" y="108" font-family="{SERIF}" font-size="43" fill="{BLUE}">{data["streak"]}</text>
<text x="718" y="134" font-family="{SANS}" font-size="13" fill="{MUTED}">day current streak</text>
<text x="718" y="196" font-family="{SERIF}" font-size="36" fill="{INK}">{data["active"]}</text>
<text x="718" y="222" font-family="{SANS}" font-size="13" fill="{MUTED}">active days this year</text>'''
    write("activity.svg", width, height, body, f'{data["total"]:,} contributions, {data["streak"]} day streak')


def render_projects() -> None:
    projects = [
        ("meeting-room", "Meeting Room Booking System", "ASP.NET Core � React � PostgreSQL", "REST API � Auth � live availability"),
        ("cicd", "React CI/CD Pipeline", "Docker � GitHub Actions � React", "Automated tests � Containerization � Deploy"),
        ("linux-monitoring", "Linux Web Server + Monitoring", "Linux � Nginx � Bash", "Performance tracking � Security hardening"),
        ("equipment-manager", "IT Equipment Request Manager", "Spring Boot � React � SQL Server", "Request tracking � Analytics dashboard"),
    ]
    for i, (slug, title, stack, detail) in enumerate(projects):
        x = 18
        body = f'''<rect x="4" y="4" width="472" height="142" rx="14" fill="{PAPER}" stroke="{RULE}"/>
<rect x="{x}" y="25" width="5" height="5" rx="2" fill="{BLUE}"/>
<text class="rise" x="36" y="43" style="animation-delay:{i*.1:.2f}s" font-family="{SERIF}" font-size="23" fill="{INK}">{html.escape(title)}</text>
<text x="22" y="79" font-family="{MONO}" font-size="11" fill="{BLUE}">{html.escape(stack)}</text>
<text x="22" y="112" font-family="{SANS}" font-size="13" fill="{MUTED}">{html.escape(detail)}</text>
<text x="446" y="126" font-family="{MONO}" font-size="13" fill="{BLUE}">?</text>'''
        write(f"project-{slug}.svg", 480, 154, body, f"{title}. {stack}. {detail}")


def render_preview() -> None:
    """Create polished starter art before the first scheduled data refresh."""
    render_hero()
    render_tiles()
    render_projects()
    cells = []
    for col in range(52):
        for row in range(7):
            cells.append(rect(42+col*17, 76+row*17, 12, 12, "#e6e5e1", 3))
    heat = f'''<rect width="1000" height="178" rx="16" fill="{PAPER}"/>
<text x="42" y="38" font-family="{SERIF}" font-size="27" fill="{INK}">A year of showing up, <tspan font-style="italic" fill="{BLUE}">in blue</tspan></text>
<text x="500" y="150" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{MUTED}">Contribution graph will populate on the first scheduled refresh</text>{''.join(cells)}'''
    write("heatmap.svg", 1000, 178, heat, "GitHub contribution calendar, awaiting first automatic refresh")
    act = f'''<rect width="1000" height="310" rx="16" fill="{PAPER}"/>
<text x="42" y="54" font-family="{SERIF}" font-size="32" fill="{INK}">GitHub activity</text>
<text x="42" y="96" font-family="{SANS}" font-size="15" fill="{MUTED}">Monthly contributions and streak stats will appear after the first refresh.</text>
<path d="M42 244h570" stroke="{RULE}"/><path d="M680 36v230" stroke="{RULE}"/>
<text x="718" y="104" font-family="{SERIF}" font-size="30" fill="{BLUE}">Live</text>
<text x="718" y="134" font-family="{SANS}" font-size="13" fill="{MUTED}">stats are generated daily</text>'''
    write("activity.svg", 1000, 310, act, "GitHub activity chart will show after first refresh")


def main() -> None:
    if "--preview" in sys.argv:
        render_preview()
        return
    days = fetch_days()
    (ROOT / "data").mkdir(exist_ok=True)
    (ROOT / "data" / "contributions.json").write_text(json.dumps({"user": USER, "days": days}, indent=2), encoding="utf-8")
    data = stats(days)
    render_hero()
    render_tiles()
    render_heatmap(days)
    render_activity(data)
    render_projects()
    print(f'Rendered profile for {USER}: {data["total"]:,} contributions, {data["streak"]}-day streak.')


if __name__ == "__main__":
    main()

